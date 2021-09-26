from argparse import ArgumentParser
from getpass import getpass
import base64, json, os

def encode(string, key, metadata):
    string = f"{metadata}==={string}"
    encoded_chars = []
    for i in range(len(string)):
        encoded_chars.append(chr(ord(string[i]) + ord(key[i % len(key)]) % 256))
    return "".join(encoded_chars)

def decode(string, key):
    decoded_chars = []
    for i in range(len(string)):
        decoded_chars.append(chr((ord(string[i]) - ord(key[i % len(key)]) + 256) % 256))
    return "".join(decoded_chars).split("===")

def encrypt(path, key):
    with open(path, "rb") as f:
        try:
            e = encode(str(base64.b64encode(f.read()))[2:-1], key, json.dumps({
                "fname" : path.split("/")[-1].split(".")[0],
                "extension" : path.split("/")[-1].split(".")[1]
            }))
        except UnicodeDecodeError:
            return "\nThere was an error with the file byte contents\n"
    encrypted = f"{path.split('/')[-1].split('.')[0]}_{path.split('/')[-1].split('.')[1]}.enfc"
    try:
        if os.path.isfile(encrypted):
            if not input("\nThis file encryption already exists.  Would you like to override it? (y/n)\n> ").lower() == "y":
                return "File not saved since user denied to override it\n"
        with open(encrypted, "w") as f:
            f.write(e)
    except OSError:
        return "\nThere was an error with the creation of the encrypted file\n"
    return f"\nSuccessfully encrypted file at {encrypted}\n"

def decrypt(path, key):
    with open(path, "r") as f:
        try:
            meta, d = decode(str(f.read()), key)
            meta = json.loads(meta)
        except UnicodeDecodeError:
            return "\nThere was an error with the file byte contents\n"
        except ValueError:
            return False
    decrypted = f"{meta['fname']}.{meta['extension']}"
    try:
        if os.path.isfile(decrypted):
            print("\nCorrect password!")
            if not input("\nThis file already exists.  Would you like to override it? (y/n)\n> ").lower() == "y":
                return "File not saved since user denied to override it\n"
        with open(decrypted, "wb") as f:
            f.write(base64.b64decode(d))
    except OSError:
        return "There was an error with the creation of the decrypted file\n"
    return f"\nDecrypted file: {decrypted}\nHopefully you entered a valid decryption password!\n"

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename", help="Filename to be encrypted/decrypted")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--encrypt", help="Encrypt the file", action="store_true")
    group.add_argument("-d", "--decrypt", help="Decrypt the file", action="store_true")
    args = parser.parse_args()
    if args.encrypt:
        print("\nCreate an encryption password\n\033[95mMake sure to remember this password!\033[0m\n")
        while True:
            p1 = getpass("Create password: ")
            if p1 == getpass("Confirm password: "):
                print(encrypt(args.filename, p1))
                break
            print("\n\033[91mPasswords do not match!\033[0m")
        if input("Would you like to remove the original file? (y/n)\n> ").lower() == "y":
            os.remove(args.filename)
            print(f"\nDeleted {args.filename}\n")
    elif args.decrypt:
        if not args.filename[-5:] == ".enfc" :
            args.filename += ".enfc"
        while True:
            dm = decrypt(args.filename, getpass("Decryption password: "))
            if dm:
                print(dm)
                break
            print("\nInvalid decryption password\n")
        if input("Would you like to remove the encrypted file? (y/n)\nEnsure that the file has been successfully decrypted first!\n> ").lower() == "y":
            os.remove(args.filename)
            print(f"\nDeleted {args.filename}\n")
