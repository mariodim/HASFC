import pandas as pd
import hashlib


class CacheException(Exception):
    pass


def check_cache(input_hash):
    try:
        id = None
        df = pd.read_csv("cache/CACHE", sep=';')
        row = df[df['configurationHash'] == input_hash]
        if len(row) > 0:
            id = row['path'].iloc[0]
        return id
    except Exception as e:
        raise CacheException('Cache file not found')


def hash_input(data):
    input_hash = str(data)
    hashed_value = hashlib.sha256(input_hash.encode('utf-8')).hexdigest()
    return hashed_value
