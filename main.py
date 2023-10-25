import os
import sys

# Funkcija, ka ģenerē one-time pad (OTP) un saglabā to failā
def generate_otp_file(otp_filename, length):
    # Ģenerē listi ar random baitiem 
    otp = [bytes([os.urandom(1)[0] for _ in range(1)]) for _ in range(length)]
    
    # Ieraksta OTP failā, bināri
    with open(otp_filename, 'wb') as otp_file:
        otp_file.write(b''.join(otp))

# Funkcija, kas izmantojot OTP sašifrē failu un saglabā to
def encrypt_file(input_filename, encrypted_filename):
    # Nolasa ievades faila saturu 
    with open(input_filename, 'rb') as input_file:
        input_data = input_file.read()

    # Ģenerē OTP, tādā pašā garumā kā ievades dati  
    otp_filename = encrypted_filename + '.otp'
    generate_otp_file(otp_filename, len(input_data))

    # Nolasa OTP no OTP faila 
    with open(otp_filename, 'rb') as otp_file:
        otp = otp_file.read()

    # Pārliecinās, ka ievades dati un OTP dati ir vienādā garumā
    if len(input_data) != len(otp):
        print("Kļūda: Ievades failam un OTP failam ir jābūt vienādā garumā.")
        return

    # Sašifrē ievades datus izmantojot XOR pret OTP
    encrypted_data = bytes([a ^ b for a, b in zip(input_data, otp)])

    # Ieraksta šifrētos datus jaunajā failā, bināri 
    with open(encrypted_filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    print(f"Fails '{input_filename}' ir sašifrēts un saglabāts kā '{encrypted_filename}'.")

# Funkcija, kas atšifrē failu izmantojot OTP 
def decrypt_file(encrypted_filename, decrypted_filename):
    # Uzģenerē OTP faila nosaukumu
    otp_filename = encrypted_filename + '.otp'

    # Nolasa sašifrētā faila saturu 
    with open(encrypted_filename, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    # No OTP faila nolasa OTP 
    with open(otp_filename, 'rb') as otp_file:
        otp = otp_file.read()

    # Pārliecinās, ka sašifrētie dati un OTP ir vienādā garumā
    if len(encrypted_data) != len(otp):
        print("Kļūda: Sašifrētajam failam un OTP ir jābūt vienādā garumā.")
        return

    # Atšifrē un sašifrē datus izmantojot XOR pret OTP
    decrypted_data = bytes([a ^ b for a, b in zip(encrypted_data, otp)])

    # Ieraksta atšifrētos datus failā, bināri 
    with open(decrypted_filename, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

    print(f"Fails '{encrypted_filename}' atšifrēts un saglabāts kā '{decrypted_filename}'.")

# Galvenā programma
if __name__ == "__main__":
    operation = input("Ievadīt komandu 'encrypt' vai 'decrypt': ")

    if operation == 'encrypt':
        input_file = input("Ievadīt nosaukumu failam, kuru šifrēs: ")
        encrypted_file = input("Ievadīt nosaukumu sašifrētajam failam: ")
        encrypt_file(input_file, encrypted_file)
    elif operation == 'decrypt':
        encrypted_file = input("Ievadīt nosaukumu failam, kuru atšifrēs: ")
        decrypted_file = input("Ievadīt nosaukumu atsašifrētajam failam: ")
        decrypt_file(encrypted_file, decrypted_file)
    else:
        print("Neatļauta operācija. Ievadiet komandu 'encrypt' vai 'decrypt'.")
