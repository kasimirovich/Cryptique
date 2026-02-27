from nacl import secret, utils
import os
import io
import zipfile
import subprocess

CURRENT_PATH = os.getcwd()
KEY = bytes.fromhex("c22cfd614357dee0da056d284ef97fbb2ff8dfe199a40019803b4e1c9a71f1b9")

def generate_zipfile() -> io.BytesIO:

    memzip = io.BytesIO()
    with zipfile.ZipFile(memzip, "w", zipfile.ZIP_STORED) as zf:
        for root, dirs, files in os.walk(CURRENT_PATH):
            dirs[:] = [d for d in dirs if d not in ['.venv', '.git', "__pycache__", "keys"]]
            
            for file in files:
                filepath = os.path.join(root, file)
                
                arcname = os.path.relpath(filepath, CURRENT_PATH)
                zf.write(filepath, arcname)
    memzip.seek(0)
    return memzip

def encrypt(memzip: io.BytesIO) -> io.BytesIO:
        box = secret.SecretBox(KEY)
        data = memzip.getvalue()
        return io.BytesIO(box.encrypt(data))

def upload():
    hexer = KEY.hex()
    memzip = generate_zipfile()
    encrypted = encrypt(memzip)
    


def download():
    encrypted = io.BytesIO() ## platzhalter für Die Github Download sachen
    dec = secret.SecretBox(KEY)
    decrypted = dec.decrypt(encrypted.getvalue())

def main():
    if not os.path.exists(os.path.join(CURRENT_PATH, "keys")):
         os.mkdir("keys")
         
    if not os.path.exists(os.path.join(CURRENT_PATH, ".git")):
        print("No git folder found. Exiting...")
        exit()

    print(r"""
 \ \   /       |              ___|                      |   
  \   /  _` |  __ \   |   |  |       __|  |   |  __ \   __| 
     |  (   |  | | |  |   |  |      |     |   |  |   |  |   
    _| \__,_| _| |_| \__,_| \____| _|    \__, |  .__/  \__| 
                                         ____/  _|                                                        
""")
    while True:

        choice = input("What do you want to do?\na) upload\nb) download\nYour choice -> ")
        if choice.lower().strip() == "a":
            upload()
            break
            
        elif choice.lower().strip() == "b":
            download()
            break

        else:
            subprocess.run("cls", shell=True)
        

    



if __name__ == "__main__":
    main()