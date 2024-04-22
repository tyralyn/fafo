def isUnique(str):
    ref = []
    for c in str:
        if c not in ref:
            ref.append(c)
        else:
            return False
    return True
