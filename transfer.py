# transfer.py
# Author: fredsta
# Version: 19.09.2021
# Purpose: Translate one encrypted file to another key

from cryptography.fernet import Fernet

class transfer:
    def transfer(old_key, new_key, old_path):
        old_fernet = Fernet(old_key.encode())
        new_fernet = Fernet(new_key.encode())

        lines = []
        decrypted = []
        with open(old_path, "r") as f:
            for line in f:
                lines.append(line)
                decrypted.append([])
        
        # Decrypt things with old key
        for j in range(len(lines)):
            for i in range(3):
                decrypted_stuff = old_fernet.decrypt(line[100*i:100+100*i].encode()).decode()
                decrypted[j].append(decrypted_stuff)
        
        # Encrypt with new key and save to file
        with open(".data.txt", "w") as f:
            for j in range(len(decrypted)):
                encrypted = ""
                for i in range(3):
                    encrypted += new_fernet.encrypt(decrypted[j][i].encode()).decode() 
                f.write(encrypted + "\n")
                

if __name__ == '__main__':
    old_key = "f8JxI5ZHAEhq-3ch1j20LC3oxeL63lONQCBODUFfYoA="
    new_key = "Z9VL9ytgJS9bcYCtJhtwIjKN-SWVVcTxv5oexh5Yjno="
    transfer.transfer(old_key, new_key, "hellow.txt")