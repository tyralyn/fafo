# A Caesar cipher is a simple substitution cipher in which each letter of
# plaintext is substituted with a letter n places down in the alphabet.
#
# Example: input "abc xyz" output "edg bcd" if the shift value is 4
#
# Write a function that takes a shift value and a word and returns the word's
# Caesar cipher.
#
# Q: if the shift value is a negative number, should it wrap around like
# python list indexing?
# A: yes
#
# Q: it looks like only the letters are changing, does that sound right?
# whitespace and punctuation are not changing?
# A: yes
#
# Note: will start off with valid inputs and go from there after

# initial strategy that I won't take: manually make a dictionary to map
# map each letter:
#
# d = {
#	'a': 'e'
#   'b': 'f'
#	...
#	'A':'E'
#	...
# }
# 
# and then iterate through the word, replacing each alphabetical char with
# the one it is mapped to.
#
# second strategy: don't make the dictionary manually

def caesar_cipher_basic(text, n):
	lowercase = range(ord('a'), ord('z') + 1)
	uppercase = range(ord('A'), ord('Z') + 1)

	#d_lower = { chr(i): chr(lowercase_letters[(i + 4)%26]) for i in range(ord('a'), ord('z') + )}
	#d_lower=dict(zip(range(ord('a'), ord('z') + 1), ))
	d_lower = { chr(lowercase[i]): chr(lowercase[(i+n)%len(lowercase)]) for i in range(len(lowercase))}
	d_upper = { chr(uppercase[i]): chr(uppercase[(i+n)%len(uppercase)]) for i in range(len(uppercase))}


	d = d_lower
	d.update(d_upper)

	cipher = ""
	for c in text:
		if c.isalpha(): 
			cipher+=d[c]
		else:
			cipher+=c
	return cipher

def cesar_cipher(text, n):
	d_lower={ ord('a') + i: ord('a') + (i + n )%26 for i in range(0,26)}
	d_upper={ ord('A') + i: ord('A') + (i + n )%26 for i in range(0,26)}

	d = {**d_lower, **d_upper}

	return text.translate(d)






