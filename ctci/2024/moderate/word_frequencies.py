'''
design a method to find the frequency of occurrence of any given word in a book -- what if running multiple times?

q: what is the input?
a: the given word, and the book presented as a list of words
alternatively if it was presented as a big ass string we could split on spaces and punctuation into words
can we assume that it's a traditional english book? if we're not receiving the book as a list of words we may have to split on spaces and punctuation

if running multiple times, it would be ideal to convert the entire book into a frquency table and refer to that for word frequencies

how do we handle all the punctuation? referring to the hints now

hint 489: think about best conceivable runtime -- if ur sln is that it can't be better
          best conceivable runtime is O(n) if n is the number if words in the book
          i would assume that collections.Counter is O(n)
hint 536: can u use a hashtable to optimize the repeated case?
		  ..... yes?
'''

from collections import Counter
def word_frequencies_collections(book):
	return Counter(book)

def word_frequencies_dict_comprehension(book):
	words = book.split("")
	return {i:words.count(i) for i in set (words)}

'''
solution from book:

for the single case go through it word-by-word, count number of times the word appears, which is O(n)
the hash table solution they are talking about is a hash table of words to frequencies like i suggested,,,, i am agenius
'''



