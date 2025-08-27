from flask import Blueprint, request, jsonify
from datetime import datetime

bp = Blueprint('config', __name__, url_prefix='/api/v1/config')

@bp.route('/', methods=['GET'])
def get_config():
    """Get system configuration"""
    return jsonify({
        'success': True,
        'data': {
            'environment': 'development',
            'version': '1.0.0'
        },
        'message': 'Configuration endpoint - coming soon',
        'timestamp': datetime.utcnow().isoformat()
    })
