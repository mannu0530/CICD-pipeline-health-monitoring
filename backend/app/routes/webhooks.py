from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import logging
import hmac
import hashlib
import json
from services import IntegrationService

bp = Blueprint('webhooks', __name__, url_prefix='/api/v1/webhooks')

# Global integration service instance
integration_service = IntegrationService()

logger = logging.getLogger(__name__)

@bp.route('/github', methods=['POST'])
def github_webhook():
    """GitHub Actions webhook"""
    try:
        # Verify webhook signature
        signature = request.headers.get('X-Hub-Signature-256')
        if not signature:
            logger.warning("GitHub webhook received without signature")
            return jsonify({
                'success': False,
                'message': 'Missing webhook signature'
            }), 401
        
        # Get webhook secret from config
        webhook_secret = current_app.config.get('GITHUB_WEBHOOK_SECRET')
        if not webhook_secret:
            logger.error("GitHub webhook secret not configured")
            return jsonify({
                'success': False,
                'message': 'Webhook secret not configured'
            }), 500
        
        # Verify signature
        expected_signature = 'sha256=' + hmac.new(
            webhook_secret.encode('utf-8'),
            request.data,
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            logger.warning("GitHub webhook signature verification failed")
            return jsonify({
                'success': False,
                'message': 'Invalid webhook signature'
            }), 401
        
        # Parse webhook payload
        payload = request.get_json()
        if not payload:
            return jsonify({
                'success': False,
                'message': 'Invalid webhook payload'
            }), 400
        
        # Process webhook based on event type
        event_type = request.headers.get('X-GitHub-Event')
        logger.info(f"Processing GitHub webhook: {event_type}")
        
        if event_type == 'workflow_run':
            process_github_workflow_run(payload)
        elif event_type == 'push':
            process_github_push(payload)
        elif event_type == 'pull_request':
            process_github_pull_request(payload)
        else:
            logger.info(f"Unhandled GitHub event type: {event_type}")
        
        return jsonify({
            'success': True,
            'message': 'GitHub webhook processed successfully',
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing GitHub webhook: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error processing webhook: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/gitlab', methods=['POST'])
def gitlab_webhook():
    """GitLab CI webhook"""
    try:
        # Verify webhook token
        token = request.headers.get('X-Gitlab-Token')
        if not token:
            logger.warning("GitLab webhook received without token")
            return jsonify({
                'success': False,
                'message': 'Missing webhook token'
            }), 401
        
        # Get webhook secret from config
        webhook_secret = current_app.config.get('GITLAB_WEBHOOK_SECRET')
        if not webhook_secret:
            logger.error("GitLab webhook secret not configured")
            return jsonify({
                'success': False,
                'message': 'Webhook secret not configured'
            }), 500
        
        # Verify token
        if token != webhook_secret:
            logger.warning("GitLab webhook token verification failed")
            return jsonify({
                'success': False,
                'message': 'Invalid webhook token'
            }), 401
        
        # Parse webhook payload
        payload = request.get_json()
        if not payload:
            return jsonify({
                'success': False,
                'message': 'Invalid webhook payload'
            }), 400
        
        # Process webhook based on event type
        event_type = request.headers.get('X-Gitlab-Event')
        logger.info(f"Processing GitLab webhook: {event_type}")
        
        if event_type == 'Pipeline Hook':
            process_gitlab_pipeline(payload)
        elif event_type == 'Push Hook':
            process_gitlab_push(payload)
        elif event_type == 'Merge Request Hook':
            process_gitlab_merge_request(payload)
        else:
            logger.info(f"Unhandled GitLab event type: {event_type}")
        
        return jsonify({
            'success': True,
            'message': 'GitLab webhook processed successfully',
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing GitLab webhook: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error processing webhook: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/jenkins', methods=['POST'])
def jenkins_webhook():
    """Jenkins webhook"""
    try:
        # Parse webhook payload
        payload = request.get_json()
        if not payload:
            return jsonify({
                'success': False,
                'message': 'Invalid webhook payload'
            }), 400
        
        # Process webhook based on payload structure
        logger.info("Processing Jenkins webhook")
        
        if 'build' in payload:
            process_jenkins_build(payload)
        elif 'job' in payload:
            process_jenkins_job(payload)
        else:
            logger.info("Unhandled Jenkins webhook payload structure")
        
        return jsonify({
            'success': True,
            'message': 'Jenkins webhook processed successfully',
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing Jenkins webhook: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error processing webhook: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/test', methods=['POST'])
def test_webhook():
    """Test webhook endpoint for development"""
    try:
        payload = request.get_json()
        logger.info(f"Test webhook received: {payload}")
        
        return jsonify({
            'success': True,
            'message': 'Test webhook processed successfully',
            'payload': payload,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error processing test webhook: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error processing test webhook: {str(e)}',
            'error': str(e)
        }), 500

def process_github_workflow_run(payload):
    """Process GitHub workflow run webhook"""
    try:
        workflow_run = payload.get('workflow_run', {})
        repository = payload.get('repository', {})
        
        # Extract relevant information
        run_id = workflow_run.get('id')
        run_number = workflow_run.get('run_number')
        status = workflow_run.get('status')
        conclusion = workflow_run.get('conclusion')
        workflow_name = workflow_run.get('name')
        repository_name = repository.get('full_name')
        
        logger.info(f"GitHub workflow run: {repository_name}#{run_number} - {status} ({conclusion})")
        
        # Create alert if workflow failed
        if conclusion == 'failure':
            create_workflow_failure_alert(
                source='github',
                repository=repository_name,
                workflow=workflow_name,
                run_number=run_number,
                run_id=run_id
            )
        
        # TODO: Store workflow run data in database
        # TODO: Update metrics
        
    except Exception as e:
        logger.error(f"Error processing GitHub workflow run: {str(e)}")

def process_github_push(payload):
    """Process GitHub push webhook"""
    try:
        ref = payload.get('ref', '')
        repository = payload.get('repository', {})
        commits = payload.get('commits', [])
        
        if ref.startswith('refs/heads/'):
            branch = ref.replace('refs/heads/', '')
            repository_name = repository.get('full_name')
            
            logger.info(f"GitHub push to {repository_name}:{branch} - {len(commits)} commits")
            
            # TODO: Store push data in database
            # TODO: Trigger CI/CD if configured
            
    except Exception as e:
        logger.error(f"Error processing GitHub push: {str(e)}")

def process_github_pull_request(payload):
    """Process GitHub pull request webhook"""
    try:
        action = payload.get('action')
        pull_request = payload.get('pull_request', {})
        repository = payload.get('repository', {})
        
        repository_name = repository.get('full_name')
        pr_number = pull_request.get('number')
        pr_title = pull_request.get('title')
        
        logger.info(f"GitHub PR {action}: {repository_name}#{pr_number} - {pr_title}")
        
        # TODO: Store PR data in database
        # TODO: Update metrics
        
    except Exception as e:
        logger.error(f"Error processing GitHub pull request: {str(e)}")

def process_gitlab_pipeline(payload):
    """Process GitLab pipeline webhook"""
    try:
        pipeline = payload.get('pipeline', {})
        project = payload.get('project', {})
        
        pipeline_id = pipeline.get('id')
        status = pipeline.get('status')
        ref = pipeline.get('ref')
        project_name = project.get('name')
        
        logger.info(f"GitLab pipeline: {project_name}#{pipeline_id} - {status} on {ref}")
        
        # Create alert if pipeline failed
        if status == 'failed':
            create_pipeline_failure_alert(
                source='gitlab',
                project=project_name,
                pipeline_id=pipeline_id,
                ref=ref
            )
        
        # TODO: Store pipeline data in database
        # TODO: Update metrics
        
    except Exception as e:
        logger.error(f"Error processing GitLab pipeline: {str(e)}")

def process_gitlab_push(payload):
    """Process GitLab push webhook"""
    try:
        ref = payload.get('ref', '')
        project = payload.get('project', {})
        commits = payload.get('commits', [])
        
        if ref.startswith('refs/heads/'):
            branch = ref.replace('refs/heads/', '')
            project_name = project.get('name')
            
            logger.info(f"GitLab push to {project_name}:{branch} - {len(commits)} commits")
            
            # TODO: Store push data in database
            # TODO: Trigger CI/CD if configured
            
    except Exception as e:
        logger.error(f"Error processing GitLab push: {str(e)}")

def process_gitlab_merge_request(payload):
    """Process GitLab merge request webhook"""
    try:
        object_attributes = payload.get('object_attributes', {})
        project = payload.get('project', {})
        
        action = object_attributes.get('action')
        mr_id = object_attributes.get('id')
        mr_title = object_attributes.get('title')
        project_name = project.get('name')
        
        logger.info(f"GitLab MR {action}: {project_name}#{mr_id} - {mr_title}")
        
        # TODO: Store MR data in database
        # TODO: Update metrics
        
    except Exception as e:
        logger.error(f"Error processing GitLab merge request: {str(e)}")

def process_jenkins_build(payload):
    """Process Jenkins build webhook"""
    try:
        build = payload.get('build', {})
        job = payload.get('job', {})
        
        build_number = build.get('number')
        build_status = build.get('status')
        job_name = job.get('name')
        
        logger.info(f"Jenkins build: {job_name}#{build_number} - {build_status}")
        
        # Create alert if build failed
        if build_status == 'FAILURE':
            create_build_failure_alert(
                source='jenkins',
                job=job_name,
                build_number=build_number
            )
        
        # TODO: Store build data in database
        # TODO: Update metrics
        
    except Exception as e:
        logger.error(f"Error processing Jenkins build: {str(e)}")

def process_jenkins_job(payload):
    """Process Jenkins job webhook"""
    try:
        job = payload.get('job', {})
        job_name = job.get('name')
        job_status = job.get('status')
        
        logger.info(f"Jenkins job: {job_name} - {job_status}")
        
        # TODO: Store job data in database
        # TODO: Update metrics
        
    except Exception as e:
        logger.error(f"Error processing Jenkins job: {str(e)}")

def create_workflow_failure_alert(source, repository, workflow, run_number, run_id):
    """Create alert for workflow failure"""
    try:
        from alerts import create_alert
        
        alert_data = {
            'title': f'{source.title()} Workflow Failed',
            'message': f'Workflow "{workflow}" failed in {repository}#{run_number}',
            'severity': 'high',
            'category': 'ci_cd',
            'source': source,
            'metadata': {
                'repository': repository,
                'workflow': workflow,
                'run_number': run_number,
                'run_id': run_id
            }
        }
        
        # Create alert using the alerts route
        create_alert(alert_data)
        
    except Exception as e:
        logger.error(f"Error creating workflow failure alert: {str(e)}")

def create_pipeline_failure_alert(source, project, pipeline_id, ref):
    """Create alert for pipeline failure"""
    try:
        from alerts import create_alert

        alert_data = {
            'title': f'{source.title()} Pipeline Failed',
            'message': f'Pipeline #{pipeline_id} failed in {project} on {ref}',
            'severity': 'high',
            'category': 'ci_cd',
            'source': source,
            'metadata': {
                'project': project,
                'pipeline_id': pipeline_id,
                'ref': ref
            }
        }
        
        # Create alert using the alerts route
        create_alert(alert_data)
        
    except Exception as e:
        logger.error(f"Error creating pipeline failure alert: {str(e)}")

def create_build_failure_alert(source, job, build_number):
    """Create alert for build failure"""
    try:
        from alerts import create_alert

        alert_data = {
            'title': f'{source.title()} Build Failed',
            'message': f'Build #{build_number} failed for job {job}',
            'severity': 'high',
            'category': 'ci_cd',
            'source': source,
            'metadata': {
                'job': job,
                'build_number': build_number
            }
        }
        
        # Create alert using the alerts route
        create_alert(alert_data)
        
    except Exception as e:
        logger.error(f"Error creating build failure alert: {str(e)}")
