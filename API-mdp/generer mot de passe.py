import random
import string

def generer_mot_de_passe(min_length, numbers=True , special_characters=True):
    lettres = string.ascii_letters
    digits = string.digits
    special = string.punctuation
    
    characters = lettres
    if numbers:
        characters += digits
    if special_characters:
        characters += special
    
    pwd = ""
    meets_criteriar = False
    has_numbers=False
    has_special=False
    
    while not meets_criteriar or len(pwd) < min_length:
        new_char=random.choice(characters)
        pwd += new_char
        
        if new_char in digits:
            has_numbers=True
        elif new_char in special:
            has_special = True
        
        meets_criteriar = True
        if numbers:
            meets_criteriar = has_numbers
        if special_characters:
            meets_criteriar = meets_criteriar and has_special
    return pwd

min_length = int(input("enter la longueur minimum : "))
has_number = input("est ce que vous voulez avoir des nombres (y/n) : ").lower()=="y"
has_special = input("est ce que vous voulez avoir des spécials (y/n) : ").lower()=="y"
pwd = generer_mot_de_passe(min_length, has_number, has_special)
print("le mot de passe généré est = ", pwd)


generer_mot_de_passe(10)