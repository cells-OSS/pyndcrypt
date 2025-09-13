import os
import sys
from cryptography.fernet import Fernet

welcomeMessage = """
===============WELCOME===============
1 = Encryptor
2 = Decryptor

TIP: If you want to come back to this menu at any time, just type "back"
"""

print(welcomeMessage)

chooseOption = input("Which option would you like to choose(1/2)?: ")

if chooseOption == 1:
    while True:
        file_input = input("Which file(s) do you want to encrypt: ")
        
        if file_input.lower() == "back":
            os.execl(sys.executable, sys.executable, *sys.argv)

        files = [f.strip() for f in file_input.split(',') if f.strip()]

        for file in files:
            if not os.path.isfile(file):
                print(f"File(s) not found: {file}")
                os.execl(sys.executable, sys.executable, *sys.argv)

        print(files)

        confirmationMessage = input("The file(s) shown above will be encrypted, are you sure(y/N)?: ")

        if confirmationMessage.lower() == "y":
            key = Fernet.generate_key()

            with open("decryption_key.txt", "wb") as decryption_key:
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
            os.execl(sys.executable, sys.executable, *sys.argv)

if chooseOption == 2:
    while True:
        for file in os.listdir():
            file_input = input("Which file do you want to decrypt?: ")

            if file_input.lower() == "back":
                os.execl(sys.executable, sys.executable, *sys.argv)
            
            files = [f.strip() for f in file_input.split(',') if f.strip()]
            
            files.append(file)
            break

        print(files)

        decryptionKey = input("Enter the name of the decryption key related to the file you want to decrypt: ")

        if decryptionKey.lower() == "back":
            os.execl(sys.executable, sys.executable, *sys.argv)

        with open(decryptionKey, "rb") as decryption_key:
            secretkey = decryption_key.read()

        keyInput = input("Press any key after placing the key in the current directory...")

        for file in files:
            with open(file, "rb") as thefile:
                contents = thefile.read()
            contents_decrypted = Fernet(secretkey).decrypt(contents)
            with open(file, "wb") as thefile:
                thefile.write(contents_decrypted)
        print("Your file has been decrypted!")
        
        input("Press any key to restart...")
        os.execl(sys.executable, sys.executable, *sys.argv)