# transfer.py
# Author: fredsta
# Version: 30.09.2021
# Translate one encrypted file to another key

from cryptography.fernet import Fernet

class transfer:
    @staticmethod
    def transfer(old_path):
        # works like import, but import is a keyword in python...
        new_key = ""
        with open(".config", "r") as config:
            new_key = config.readlines()[0].strip("\n")
        old_key = transfer.get_old_key(old_path)
        old_fernet = Fernet(old_key.encode())
        new_fernet = Fernet(new_key.encode())

        lines = []
        decrypted = []
        with open(old_path, "r") as f:
            for line in f:
                lines.append(line)
                decrypted.append([])
        
        # Decrypt things with old key
        j = 0
        for line in lines:
            separators, index = [], 0
            separators.append(0)
            for i in range(2):
                index = line.find("|", index)
                separators.append(index)
                index += 1
            separators.append(len(line))
            for q in range(3):
                decrypted_stuff = old_fernet.decrypt(line[separators[q]:separators[q+1]].encode()).decode()
                decrypted[j].append(decrypted_stuff)
            j += 1
        
        # Encrypt with new key and save to file
        with open(".data.txt", "w") as f:
            for j in range(len(decrypted)):
                encrypted = ""
                for i in range(3):
                    encrypted += new_fernet.encrypt(decrypted[j][i].encode()).decode() + "|"
                f.write(encrypted + "\n")

    
    @staticmethod
    def get_old_key(path):
        # Old key is/will be stored in the first line of the data-transfer file
        key = ""
        content = []
        with open(path, "r") as f:
            content = f.readlines()
        key = content.pop(0).strip("\n")
        with open(path, "w") as g:
            for line in content:
                g.writelines(line)
        return key

    @staticmethod
    def export(export_path):
        print("Export's running...")
        # Exports the data-file including the key to the given path
        key = ""
        content = []
        with open(".config", "r") as config:
            key = config.readlines()[0].strip("\n")
        content.append(key+"\n")
        with open(".data.txt", "r") as data:
            for line in data:
                content.append(line)
        with open(export_path, "w") as output:
            for line in content:
                output.writelines(line)