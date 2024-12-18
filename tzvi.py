import subprocess
import pytest
from threading import Timer
import json
import os

# Path to the JSON configuration file
CONFIG_FILE = "config.json"

# Load configuration from JSON
def load_config(config_file):
    with open(config_file, "r") as file:
        return json.load(file)

config = load_config(CONFIG_FILE)

# Extract parameters from config
TIME_FOR_TEST = config["SLEEP_TIME"]
COM_PORT = config["COM"]
MAC_ADDRESS = config["address"]
SCRIPTS = config["test_list"]
# PATH = config["attack_path"]

# The failure phrase to look for in the output
FAILURE_PHRASE = "The device may have crashed"

@pytest.mark.parametrize("script_name", SCRIPTS)
def test_attack_script(script_name):
    """
    Run an attack script, capture its output, and validate it.
    """

    command = ["python", script_name, COM_PORT, MAC_ADDRESS]
    print(command)
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
