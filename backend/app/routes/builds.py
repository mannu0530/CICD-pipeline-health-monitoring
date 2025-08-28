from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
from ...services import IntegrationService

bp = Blueprint('builds', __name__, url_prefix='/api/v1/builds')

# Global integration service instance
integration_service = IntegrationService()

logger = logging.getLogger(__name__)

@bp.route('/', methods=['GET'])
def list_builds():
    """List all builds from connected services"""
    try:
        limit = request.args.get('limit', 100, type=int)
        result = integration_service.get_all_builds(limit=limit)
        if result['success']:
            return jsonify({
                'success': True,
                'data': result['data'],
                'message': 'Builds retrieved successfully',
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
        logger.error(f"Error listing builds: {str(e)}")
        return jsonify({
            'success': False,
            'data': [],
            'message': f'Error retrieving builds: {str(e)}',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@bp.route('/<build_id>', methods=['GET'])
def get_build(build_id):
    """Get build by ID from the appropriate service"""
    try:
        # Parse build_id format: service:job_name:build_number
        if ':' in build_id:
            parts = build_id.split(':')
            if len(parts) >= 3:
                service, job_name, build_number = parts[0], parts[1], parts[2]
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid build ID format. Use: service:job_name:build_number',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid build ID format. Use: service:job_name:build_number',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        if service == 'jenkins':
            if integration_service.jenkins_service:
                result = integration_service.jenkins_service.get_build_info(job_name, int(build_number))
                if result['success']:
                    return jsonify({
                        'success': True,
                        'data': result['data'],
                        'message': 'Build details retrieved successfully',
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
            # For GitHub, build_id format: github:owner/repo:run_id:job_id
            if len(parts) >= 4:
                repo, run_id, job_id = parts[1], parts[2], parts[3]
                owner, repo_name = repo.split('/', 1)
                if integration_service.github_service:
                    # Get workflow run details and then job details
                    run_result = integration_service.github_service.get_workflow_run_details(owner, repo_name, int(run_id))
                    if run_result['success']:
                        jobs_result = integration_service.github_service.get_workflow_jobs(owner, repo_name, int(run_id))
                        if jobs_result['success']:
                            # Find the specific job
                            job = next((j for j in jobs_result['data'] if str(j.get('id')) == job_id), None)
                            if job:
                                return jsonify({
                                    'success': True,
                                    'data': job,
                                    'message': 'Build details retrieved successfully',
                                    'timestamp': datetime.utcnow().isoformat()
                                })
                            else:
                                return jsonify({
                                    'success': False,
                                    'message': f'Job {job_id} not found',
                                    'timestamp': datetime.utcnow().isoformat()
                                }), 404
                        else:
                            return jsonify({
                                'success': False,
                                'message': jobs_result['message'],
                                'timestamp': datetime.utcnow().isoformat()
                            }), 400
                    else:
                        return jsonify({
                            'success': False,
                            'message': run_result['message'],
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
                    'message': 'Invalid GitHub build ID format. Use: github:owner/repo:run_id:job_id',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        elif service == 'gitlab':
            # For GitLab, build_id format: gitlab:project_id:pipeline_id:job_id
            if len(parts) >= 4:
                project_id, pipeline_id, job_id = parts[1], parts[2], parts[3]
                if integration_service.gitlab_service:
                    # Get pipeline jobs and find the specific job
                    jobs_result = integration_service.gitlab_service.get_pipeline_jobs(int(project_id), int(pipeline_id))
                    if jobs_result['success']:
                        job = next((j for j in jobs_result['data'] if str(j.get('id')) == job_id), None)
                        if job:
                            return jsonify({
                                'success': True,
                                'data': job,
                                'message': 'Build details retrieved successfully',
                                'timestamp': datetime.utcnow().isoformat()
                            })
                        else:
                            return jsonify({
                                'success': False,
                                'message': f'Job {job_id} not found',
                                'timestamp': datetime.utcnow().isoformat()
                            }), 404
                    else:
                        return jsonify({
                            'success': False,
                            'message': jobs_result['message'],
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
                    'message': 'Invalid GitLab build ID format. Use: gitlab:project_id:pipeline_id:job_id',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        else:
            return jsonify({
                'success': False,
                'message': f'Unknown service: {service}',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
            
    except Exception as e:
        logger.error(f"Error getting build {build_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error retrieving build details: {str(e)}',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@bp.route('/<build_id>/logs', methods=['GET'])
def get_build_logs(build_id):
    """Get logs for a specific build"""
    try:
        # Parse build_id format: service:job_name:build_number
        if ':' in build_id:
            parts = build_id.split(':')
            if len(parts) >= 3:
                service, job_name, build_number = parts[0], parts[1], parts[2]
            else:
                return jsonify({
                    'success': False,
                    'message': 'Invalid build ID format. Use: service:job_name:build_number',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid build ID format. Use: service:job_name:build_number',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
        
        if service == 'jenkins':
            if integration_service.jenkins_service:
                result = integration_service.jenkins_service.get_build_logs(job_name, int(build_number))
                if result['success']:
                    return jsonify({
                        'success': True,
                        'data': result['data'],
                        'message': 'Build logs retrieved successfully',
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
            # For GitHub, get job logs
            if len(parts) >= 4:
                repo, run_id, job_id = parts[1], parts[2], parts[3]
                owner, repo_name = repo.split('/', 1)
                if integration_service.github_service:
                    result = integration_service.github_service.get_workflow_logs(owner, repo_name, int(job_id))
                    if result['success']:
                        return jsonify({
                            'success': True,
                            'data': result['data'],
                            'message': 'Build logs retrieved successfully',
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
                    'message': 'Invalid GitHub build ID format. Use: github:owner/repo:run_id:job_id',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        elif service == 'gitlab':
            # For GitLab, get job logs
            if len(parts) >= 4:
                project_id, pipeline_id, job_id = parts[1], parts[2], parts[3]
                if integration_service.gitlab_service:
                    result = integration_service.gitlab_service.get_job_logs(int(project_id), int(job_id))
                    if result['success']:
                        return jsonify({
                            'success': True,
                            'data': result['data'],
                            'message': 'Build logs retrieved successfully',
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
                    'message': 'Invalid GitLab build ID format. Use: gitlab:project_id:pipeline_id:job_id',
                    'timestamp': datetime.utcnow().isoformat()
                }), 400
        else:
            return jsonify({
                'success': False,
                'message': f'Unknown service: {service}',
                'timestamp': datetime.utcnow().isoformat()
            }), 400
            
    except Exception as e:
        logger.error(f"Error getting build logs for {build_id}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error retrieving build logs: {str(e)}',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
