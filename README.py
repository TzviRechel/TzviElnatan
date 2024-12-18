import subprocess
import pytest
from threading import Timer
import os

# Default parameters
TIME_FOR_TEST = 3  # Timeout for each script in seconds
COM_PORT = "COM4"
MAC_ADDRESS = "84:72:93:3c:5d:d6"

# Path to the directory containing attack scripts
SCRIPTS_DIRECTORY = "./attack_scripts"

# The failure phrase to look for in the output
FAILURE_PHRASE = "The device may have crashed"

# Dynamically list all Python files in the specified directory
def get_attack_scripts(directory):
    return [
        os.path.join(directory, f) for f in os.listdir(directory)
        if f.endswith(".py")
    ]

attack_scripts = get_attack_scripts(SCRIPTS_DIRECTORY)

@pytest.mark.parametrize("script_name", attack_scripts)
def test_attack_script(script_name):
    """
    Run an attack script, capture its output, and validate it.
    """
    command = ["python", script_name, COM_PORT, MAC_ADDRESS]
    print(f"Running script: {script_name}")

    try:
        # Run the script with a timeout
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        timer = Timer(TIME_FOR_TEST, process.terminate)  # Terminate process after timeout
        timer.start()
        stdout, stderr = process.communicate()  # Capture stdout and stderr
    finally:
        timer.cancel()  # Cancel the timer if the process finishes

    # Combine stdout and stderr for full output
    full_output = stdout + stderr
    print(f"Output of {script_name}:\n{full_output}\n{'=' * 50}")

    # Assert that the output does not contain the failure phrase
    assert FAILURE_PHRASE not in full_output, f"Script {script_name} failed. Found '{FAILURE_PHRASE}' in output."
