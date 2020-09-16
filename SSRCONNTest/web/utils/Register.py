from utils.TokenGenerator import Generator
from utils.database import UserHandler

def register(username, uid, permission):
    token = _generate_token(username, uid)[1]
    return _add_new_user(username, uid, permission, token)

def _generate_token(username, uid):
    return Generator.TokenGenerator().new(username, uid)

def _add_new_user(username, uid, permission, token):
    u = UserHandler.UserHandler()
    return u.add_users(uid, username, permission, token)

if __name__ == "__main__":
    print(register("TestName", 114514, "manager"))
