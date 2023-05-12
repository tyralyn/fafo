"""Check whether two strings are a single edit away from each other.

The three types of edits that can be performed on strings are:
* insert a character
* remove a character
* replace a character.
"""

def one_away(str1, str2):
    """go from front-->back and then back--> front, looking for differences."""

    # figure out which string is bigger and smaller
    if len(str1) >= len(str2):
        big_str, small_str  = list(str1), list(str2)
    else:
    	big_str, small_str = list(str2), list(str1)

    # remove matching items from front of strings
    for i in range(len(small_str)):
        if small_str[0] == big_str[0]:
            small_str.pop(0)
            big_str.pop(0)
        else:
            break

    # remove matching items from back of strings
    for i in range(-1, -len(small_str)-1, -1):
        if small_str[-1] == big_str[-1]:
            small_str.pop(-1)
            big_str.pop(-1)
        else:
            break

    # at the end, the big string should have at most 1 item, and the small string 0
    return len(big_str)<=1 && len(small_str)==0


def is_one_away_simple(str1, str2):
    """Separate cases for equal length strings and the others"""
    if len(str1)==len(str2):
        d_count=0
        for i in range(len(str1)):
            if str1[i] != str2[i]:
                d_count+=1
        return True if d_count <= 1 else False
    return is_one_away(str1, str2)



def one_away_quick_opt(str1, str2):
    # quick optimization -- diff between string len is <=1
    if abs(len(str1)-len(str2)) > 1:
        return False

