import subprocess
import time
from config import ALLOWED_TOOLS

def is_command_allowed(command):
    if not command:
        return False
    
    command_name = command.split()[0]
    return command_name in ALLOWED_TOOLS

def run_command(command):
    if not is_command_allowed(command):
        return {"success": False, "output": "", "duration": 0, "error": "Command not allowed"}

    start_time = time.time()

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )
    end_time = time.time()
    return {
        "success": True,
        "output": result.stdout,
        "duration": end_time - start_time,
        "error": result.stderr
    }