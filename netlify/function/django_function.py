from SAMS.wsgi import application
from flask import Flask, request, Response
import os

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handler(path):
    environ = request.environ
    environ['PATH_INFO'] = '/' + path
    environ['REQUEST_METHOD'] = request.method

    # Call Django's WSGI app
    response = application(environ, lambda status, headers: None)
    return Response(response, status=200)

def main():
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=False, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
