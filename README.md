# pyndcrypt
A simple CLI file encryption/decryption script made with Python.

This script will either encrypt or decrypt the files that you choose.

# USE AT YOUR OWN RISK
 
I AM NOT RESPONSIBLE FOR ANY DATA LOSS, MAKE SURE TO KEEP THE DECRYPTION KEY IN A SECURE PLACE.

This script has been inspired by NetworkChuck: https://www.youtube.com/watch?v=UtMMjXOlRQc

Credits to him, this script at core has the code from NetworkChuck. It's just a fun project I wanted to try, he on his video made a "ransomware", but i decided to take the code and make it a encryption/decryption script.

# HOW TO USE?

-----ENCRYPTION (option 1)-----

First of all, make sure you have the file you want to encrypt in the same folder as the script. Then run the script and choose the first option. Then type the name of the file(s) you want to encrypt(put a comma between the files if you want to encrypt more than one file at a time). It will ask you if you're sure you want to encrypt the file and if answered positively there will be a .txt file created with the name of "decryption_key.txt" and if you choose to encrypt more than one file at a time they will be sharing the same decryption key. Typing "back" at any moment will take you back to the welcome message.

-----DECRYPTION (option 2)-----

First of all, make sure you have the file you want to decrypt in the same folder as the script. Then run the script and choose the second option. Then type the name of the file(s) you want to decrypt(put a comma between the files if you want to decrypt more than one file at a time). it will ask you to put the decryption key in the same directory of the script and it will ask for the name of the decryption key. After that it should decrypt the file(s) that you chose. Typing "back" at any moment will take you back to the welcome message.

-----SETTINGS (option 3)-----

Change welcome message (0) = This will allow you to change the message that pops up each time you run the script. Just choose the setting and then type in whatever you want. This will create a config file in the same directory as the script and save the setting there. Deleting this file will reset the welcome message to default.

# THE HISTORY

This script is a merged version of https://github.com/cells-OSS/pyncrypt and https://github.com/cells-OSS/pydcrypt. The projects pyncrypt and pydcrypt are no longer going to get updated and possibly going to get archived. This script will keep on receiving updates.

# PREREQUISITES
python (https://www.python.org/)

cryptography (Windows = pip install cryptography, MacOS/Linux = pip3 install cryptography)

# Addressing the False Positives.
Here is a virustotal report as of 9/19/2025: https://www.virustotal.com/gui/file/0db857c225c2c0694775d277083387ce87a3f16ce71f03ac9efefe2da5ffe354?nocache=1

You can see here that only 2 vendors flag it as malicious one of which is the Windows Defender.
I have looked into the code with VSCode without trusting the window and seems like the issue is at the 3rd line, which is "from cryptography.fernet import Fernet"
this line just imports fernet from the library cryptography, which is an encryption algorithm/method that this script uses to encrypt/decrypt the files. Malicious actors can also use this for a ransomware. We recommend excluding this script from Windows Defender.