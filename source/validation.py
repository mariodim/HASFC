class ValidationException(Exception):
    pass


def validate_post_availability_input(data):
    if 'Costs' in data and data['Costs'] is not None and len(
            data['Costs']) == 3:
        try:
            costs = [float(k) for k in data['Costs']]
        except ValueError:
            raise ValidationException(
                'Costs should be an array of float. Try to use default [1,1,1]')
    else:
        raise ValidationException(
            'Costs should be an array of size 3. Try to use default [1,1,1]')

    availability_target = get_availability_target(data)
    # pruning algorithm weights, could be configurable
    weights = [0.5, 0.75, 1, 1.25]
    configuration = {'costs': costs, 'weights': weights,
                     'availability_target': availability_target}
    parameters = validate_parameters(data)

    return configuration, parameters


def get_availability_target(data):
    if 'AvailabilityTarget' in data and data['AvailabilityTarget'] is not None:
        if isinstance(data['AvailabilityTarget'], str):
            try:
                availability_target = [data['AvailabilityTarget']]
            except BaseException:
                raise ValidationException(
                    'AvailabilityTarget should be an array of float. Try to use default [0.9999,0.99999,0.999999]')
        elif len(data['AvailabilityTarget']) > 0:
            try:
                availability_target = [
                    float(k) for k in data['AvailabilityTarget']]
            except BaseException:
                raise ValidationException(
                    'AvailabilityTarget should be an array of float. Try to use default [0.9999,0.99999,0.999999]')
        else:
            raise ValidationException(
                'AvailabilityTarget should be an array of float. Try to use default [0.9999,0.99999,0.999999]')
    else:
        raise ValidationException(
            'AvailabilityTarget should be an array of float. Try to use default [0.9999,0.99999,0.999999]')

    return availability_target


def validate_param(params, name):
    if name in params and params[name] is not None:
        try:
            return float(params[name])
        except ValueError:
            raise ValidationException(f'{name} should be a number')
    else:
        raise ValidationException(f'{name} is not present')


def validate_parameters(data):
    params = {}
    if 'params' in data and data['params'] is not None:
        paramsJSON = data['params']
        params['muHW'] = validate_param(paramsJSON, 'muHW')
        params['lamHW'] = validate_param(paramsJSON, 'lamHW')
        params['muHYP'] = validate_param(paramsJSON, 'muHYP')
        params['lamHYP'] = validate_param(paramsJSON, 'lamHYP')
        params['muVNF'] = validate_param(paramsJSON, 'muVNF')
        params['lamVNF'] = validate_param(paramsJSON, 'lamVNF')
        if 'maxVNF' in paramsJSON and paramsJSON['maxVNF'] is not None:
            try:
                params['maxVNF'] = int(paramsJSON['maxVNF'])
                if params['maxVNF'] < 0 and params['maxVNF'] > 7:
                    raise ValidationException(
                        'maxVNF should be an integer less then 7')
            except ValueError:
                raise ValidationException(
                    'maxVNF should be an integer less than 7')
        else:
            raise ValidationException(
                'maxVNF should be an integer less than 7')
        if 'maxNR' in paramsJSON and paramsJSON['maxNR'] is not None:
            try:
                params['maxNR'] = int(paramsJSON['maxNR'])
                if params['maxNR'] < 0 and params['maxNR'] > 4:
                    raise ValidationException(
                        'maxNR should be an integer less than 5')
            except ValueError:
                raise ValidationException(
                    'maxNR should be an integer less than 5')
        else:
            raise ValidationException('maxNR should be an integer less than 5')
    else:
        raise ValidationException('parameter of simulation missing')

    params['perf'] = 3
    return params


def validate_get_availability_input(request):
    if request.args.get('id') is not None:
        id = request.args.get('id')
    else:
        raise ValidationException('You need your id to access your data')

    availability_target = request.args.get('AvailabilityTarget') if request.args.get(
        'AvailabilityTarget') is not None else '0.9999'
    maxSFC = request.args.get('maxSFC') if request.args.get(
        'maxSFC') is not None else 10

    return {
        'id': id,
        'maxSFC': maxSFC,
        'availability_target': availability_target}


def validate_post_performability_input(data):
    performability = get_performability_params(data)
    availability_target = get_availability_target(data)
    # pruning algorithm weights, could be configurable
    weights = [0.5, 0.75, 1, 1.25]

    configuration = {'performability': performability, 'weights': weights,
                     'availability_target': availability_target}
    parameters = validate_parameters(data)
    return configuration, parameters


def get_performability_params(data):
    if 'Alpha' in data and data['Alpha'] is not None:
        try:
            alpha = [float(data['Alpha'])] * 4
        except ValueError:
            raise ValidationException(
                'Alpha should be a valid value (numeric). Try to use default 200')
    else:
        raise ValidationException(
            'Alpha should be a valid value (numeric). Try to use default 200')
    if 'Beta' in data and data['Beta'] is not None and len(
            data['Beta']) == 3:
        try:
            beta = [float(k) for k in data['Beta']]
        except ValueError:
            raise ValidationException(
                'Beta should be an array of float. Try to use default [125,147,185,111]')
    else:
        raise ValidationException(
            'Beta should be an array of size 4. Try to use default [125,147,185,111]')
    if 'D' in data and data['D'] is not None:
        try:
            d = float(data['D'])
        except ValueError:
            raise ValidationException(
                'D should be a valid value (numeric). Try to use default 0.3')
    else:
        raise ValidationException(
            'D should be a valid value (numeric). Try to use default 0.3')
    performability = {'alpha': alpha, 'beta': beta, 'd': d}
    return performability


def validate_get_performability_input(request):
    if request.args.get('id') is not None:
        id = request.args.get('id')
    else:
        raise ValidationException('You need your id to access your data')

    availability_target = request.args.get('AvailabilityTarget') if request.args.get(
        'AvailabilityTarget') is not None else '0.9999'
    maxSFC = request.args.get('maxSFC') if request.args.get(
        'maxSFC') is not None else 10

    return {
        'id': id,
        'maxSFC': maxSFC,
        'availability_target': availability_target}
