# Write a method to replace all spaces in a string with %20
#
# Input: Mr. John Smith
# Output: Mr.%20John%20Smith

def URLify(url):
	return url.replace(" ", "%20")

print(URLify("Mr. John Smith"))