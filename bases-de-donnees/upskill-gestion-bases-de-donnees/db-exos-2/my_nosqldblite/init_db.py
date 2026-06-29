import random
from model import get_database, get_user_data, set_all_initial_city, city_list

def main():
    # Connexion à MongoDB
    mydb = get_database()
    
    # 1. Initialisation des utilisateurs
    users_collection = mydb["users"]
    if users_collection.count_documents({}) == 0:
        print("Ajout des utilisateurs...")
        users_collection.insert_many(get_user_data())
    else:
        print("Les utilisateurs existent déjà.")

    # 2. Limiter l'accès à city_list pour éviter les indices hors limites
    global city_list
    city_list = city_list[:len(city_list)]  # Pas nécessaire mais permet d'assurer qu'on ne sortira pas des bornes

    # 3. Initialisation des villes
    print("Ajout des villes initiales...")
    set_all_initial_city(mydb, random)
    print("Villes ajoutées avec succès.")

if __name__ == "__main__":
    main()
