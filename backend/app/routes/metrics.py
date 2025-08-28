from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import logging
from ...services import IntegrationService

bp = Blueprint('metrics', __name__, url_prefix='/api/v1/metrics')

# Global integration service instance
integration_service = IntegrationService()

logger = logging.getLogger(__name__)

@bp.route('/', methods=['GET'])
def get_metrics():
    """Get dashboard metrics from connected services"""
    try:
        result = integration_service.get_dashboard_metrics()
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'message': 'Metrics retrieved successfully',
                'timestamp': datetime.utcnow().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'data': {
                    'total_pipelines': 0,
                    'total_builds': 0,
                    'success_rate': 0,
                    'failure_rate': 0,
                    'average_build_time': 0,
                    'recent_activity': [],
                    'service_status': {}
                },
                'message': result['message'],
                'timestamp': datetime.utcnow().isoformat()
            }), 400
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        return jsonify({
            'success': False,
            'data': {
                'total_pipelines': 0,
                'total_builds': 0,
                'success_rate': 0,
                'failure_rate': 0,
                'average_build_time': 0,
                'recent_activity': [],
                'service_status': {}
            },
            'message': f'Error retrieving metrics: {str(e)}',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@bp.route('/pipelines', methods=['GET'])
def get_pipeline_metrics():
    """Get detailed pipeline metrics"""
    try:
        result = integration_service.get_all_pipelines()
        if result['success']:
            data = result['data']
            
            # Calculate pipeline metrics
            total_pipelines = data['total_count']
            jenkins_pipelines = len(data['jenkins'])
            github_pipelines = len(data['github'])
            gitlab_pipelines = len(data['gitlab'])
            
            # Get build metrics for Jenkins
            build_metrics = {}
            if integration_service.jenkins_service:
                builds_result = integration_service.get_all_builds(limit=100)
                if builds_result['success']:
                    jenkins_builds = builds_result['data']['jenkins']
                    if jenkins_builds:
                        successful = sum(1 for build in jenkins_builds if build.get('result') == 'SUCCESS')
                        failed = sum(1 for build in jenkins_builds if build.get('result') == 'FAILURE')
                        total = len(jenkins_builds)
                        
                        if total > 0:
                            build_metrics = {
                                'total_builds': total,
                                'successful': successful,
                                'failed': failed,
                                'success_rate': round((successful / total) * 100, 2),
                                'failure_rate': round((failed / total) * 100, 2)
                            }
            
            metrics = {
                'total_pipelines': total_pipelines,
                'by_service': {
                    'jenkins': jenkins_pipelines,
                    'github': github_pipelines,
                    'gitlab': gitlab_pipelines
                },
                'build_metrics': build_metrics,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            return jsonify({
                'success': True,
                'data': metrics,
                'message': 'Pipeline metrics retrieved successfully'
            })
        else:
            return jsonify({
                'success': False,
                'data': {},
                'message': result['message']
            }), 400
    except Exception as e:
        logger.error(f"Error getting pipeline metrics: {str(e)}")
        return jsonify({
            'success': False,
            'data': {},
            'message': f'Error retrieving pipeline metrics: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/builds', methods=['GET'])
def get_build_metrics():
    """Get detailed build metrics"""
    try:
        limit = request.args.get('limit', 100, type=int)
        result = integration_service.get_all_builds(limit=limit)
        
        if result['success']:
            data = result['data']
            jenkins_builds = data['jenkins']
            
            # Calculate build metrics
            total_builds = data['total_count']
            build_metrics = {
                'total_builds': total_builds,
                'by_service': {
                    'jenkins': len(jenkins_builds),
                    'github': len(data['github']),
                    'gitlab': len(data['gitlab'])
                }
            }
            
            # Calculate Jenkins-specific metrics
            if jenkins_builds:
                successful = sum(1 for build in jenkins_builds if build.get('result') == 'SUCCESS')
                failed = sum(1 for build in jenkins_builds if build.get('result') == 'FAILURE')
                running = sum(1 for build in jenkins_builds if build.get('result') is None)
                
                total = len(jenkins_builds)
                if total > 0:
                    build_metrics['jenkins'] = {
                        'total': total,
                        'successful': successful,
                        'failed': failed,
                        'running': running,
                        'success_rate': round((successful / total) * 100, 2),
                        'failure_rate': round((failed / total) * 100, 2),
                        'running_rate': round((running / total) * 100, 2)
                    }
                
                # Calculate average build time
                build_times = [build.get('duration', 0) for build in jenkins_builds if build.get('duration')]
                if build_times:
                    build_metrics['jenkins']['average_build_time'] = round(sum(build_times) / len(build_times), 2)
                    build_metrics['jenkins']['min_build_time'] = min(build_times)
                    build_metrics['jenkins']['max_build_time'] = max(build_times)
            
            return jsonify({
                'success': True,
                'data': build_metrics,
                'message': 'Build metrics retrieved successfully'
            })
        else:
            return jsonify({
                'success': False,
                'data': {},
                'message': result['message']
            }), 400
    except Exception as e:
        logger.error(f"Error getting build metrics: {str(e)}")
        return jsonify({
            'success': False,
            'data': {},
            'message': f'Error retrieving build metrics: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/trends', methods=['GET'])
def get_trend_metrics():
    """Get trend metrics over time"""
    try:
        days = request.args.get('days', 7, type=int)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get builds for trend analysis
        result = integration_service.get_all_builds(limit=1000)
        
        if result['success']:
            jenkins_builds = result['data']['jenkins']
            
            # Group builds by date
            daily_metrics = {}
            for build in jenkins_builds:
                if build.get('timestamp'):
                    try:
                        build_date = datetime.fromtimestamp(build['timestamp'] / 1000).strftime('%Y-%m-%d')
                        if build_date not in daily_metrics:
                            daily_metrics[build_date] = {
                                'success': 0,
                                'failure': 0,
                                'total': 0,
                                'total_duration': 0
                            }
                        
                        daily_metrics[build_date]['total'] += 1
                        if build.get('result') == 'SUCCESS':
                            daily_metrics[build_date]['success'] += 1
                        elif build.get('result') == 'FAILURE':
                            daily_metrics[build_date]['failure'] += 1
                        
                        if build.get('duration'):
                            daily_metrics[build_date]['total_duration'] += build['duration']
                    except:
                        continue
            
            # Convert to list format for frontend
            trends = []
            for date, metrics in daily_metrics.items():
                avg_duration = 0
                if metrics['total'] > 0:
                    avg_duration = metrics['total_duration'] / metrics['total']
                
                trends.append({
                    'date': date,
                    'success': metrics['success'],
                    'failure': metrics['failure'],
                    'total': metrics['total'],
                    'success_rate': round((metrics['success'] / metrics['total']) * 100, 2) if metrics['total'] > 0 else 0,
                    'average_duration': round(avg_duration, 2)
                })
            
            # Sort by date
            trends.sort(key=lambda x: x['date'])
            
            return jsonify({
                'success': True,
                'data': trends,
                'message': 'Trend metrics retrieved successfully'
            })
        else:
            return jsonify({
                'success': False,
                'data': [],
                'message': result['message']
            }), 400
    except Exception as e:
        logger.error(f"Error getting trend metrics: {str(e)}")
        return jsonify({
            'success': False,
            'data': [],
            'message': f'Error retrieving trend metrics: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/service-status', methods=['GET'])
def get_service_status():
    """Get status of all connected services"""
    try:
        status = integration_service.get_connection_status()
        return jsonify({
            'success': True,
            'data': status,
            'message': 'Service status retrieved successfully'
        })
    except Exception as e:
        logger.error(f"Error getting service status: {str(e)}")
        return jsonify({
            'success': False,
            'data': {},
            'message': f'Error retrieving service status: {str(e)}',
            'error': str(e)
        }), 500
