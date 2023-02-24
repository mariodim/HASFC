import pandas as pd
from multiprocessing import Pool
import uuid

from source.core import *
from source.cache import *
from source.validation import ValidationException


def availability_post(parameters, configuration):  
    input_hash = hash_input(parameters,configuration)
    id = check_cache(input_hash)
    if id is not None:
        return {'Status': 'Success', 'Message': 'Results available in cache. Use the Id to access.', 'Id' : id}
    
    id=str(uuid.uuid1())  
    pool=Pool(1)
    pool.apply_async(async_operation, [id, configuration, parameters])
    
    with open("cache/CACHE", "a+") as cache_file:
        cache_file.write(str(input_hash) + ";" + id + "\n")
    
    return {'Status': 'Success', 'Message': 'Results will be available as soon as possible. Use the Id to access.', 'Id' : id}

def availability_get(parameters):
    availability_target=parameters['availability_target']
    id=parameters['id']
    maxSFC=parameters['maxSFC']
    try:
        with open("logs//" + id + "_log", 'r') as logfile:
            last_line = logfile.readlines()[-1]                
            values = last_line.split('\n')[0].split('|')                    
            perc=float(values[0])/float(values[1]) * 100
            if perc==100:
                out_filename = "results//" + id + "_" + str(availability_target) + "_results.csv"
                n_sfc=int(maxSFC) if int(maxSFC)<100 else 100
                df = pd.read_csv(out_filename,sep=';').sort_values(by=['cost'])
                out = df[:n_sfc].to_dict(orient='records')
                return {'Results': out, 'MaxSFC':min (n_sfc, len(out)), 'Id' : id}
            else:
                return {'Status': 'Success', 'Message': str(round(perc,3))+ ' % ' +'results ready. We will finish as soon as possible', 'Id': id}
    except Exception:
        raise ValidationException('Id not found')

def performability_post():
    pass

def performability_get():
    pass