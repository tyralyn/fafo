""" Make a string appropriate for URLS.

Replace spaces in a string with %20. Presume that the string can
contain the new string at the end, and that you are given the true
length of the string.
"""

def URLify(url_string):
    return url_string.replace(' ', '%20')