# write a fn to swap a number in place (without temporary variables)
# 
# what is the input? primitives are immutable so this can't be like a plain number
# assuming the input is in a list
#
# hint 492: try picturing two numbers on a number line...?
# hint 716: let diff be the difference between a and b. can u use diff in some way?
# hint 737: try using XOR?
# 
# so u can use a variable, u just cant store it somewhere. should have clarified that
#
# inputs: numbers to swap (indices), a list

# ok the solution to this one according to the book is not actually written code
# basically u set a diff to be the difference between a and b
# if you know which one is greater than the other 
# so if a is the bigger number, and b is smaller, and diff=a-b
# set a = a - diff and b = b + diff
#
#
# apparently u can do this with XOR as well but idc about bits
#
# i think in python u could just do a,b = b,a.....