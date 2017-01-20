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


def get_header():
    with open("input_file.csv") as f:
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames
    f.close()
    return headers


def write_to_csv():
    with open('output1.csv', 'w') as csvfile:
        headers = get_header()
        fieldnames = headers
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with open("input_file.csv") as f:
            # rows = csv.reader(f)
            # total_column = len(headers)
            for line in f:
                data = line.split(',')
                anonymized_data = anonymize_data(iv, cipher, data[1])
                dict = {}
                for name in headers:
                    dict[name] = anonymized_data
                writer.writerow(dict)


key = get_hash_key()
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CFB, iv)
write_to_csv()