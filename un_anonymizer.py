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

def un_anonymize_data(cipher, anonymized_data):
    return cipher.decrypt(base64.b64decode(anonymized_data))

def get_header():
    with open("output1.csv") as f:
        d_reader = csv.DictReader(f)
        headers = d_reader.fieldnames
    f.close()
    return headers

def write_to_csv(cipher, names=None):
    with open('output2.csv', 'w') as csvfile:
        headers = get_header()
        fieldnames = headers
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with open("output1.csv") as f:
            lines = f.read().splitlines()[1:]
            for i in range(len(lines)):
                data = lines[i].split(',')
                dict = {}
                counter = 0

                for name in headers:
                    if not names:
                        un_anonymized_data = un_anonymize_data(cipher, data[counter]).lstrip()
                    else:
                        un_anonymized_data = data[counter]
                        if name in names:
                            un_anonymized_data = un_anonymize_data(cipher, data[counter]).lstrip()

                    dict[name] = un_anonymized_data
                    counter += 1
                writer.writerow(dict)

key = get_hash_key()
cipher = AES.new(key, AES.MODE_ECB)
# write_to_csv(cipher)

if 'all' in sys.argv:
    write_to_csv(cipher)
elif 'names' in sys.argv:
    column_names = raw_input("Please enter column names separeted by comma\n")
    try:
        write_to_csv(cipher, column_names)
    except:
        print "Please, be sure that you are entered anonymize column names."
else:
    print "Availible arguments are:\n all - unanonymize all column\n names - unanonymize choosen columns\n\n Please try: python un_anonymizer.py all or python un_anonymizer.py names"
