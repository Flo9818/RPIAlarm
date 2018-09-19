from flask import Flask, Response, request, jsonify
app = Flask(__name__)

activeUsers = []

@app.route("/trigger", methods=['PUT'])
def trigger():
    if 'Authorization' in request.headers:
        secret = request.headers.get('Authorization')
        if secret != 'Bearer secret':
            return jsonify({'error': 'Wrong credentials'}), 400

        user = request.args.get('user')
        if user:
            if user in activeUsers:
                activeUsers.remove(user)
            else:
                activeUsers.append(user)
            print(activeUsers)
            return jsonify({'success': True}), 400
    return jsonify({'error':'Bad request'}), 400

if __name__ == "__main__":
    app.run(ssl_context='adhoc')