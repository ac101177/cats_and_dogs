#!/usr/local/bin/python3

import database


class Owner:
    def __init__(self, database, first_name, last_name, birthday):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.id = database.insert_or_replace_into_table('owners', ["first_name", "last_name", "birthday"],
            [first_name, last_name, birthday])

        print('Owner id: '+ str(self.id))

    def update(self, first_name, last_name, birthday):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.id = database.insert_or_replace_into_table('owners', ["id", "name", "first_name", "last_name", "birthday"],
            [self.id, first_name, last_name, birthday])

    def delete(self, database):
        database.delete_from_table(self, 'owners', ["id"], [self.id])


    def get(self, database, owner_id):
        return database.fetch_first_match_for_table_query(database, 'owners', ["id"], [owner_id])


class Pet(object):
    def __init__(self, database, name, birthday, owner, pet_type):
        self.name = name
        self.birthday = birthday
        self.owner = owner
        self.pet_type = pet_type
        self.id = database.insert_or_replace_into_table('pets', ["name", "birthday", "owner", "pet_type"],
            [name, birthday, owner, pet_type])

        print('Pet id: '+ str(self.id))

    def update(self, database, name, birthday, owner, pet_type):
        self.name = name
        self.birthday = birthday
        self.owner = owner
        self.pet_type = pet_type
        self.id = database.insert_or_replace_into_table('pets', ["id", "name", "birthday", "owner", "pet_type"],
            [self.id, name, birthday, owner, pet_type])

    def delete(self, database):
        database.delete_from_table('pets', ["id"], [self.id])

    def delete(self, database, pet_id):
        return database.fetch_first_match_for_table_query('pets', ["id"], [pet_id])

class Cat(Pet):
    def __init__(self, database, name, birthday, owner):
        Pet.__init__(self, database, name, birthday, owner, pet_type='cat')

class Dog(Pet):
    def __init__(self, database, name, birthday, owner):
        Pet.__init__(self, database, name, birthday, owner, pet_type='dog')

class App:
    def __init__(self, database_path):
        self.database = database.Database(database_path)
        self.database.create_table("owners", ["id", "first_name", "last_name", "birthday"], ["integer", "text", "text", "text"])
        self.database.create_table("pets", ["id", "name", "birthday", "owner", "pet_type"], ["integer", "text", "text", "integer" ,"text"])

    def add_owner_prompt(self):
        first_name = input("Enter owner first name: ")
        last_name = input("Enter owner last name: ")
        birthday = input("Enter owner birthday: ")
        Owner(self.database, first_name, last_name, birthday)

    def add_pet_prompt(self):
        name = input("Enter pet name: ")
        birthday = input("Enter pet birthday: ")
        owner = input("Enter owner id: ")
        pet_type = input("Enter pet type (cat or dog): ")
        if pet_type == 'cat':
            Cat(self.database, name, birthday, owner)
        elif pet_type == 'dog':
            Dog(self.database, name, birthday, owner)
        else:
            pass

    def init_prompt(self):
        if self.database.check_if_table_is_nonempty("owners"):
            #self.init_prompt()

            if self.database.check_if_table_is_nonempty("pets"):
                self.main_prompt()

            else:
                print("Please add some pets first")
                self.add_pet_prompt()
                self.main_prompt()

        else:
            print("Please add some owners first")
            self.add_owner_prompt()
            self.main_prompt()

    def list_prompt(self, table_name):
        self.database.print_all_rows_of_table(table_name)

    def main_prompt(self):
        print("add owner(ao), add pet (ap),")
        response = input("list owners(o), list pets by owner(p), list owners with pets(n) or quit(q):")
        if response == "owners" or response == "o":
            self.list_prompt('owners')
            self.main_prompt()
        elif response == "pets" or response == "p":
            self.list_prompt('pets')
            self.main_prompt()
        elif response == "number" or response == "n":
            print("Could not implement it yet.")
            self.main_prompt()
        elif response == "add owner" or response == "ao":
            self.add_owner_prompt()
            self.main_prompt()
        elif response == "add pet" or response == "ap":
            self.add_pet_prompt()
            self.main_prompt()
        elif response == "quit" or response == "q":
            #self.auto_activate(self.generate_auto_activate_number())
            self.database.close()
            quit()
        else:
            self.main_prompt()

if __name__ == '__main__':
    my_app = App('tmp')
    my_app.init_prompt()