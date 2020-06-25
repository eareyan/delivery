from flask import Flask, request
from google.cloud import storage

app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""

    form  = """
    <form action="/signup" method="post">
        <input type="text" name="email"></input>
        <input type="submit" value="Signup"></input>
    </form>"""

    return f"<h1>Hello World! Here we are!</h1><h2>Please sign up</h2>{form}"

@app.route('/enrique')
def enrique():
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
    return f"<h1>ENRIQUE</h1>"


@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']

    return "The email address is '" + email + "'"


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
