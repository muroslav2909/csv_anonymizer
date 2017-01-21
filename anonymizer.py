from Crypto.Cipher import AES
import os
import csv
import base64
import sys

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

def write_to_csv(cipher, names=None):
    with open('output1.csv', 'w') as csvfile:
        headers = get_header()
        fieldnames = headers
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        with open("input_file.csv") as f:
            lines = f.read().splitlines()[1:]
            for i in range(len(lines)):
                data = lines[i].split(',')
                dict = {}
                counter = 0
                for name in headers:
                    if not names:
                        try:
                            anonymized_data = anonymize_data(cipher, data[counter])
                        except:
                            anonymized_data = anonymize_data(cipher, data[counter], size=512)
                        dict[name] = anonymized_data
                    else:
                        value = data[counter]
                        if name in names:
                            try:
                                anonymized_data = anonymize_data(cipher, data[counter])
                            except:
                                anonymized_data = anonymize_data(cipher, data[counter], size=512)
                            value = anonymized_data
                        dict[name] = value

                    counter += 1
                writer.writerow(dict)


key = get_hash_key()
cipher = AES.new(key, AES.MODE_ECB)
if 'all' in sys.argv:
    write_to_csv(cipher)
elif 'names' in sys.argv:
    column_names = raw_input("Please enter column names separeted by comma\n")
    write_to_csv(cipher, column_names)
else:
    print "Availible arguments are:\n all - anonymize all column\n names - anonymize choosen columns\n\n Please try: python anonymizer.py all or python anonymizer.py names"
