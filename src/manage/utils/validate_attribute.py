def validateAttribute(object: object, key: str):
    try:
        object[key]
        return True
    except:
        return False