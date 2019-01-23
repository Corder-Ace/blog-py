def trueReturn(data, msg):
    return {
        "status": 200,
        "data": data,
        "msg": msg
    }


def falseReturn(data, msg):
    return {
        "status": 403,
        "data": data,
        "msg": msg
    }

def tokenLoseReturn(data, msg):
    return {
        "status": 401,
        "data": data,
        "msg": msg
    }