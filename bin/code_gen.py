import hashlib
import random
import os
import csv


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


def save_codes_to_csv(codes):
    file_path = os.path.join(os.getcwd(), "generated_codes.csv")
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Code"])
        for code in codes:
            writer.writerow([code])
    return file_path


def main():
    try:
        num_codes = int(input("Inserisci il numero di codici da generare: "))
        if num_codes <= 0:
            raise ValueError("Il numero di codici deve essere maggiore di zero.")

        print("Generazione dei codici in corso...")
        unique_codes = generate_unique_codes(num_codes)

        file_path = save_codes_to_csv(unique_codes)
        print(f"I codici sono stati salvati in: {file_path}")

    except ValueError as e:
        print(f"Errore: {e}")


if __name__ == "__main__":
    main()