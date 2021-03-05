import pandas as pd
import hashlib

def check_cache(input_hash):
    try:
        id=None
        cache = open("CACHE")
        for line in cache:
            (key, val) = line.split(";")
            if key == input_hash:
                id = val
        if id is None:
            return None, False, False
        else:
            return {'Status': 'Success', 'Message': 'Results available in cache. Use the Id to access.', 'Id' : id.split("\n")[0]}, True, False
    except Exception as e:
        return {'Status': 'Error', 'Message': 'Cache file not found'}, False, True
        
    
def hash_input (parameters, configuration):
    input_hash = str(parameters) + str(configuration)
    hashed_value = hashlib.sha256(input_hash.encode('utf-8')).hexdigest()
    return hashed_value
    