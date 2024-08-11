import subprocess
import tempfile
import os
import time

def lambda_handler(event, context):
    code = event.get('code', '')
    user_input = event.get('user_input', '')

    if not code:
        return {
            'error': True,
            'data': {
                'message': 'Code not found'
            }
        }

    try:
        # Create temporary file for C++ code
        with tempfile.NamedTemporaryFile(suffix='.cpp', delete=False) as cpp_file:
            cpp_file.write(code.encode('utf-8'))
            cpp_file_path = cpp_file.name

        # Compile the C++ code
        executable_path = cpp_file_path[:-4]

        compile_process = subprocess.run(
            ['g++', cpp_file_path, '-o', executable_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        if compile_process.returncode != 0:
            return {
                'error': True,
                'data': {
                    'message': 'Compilation error',
                    'details': compile_process.stderr
                }
            }

        start_time = time.time()
        # Execute the compiled code with input
        execution_process = subprocess.run(
            [executable_path],
            input=user_input,
            capture_output=True,
            text=True,
            timeout=5
        )
        end_time = time.time()
        # Return the output
        return {
            'error': False,
            'data': {
                'message': 'Success',
                'output': execution_process.stdout,
                'error': execution_process.stderr,
                'exec_time': end_time - start_time
            }
        }

    except subprocess.TimeoutExpired:
        return {
            'error': True,
            'data': {
                'message': 'Took too long to run'
            }
        }
    except Exception as e:
        return {
            'error': True,
            'body': {
                'message': 'Internal Server Error',
                'error': str(e)
            }
        }
    finally:
        # Cleanup temporary files
        if os.path.exists(cpp_file_path):
            os.remove(cpp_file_path)
        if os.path.exists(executable_path):
            os.remove(executable_path)
