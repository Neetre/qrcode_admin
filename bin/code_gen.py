import hashlib
import random
import argparse
from data_manager import DataManager

datamanager = DataManager("../data/qr_codes.db")

def generate_complex_code():
    random_seed = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=128))
    hash_object = hashlib.sha256(random_seed.encode('utf-8'))
    hashed_code = hash_object.hexdigest()
    return hashed_code[:64]


def generate_unique_codes(count):
    codes = set()
    while len(codes) < count:
        codes.add(generate_complex_code())
    return list(codes)


def save_codes(codes):
    file_path = "../data/codes.txt"
    with open(file_path, 'w') as file:
        for code in codes:
            file.write(f"{code}\n")
            datamanager.insert_code(code)
    return file_path


def parse_args():
    parser = argparse.ArgumentParser(description='Generatore di codici univoci')
    parser.add_argument('-n', '--num_codes', type=int, help='Numero di codici da generare')
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        num_codes = args.num_codes
        if num_codes <= 0:
            raise ValueError("Il numero di codici deve essere maggiore di zero.")

        print("Generazione dei codici in corso...")
        unique_codes = generate_unique_codes(num_codes)

        file_path = save_codes(unique_codes)
        print(f"I codici sono stati salvati in: {file_path}")

    except ValueError as e:
        print(f"Errore: {e}")


if __name__ == "__main__":
    main()