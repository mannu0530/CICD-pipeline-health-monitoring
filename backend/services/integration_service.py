import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from .github_service import GitHubService
from .gitlab_service import GitLabService
from .jenkins_service import JenkinsService

logger = logging.getLogger(__name__)

class IntegrationService:
    """Service to manage integrations with various CI/CD tools"""
    
    def __init__(self):
        self.github_service = None
        self.gitlab_service = None
        self.jenkins_service = None
        self.connections = {}
    
    def setup_github(self, username: str, password: str, base_url: str = "https://api.github.com") -> Dict:
        """Setup GitHub integration"""
        try:
            self.github_service = GitHubService(username, password, base_url)
            result = self.github_service.test_connection()
            
            if result['success']:
                self.connections['github'] = {
                    'service': self.github_service,
                    'username': username,
                    'base_url': base_url,
                    'connected_at': datetime.utcnow().isoformat(),
                    'status': 'connected'
                }
                logger.info(f"GitHub integration setup successful for user: {username}")
            else:
                logger.error(f"GitHub integration setup failed: {result['message']}")
            
            return result
        except Exception as e:
            logger.error(f"Error setting up GitHub integration: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to setup GitHub integration: {str(e)}',
                'error': str(e)
            }
    
    def setup_gitlab(self, username: str, password: str, base_url: str = "https://gitlab.com") -> Dict:
        """Setup GitLab integration"""
        try:
            self.gitlab_service = GitLabService(username, password, base_url)
            result = self.gitlab_service.test_connection()
            
            if result['success']:
                self.connections['gitlab'] = {
                    'service': self.gitlab_service,
                    'username': username,
                    'base_url': base_url,
                    'connected_at': datetime.utcnow().isoformat(),
                    'status': 'connected'
                }
                logger.info(f"GitLab integration setup successful for user: {username}")
            else:
                logger.error(f"GitLab integration setup failed: {result['message']}")
            
            return result
        except Exception as e:
            logger.error(f"Error setting up GitLab integration: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to setup GitLab integration: {str(e)}',
                'error': str(e)
            }
    
    def setup_jenkins(self, username: str, password: str, base_url: str) -> Dict:
        """Setup Jenkins integration"""
        try:
            self.jenkins_service = JenkinsService(username, password, base_url)
            result = self.jenkins_service.test_connection()
            
            if result['success']:
                self.connections['jenkins'] = {
                    'service': self.jenkins_service,
                    'username': username,
                    'base_url': base_url,
                    'connected_at': datetime.utcnow().isoformat(),
                    'status': 'connected'
                }
                logger.info(f"Jenkins integration setup successful for user: {username}")
            else:
                logger.error(f"Jenkins integration setup failed: {result['message']}")
            
            return result
        except Exception as e:
            logger.error(f"Error setting up Jenkins integration: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to setup Jenkins integration: {str(e)}',
                'error': str(e)
            }
    
    def get_connection_status(self) -> Dict:
        """Get status of all integrations"""
        status = {}
        for tool, connection in self.connections.items():
            status[tool] = {
                'status': connection['status'],
                'username': connection['username'],
                'base_url': connection['base_url'],
                'connected_at': connection['connected_at']
            }
        return status
    
    def test_all_connections(self) -> Dict:
        """Test all active integrations"""
        results = {}
        
        if self.github_service:
            results['github'] = self.github_service.test_connection()
        
        if self.gitlab_service:
            results['gitlab'] = self.gitlab_service.test_connection()
        
        if self.jenkins_service:
            results['jenkins'] = self.jenkins_service.test_connection()
        
        return results
    
    def get_all_pipelines(self) -> Dict:
        """Get pipelines from all connected services"""
        pipelines = {
            'github': [],
            'gitlab': [],
            'jenkins': [],
            'total_count': 0
        }
        
        try:
            # Get GitHub workflow runs
            if self.github_service:
                # This would need to be configured with specific repos
                # For now, return empty list
                pipelines['github'] = []
            
            # Get GitLab pipelines
            if self.gitlab_service:
                # This would need to be configured with specific projects
                # For now, return empty list
                pipelines['gitlab'] = []
            
            # Get Jenkins jobs
            if self.jenkins_service:
                result = self.jenkins_service.get_jobs()
                if result['success']:
                    pipelines['jenkins'] = result['data']
                else:
                    pipelines['jenkins'] = []
            
            # Calculate total
            pipelines['total_count'] = (
                len(pipelines['github']) + 
                len(pipelines['gitlab']) + 
                len(pipelines['jenkins'])
            )
            
            return {
                'success': True,
                'data': pipelines
            }
        except Exception as e:
            logger.error(f"Error fetching all pipelines: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching pipelines: {str(e)}',
                'error': str(e)
            }
    
    def get_all_builds(self, limit: int = 100) -> Dict:
        """Get builds from all connected services"""
        builds = {
            'github': [],
            'gitlab': [],
            'jenkins': [],
            'total_count': 0
        }
        
        try:
            # Get Jenkins builds
            if self.jenkins_service:
                result = self.jenkins_service.get_jobs()
                if result['success']:
                    for job in result['data'][:10]:  # Limit to 10 jobs
                        job_builds = self.jenkins_service.get_builds(job['name'], limit=5)
                        if job_builds['success']:
                            builds['jenkins'].extend(job_builds['data'])
            
            # Calculate total
            builds['total_count'] = (
                len(builds['github']) + 
                len(builds['gitlab']) + 
                len(builds['jenkins'])
            )
            
            return {
                'success': True,
                'data': builds
            }
        except Exception as e:
            logger.error(f"Error fetching all builds: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching builds: {str(e)}',
                'error': str(e)
            }
    
    def get_dashboard_metrics(self) -> Dict:
        """Get comprehensive dashboard metrics from all services"""
        try:
            metrics = {
                'total_pipelines': 0,
                'total_builds': 0,
                'success_rate': 0,
                'failure_rate': 0,
                'average_build_time': 0,
                'recent_activity': [],
                'service_status': self.get_connection_status()
            }
            
            # Get pipeline and build counts
            pipelines_result = self.get_all_pipelines()
            builds_result = self.get_all_builds()
            
            if pipelines_result['success']:
                metrics['total_pipelines'] = pipelines_result['data']['total_count']
            
            if builds_result['success']:
                metrics['total_builds'] = builds_result['data']['total_count']
                
                # Calculate success/failure rates from Jenkins builds
                jenkins_builds = builds_result['data']['jenkins']
                if jenkins_builds:
                    successful = sum(1 for build in jenkins_builds if build.get('result') == 'SUCCESS')
                    failed = sum(1 for build in jenkins_builds if build.get('result') == 'FAILURE')
                    total = len(jenkins_builds)
                    
                    if total > 0:
                        metrics['success_rate'] = round((successful / total) * 100, 2)
                        metrics['failure_rate'] = round((failed / total) * 100, 2)
                
                # Calculate average build time
                build_times = [build.get('duration', 0) for build in jenkins_builds if build.get('duration')]
                if build_times:
                    metrics['average_build_time'] = round(sum(build_times) / len(build_times), 2)
            
            return {
                'success': True,
                'data': metrics
            }
        except Exception as e:
            logger.error(f"Error fetching dashboard metrics: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching metrics: {str(e)}',
                'error': str(e)
            }
    
    def disconnect_service(self, service_name: str) -> Dict:
        """Disconnect a specific service"""
        try:
            if service_name in self.connections:
                if service_name == 'github':
                    self.github_service = None
                elif service_name == 'gitlab':
                    self.gitlab_service = None
                elif service_name == 'jenkins':
                    self.jenkins_service = None
                
                del self.connections[service_name]
                
                return {
                    'success': True,
                    'message': f'{service_name} service disconnected successfully'
                }
            else:
                return {
                    'success': False,
                    'message': f'{service_name} service not found'
                }
        except Exception as e:
            logger.error(f"Error disconnecting {service_name} service: {str(e)}")
            return {
                'success': False,
                'message': f'Error disconnecting service: {str(e)}',
                'error': str(e)
            }
    
    def disconnect_all(self) -> Dict:
        """Disconnect all services"""
        try:
            self.github_service = None
            self.gitlab_service = None
            self.jenkins_service = None
            self.connections.clear()
            
            return {
                'success': True,
                'message': 'All services disconnected successfully'
            }
        except Exception as e:
            logger.error(f"Error disconnecting all services: {str(e)}")
            return {
                'success': False,
                'message': f'Error disconnecting services: {str(e)}',
                'error': str(e)
            }
