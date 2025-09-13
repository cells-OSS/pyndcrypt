# pyndcrypt
A simple CLI file encryption/decryption script made with Python.

This script will either encrypt or decrypt the files that you choose.

# USE AT YOUR OWN RISK
 
I AM NOT RESPONSIBLE FOR ANY DATA LOSS, MAKE SURE TO KEEP THE DECRYPTION KEY IN A SECURE PLACE.

This script has been inspired by NetworkChuck: https://www.youtube.com/watch?v=UtMMjXOlRQc

Credits to him, this script at core has the code from NetworkChuck. It's just a fun project I wanted to try, he on his video made a "ransomware", but i decided to take the code and make it a encryption/decryption script.

# HOW TO USE?

-----ENCRYPTION-----

First of all, make sure you have the file you want to encrypt in the same folder as the script. Then run the script and choose the first option. Then type the name of the file(s) you want to encrypt(put a comma between the files if you want to encrypt more than one file at a time). It will ask you if you're sure you want to encrypt the file and if answered positively there will be a .txt file created with the name of "decryption_key.txt" and if you choose to encrypt more than one file at a time they will be sharing the same decryption key. Typing "back" at any moment will take you back to the welcome message.

-----DECRYPTION-----

First of all, make sure you have the file you want to decrypt in the same folder as the script. Then run the script and choose the second option. Then type the name of the file(s) you want to decrypt(put a comma between the files if you want to decrypt more than one file at a time). it will ask you to put the decryption key in the same directory of the script and it will ask for the name of the decryption key (by default it's called "decryption_key"). After that it should decrypt the file(s) that you chose. Typing "back" at any moment will take you back to the welcome message.

# THE HISTORY

This script is a merged version of https://github.com/cells-OSS/pyncrypt and https://github.com/cells-OSS/pydcrypt. The projects pyncrypt and pydcrypt are no longer going to get updated and possibly going to get archived. This script will keep on receiving updates.