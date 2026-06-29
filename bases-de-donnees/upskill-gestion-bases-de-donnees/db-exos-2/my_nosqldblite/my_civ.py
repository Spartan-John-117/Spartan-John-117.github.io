from pymongo import MongoClient
from model import get_database, get_user_data, building_list 

def init_once(db, collection_name, datalist):
    collection = db[collection_name]

    for data in datalist:

        if not collection.find_one(data):
            collection.insert_one(data)

def get_city_by_owner(db, login):
    user = db["users"].find_one({"login": login})
    
    if not user:
        return None
    
    city = db["mycity"].find_one({"owner": user["_id"]})
    
    return city

def add_food_into_city(collection, city_id, apple_current, apple_by_turn, next_increase):
    city = collection.find_one({"_id": city_id})

    if not city:
        raise ValueError("City not found")

    food_data = {
        "apple_current": apple_current,
        "apple_by_turn": apple_by_turn,
        "next_increase": next_increase
    }

    collection.update_one(
        {"_id": city_id},
        {"$set": {"foods": food_data}}
    )

def add_production_in_queue(db, cityid, prod_name, hammer_current, hammer_by_turn):
    city_collection = db["mycity"]
    
    city = city_collection.find_one({"_id": cityid})
    
    if not city:
        raise ValueError(f"City with ID {cityid} not found.")
    
    building = next((b for b in model.building_list if b["name"] == prod_name), None)
    
    if not building:
        raise ValueError(f"Production {prod_name} not found in the building list.")
    
    hammer_total = building["hammer_total"]
    
    if "productions" not in city:
        city["productions"] = []
    
    existing_prod = next((p for p in city["productions"] if p["name"] == prod_name), None)
    
    if existing_prod:
        existing_prod["hammer_current"] = hammer_current
        existing_prod["hammer_by_turn"] = hammer_by_turn
        existing_prod["hammer_total"] = hammer_total
    else:
        city["productions"].append({
            "name": prod_name,
            "hammer_current": hammer_current,
            "hammer_by_turn": hammer_by_turn,
            "hammer_total": hammer_total
        })
    
    city_collection.update_one(
        {"_id": cityid},
        {"$set": {"productions": city["productions"]}}
    )
    
    return True

