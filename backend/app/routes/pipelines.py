from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
from ...services import IntegrationService

bp = Blueprint('pipelines', __name__, url_prefix='/api/v1/pipelines')

# Global integration service instance
integration_service = IntegrationService()

logger = logging.getLogger(__name__)

@bp.route('/', methods=['GET'])
def list_pipelines():
    """List all pipelines from connected services"""
    try:
        result = integration_service.get_all_pipelines()
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'message': 'Pipelines retrieved successfully',
                'timestamp': datetime.utcnow().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'data': [],
                'message': result['message'],
                'timestamp': datetime.utcnow().isoformat()
            }), 400
    except Exception as e:
        logger.error(f"Error listing pipelines: {str(e)}")
        return jsonify({
            'success': False,
            'data': [],
            'message': f'Error retrieving pipelines: {str(e)}',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@bp.route('/<pipeline_id>', methods=['GET'])
def get_pipeline(pipeline_id):
    """Get pipeline by ID from the appropriate service"""
    try:
        # Parse pipeline_id format: service:actual_id
        if ':' in pipeline_id:
            service, actual_id = pipeline_id.split(':', 1)
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid pipeline ID format. Use: service:actual_id',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        if service == 'jenkins':
            # For Jenkins, pipeline_id is actually job name
            if integration_service.jenkins_service:
                result = integration_service.jenkins_service.get_job_info(actual_id)
                if result['success']:
                    return jsonify({
                        'success': True,
                        'data': result['data'],
                        'message': 'Pipeline details retrieved successfully',
                        'timestamp': datetime.utcnow().isoformat()
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': result['message'],
                        'timestamp': datetime.utcnow().isoformat()
                    }), 400
            else:
                return jsonify({
                    'success': False,
                    'message': 'Jenkins service not connected',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        elif service == 'github':
            # For GitHub, we need repo and run_id
            if ':' in actual_id:
                repo, run_id = actual_id.split(':', 1)
                owner, repo_name = repo.split('/', 1)
                if integration_service.github_service:
                    result = integration_service.github_service.get_workflow_run_details(owner, repo_name, int(run_id))
                    if result['success']:
                        return jsonify({
                            'success': True,
                            'data': result['data'],
                            'message': 'Pipeline details retrieved successfully',
                            'timestamp': datetime.utcnow().isoformat()
                        })
                    else:
                        return jsonify({
                            'success': False,
                            'message': result['message'],
                            'timestamp': datetime.utcnow().isoformat()
                        }), 400
                else:
                    return jsonify({
                        'success': False,
                        'message': 'GitHub service not connected',
                        'timestamp': datetime.utcnow().isoformat()
                    }), 400
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid GitHub pipeline ID format. Use: github:owner/repo:run_id',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        elif service == 'gitlab':
            # For GitLab, we need project_id and pipeline_id
            if ':' in actual_id:
                project_id, pipeline_id = actual_id.split(':', 1)
                if integration_service.gitlab_service:
                    result = integration_service.gitlab_service.get_pipeline_details(int(project_id), int(pipeline_id))
                    if result['success']:
                        return jsonify({
                            'success': True,
                            'data': result['data'],
                            'message': 'Pipeline details retrieved successfully',
                            'timestamp': datetime.utcnow().isoformat()
                        })
                    else:
                        return jsonify({
                            'success': False,
                            'message': result['message'],
                            'timestamp': datetime.utcnow().isoformat()
                        }), 400
                else:
                    return jsonify({
                        'success': False,
                        'message': 'GitLab service not connected',
                        'timestamp': datetime.utcnow().isoformat()
                    }), 400
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid GitLab pipeline ID format. Use: gitlab:project_id:pipeline_id',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        else:
            return jsonify({
                'success': False,
                'message': f'Unknown service: {service}',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
            
    except Exception as e:
        logger.error(f"Error getting pipeline {pipeline_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error retrieving pipeline details: {str(e)}',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@bp.route('/<pipeline_id>/jobs', methods=['GET'])
def get_pipeline_jobs(pipeline_id):
    """Get jobs for a specific pipeline"""
    try:
        # Parse pipeline_id format: service:actual_id
        if ':' in pipeline_id:
            service, actual_id = pipeline_id.split(':', 1)
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid pipeline ID format. Use: service:actual_id',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        if service == 'jenkins':
            # For Jenkins, get builds for the job
            if integration_service.jenkins_service:
                result = integration_service.jenkins_service.get_builds(actual_id, limit=50)
                if result['success']:
                    return jsonify({
                        'success': True,
                        'data': result['data'],
                        'message': 'Pipeline jobs retrieved successfully',
                        'timestamp': datetime.utcnow().isoformat()
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': result['message'],
                        'timestamp': datetime.utcnow().isoformat()
                    }), 400
            else:
                return jsonify({
                    'success': False,
                    'message': 'Jenkins service not connected',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        elif service == 'github':
            # For GitHub, get jobs for the workflow run
            if ':' in actual_id:
                repo, run_id = actual_id.split(':', 1)
                owner, repo_name = repo.split('/', 1)
                if integration_service.github_service:
                    result = integration_service.github_service.get_workflow_jobs(owner, repo_name, int(run_id))
                    if result['success']:
                        return jsonify({
                            'success': True,
                            'data': result['data'],
                            'message': 'Pipeline jobs retrieved successfully',
                            'timestamp': datetime.utcnow().isoformat()
                        })
                    else:
                        return jsonify({
                            'success': False,
                            'message': result['message'],
                            'timestamp': datetime.utcnow().isoformat()
                        }), 400
                else:
                    return jsonify({
                        'success': False,
                        'message': 'GitHub service not connected',
                        'timestamp': datetime.utcnow().isoformat()
                    }), 400
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid GitHub pipeline ID format. Use: github:owner/repo:run_id',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        elif service == 'gitlab':
            # For GitLab, get jobs for the pipeline
            if ':' in actual_id:
                project_id, pipeline_id = actual_id.split(':', 1)
                if integration_service.gitlab_service:
                    result = integration_service.gitlab_service.get_pipeline_jobs(int(project_id), int(pipeline_id))
                    if result['success']:
                        return jsonify({
                            'success': True,
                            'data': result['data'],
                            'message': 'Pipeline jobs retrieved successfully',
                            'timestamp': datetime.utcnow().isoformat()
                        })
                    else:
                        return jsonify({
                            'success': False,
                            'message': result['message'],
                            'timestamp': datetime.utcnow().isoformat()
                        }), 400
                else:
                    return jsonify({
                        'success': False,
                        'message': 'GitLab service not connected',
                        'timestamp': datetime.utcnow().isoformat()
                    }), 400
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid GitLab pipeline ID format. Use: gitlab:project_id:pipeline_id',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        else:
            return jsonify({
                'success': False,
                'message': f'Unknown service: {service}',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
            
    except Exception as e:
        logger.error(f"Error getting pipeline jobs for {pipeline_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error retrieving pipeline jobs: {str(e)}',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
