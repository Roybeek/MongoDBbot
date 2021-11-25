import pymongo

import mongo_operatons

client = pymongo.MongoClient('localhost', 27017)
db = client['UserStates']
users = db['users']
states = db['states']


class User:

    # конструктор
    def __init__(self, user_id: int):
        self.user_id = user_id  # устанавливаем id
        user_info = mongo_operatons.find_document(users, {"user_id": user_id})

        if user_info:
            self.name = user_info['name']
            self.surname = user_info['surname']
            self.age = user_info['age']
            self.is_db_user = True
        else:
            self.is_db_user = False

    def check_db_user(self):
        return self.is_db_user

    def update_user_info(self, name, surname, age):
        self.name = name
        self.surname = surname
        self.age = age
        mongo_operatons.insert_document(users, {"type": 'user',
                                                "user_id": self.user_id, "name": name,
                                                "surname": surname,
                                                "age": age})
        return

    def remove_db_user(self):
        mongo_operatons.delete_document(users, {"user_id": self.user_id})
        return

    def get_user_info(self):
        user_info = mongo_operatons.find_document(users, {"user_id": self.user_id})
        return f"В базе теперь есть запись: {user_info['surname']} {user_info['name']}, возраст {user_info['age']}"

    def get_all_users(self):
        def to_text(user):
            return f"\nВ базе есть запись: {user['surname']} {user['name']}, возраст {user['age']}"
        users_list = mongo_operatons.find_document(users, {"type": "user"}, True)
        msg = ''
        if users_list:
            for i in map(to_text, users_list):
                msg += i
            if self.check_db_user():
                return msg
            else:
                msg += '\nНо Вас в этом списке нет'
                return msg
        else:
            return "В базе нет пользователей"

