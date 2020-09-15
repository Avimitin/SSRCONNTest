from utils.TokenGenerator import Generator
from utils.database import UserHandler

def register(username, uid, permission):
    token = generate_token(username, uid)[1]
    return add_new_user(username, uid, permission, token)

def generate_token(username, uid):
    return Generator.TokenGenerator().new(username, uid)

def add_new_user(username, uid, permission, token):
    u = UserHandler.UserHandler()
    return u.add_users(uid, username, permission, token)

if __name__ == "__main__":
    print(register("TestName", 114514, "manager"))
