"""Given two strings, decide if one is a permutation of the other.

Assumptions:
 * repeated characters DO count

"""

def check_permutation(str1, str2):
    biggerStr, smallerStr = ((str1, str2) if len(str1) > len(str2) else (str2, str1))

    for c in smallerStr:
    	if smallerStr.count(c) > biggerStr.count(c):
    	    return False
    return True

