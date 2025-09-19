from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
from services import IntegrationService

bp = Blueprint('config', __name__, url_prefix='/api/v1/config')

# Global integration service instance
integration_service = IntegrationService()

logger = logging.getLogger(__name__)

@bp.route('/', methods=['GET'])
def get_config():
    """Get system configuration and integration status"""
    try:
        connection_status = integration_service.get_connection_status()
        return jsonify({
            'success': True,
            'data': {
                'environment': 'development',
                'version': '1.0.0',
                'integrations': connection_status,
                'timestamp': datetime.utcnow().isoformat()
            },
            'message': 'Configuration retrieved successfully'
        })
    except Exception as e:
        logger.error(f"Error getting configuration: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error retrieving configuration: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/integrations/github', methods=['POST'])
def setup_github():
    """Setup GitHub integration"""
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        base_url = data.get('base_url', 'https://api.github.com')
        result = integration_service.setup_github(
            username=data['username'],
            password=data['password'],
            base_url=base_url
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error setting up GitHub integration: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error setting up GitHub integration: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/integrations/gitlab', methods=['POST'])
def setup_gitlab():
    """Setup GitLab integration"""
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        base_url = data.get('base_url', 'https://gitlab.com')
        result = integration_service.setup_gitlab(
            username=data['username'],
            password=data['password'],
            base_url=base_url
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error setting up GitLab integration: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error setting up GitLab integration: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/integrations/jenkins', methods=['POST'])
def setup_jenkins():
    """Setup Jenkins integration"""
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data or 'base_url' not in data:
            return jsonify({
                'success': False,
                'message': 'Username, password, and base_url are required'
            }), 400
        
        result = integration_service.setup_jenkins(
            username=data['username'],
            password=data['password'],
            base_url=data['base_url']
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error setting up Jenkins integration: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error setting up Jenkins integration: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/integrations/test', methods=['POST'])
def test_integrations():
    """Test all active integrations"""
    try:
        result = integration_service.test_all_connections()
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Integration tests completed'
        })
    except Exception as e:
        logger.error(f"Error testing integrations: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error testing integrations: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/integrations/<service_name>/disconnect', methods=['DELETE'])
def disconnect_service(service_name):
    """Disconnect a specific service"""
    try:
        result = integration_service.disconnect_service(service_name)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    except Exception as e:
        logger.error(f"Error disconnecting {service_name}: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error disconnecting {service_name}: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/integrations/disconnect-all', methods=['DELETE'])
def disconnect_all():
    """Disconnect all services"""
    try:
        result = integration_service.disconnect_all()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error disconnecting all services: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error disconnecting all services: {str(e)}',
            'error': str(e)
        }), 500

@bp.route('/integrations/status', methods=['GET'])
def get_integration_status():
    """Get status of all integrations"""
    try:
        status = integration_service.get_connection_status()
        return jsonify({
            'success': True,
            'data': status,
            'message': 'Integration status retrieved successfully'
        })
    except Exception as e:
        logger.error(f"Error getting integration status: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Error getting integration status: {str(e)}',
            'error': str(e)
        }), 500
