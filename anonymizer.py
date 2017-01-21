from Crypto.Cipher import AES
import os
import csv
import base64

def get_hash_key():
    with open('hash_key.txt', 'r+') as f:
        hash_key = f.read()
        if not hash_key:
            hash_key = os.urandom(16)
            f.write(hash_key)
    f.close()
    return hash_key

def anonymize_data(cipher, data, size=64):
    data = (data).rjust(size)
    return base64.b64encode(cipher.encrypt(data))

def get_header():
    with open("input_file.csv") as f:
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames
    f.close()
    return headers

def write_to_csv(cipher):
    with open('output1.csv', 'w') as csvfile:
        headers = get_header()
        fieldnames = headers
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with open("input_file.csv") as f:
            # rows = csv.reader(f)
            # total_column = len(headers)
            lines = f.read().splitlines()[1:]
            for i in range(len(lines)):
                data = lines[i].split(',')
                dict = {}
                counter = 0
                for name in headers:
                    try:
                        anonymized_data = anonymize_data(cipher, data[counter])
                    except:
                        anonymized_data = anonymize_data(cipher, data[counter], size=512)
                    dict[name] = anonymized_data
                    counter += 1
                writer.writerow(dict)


key = get_hash_key()
cipher = AES.new(key, AES.MODE_ECB)
write_to_csv(cipher)


