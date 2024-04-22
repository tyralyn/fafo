def string_rotation(str1, str2):
    # optimization -- if strings r diff lengths this is auto false
    if len(str1)!=len(str2): return False
    for i in range(0, len(str1)):
        if str1==str2[-i:]+str2[:-i]:
            return True
    return False
