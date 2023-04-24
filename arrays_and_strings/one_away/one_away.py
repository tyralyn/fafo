"""Check whether two strings are a single edit away from each other.

The three types of edits that can be performed on strings are:
* insert a character
* remove a character
* replace a character.
"""

def is_one_away(str1, str2):
    """ insert and delete r basically the same thing."""
    big_str, small_str = ((str1, str2) if len(str1) > len(str2) else (str2, str1))
    print(big_str, small_str)

    d_index=-1

    for i in range(len(small_str)):
        print(i, small_str[i], big_str[i])
        if small_str[i] == big_str[i]:
    	    small_str.pop(i)
    	    big_str.pop(i)
        else:
            d_index=i
            break

    for i in range(-1, -len(small_str)-1, -1):
        print(i, small_str[i], big_str[i])


def is_one_away_simple(str1, str2):
    if len(str1)==len(str2):
    	d_count=0
    	for i in range(len(str1)):
    		if str1[i] != str2[i]:
    			d_count+=1
    	return True if d_count <= 1 else False
    
    big_str, small_str = ((str1, str2) if len(str1) > len(str2) else (str2, str1))
    

    


def one_away(str1, str2):
	# quick optimization -- diff between string len is <=1
	if abs(len(str1)-len(str2)) > 1:
		return False

