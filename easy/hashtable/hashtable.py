hashTable = {} 

def insert(key, value):
  hashKey = hash(key)
  if key not in hashTable:
    hashTable[hashKey] = [value]
    return None
  hashTable[hashKey].append(value)

def retrieve(key):
  return hashTable[hash(key)]

def main():
  if __name__!='__main__':
    return None

