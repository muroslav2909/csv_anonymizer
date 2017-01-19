from Crypto.Cipher import AES
from Crypto import Random
import os

def get_hash_key():
    with open('hash_key.txt', 'r+') as f:
        hash_key = f.read()
        if not hash_key:
            hash_key = os.urandom(16)
            f.write(hash_key)
    f.close()
    return hash_key

def un_anonymize_data(iv, cipher, anonymized_data):
    return cipher.decrypt(anonymized_data.decode("hex"))[len(iv):]

key = get_hash_key()
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CFB, iv)
anonymized_data = raw_input('please enter data: \n')
print un_anonymize_data(iv, cipher, anonymized_data)