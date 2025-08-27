from flask import Blueprint, request, jsonify
from datetime import datetime

bp = Blueprint('alerts', __name__, url_prefix='/api/v1/alerts')

@bp.route('/', methods=['GET'])
def list_alerts():
    """List all alerts"""
    return jsonify({
        'success': True,
        'data': [],
        'message': 'Alerts endpoint - coming soon',
        'timestamp': datetime.utcnow().isoformat()
    })
