# -*- coding: utf-8 -*-
# author: Avimitin
# datetime: 2020/8/30 16:16

UNAUTHORIZED = {
    "ok": False,
    "error_code": 401,
    "description": "Unauthorized"
}

NOTFOUND = {
    "ok": False,
    "error_code": 404,
    "description": "Not Found"
}

INVALID = {
    "ok": False,
    "error_code": 400,
    "description": "INVALID REQUEST"
}


EMPTY = {
    "error": "EMPTY JSON REQUEST"
}

EMPTY_ARGS_GUIDE = {
    "ok": False,
    "error_code": 400,
    "description": "YOUR SEARCHING ARGS ARE EMPTY, YOU MUST INPUT SEARCHING ARGS LIKE: "
                   "https://example.com/api/v1/result?time=114514 "
}
