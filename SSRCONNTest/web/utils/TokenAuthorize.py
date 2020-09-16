# Author: Avimitin
from utils.database.UserHandler import UserHandler

u = UserHandler()
__ADMIN__ = []
__MANAGER__ = []

def get_admin():
    global __ADMIN__
    response = u.get_user_by_keyword(permission="admin")
    try:
        TOKENS = [user["TOKEN"] for user in response["results"]]
    except KeyError:
        return
    __ADMIN__ = TOKENS
    return TOKENS

def get_manager():
    response = u.get_user_by_keyword(permission="manager")
    try:
        TOKENS = [user["TOKEN"] for user in response["results"]]
    except KeyError:
        return
    __MANAGER__ = TOKENS
    return TOKENS

def auth(token):
    get_admin()
    get_manager()
    return token in __ADMIN__ or token in __MANAGER__

