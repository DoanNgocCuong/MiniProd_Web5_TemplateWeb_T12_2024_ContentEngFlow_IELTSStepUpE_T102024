from flask import Blueprint, jsonify, request
import asyncio
import subprocess
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('scripts', __name__)

SCRIPTS_FOLDER = Path(__file__).parent.parent / 'scripts'

# Create thread pool
executor = ThreadPoolExecutor(max_workers=4)  # Limit concurrent scripts

def run_script_task(script_path):
    try:
        result = subprocess.run(
            ['python', str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(SCRIPTS_FOLDER)
        )
        return result
    except Exception as e:
        return str(e)

@bp.route('/run-multiple', methods=['POST'])
def run_multiple_scripts():
    script_names = request.json.get('scripts', [])
    results = {}
    
    # Run scripts in parallel using thread pool
    futures = []
    for script_name in script_names:
        script_path = SCRIPTS_FOLDER / f'{script_name}.py'
        if script_path.exists():
            future = executor.submit(run_script_task, script_path)
            futures.append((script_name, future))
    
    # Collect results
    for script_name, future in futures:
        result = future.result()
        if isinstance(result, subprocess.CompletedProcess):
            if result.returncode == 0:
                results[script_name] = {
                    'success': True,
                    'output': result.stdout
                }
            else:
                results[script_name] = {
                    'success': False,
                    'error': result.stderr
                }
        else:
            results[script_name] = {
                'success': False,
                'error': str(result)
            }
    
    return jsonify(results) 