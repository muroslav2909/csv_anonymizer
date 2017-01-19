from Crypto.Cipher import AES
from Crypto import Random
import os
import csv

def get_hash_key():
    with open('hash_key.txt', 'r+') as f:
        hash_key = f.read()
        if not hash_key:
            hash_key = os.urandom(16)
            f.write(hash_key)
    f.close()
    return hash_key

def anonymize_data(iv, cipher, data):
    msg = iv + cipher.encrypt(data)
    return msg.encode("hex")


# with open("input_file.csv", "rb") as f:
#     # reader = csv.reader(f, delimiter="\t")
#     reader = csv.reader(f, delimiter="\n")
#     for row in reader:
#         # content = list(row[i] for i in included_cols)
#         print row[0]


with open("input_file.csv") as f:
    rows = csv.reader(f)
    total_line, total_column = 0, 0
    for line in f:
        total_column = len(line.split(','))
        break
    for line in f:
        data = line.split(',')[1]
        key = get_hash_key()
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, iv)

        anonymized_data = anonymize_data(iv, cipher, data)
        print anonymized_data
