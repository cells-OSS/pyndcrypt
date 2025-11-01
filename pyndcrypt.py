import os
from logging import config
import json
import sys
import base64
import hashlib
import subprocess
import pyfiglet
import requests
from cryptography.fernet import Fernet
from packaging import version

__version__ = "v2.0"


def get_latest_release_tag():
    try:
        url = "https://api.github.com/repos/cells-OSS/pyndcrypt/releases/latest"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["tag_name"].lstrip("v")
    except Exception as e:
        print("Failed to check for updates:", e)
        return __version__.lstrip("v")


def is_update_available(current_version):
    latest = get_latest_release_tag()
    return version.parse(latest) > version.parse(current_version.lstrip("v"))


def download_latest_script():
    latest_version = get_latest_release_tag()
    filename = f"pyndcrypt-v{latest_version}.py"
    url = "https://raw.githubusercontent.com/cells-OSS/pyndcrypt/main/pyndcrypt.py"
    response = requests.get(url)
    lines = response.text.splitlines()
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line.rstrip() + "\n")
    print(
        f"Current version: {__version__}, Latest: v{get_latest_release_tag()}")
    print(
        f"Downloaded update as '{filename}'. You can now safely delete the old version.")

    input("Press Enter to exit...")
    exit()

if os.name == "nt":
    config_dir = os.path.join(os.getenv("APPDATA"), "pyndcrypt")
else:
    config_dir = os.path.expanduser("~/.config/pyndcrypt")

os.makedirs(config_dir, exist_ok=True)

config_path = os.path.join(config_dir, "config.json")

