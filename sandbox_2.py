from pymongo import MongoClient


"----mongo----"
client = MongoClient(serverSelectionTimeoutMS=5000)


def create_one(first_name: str, last_name: str, email: str, password: str):

    users_collection = client["data"]["users"]
    users_dict = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "password": password
    }

    users_collection.insert_one(users_dict)


def delete_all_users():
    users_collection = client['data']['users']
    deleted_users = users_collection.delete_many({})
    print(f"Deleted {deleted_users.deleted_count} users from database.")


def create_index():
    users_collection = client['data']['users']
    users_collection.create_index("email", unique=True)


def list_indexes():
    users_collection = client["data"]["users"]
    index_list = users_collection.list_indexes()
    for index in index_list:
        print(index)


# create_one("John", "Kowalski", "john.kowalski@mail.com", "SomePass")
# create_one("Peter", "Kow", "peter.kow@mail.com", "SomePass_1")
# create_one("Rex", "Mod", "rex.mod@mail.com", "SomePass_2")
# create_one("Ted", "Lex", "ted.lex@mail.com", "SomePass_3")


# delete_all_users()
# create_index()
# list_indexes()

