# Author: Avimitin
from utils.database.UserHandler import UserHandler

u = UserHandler()
__ADMIN__ = []
__MANAGER__ = []

def get_admin():
    global __ADMIN__
    response = u.get_user_by_keyword(permission="admin")
    TOKENS = [user["TOKEN"] for user in response["results"]]
    __ADMIN__ = TOKENS
    return TOKENS

def get_manager():
    response = u.get_user_by_keyword(permission="manager")
    TOKENS = [user["TOKEN"] for user in response["results"]]
    return TOKENS


def auth(token):
    get_admin()
    return token in __ADMIN__

if __name__ == "__main__":
    print(auth("2B4W6yONPXlslr0JhOAD8nbrI4fo1F2x4NfqJlSkbAI"))
    print(__ADMIN__)
