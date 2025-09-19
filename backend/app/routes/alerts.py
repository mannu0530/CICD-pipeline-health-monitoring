from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import logging
import json
import random
import requests
from services import IntegrationService
import os

bp = Blueprint('alerts', __name__, url_prefix='/api/v1/alerts')

# Global integration service instance
integration_service = IntegrationService()

logger = logging.getLogger(__name__)

# In-memory storage for alerts (in production, this should be in database)
alerts_storage = []
alert_rules = []

@bp.route('/', methods=['GET'])
def list_alerts():
    """List all alerts"""
    try:
        # Get query parameters
        status = request.args.get('status')
        severity = request.args.get('severity')
        limit = request.args.get('limit', 50, type=int)
        
        filtered_alerts = alerts_storage.copy()
        
        # Apply filters
        if status:
            filtered_alerts = [a for a in filtered_alerts if a.get('status') == status]
        if severity:
            filtered_alerts = [a for a in filtered_alerts if a.get('severity') == severity]
        
        # Sort by timestamp (newest first) and limit
        filtered_alerts.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        filtered_alerts = filtered_alerts[:limit]
        
        return jsonify({
            'success': True,
            'data': filtered_alerts,
            'count': len(filtered_alerts),
            'total': len(alerts_storage),
            'message': 'Alerts retrieved successfully',
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error listing alerts: {str(e)}")
        return jsonify({
            'success': False,
            'data': [],
            'message': f'Error retrieving alerts: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/', methods=['POST'])
def create_alert():
    """Create a new alert"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Alert data is required'
            }), 400
        
        # Validate required fields
        required_fields = ['title', 'message', 'severity']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Required field missing: {field}'
                }), 400
        
        # Create alert object
        alert = {
            'id': f"alert_{len(alerts_storage) + 1}_{int(datetime.utcnow().timestamp())}",
            'title': data['title'],
            'message': data['message'],
            'severity': data['severity'],
            'status': data.get('status', 'active'),
            'category': data.get('category', 'general'),
            'source': data.get('source', 'manual'),
            'timestamp': datetime.utcnow().isoformat(),
            'acknowledged_at': None,
            'acknowledged_by': None,
            'resolved_at': None,
            'resolved_by': None,
            'metadata': data.get('metadata', {})
        }
        
        # Add to storage
        alerts_storage.append(alert)
        
        # Send alert notifications if configured
        send_alert_notifications(alert)
        
        return jsonify({
            'success': True,
            'data': alert,
            'message': 'Alert created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating alert: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error creating alert: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/<alert_id>', methods=['GET'])
def get_alert(alert_id):
    """Get alert by ID"""
    try:
        alert = next((a for a in alerts_storage if a.get('id') == alert_id), None)
        if alert:
            return jsonify({
                'success': True,
                'data': alert,
                'message': 'Alert retrieved successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Alert not found'
            }), 404
    except Exception as e:
        logger.error(f"Error getting alert {alert_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error retrieving alert: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/<alert_id>', methods=['PUT'])
def update_alert(alert_id):
    """Update alert by ID"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Update data is required'
            }), 400
        
        alert = next((a for a in alerts_storage if a.get('id') == alert_id), None)
        if not alert:
            return jsonify({
                'success': False,
                'message': 'Alert not found'
            }), 404
        
        # Update allowed fields
        allowed_fields = ['title', 'message', 'severity', 'status', 'category']
        for field in allowed_fields:
            if field in data:
                alert[field] = data[field]
        
        # Handle status changes
        if 'status' in data:
            if data['status'] == 'acknowledged':
                alert['acknowledged_at'] = datetime.utcnow().isoformat()
                alert['acknowledged_by'] = data.get('acknowledged_by', 'system')
            elif data['status'] == 'resolved':
                alert['resolved_at'] = datetime.utcnow().isoformat()
                alert['resolved_by'] = data.get('resolved_by', 'system')
        
        alert['updated_at'] = datetime.utcnow().isoformat()
        
        return jsonify({
            'success': True,
            'data': alert,
            'message': 'Alert updated successfully'
        })
        
    except Exception as e:
        logger.error(f"Error updating alert {alert_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error updating alert: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/<alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Acknowledge an alert"""
    try:
        data = request.get_json() or {}
        user = data.get('user', 'system')
        
        alert = next((a for a in alerts_storage if a.get('id') == alert_id), None)
        if not alert:
            return jsonify({
                'success': False,
                'message': 'Alert not found'
            }), 404
        
        if alert.get('status') == 'resolved':
            return jsonify({
                'success': False,
                'message': 'Cannot acknowledge a resolved alert'
            }), 400
        
        alert['status'] = 'acknowledged'
        alert['acknowledged_at'] = datetime.utcnow().isoformat()
        alert['acknowledged_by'] = user
        alert['updated_at'] = datetime.utcnow().isoformat()
        
        return jsonify({
            'success': True,
            'data': alert,
            'message': 'Alert acknowledged successfully'
        })
        
    except Exception as e:
        logger.error(f"Error acknowledging alert {alert_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error acknowledging alert: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/<alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    """Resolve an alert"""
    try:
        data = request.get_json() or {}
        user = data.get('user', 'system')
        resolution_notes = data.get('resolution_notes', '')
        
        alert = next((a for a in alerts_storage if a.get('id') == alert_id), None)
        if not alert:
            return jsonify({
                'success': False,
                'message': 'Alert not found'
            }), 404
        
        alert['status'] = 'resolved'
        alert['resolved_at'] = datetime.utcnow().isoformat()
        alert['resolved_by'] = user
        alert['resolution_notes'] = resolution_notes
        alert['updated_at'] = datetime.utcnow().isoformat()
        
        return jsonify({
            'success': True,
            'data': alert,
            'message': 'Alert resolved successfully'
        })
        
    except Exception as e:
        logger.error(f"Error resolving alert {alert_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error resolving alert: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/<alert_id>', methods=['DELETE'])
def delete_alert(alert_id):
    """Delete alert by ID"""
    try:
        alert = next((a for a in alerts_storage if a.get('id') == alert_id), None)
        if not alert:
            return jsonify({
                'success': False,
                'message': 'Alert not found'
            }), 404
        
        alerts_storage.remove(alert)
        
        return jsonify({
            'success': True,
            'message': 'Alert deleted successfully'
        })
        
    except Exception as e:
        logger.error(f"Error deleting alert {alert_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error deleting alert: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/rules', methods=['GET'])
def list_alert_rules():
    """List all alert rules"""
    try:
        return jsonify({
            'success': True,
            'data': alert_rules,
            'count': len(alert_rules),
            'message': 'Alert rules retrieved successfully'
        })
    except Exception as e:
        logger.error(f"Error listing alert rules: {str(e)}")
        return jsonify({
            'success': False,
            'data': [],
            'message': f'Error retrieving alert rules: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/rules', methods=['POST'])
def create_alert_rule():
    """Create a new alert rule"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Rule data is required'
            }), 400
        
        # Validate required fields
        required_fields = ['name', 'condition', 'severity']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Required field missing: {field}'
                }), 400
        
        # Create rule object
        rule = {
            'id': f"rule_{len(alert_rules) + 1}_{int(datetime.utcnow().timestamp())}",
            'name': data['name'],
            'description': data.get('description', ''),
            'condition': data['condition'],
            'severity': data['severity'],
            'enabled': data.get('enabled', True),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Add to storage
        alert_rules.append(rule)
        
        return jsonify({
            'success': True,
            'data': rule,
            'message': 'Alert rule created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating alert rule: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error creating alert rule: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/stats', methods=['GET'])
def get_alert_stats():
    """Get alert statistics"""
    try:
        total_alerts = len(alerts_storage)
        active_alerts = len([a for a in alerts_storage if a.get('status') == 'active'])
        acknowledged_alerts = len([a for a in alerts_storage if a.get('status') == 'acknowledged'])
        resolved_alerts = len([a for a in alerts_storage if a.get('status') == 'resolved'])

        # Count by severity
        severity_counts = {}
        for alert in alerts_storage:
            severity = alert.get('severity', 'unknown')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        # Count by category
        category_counts = {}
        for alert in alerts_storage:
            category = alert.get('category', 'unknown')
            category_counts[category] = category_counts.get(category, 0) + 1

        stats = {
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'acknowledged_alerts': acknowledged_alerts,
            'resolved_alerts': resolved_alerts,
            'by_severity': severity_counts,
            'by_category': category_counts,
            'total_rules': len(alert_rules),
            'enabled_rules': len([r for r in alert_rules if r.get('enabled')])
        }

        return jsonify({
            'success': True,
            'data': stats,
            'message': 'Alert statistics retrieved successfully'
        })

    except Exception as e:
        logger.error(f"Error getting alert stats: {str(e)}")
        return jsonify({
            'success': False,
            'data': {},
            'message': f'Error retrieving alert statistics: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/demo/generate', methods=['POST'])
def generate_demo_alerts():
    """Generate random demo alerts for testing"""
    try:
        data = request.get_json() or {}
        count = data.get('count', 5)
        count = min(count, 20)  # Limit to 20 alerts at once

        # Sample data for randomization
        severities = ['critical', 'high', 'medium', 'low', 'info']
        categories = ['pipeline', 'build', 'deployment', 'infrastructure', 'security', 'performance']
        statuses = ['active', 'acknowledged', 'resolved']
        sources = ['jenkins', 'github', 'gitlab', 'manual', 'monitoring']

        pipeline_titles = [
            'Pipeline Failed: Build #1234',
            'Pipeline Timeout: Deployment Stuck',
            'Pipeline Error: Test Suite Failed',
            'Pipeline Warning: Slow Performance',
            'Pipeline Success: All Tests Passed',
            'Pipeline Issue: Resource Limit Exceeded',
            'Pipeline Alert: Security Scan Failed',
            'Pipeline Notification: New Release Available'
        ]

        build_messages = [
            'Build failed due to compilation errors',
            'Unit tests failed with 3 test cases',
            'Integration tests timed out after 30 minutes',
            'Code coverage below threshold (75%)',
            'Security vulnerability detected in dependencies',
            'Build artifacts corrupted during upload',
            'Docker image build failed',
            'Database migration script error'
        ]

        generated_alerts = []

        for i in range(count):
            severity = random.choice(severities)
            category = random.choice(categories)
            status = random.choice(statuses)
            source = random.choice(sources)

            # Generate appropriate title and message based on category
            if category == 'pipeline':
                title = random.choice(pipeline_titles)
                message = f"Pipeline issue detected in {source} integration"
            elif category == 'build':
                title = f"Build Alert: {random.choice(['Failed', 'Warning', 'Error', 'Timeout'])}"
                message = random.choice(build_messages)
            elif category == 'deployment':
                title = f"Deployment Alert: {random.choice(['Failed', 'Stuck', 'Rollback', 'Timeout'])}"
                message = f"Deployment issue in production environment"
            elif category == 'infrastructure':
                title = f"Infrastructure Alert: {random.choice(['High CPU', 'Memory Leak', 'Disk Full', 'Network Issue'])}"
                message = f"System resource utilization is critical"
            elif category == 'security':
                title = f"Security Alert: {random.choice(['Vulnerability', 'Access Denied', 'Suspicious Activity'])}"
                message = f"Security incident detected and logged"
            else:  # performance
                title = f"Performance Alert: {random.choice(['Slow Response', 'High Latency', 'Memory Usage'])}"
                message = f"Performance metrics exceed thresholds"

            alert = {
                'id': f"demo_alert_{len(alerts_storage) + i + 1}_{int(datetime.utcnow().timestamp())}",
                'title': title,
                'message': message,
                'severity': severity,
                'status': status,
                'category': category,
                'source': source,
                'timestamp': datetime.utcnow().isoformat(),
                'acknowledged_at': datetime.utcnow().isoformat() if status in ['acknowledged', 'resolved'] else None,
                'acknowledged_by': 'demo_user' if status in ['acknowledged', 'resolved'] else None,
                'resolved_at': datetime.utcnow().isoformat() if status == 'resolved' else None,
                'resolved_by': 'demo_user' if status == 'resolved' else None,
                'metadata': {
                    'demo': True,
                    'generated_at': datetime.utcnow().isoformat(),
                    'random_seed': random.randint(1000, 9999)
                }
            }

            alerts_storage.append(alert)
            generated_alerts.append(alert)

            # Send notifications for active alerts
            if status == 'active':
                send_alert_notifications(alert)

        return jsonify({
            'success': True,
            'data': generated_alerts,
            'count': len(generated_alerts),
            'message': f'Successfully generated {len(generated_alerts)} demo alerts'
        }), 201

    except Exception as e:
        logger.error(f"Error generating demo alerts: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error generating demo alerts: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/demo/clear', methods=['DELETE'])
def clear_demo_alerts():
    """Clear all demo alerts"""
    try:
        # Find and remove demo alerts
        demo_alerts = [a for a in alerts_storage if a.get('metadata', {}).get('demo') == True]
        for alert in demo_alerts:
            alerts_storage.remove(alert)

        return jsonify({
            'success': True,
            'cleared_count': len(demo_alerts),
            'message': f'Successfully cleared {len(demo_alerts)} demo alerts'
        })

    except Exception as e:
        logger.error(f"Error clearing demo alerts: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error clearing demo alerts: {str(e)}',
            'error': str(e)
        }), 500

def send_alert_notifications(alert):
    """Send alert notifications to configured channels"""
    try:
        # Log the alert
        logger.info(f"Alert notification: {alert['severity'].upper()} - {alert['title']}: {alert['message']}")

        # Send to Slack if configured
        slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')

        if slack_webhook_url:
            try:
                # Format message based on severity
                severity_emoji = {
                    'critical': '🚨',
                    'high': '⚠️',
                    'medium': '⚡',
                    'low': 'ℹ️',
                    'info': '📢'
                }.get(alert.get('severity', 'info'), '📢')

                # Create Slack message payload
                slack_message = {
                    "username": "CI/CD Monitor",
                    "icon_emoji": ":robot_face:",
                    "text": f"{severity_emoji} *{alert['severity'].upper()} ALERT*",
                    "attachments": [
                        {
                            "color": {
                                'critical': 'danger',
                                'high': 'warning',
                                'medium': 'good',
                                'low': '#808080',
                                'info': '#439FE0'
                            }.get(alert.get('severity', 'info'), '#439FE0'),
                            "fields": [
                                {
                                    "title": "Title",
                                    "value": alert['title'],
                                    "short": True
                                },
                                {
                                    "title": "Status",
                                    "value": alert.get('status', 'active').title(),
                                    "short": True
                                },
                                {
                                    "title": "Category",
                                    "value": alert.get('category', 'general').title(),
                                    "short": True
                                },
                                {
                                    "title": "Source",
                                    "value": alert.get('source', 'manual').title(),
                                    "short": True
                                }
                            ],
                            "text": alert['message'],
                            "footer": "CI/CD Pipeline Monitor",
                            "ts": datetime.utcnow().timestamp()
                        }
                    ]
                }

                # Send webhook request
                response = requests.post(
                    slack_webhook_url,
                    json=slack_message,
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )

                if response.status_code == 200:
                    logger.info(f"Slack webhook notification sent successfully for alert {alert['id']}")
                else:
                    logger.error(f"Slack webhook failed with status {response.status_code}: {response.text}")

            except requests.exceptions.RequestException as e:
                logger.error(f"Error sending Slack webhook notification: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error sending Slack notification: {str(e)}")
        else:
            logger.warning("Slack not configured - SLACK_WEBHOOK_URL missing")

        # TODO: Implement email notifications
        # TODO: Implement webhook notifications to external systems

    except Exception as e:
        logger.error(f"Error sending alert notifications: {str(e)}")

def check_alert_rules():
    """Check alert rules and create alerts if conditions are met"""
    try:
        # This would be called periodically to check for conditions
        # For now, just a placeholder
        pass
    except Exception as e:
        logger.error(f"Error checking alert rules: {str(e)}")
