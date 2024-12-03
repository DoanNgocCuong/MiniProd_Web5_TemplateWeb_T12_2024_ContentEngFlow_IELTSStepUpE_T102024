from flask import Blueprint, jsonify
import subprocess
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('scripts', __name__)

SCRIPTS_FOLDER = Path(__file__).parent.parent / 'scripts'

@bp.route('/run/<script_name>', methods=['POST'])
def run_script(script_name):
    script_path = SCRIPTS_FOLDER / f'{script_name}.py'
    
    if not script_path.exists():
        logger.error(f'Script not found: {script_name}')
        return jsonify({'error': f'Script {script_name} not found'}), 404
        
    try:
        logger.info(f'Running script: {script_name}')
        result = subprocess.run(
            ['python', str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(SCRIPTS_FOLDER)  # Set working directory to scripts folder
        )
        
        if result.returncode == 0:
            logger.info(f'Script {script_name} completed successfully')
            return jsonify({
                'success': True,
                'message': f'Script {script_name} executed successfully',
                'output': result.stdout
            })
        else:
            logger.error(f'Script {script_name} failed: {result.stderr}')
            return jsonify({
                'success': False,
                'error': result.stderr
            }), 500
            
    except Exception as e:
        logger.error(f'Error running script {script_name}: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 