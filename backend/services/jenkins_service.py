import requests
import json
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class JenkinsService:
    """Jenkins API service for CI/CD pipeline monitoring"""
    
    def __init__(self, username: str, password: str, base_url: str):
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self._setup_auth()
    
    def _setup_auth(self):
        """Setup authentication for Jenkins API"""
        self.session.auth = (self.username, self.password)
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def test_connection(self) -> Dict:
        """Test Jenkins API connection"""
        try:
            response = self.session.get(f"{self.base_url}/api/json")
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'message': f'Successfully connected to Jenkins',
                    'data': {
                        'version': data.get('version'),
                        'description': data.get('description'),
                        'url': data.get('url')
                    }
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to connect: {response.status_code} - {response.text}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Jenkins connection test failed: {str(e)}")
            return {
                'success': False,
                'message': f'Connection failed: {str(e)}',
                'error': str(e)
            }
    
    def get_jobs(self, folder: Optional[str] = None) -> Dict:
        """Get all jobs from Jenkins"""
        try:
            if folder:
                url = f"{self.base_url}/job/{folder}/api/json"
            else:
                url = f"{self.base_url}/api/json"
            
            response = self.session.get(url, params={'tree': 'jobs[name,url,color,description]'})
            if response.status_code == 200:
                data = response.json()
                jobs = data.get('jobs', [])
                return {
                    'success': True,
                    'data': jobs,
                    'count': len(jobs)
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch jobs: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch Jenkins jobs: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching jobs: {str(e)}',
                'error': str(e)
            }
    
    def get_job_info(self, job_name: str, folder: Optional[str] = None) -> Dict:
        """Get detailed information about a specific job"""
        try:
            if folder:
                url = f"{self.base_url}/job/{folder}/job/{job_name}/api/json"
            else:
                url = f"{self.base_url}/job/{job_name}/api/json"
            
            response = self.session.get(url)
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch job info: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch Jenkins job info: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching job info: {str(e)}',
                'error': str(e)
            }
    
    def get_builds(self, job_name: str, folder: Optional[str] = None, limit: int = 50) -> Dict:
        """Get builds for a specific job"""
        try:
            if folder:
                url = f"{self.base_url}/job/{folder}/job/{job_name}/api/json"
            else:
                url = f"{self.base_url}/job/{job_name}/api/json"
            
            response = self.session.get(url, params={'tree': f'builds[number,url,timestamp,result,duration,description]&limit={limit}'})
            if response.status_code == 200:
                data = response.json()
                builds = data.get('builds', [])
                return {
                    'success': True,
                    'data': builds,
                    'count': len(builds)
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch builds: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch Jenkins builds: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching builds: {str(e)}',
                'error': str(e)
            }
    
    def get_build_info(self, job_name: str, build_number: int, folder: Optional[str] = None) -> Dict:
        """Get detailed information about a specific build"""
        try:
            if folder:
                url = f"{self.base_url}/job/{folder}/job/{job_name}/{build_number}/api/json"
            else:
                url = f"{self.base_url}/job/{job_name}/{build_number}/api/json"
            
            response = self.session.get(url)
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch build info: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch Jenkins build info: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching build info: {str(e)}',
                'error': str(e)
            }
    
    def get_build_logs(self, job_name: str, build_number: int, folder: Optional[str] = None) -> Dict:
        """Get logs for a specific build"""
        try:
            if folder:
                url = f"{self.base_url}/job/{folder}/job/{job_name}/{build_number}/consoleText"
            else:
                url = f"{self.base_url}/job/{job_name}/{build_number}/consoleText"
            
            response = self.session.get(url)
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.text
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch build logs: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch Jenkins build logs: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching build logs: {str(e)}',
                'error': str(e)
            }
    
    def trigger_build(self, job_name: str, folder: Optional[str] = None, parameters: Optional[Dict] = None) -> Dict:
        """Trigger a new build for a job"""
        try:
            if folder:
                url = f"{self.base_url}/job/{folder}/job/{job_name}/build"
            else:
                url = f"{self.base_url}/job/{job_name}/build"
            
            if parameters:
                # For parameterized builds
                url = url.replace('/build', '/buildWithParameters')
                response = self.session.post(url, data=parameters)
            else:
                response = self.session.post(url)
            
            if response.status_code in [200, 201]:
                return {
                    'success': True,
                    'message': f'Build triggered successfully for {job_name}',
                    'data': {
                        'job_name': job_name,
                        'status': 'triggered',
                        'timestamp': datetime.utcnow().isoformat()
                    }
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to trigger build: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to trigger Jenkins build: {str(e)}")
            return {
                'success': False,
                'message': f'Error triggering build: {str(e)}',
                'error': str(e)
            }
    
    def get_queue_info(self) -> Dict:
        """Get information about the build queue"""
        try:
            url = f"{self.base_url}/queue/api/json"
            response = self.session.get(url)
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch queue info: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch Jenkins queue info: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching queue info: {str(e)}',
                'error': str(e)
            }
