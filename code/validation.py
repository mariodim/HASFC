def validate_input(data):
    if 'Costs' in data and data['Costs'] is not None and len(data['Costs']) == 3:
        try: 
            costs =  [float(k) for k in data['Costs']]
        except ValueError:
            return {'Status': 'Failure', 'Message': 'Costs should be an array of float. Try to use default [1,1,1]'}, True
    else:
        return {'Status': 'Failure', 'Message': 'Costs should be an array of size 3. Try to use default [1,1,1]'}, True
    
    if 'AvailabilityTarget' in data and data['AvailabilityTarget'] is not None:
        if type(data['AvailabilityTarget']) == str:
            try:
                availability_target = [data['AvailabilityTarget']] 
            except:
                return {'Status': 'Failure', 'Message': 'AvailabilityTarget should be an array of float. Try to use default [0.9999,0.99999,0.999999]'}, None, True
        elif len(data['AvailabilityTarget']) > 0:
            try: 
                availability_target = [float(k) for k in data['AvailabilityTarget']]
            except:
                return {'Status': 'Failure', 'Message': 'AvailabilityTarget should be an array of float. Try to use default [0.9999,0.99999,0.999999]'}, None, True
        else:
            return {'Status': 'Failure', 'Message': 'AvailabilityTarget should be an array of float. Try to use default [0.9999,0.99999,0.999999]'}, None, True
    else:
        return {'Status': 'Failure', 'Message': 'AvailabilityTarget should be an array of float. Try to use default [0.9999,0.99999,0.999999]'}, None, True
    
    weights = [0.5,0.75,1,1.25] #pruning algorithm weights, could be configurable

    configuration = {'costs':costs, 'weights':weights, 'availability_target':availability_target}
    
    parameters, error = validate_parameters(data)

    return configuration, parameters, error

def validate_parameters(data):
    params={}
    if 'params' in data and data['params'] is not None:
        paramsJSON = data['params']
        if 'muHW' in paramsJSON and paramsJSON['muHW'] is not None:
            try:
                params['muHW']=float(paramsJSON['muHW'])
            except ValueError:
                return {'Status': 'Failure', 'Message': 'muHW should be a number'}, True
        else:
            return {'Status': 'Failure', 'Message': 'muHW should be a number'}, True
        if 'lamHW' in paramsJSON and paramsJSON['lamHW'] is not None:
            try:
                params['lamHW']=float(paramsJSON['lamHW'])
            except ValueError:
                return {'Status': 'Failure', 'Message': 'lamHW should be a number'}, True
        else:
            return {'Status': 'Failure', 'Message': 'lamHW should be a number'}, True
        if 'muVM' in paramsJSON and paramsJSON['muVM'] is not None:
            try:
                params['muVM']=float(paramsJSON['muVM'])
            except ValueError:
                return {'Status': 'Failure', 'Message': 'muVM should be a number'}, True
        else:
            return {'Status': 'Failure', 'Message': 'muVM should be a number'}, True        
        if 'lamVM' in paramsJSON and paramsJSON['lamVM'] is not None:
            try:
                params['lamVM']=float(paramsJSON['lamVM'])
            except ValueError:
                return {'Status': 'Failure', 'Message': 'lamVM should be a number'}, True
        else:
            return {'Status': 'Failure', 'Message': 'lamVM should be a number'}, True        
        if 'muVNF' in paramsJSON and paramsJSON['muVNF'] is not None:
            try:
                params['muVNF']=float(paramsJSON['muVNF'])
            except ValueError:
                return {'Status': 'Failure', 'Message': 'muVNF should be a number'}, True
        else:
            return {'Status': 'Failure', 'Message': 'muVNF should be a number'}, True    
        if 'lamVNF' in paramsJSON and paramsJSON['lamVNF'] is not None:
            try:
                params['lamVNF']=float(paramsJSON['lamVNF'])
            except ValueError:
                return {'Status': 'Failure', 'Message': 'lamVNF should be a number'}, True
        else:
            return {'Status': 'Failure', 'Message': 'lamVNF should be a number'}, True                
        if 'maxVNF' in paramsJSON and paramsJSON['maxVNF'] is not None:
            try:
                params['maxVNF']=int(paramsJSON['maxVNF'])
                if params['maxVNF'] < 0 and params['maxVNF'] > 7:
                    return {'Status': 'Failure', 'Message': 'maxVNF should be an integer less then 7'}, True
            except ValueError:
                return {'Status': 'Failure', 'Message': 'maxVNF should be an integer less than 7'}, True
        else:
            return {'Status': 'Failure', 'Message': 'maxVNF should be an integer less than 7'}, True
        if 'maxNR' in paramsJSON and paramsJSON['maxNR'] is not None:
            try:
                params['maxNR']=int(paramsJSON['maxNR'])
                if params['maxNR'] < 0 and params['maxNR'] > 4:
                    return {'Status': 'Failure', 'Message': 'maxNR should be an integer less than 5'}, True
            except ValueError:
                return {'Status': 'Failure', 'Message': 'maxNR should be an integer less than 5'}, True
        else:
            return {'Status': 'Failure', 'Message': 'maxNR should be an integer less than 5'}, True
    else:
        return {'Status': 'Failure', 'Message': 'parameter of simulation missing'}, True
    
    params['perf'] = 3
    return params, False

