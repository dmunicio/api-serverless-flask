from flask import Blueprint
from flask import request, jsonify

from .errors import error_message

from datetime import datetime, time
from .helpers import days_to_birthday
from flask import request
from flask import current_app

api = Blueprint('api', __name__)

@api.app_errorhandler(404)
def handle404(error=None):
    return error_message(404, 'Not found url {}'.format(request.url))

@api.app_errorhandler(405)
def handle405(error=None):
    return error_message(405, 'Method not supported')

#@api.app_errorhandler(500)
#def handle500(error=None):
#    return error_message(500, 'Something went wrong')

@api.route('/hello/<username>', methods=['GET','OPTIONS'])
def get_birthday(username):
    """Get birthday for username
    ---
    parameters:
      - name: username
        in: path
        type: string
        required: true
    definitions:
      Username:
        type: string
    responses:
      200:
        description: Get birthday for username
        schema:
          $ref: '#/definitions/Username'
        examples:
          usernameA
    """
    if request.method == "OPTIONS":
      json_response = jsonify("")
      json_response.headers.add('Access-Control-Allow-Origin', '*')
      return json_response, 200

    # Username must contain only letters
    if not username.isalpha():
        return "username must contain only letters.", 400    
    db = current_app.config["users.db"]
    user = db.get_by_username(username)
    
    if user is None:
        return "user not found", 204
    birthday = datetime.strptime(user.date_of_birth, "%Y-%m-%d")
    days = days_to_birthday(birthday)

    if days is None:
        return "", 204
    if days == 0:
        response = { "message": f"Hello, {username}! Happy birthday!" }
    else:
        response = { "message": f"Hello, {username}! Your birthday is in {days} day(s)!" }
    json_response = jsonify(response)
    json_response.headers.add('Access-Control-Allow-Origin', '*')
    return  json_response, 200

@api.route('/hello/<username>', methods=['PUT'])
def set_birthday(username):
    """Get birthday for username
    ---
    parameters:
      - name: username
        in: path
        type: string
        required: true
    definitions:
      Birthday:
        required:
        - dateOfBirth
        type: object
        properties:
          dateOfBirth:
            type: string
    requestBody:
      description: A JSON object containing birthday information
      content:
        application/json:
          schema:
            $ref: '#/definitions/Birthday'
            
    responses:
      204:
        description: No Content
    """    
    # Username must contain only letters
    if not username.isalpha():
        return "username must contain only letters.", 400

    try:
        data = request.get_json()
        date_of_birth = data.get('dateOfBirth', None)        
    except:
        return "error obtaining dateOfBirth", 400    

    if date_of_birth is None:
        return '', 400
    try:
        parsed_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
    except:
        return "error parsing dateOfBirth format", 400

    if parsed_date > datetime.combine(datetime.now(), time.min):
        return "dateOfBirth must be a date before today", 400

    db = current_app.config["users.db"]

    db.add_birthday(username, date_of_birth)

    return '', 204

@api.route('/healthcheck', methods=('HEAD', 'GET'))
def handle_healthcheck():
    return 'ok'
