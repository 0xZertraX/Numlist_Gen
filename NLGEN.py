import random
import phonenumbers
from phonenumbers import carrier, geocoder
from colorama import init, Fore
import os
import re
import ctypes

# Définition de la fonction pour modifier le titre de la fenêtre
def set_console_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

# Appel de la fonction pour définir le titre de la fenêtre
set_console_title("NL GEN 〃@ZertraX ON TELEGRAM")

init()

def generate_phone_number(chiffre_initial):
    phone_number = str(chiffre_initial)
    for _ in range(8):
        phone_number += str(random.randint(0, 9))
    return phone_number

def is_valid_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, "FR")
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

def get_number_info(phone_number):
    parsed_number = phonenumbers.parse(phone_number, "FR")
    operator = carrier.name_for_number(parsed_number, "fr")
    return operator

def generate_numbers():
    chiffre_initial = input("Entrez le chiffre initial (6, 7, ou A pour aléatoire) : ")
    if chiffre_initial.lower() == "a":
        chiffre_initial = random.choice(["6", "7"])
    elif chiffre_initial not in ["6", "7"]:
        print("Chiffre invalide. Veuillez entrer 6, 7, ou A.")
        return

    inclure_prefixe = input("Voulez-vous inclure le préfixe '+33' devant les numéros ? (Oui/Non) : ")
    prefixe = "+33" if inclure_prefixe.lower() == "oui" else ""

    check_operateur = input("Voulez-vous effectuer une vérification par opérateur ? (Oui/Non) : ")
    if check_operateur.lower() == "oui":
        print("\nExemples d'opérateurs :")
        print("\n1. Orange")
        print("2. SFR")
        print("3. Bouygues Telecom")
        operateur_choisi = input("\nChoisissez un opérateur (1, 2, 3, etc.) : ")
        operateur_choisi = operateur_choisi.strip().lower()
        if operateur_choisi == "1":
            operateur = "Orange"
        elif operateur_choisi == "2":
            operateur = "SFR"
        elif operateur_choisi == "3":
            operateur = "Bouygues Telecom"
        else:
            print("Opérateur invalide. Veuillez réessayer.")
            return
    else:
        operateur = None

    nombre_numeros = input("Combien de numéros souhaitez-vous générer ? ")
    try:
        nombre_numeros = int(nombre_numeros)
    except ValueError:
        print("Nombre invalide. Veuillez entrer un nombre entier.")
        return

    operateur_numeros = {}
    count = 0
    while count < nombre_numeros:
        random_phone_number = generate_phone_number(chiffre_initial)
        if is_valid_phone_number(random_phone_number):
            numero_operateur = get_number_info(random_phone_number)
            if operateur is None or operateur.lower() == numero_operateur.lower():
                operateur_numeros.setdefault(numero_operateur, []).append(random_phone_number)
                count += 1
                print(f"{Fore.GREEN}HIT{Fore.RESET} {Fore.MAGENTA}|==>{Fore.RESET} {prefixe}{Fore.YELLOW}{random_phone_number} {Fore.MAGENTA}| {Fore.CYAN}{numero_operateur}")
        else:
            print(f"{Fore.RED}MISS{Fore.RESET} {Fore.MAGENTA}|==>{Fore.RESET} {prefixe}{Fore.YELLOW}{random_phone_number} {Fore.MAGENTA}| {Fore.RED}Invalid number")

    print(f"{Fore.GREEN}{'=' * 34}{Fore.RESET}\n")

    dossier_sortie = input("Entrez le nom du dossier de sortie : ")
    os.makedirs(dossier_sortie, exist_ok=True)

    for operator, numeros in operateur_numeros.items():
        nombre_numeros = len(numeros)
        # Supprimer les caractères invalides du nom du fichier
        nom_fichier = re.sub(r'[<>:"/\\|?*]', '', f"{operator}_{nombre_numeros}_numeros.txt")
        chemin_fichier = os.path.join(dossier_sortie, nom_fichier)

        with open(chemin_fichier, "w") as fichier_sortie:
            for numero in numeros:
                fichier_sortie.write(f"{prefixe}{numero}\n")

    reponse = input("Voulez-vous générer de nouveaux numéros de téléphone ? (Oui/Non) : ")
    if reponse.lower() == "oui":
        generate_numbers()

generate_numbers()
