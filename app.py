from flask import Flask, request, Response
from flask_restful import Api
from waitress import serve
from controller import controller
from source import validation

app = Flask(__name__)
api = Api(app)


@app.route('/availability', methods=['GET', 'POST'])
def availability():
    try:
        if request.method == 'POST':
            data = validation.validate_post_availability_input(
                request.get_json())
            return controller.availability_post(data)
        else:
            data = validation.validate_get_availability_input(request)
            return controller.availability_get(data)
    except validation.ValidationException as e:
        return Response(response=str(e), status=400, mimetype="text/plain")
    except Exception as e:
        return Response(response=str(e), status=500, mimetype="text/plain")


@app.route('/performability', methods=['GET', 'POST'])
def performability():
    try:
        if request.method == 'POST':
            data = validation.validate_post_performability_input(
                request.get_json())
            return controller.performability_post(data)
        else:
            data = validation.validate_get_performability_input(request)
            return controller.performability_get(data)
    except validation.ValidationException as e:
        return Response(response=str(e), status=400, mimetype="text/plain")
    except Exception as e:
        return Response(response=str(e), status=500, mimetype="text/plain")


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5002)
