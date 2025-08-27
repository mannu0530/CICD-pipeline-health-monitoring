from flask import Blueprint, request, jsonify
from datetime import datetime

bp = Blueprint('builds', __name__, url_prefix='/api/v1/builds')

@bp.route('/', methods=['GET'])
def list_builds():
    """List all builds"""
    return jsonify({
        'success': True,
        'data': [],
        'message': 'Builds endpoint - coming soon',
        'timestamp': datetime.utcnow().isoformat()
    })
