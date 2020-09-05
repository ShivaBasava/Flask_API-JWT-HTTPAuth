from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
import jwt, json
import datetime

application = Flask(__name__)
auth = HTTPBasicAuth()
application.config['SECRET_KEY_FOR_TOKEN'] = 'myBearerAccessSecret_Token'
USER_CREDENTIAL = {"username":"Ram","password":"admin123"}
#on_success  = {"message":"Hello, World"}

from functools import wraps
def verify_token(f):
    @wraps(f)
    def decorator(*args, **kwargs): 
        token = request.args.get('token', None)
        if token is None: 
            return jsonify({"message":"Your are missing Token"}), 404
        try:
            data = jwt.decode(token, application.config['SECRET_KEY_FOR_TOKEN'])#app.config['SECRET_KEY_FOR_TOKEN'])
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:           
            # the token is expired, return an error string and responding with STATUS Code
            return jsonify({"message" : "Token has Expired! Please login to get a new token"}), 401
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string and responding with STATUS Code
            return jsonify({"message" : "Invalid token. Please try login after sometime"}), 401
        except jwt.InvalidSignatureError:
            return jsonify({"message" : "Signature verification failed"}), 500
        except Exception as e:
            # if any other, Exception
            return json.dumps({"{}".format('Message'): "{}".format(e)})
    return decorator


@auth.verify_password
@verify_token
def verify(username, password):
    if not (username and password):
        return False
    return USER_CREDENTIAL.get(username) == password


@application.route('/')
@auth.login_required
def get():
    #Encoding
    try:
        token = jwt.encode({
        'user':request.authorization,#.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=3),
        }, application.config['SECRET_KEY_FOR_TOKEN'])
        
        if jwt.decode(token, application.config['SECRET_KEY_FOR_TOKEN']):
            #return jsonify(on_success['message']), 200
            #return render_template('abc.html')#jsonify(on_success.get('message')), 200
            return ("<h1>Hell World!</h1>")
    except Exception as e:
        return json.dumps({"{}".format('Message'): "{}".format(e)})

if __name__ == '__main__':
    application.run(port="8080",debug=True) #host="0.0.0.0",
