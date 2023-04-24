# Hash Table

P: Implement a hash table.

## What is a hash table? / Hash map?

* Data structure that stores data in an associative way -- we want to store a key and value together.
* Accesses are fast if we know the index of the desired data.
* Insertions and searches are fast. 
* Basically we want to store pairs of data by some kinda key -- e.g. a phone book, where the key is the name and the phone numnber is the value

## Implementation -- basic

To store something:
* input: key, value
* hash the key
* store the value at the index of the hashed key

To retrieve something:
* input: key
* hash the key, get the value at the key and return it 
