'''
design an algorithm to figure out if someone has won a game of tictactoe

q: so given a tictactoe board, if there's a winner, then return the winner, otherwise return none

q: let's say that return True if x won, false if o won, and none if no one won

q: are we assuming this is a valid tictactoe board? like u couldnt have two winners?

hint 710: if you were calling hasWon multiple times, how might your solution change?
hint 732: if you were designing for a nxn board, how would ur solkution change?
'''

'''
when determining whether a tictactoe board has been won, you have to check all verticals, all horizontals, and all diagonals
so if we're taking the board represented as a list of lists (i changed my mind from list of tuples bc idgaf)
'''

