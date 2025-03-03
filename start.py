import os
import subprocess
import platform
import string
import random
import json

try:

        # Determine the OS
        OS = platform.system()

        # Define the virtual environment activation command
        if OS in ["Linux", "Darwin"]:
            print(f"Activating venv for {OS}")
            activate_cmd = ". .venv/bin/activate"
        elif OS == "Windows":
            print(f"Activating venv for {OS}")
            activate_cmd = ".venv\\Scripts\\activate"
        else:
            print("Unsupported OS")
            exit()

        # Function to run a shell command
        def run_command(command, shell=True):
            result = subprocess.run(command, shell=shell, text=True)
            if result.returncode != 0:
                print(f"Error running command: {command}")
                exit()

        # Check if .env file exists
        if not os.path.exists(".env"):
            print("Warning: .env file not found. Creating one now...")
            f = open(".env", "a")
            size = 69
            chars = string.ascii_letters + string.digits + string.punctuation
            SECRET_KEY = ''.join(c.lower() if random.choice([True, False]) else c for c in (random.choice(chars) for _ in range(size)))
            f.write(f"SECRET_KEY={SECRET_KEY}")
            f.close()
            print("Created .env")

        # Check if virtual environment exists
        if not os.path.exists(".venv"):
            print("Virtual environment not found. Creating one...")
            if OS in ["Linux", "Darwin"]:
                run_command("python -m venv .venv")
            elif OS == "Windows":
                run_command("py -m venv .venv")

            print("Created .venv")

        with open('conf.json', 'r') as file:
            conf = json.load(file)

        port = conf["port"]

        # Activate virtual environment
        if OS == "Windows":
            venv_cmd = f'cmd.exe /c "{activate_cmd} && pip install -r requirements.txt && py manage.py makemigrations && py manage.py migrate && py manage.py runserver 0.0.0.0:{port}"'
            subprocess.run(venv_cmd, shell=True)
        else:
            commands = [
                f"{activate_cmd} && pip install -r requirements.txt",
                f"{activate_cmd} && python manage.py makemigrations",
                f"{activate_cmd} && python manage.py migrate",
                f"{activate_cmd} && python manage.py runserver 0.0.0.0:{port}"
            ]

            for cmd in commands:
                run_command(cmd)


except KeyboardInterrupt as e:
    print("\nStopping server...")
    exit()