# transfer.py
# Author: fredsta
# Version: 19.09.2021
# Purpose: Translate one encrypted file to another key

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

        # ToDo: Override the .config file with the new key
    
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
        export_path += "/heinz.txt"
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

            

if __name__ == '__main__':
    old_key = "f8JxI5ZHAEhq-3ch1j20LC3oxeL63lONQCBODUFfYoA="
    new_key = "Z9VL9ytgJS9bcYCtJhtwIjKN-SWVVcTxv5oexh5Yjno="
    #transfer.transfer(old_key, new_key, "hanspeter.txt")
    #transfer.export("testexport.txt")