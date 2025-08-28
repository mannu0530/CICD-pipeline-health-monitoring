import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GitLabService:
    """GitLab API service for CI/CD pipeline monitoring"""
    
    def __init__(self, username: str, password: str, base_url: str = "https://gitlab.com"):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.session = requests.Session()
        self._setup_auth()
    
    def _setup_auth(self):
        """Setup authentication for GitLab API"""
        if self.password.startswith('glpat-'):
            # Personal Access Token
            self.session.headers.update({
                'PRIVATE-TOKEN': self.password,
                'Content-Type': 'application/json'
            })
        else:
            # Username/Password authentication
            self.session.auth = (self.username, self.password)
            self.session.headers.update({
                'Content-Type': 'application/json'
            })
    
    def test_connection(self) -> Dict:
        """Test GitLab API connection"""
        try:
            response = self.session.get(f"{self.base_url}/api/v4/user")
            if response.status_code == 200:
                user_data = response.json()
                return {
                    'success': True,
                    'message': f'Successfully connected to GitLab as {user_data.get("username")}',
                    'user': user_data
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to connect: {response.status_code} - {response.text}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"GitLab connection test failed: {str(e)}")
            return {
                'success': False,
                'message': f'Connection failed: {str(e)}',
                'error': str(e)
            }
    
    def get_projects(self, group_id: Optional[int] = None) -> Dict:
        """Get projects from GitLab"""
        try:
            if group_id:
                url = f"{self.base_url}/api/v4/groups/{group_id}/projects"
            else:
                url = f"{self.base_url}/api/v4/projects"
            
            response = self.session.get(url, params={'per_page': 100})
            if response.status_code == 200:
                projects = response.json()
                return {
                    'success': True,
                    'data': projects,
                    'count': len(projects)
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch projects: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch GitLab projects: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching projects: {str(e)}',
                'error': str(e)
            }
    
    def get_pipelines(self, project_id: int, branch: Optional[str] = None) -> Dict:
        """Get pipelines for a project"""
        try:
            url = f"{self.base_url}/api/v4/projects/{project_id}/pipelines"
            params = {'per_page': 100}
            if branch:
                params['ref'] = branch
            
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                pipelines = response.json()
                return {
                    'success': True,
                    'data': pipelines,
                    'count': len(pipelines)
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch pipelines: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch GitLab pipelines: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching pipelines: {str(e)}',
                'error': str(e)
            }
    
    def get_pipeline_details(self, project_id: int, pipeline_id: int) -> Dict:
        """Get detailed information about a specific pipeline"""
        try:
            url = f"{self.base_url}/api/v4/projects/{project_id}/pipelines/{pipeline_id}"
            response = self.session.get(url)
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch pipeline: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch GitLab pipeline details: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching pipeline details: {str(e)}',
                'error': str(e)
            }
    
    def get_pipeline_jobs(self, project_id: int, pipeline_id: int) -> Dict:
        """Get jobs for a specific pipeline"""
        try:
            url = f"{self.base_url}/api/v4/projects/{project_id}/pipelines/{pipeline_id}/jobs"
            response = self.session.get(url)
            if response.status_code == 200:
                jobs = response.json()
                return {
                    'success': True,
                    'data': jobs
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch pipeline jobs: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch GitLab pipeline jobs: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching pipeline jobs: {str(e)}',
                'error': str(e)
            }
    
    def get_job_logs(self, project_id: int, job_id: int) -> Dict:
        """Get logs for a specific job"""
        try:
            url = f"{self.base_url}/api/v4/projects/{project_id}/jobs/{job_id}/trace"
            response = self.session.get(url)
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.text
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch job logs: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch GitLab job logs: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching job logs: {str(e)}',
                'error': str(e)
            }
    
    def get_project_variables(self, project_id: int) -> Dict:
        """Get project variables (for CI/CD configuration)"""
        try:
            url = f"{self.base_url}/api/v4/projects/{project_id}/variables"
            response = self.session.get(url)
            if response.status_code == 200:
                variables = response.json()
                return {
                    'success': True,
                    'data': variables
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch project variables: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch GitLab project variables: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching project variables: {str(e)}',
                'error': str(e)
            }
