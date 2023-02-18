def add_log(func):
    def wrapper(*args, **kwargs):
        print("func=" + str(func))
        print("args="+str(args))
        print("kwargs="+str(kwargs))
        ret = func(*args, **kwargs)
        print("return=" + str(ret))
        return ret

    return wrapper
