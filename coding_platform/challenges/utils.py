import os
import uuid

TEMP_DIR = "C:\Users\96650\OneDrive\Desktop\code\coding_challenge_platform\coding_platform\temp_code"  # Change this to the actual path

def save_code_to_file(code, language_extension):
    # Generate a unique filename for the code file
    filename = f"{uuid.uuid4()}.{language_extension}"
    file_path = os.path.join(TEMP_DIR, filename)

    # Write the code to the file
    with open(file_path, "w") as code_file:
        code_file.write(code)
    
    return file_path

import subprocess

def execute_code(file_path, language):
    """
    Executes the code saved in the temporary file based on the selected language.
    
    :param file_path: The path to the file containing the user's code
    :param language: The language in which the code is written (e.g., 'python', 'java')
    :return: The output or error message from the execution
    """
    try:
        # Run the code depending on the language
        if language == "python":
            result = subprocess.run(
                ["python", file_path], capture_output=True, text=True, timeout=5
            )
        elif language == "java":
            result = subprocess.run(
                ["javac", file_path], capture_output=True, text=True, timeout=5
            )
            result = subprocess.run(
                ["java", file_path.replace(".java", "")], capture_output=True, text=True, timeout=5
            )
        elif language == "cpp":
            executable_path = file_path.replace(".cpp", "")
            subprocess.run(["g++", file_path, "-o", executable_path], timeout=5)
            result = subprocess.run([executable_path], capture_output=True, text=True, timeout=5)
        
        # Return the output if successful, or the error if failed
        return result.stdout if result.returncode == 0 else result.stderr
    except subprocess.TimeoutExpired:
        return "Execution timed out."
    except Exception as e:
        return f"Error: {str(e)}"

import os

def clean_up(file_path):
    """
    Deletes the temporary code file after execution to free up resources.
    
    :param file_path: The path of the temporary code file to be deleted
    """
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error: {file_path} : {e.strerror}")

import subprocess

def execute_code(file_path, language, timeout=5):
    """
    Executes code from a file with a time limit.
    
    Args:
        file_path (str): Path to the code file to execute.
        language (str): Programming language of the code (for setting the command).
        timeout (int): Maximum execution time in seconds.
    
    Returns:
        str: Output of the code execution, or an error message if execution fails or times out.
    """
    # Command based on the language (adjust paths/commands as needed)
    commands = {
        "python": ["python", file_path],
        "java": ["java", file_path],
        "cpp": ["g++", file_path, "-o", "program.out", "&&", "./program.out"]
    }
    
    command = commands.get(language)
    if not command:
        return "Unsupported language."

    try:
        # Run the command with a timeout
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout  # Specify timeout in seconds
        )
        
        # Capture output and errors
        if result.returncode == 0:
            return result.stdout  # Successful execution
        else:
            return result.stderr  # Error during execution

    except subprocess.TimeoutExpired:
        return "Execution timed out."
    except Exception as e:
        return f"An error occurred: {e}"
