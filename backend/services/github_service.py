import requests
import base64
import json
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GitHubService:
    """GitHub API service for CI/CD pipeline monitoring"""
    
    def __init__(self, username: str, password: str, base_url: str = "https://api.github.com"):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.session = requests.Session()
        self._setup_auth()
    
    def _setup_auth(self):
        """Setup authentication for GitHub API"""
        if self.password.startswith('ghp_') or self.password.startswith('github_pat_'):
            # Personal Access Token
            self.session.headers.update({
                'Authorization': f'token {self.password}',
                'Accept': 'application/vnd.github.v3+json'
            })
        else:
            # Username/Password authentication
            self.session.auth = (self.username, self.password)
            self.session.headers.update({
                'Accept': 'application/vnd.github.v3+json'
            })
    
    def test_connection(self) -> Dict:
        """Test GitHub API connection"""
        try:
            response = self.session.get(f"{self.base_url}/user")
            if response.status_code == 200:
                user_data = response.json()
                return {
                    'success': True,
                    'message': f'Successfully connected to GitHub as {user_data.get("login")}',
                    'user': user_data
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to connect: {response.status_code} - {response.text}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"GitHub connection test failed: {str(e)}")
            return {
                'success': False,
                'message': f'Connection failed: {str(e)}',
                'error': str(e)
            }
    
    def get_repositories(self, org: Optional[str] = None) -> Dict:
        """Get repositories from GitHub"""
        try:
            if org:
                url = f"{self.base_url}/orgs/{org}/repos"
            else:
                url = f"{self.base_url}/user/repos"
            
            response = self.session.get(url, params={'per_page': 100})
            if response.status_code == 200:
                repos = response.json()
                return {
                    'success': True,
                    'data': repos,
                    'count': len(repos)
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch repositories: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch GitHub repositories: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching repositories: {str(e)}',
                'error': str(e)
            }
    
    def get_workflow_runs(self, owner: str, repo: str, branch: Optional[str] = None) -> Dict:
        """Get workflow runs for a repository"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/actions/runs"
            params = {'per_page': 100}
            if branch:
                params['branch'] = branch
            
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'data': data.get('workflow_runs', []),
                    'total_count': data.get('total_count', 0)
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch workflow runs: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch GitHub workflow runs: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching workflow runs: {str(e)}',
                'error': str(e)
            }
    
    def get_workflow_run_details(self, owner: str, repo: str, run_id: int) -> Dict:
        """Get detailed information about a specific workflow run"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/actions/runs/{run_id}"
            response = self.session.get(url)
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch workflow run: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch GitHub workflow run details: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching workflow run details: {str(e)}',
                'error': str(e)
            }
    
    def get_workflow_jobs(self, owner: str, repo: str, run_id: int) -> Dict:
        """Get jobs for a specific workflow run"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/actions/runs/{run_id}/jobs"
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'data': data.get('jobs', [])
                }
            else:
                return {
                    'success': False,
                    'message': f'Failed to fetch workflow jobs: {response.status_code}',
                    'error': response.text
                }
        except Exception as e:
            logger.error(f"Failed to fetch GitHub workflow jobs: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching workflow jobs: {str(e)}',
                'error': str(e)
            }
    
    def get_workflow_logs(self, owner: str, repo: str, job_id: int) -> Dict:
        """Get logs for a specific job"""
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/actions/jobs/{job_id}/logs"
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
            logger.error(f"Failed to fetch GitHub job logs: {str(e)}")
            return {
                'success': False,
                'message': f'Error fetching job logs: {str(e)}',
                'error': str(e)
            }