def load_config():
    path = os.path.join(config_dir, "config.json")
    if not os.path.exists(path):
        default = {"auto_updates": True, "figlet_welcome": False}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4)
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(config):
    with open(os.path.join(config_dir, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

def toggle_auto_updates():
    config = load_config()
    
    config["auto_updates"] = not config.get("auto_updates", True)
    
    save_config(config)
    print(f"Auto updates are now {'ON' if config['auto_updates'] else 'OFF'}")

def toggle_figlet():
    config = load_config()
    
    config["figlet_welcome"] = not config.get("figlet_welcome", False)
    
    save_config(config)
    print(f"Figlet welcome message is now {'ON' if config['figlet_welcome'] else 'OFF'}")

welcomeMessage_config_path = os.path.join(config_dir, "welcome_message.conf")

if os.path.isfile(welcomeMessage_config_path):
    with open(welcomeMessage_config_path, "rb") as configFile:
        welcomeMessage = configFile.read().decode()
else:
    welcomeMessage = """
    ===============WELCOME===============

    """
if config["figlet_welcome"]:
    welcomeMessage = pyfiglet.figlet_format(welcomeMessage)


if config["auto_updates"]:
    if is_update_available(__version__):
        print("A new version of Pyculator is available!")
        user_input = input(
            "Would you like to download the latest version? (y/n): ").strip().lower()
        if user_input == "y":
            download_latest_script()

menu = """
1 = Encryptor
2 = Decryptor
3 = Settings

TIP: If you want to come back to this menu at any time, just type "back"
"""

print(welcomeMessage, menu)

chooseOption = input("Which option would you like to choose(1/2/3)?: ")

if chooseOption == "1":
    while True:
        file_input = input("Which file(s) do you want to encrypt: ")

        if file_input.lower() == "back":
            os.execv(sys.executable, [sys.executable] + sys.argv)

        files = [f.strip() for f in file_input.split(',') if f.strip()]

        for file in files:
            if not os.path.isfile(file):
                print(f"File(s) not found: {file}")
                subprocess.Popen([sys.executable] + sys.argv)
                sys.exit()

        print(files)

        confirmationMessage = input(
            "The file(s) shown above will be encrypted, are you sure(y/N)?: ")

        if confirmationMessage.lower() == "y":
            keyOption = input("Would you like to generate a key(Y/n)?: ")
            if keyOption.lower() == "n":
                user_key = input("Enter your custom key (passphrase or base64 key): ").strip()
                try:
                    decoded = base64.urlsafe_b64decode(user_key)
                    if len(decoded) == 32:
                        key = user_key.encode()
                    else:
                        raise ValueError("not 32 bytes")
                except Exception:
                    key = base64.urlsafe_b64encode(hashlib.sha256(user_key.encode()).digest())
                keyName = input("The name of the key: ")
            
            else:
                key = Fernet.generate_key()
                keyName = input("The name of the key: ")

            with open(keyName + ".txt", "wb") as decryption_key:
                decryption_key.write(key)

            for file in files:
                with open(file, "rb") as thefile:
                    contents = thefile.read()
                contents_encrypted = Fernet(key).encrypt(contents)
                with open(file, "wb") as thefile:
                    thefile.write(contents_encrypted)

            print("File(s) encrypted successfully!")
        else:
            print("Encryption canceled.")

        input("Press any key to restart...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

if chooseOption == "2":
    while True:

        file_input = input("Which file(s) do you want to decrypt?: ")


        if file_input.lower() == "back":
            os.execv(sys.executable, [sys.executable] + sys.argv)

        files = [f.strip() for f in file_input.split(',') if f.strip()]

        print(files)

        decryption_input = input("Enter the decryption key (paste key or passphrase): ").strip()
        if decryption_input.lower() == "back":
            os.execv(sys.executable, [sys.executable] + sys.argv)

        try:
            decoded = base64.urlsafe_b64decode(decryption_input)
            if len(decoded) == 32:
                key = decryption_input.encode()
            else:
                raise ValueError("not 32 bytes")
        except Exception:
            key = base64.urlsafe_b64encode(hashlib.sha256(decryption_input.encode()).digest())

        try:
            for file in files:
                with open(file, "rb") as thefile:
                    contents = thefile.read()
                contents_decrypted = Fernet(key).decrypt(contents)
                with open(file, "wb") as thefile:
                    thefile.write(contents_decrypted)
            print("Your file(s) have been decrypted!")
        except Exception as e:
            print("Decryption failed:", e)

        input("Press any key to restart...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

if chooseOption == "3":
    while True:

        settingsMenu = """
    ===============SETTINGS===============

    1 = Change welcome message
    2 = Figlet welcome message
    3 = Reset welcome message
    4 = Change auto-update settings
    """
        print(settingsMenu)

        chooseSetting = input(
            "Which setting would you like to change(1/2/3/4)?: ")

        if chooseSetting.lower() == "back":
            os.execv(sys.executable, [sys.executable] + sys.argv)

        if chooseSetting == "1":
            new_welcomeMessage = input("New welcome message: ")

            config_path = os.path.join(config_dir, "welcome_message.conf")

            with open(config_path, "wb") as configFile:
                configFile.write(new_welcomeMessage.encode())

            print("Changes saved successfully!")
            input("Press any key to restart...")
            os.execv(sys.executable, [sys.executable] + sys.argv)

        if chooseSetting == "2":
            figletWelcome = """
        ===============FIGLET===============

        1 = Toggle Figlet welcome message
        """

            print(figletWelcome)
            figletOption = input("Which option would you like to choose(1/2)?: ")

            if figletOption.lower() == "back":
                os.execv(sys.executable, [sys.executable] + sys.argv)

            if figletOption == "1":
                toggle_figlet()
                print("Figlet welcome message setting toggled.")
                input("Press Enter to continue...")
                os.execv(sys.executable, [sys.executable] + sys.argv)

        if chooseSetting == "3":
            config_path = os.path.join(config_dir, "welcome_message.conf")

            if os.path.exists(config_path):
                os.remove(config_path)
                print("Changes saved successfully!")
                input("Press any key to restart...")
                os.execv(sys.executable, [sys.executable] + sys.argv)
            else:
                print("You haven't changed the welcome message yet!")
                input("Press any key to restart...")
                os.execv(sys.executable, [sys.executable] + sys.argv)


        if chooseSetting == "4":
            aUpdateMenu = """
    ===============AUTO-UPDATE===============

    1 = Turn on
    2 = Turn off
    """

            print(aUpdateMenu)
            aUpdateOption = input(
                "Which option would you like to choose(1/2)?: ")

            if aUpdateOption.lower() == "back":
                os.execv(sys.executable, [sys.executable] + sys.argv)

            if aUpdateOption == "1":
                config_path = os.path.join(config_dir, "auto_update.conf")

                with open(config_path, "wb") as auto_update_configFile:
                    auto_update_configFile.write("True".encode())

                print("Changes saved successfully!")
                input("Press any key to restart...")
                os.execv(sys.executable, [sys.executable] + sys.argv)

            if aUpdateOption == "2":
                with open(config_path, "wb") as auto_update_configFile:
                    auto_update_configFile.write("False".encode())

                print("Changes saved successfully!")
                input("Press any key to restart...")
                os.execv(sys.executable, [sys.executable] + sys.argv)
            
            else:
                print("Invalid option.")
                input("Press Enter to restart...")
                os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print("Invalid option.")
            input("Press Enter to restart...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
else:
    print("Invalid option.")
    input("Press Enter to restart...")
    os.execv(sys.executable, [sys.executable] + sys.argv)