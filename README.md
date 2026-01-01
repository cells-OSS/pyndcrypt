# pyndcrypt
A simple CLI file encryption/decryption script written in Python.

This script will either encrypt or decrypt the files that you choose.

# USE AT YOUR OWN RISK
 
I AM NOT RESPONSIBLE FOR ANY DATA LOSS, MAKE SURE TO KEEP THE DECRYPTION KEY IN A SECURE PLACE.

This script has been inspired by NetworkChuck: https://www.youtube.com/watch?v=UtMMjXOlRQc

Credits to him, this script at core has the code from NetworkChuck. It's just a fun project I wanted to try, he on his video made a "ransomware", but i decided to take the code and make it an encryption/decryption script.

# PREREQUISITES
[Python](https://www.python.org/)

WARNING FOR LINUX USERS!

Even though automatic prerequisite installation is supported, some Linux distributions (such as Arch Linux) may not include the pip package manager by default.
If you want to use the automatic prerequisite installation, please consult your local package manager for the python package manager.

If you prefer to manually install these python packages, please refer to [pip-packages.md](https://github.com/cells-OSS/pyndcrypt/blob/main/pip-packages.md)

# HOW TO USE?

-----ENCRYPTION (option 1)-----

First of all, make sure you have the file you want to encrypt in the same folder as the script. Then run the script and choose the first option. Then type the name of the file(s) you want to encrypt (put a comma between the files if you want to encrypt more than one file at a time). It will ask you if you're sure you want to encrypt the file and if answered positively it will ask you if you want to create a strong passphrase or if you want to use your own password. Then the file that you chose to encrypt will be encrypted with the passphrase you provided or the program generated. if you choose to encrypt more than one file at a time they will share the same decryption key. If you choose to generate a passphrase it will ask you for a file name and then the generated key will be saved in a file with the name of your choosing. Typing "back" at any moment will take you back to the welcome message.

-----DECRYPTION (option 2)-----

First of all, make sure you have the file you want to decrypt in the same folder as the script. Then run the script and choose the second option. Then type the name of the file(s) you want to decrypt (put a comma between the files if you want to decrypt more than one file at a time). It will ask you for the passphrase. After that it should decrypt the file(s) that you chose. Typing "back" at any moment will take you back to the welcome message.

-----SETTINGS (option 3)-----

Change welcome message (0) = This will allow you to change the message that pops up each time you run the script. Just choose the setting and then type in whatever you want. This will create a config file in the same directory as the script and save the setting there. Deleting this file will reset the welcome message to default.

Figlet welcome message (1) = This will turn on or off the figlet-style welcome message font. Once turned on (turned off by default) it will create a figlet.conf file that will say "True" inside of it.

Reset welcome message (2) = This will reset the welcome message by deleting the welcome message configuration file.

# THE HISTORY

This script is a merged version of 2 seperate scripts called pyncrypt and pyndcrypt. The projects pyncrypt and pydcrypt are no longer going to get updated and they are currently privately archived. This script will keep on receiving updates.

# Addressing the False Positives.
Here is a virustotal report as of 9/19/2025: https://www.virustotal.com/gui/file/0db857c225c2c0694775d277083387ce87a3f16ce71f03ac9efefe2da5ffe354?nocache=1

You can see here that some vendors flag it as malicious one of which is the Windows Defender.
I have looked into the code with VSCode without trusting the window and seems like the issue is at one of the imports, which is "from cryptography.fernet import Fernet"
this line just imports fernet from the library cryptography, which is an encryption algorithm/method that this script uses to encrypt/decrypt the files. Malicious actors can also use this for a ransomware. We recommend excluding this script from Windows Defender. If you have any concerns about the safety of this script, it's completely open source meaning you or anyone else can check the code for malwares at any time.