"""Fns to determine whether strings are unique with O(1) memory complexity.
"""

def is_unique_double_loop(strng):
    """Returns whether the string is unique without creating another datastructure."""
    for i in range(len(strng)):
        for j in range(i+1, len(strng)):
            if strng[i]==strng[j]:
                return False
    return True

def is_unique_slices(strng):
    for i in range(len(strng)):
        print("---"+repr(i)+"---: "+strng[:i] + ", " + strng[i+1:])
        if strng[i] in (strng[:i]+strng[i+1:]):
            return False
    return True
