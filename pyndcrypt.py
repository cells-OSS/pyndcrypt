import os
import sys
import subprocess
import pyfiglet
import requests
from cryptography.fernet import Fernet
from packaging import version

__version__ = "v1.7"


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

welcomeMessage_config_path = os.path.join(config_dir, "welcome_message.conf")
figlet_config_path = os.path.join(config_dir, "figlet.conf")
auto_update_config_path = os.path.join(config_dir, "auto_update.conf")


if os.path.isfile(welcomeMessage_config_path):
    with open(welcomeMessage_config_path, "rb") as configFile:
        welcomeMessage = configFile.read().decode()
else:
    welcomeMessage = """
    ===============WELCOME===============

    """
if os.path.exists(figlet_config_path):
    with open(figlet_config_path, "rb") as figlet_configFile:
        figlet_config = figlet_configFile.read().decode()
        if figlet_config == "True":
            welcomeMessage = pyfiglet.figlet_format(welcomeMessage)


if os.path.exists(auto_update_config_path):
    with open(auto_update_config_path, "rb") as auto_update_configFile:
        auto_update_config = auto_update_configFile.read().decode()
        if auto_update_config == "True":
            if is_update_available(__version__):
                print("New version available!")
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

        file_input = input("Which file do you want to decrypt?: ")

        for file in os.listdir():

            if file_input.lower() == "back":
                os.execv(sys.executable, [sys.executable] + sys.argv)

            files = [f.strip() for f in file_input.split(',') if f.strip()]

            if file[0] == ".":
                continue

            files.append(file)
            break

        print(files)

        decryptionKey = input("Enter the name of the decryption key: ")

        if decryptionKey.lower() == "back":
            os.execv(sys.executable, [sys.executable] + sys.argv)

        with open(decryptionKey, "rb") as decryption_key:
            secretkey = decryption_key.read()

        keyInput = input(
            "Press any key after placing the key in the current directory...")

        for file in files:
            with open(file, "rb") as thefile:
                contents = thefile.read()
            contents_decrypted = Fernet(secretkey).decrypt(contents)
            with open(file, "wb") as thefile:
                thefile.write(contents_decrypted)
        print("Your file has been decrypted!")

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

        1 = Turn on
        2 = Turn off
        """

            print(figletWelcome)
            figletOption = input("Which option would you like to choose(1/2)?: ")

            if figletOption.lower() == "back":
                os.execv(sys.executable, [sys.executable] + sys.argv)

            if figletOption == "1":

                config_path = os.path.join(config_dir, "figlet.conf")

                with open(config_path, "wb") as figlet_configFile:
                    figlet_configFile.write("True".encode())

                print("Changes saved successfully!")
                input("Press any key to restart...")
                os.execv(sys.executable, [sys.executable] + sys.argv)

            if figletOption == "2":
                config_path = os.path.join(config_dir, "figlet.conf")

                if os.path.exists(config_path):
                    os.remove(config_path)

                print("Changes saved successfully!")
                input("Press any key to restart...")
                subprocess.Popen([sys.executable] + sys.argv)
                sys.exit()

            else:
                print("Invalid option.")
                input("Press Enter to restart...")
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

        else:
            print("Invalid option.")
            input("Press Enter to restart...")
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