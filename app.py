import pandas as pd

from flask import Flask, request
from flask_restful import Api
from waitress import serve

from multiprocessing import Pool
import uuid

from code.validation import *
from code.core import *
from code.cache import *

app = Flask(__name__)
api = Api(app)

@app.route('/availability', methods = ['GET'])
def get_availability():
    if request.args.get('id') is not None:
        id = request.args.get('id') 
    else:
        return {'Status': 'Error', 'Message': 'You need your id to access your data'}

    availability_target = request.args.get('AvailabilityTarget') if request.args.get('AvailabilityTarget') is not None else '0.9999'
    maxSFC = request.args.get('maxSFC') if request.args.get('maxSFC') is not None else 10
    
    try:
        with open("logs//" + id + "_log", 'r') as logfile:
            last_line = logfile.readline()
            for last_line in logfile:
                pass
                
            values = last_line.split('\n')[0].split('|')                    
            perc=float(values[0])/float(values[1]) * 100
        
            out_filename = "results//" + id + "_" + str(availability_target) + "_results.csv"
            
            try:
                n_sfc=int(maxSFC) if int(maxSFC)<100 else 100
                df = pd.read_csv(out_filename,sep=';').sort_values(by=['cost'])
                out = df[:n_sfc].to_dict(orient='records')
                return {'Results': out, 'MaxSFC':min (n_sfc, len(out)), 'Id' : id}
            except FileNotFoundError:
                if perc != 100:
                    return {'Status': 'Success', 'Message': str(round(perc,3))+ ' % ' +'results ready. We will finish as soon as possible', 'Id': id}
                else:
                    return {'Status': 'Error', 'Message': 'Availability Target value requested is not valid.'}
    except Exception as e:
        return {'Status': 'Error', 'Message': 'Id not found'}

@app.route('/availability', methods = ['POST'])
def availability():
    id=str(uuid.uuid1())

    configuration, parameters, error = validate_input(request.get_json())
    if error:
        if parameters is None:
            return configuration
        return parameters
    
    input_hash = hash_input(parameters,configuration)
    message, found, error = check_cache(input_hash)
    
    if found or error:
        return message
    
    pool=Pool(1)
    pool.apply_async(async_operation, [id, configuration, parameters])
    
    with open("CACHE", "a+") as cache_file:
        cache_file.write(str(input_hash) + ";" + id + "\n")
    
    return {'Status': 'Success', 'Message': 'Results will be available as soon as possible. Use the Id to access.', 'Id' : id}

if __name__ == '__main__':
    serve(app, host = "0.0.0.0", port = 5002)
    
