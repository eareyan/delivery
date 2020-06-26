import os
import sqlalchemy
from flask import Flask, request, render_template
from google.cloud import storage

app = Flask(__name__)


@app.route('/')
def hello():

    with db.connect() as conn:
        # Execute the query and fetch all results
        data = conn.execute("SELECT * FROM entries").fetchall()
        list_of_people = "<ul>"
        for a, b, c in data:
            list_of_people += f"<li>{a}, {b}, {c}</li>"
        list_of_people += "</ul>"

    form = """ 
    <form action="/signup" method="post">
        <input type="text" name="email"></input>
        <input type="submit" value="Signup"></input>
    </form>"""

    return f"<h1>Hello World! Here we are 2!</h1><h2>Please sign up</h2>{form}{list_of_people}"


@app.route('/name')
def name():
    return render_template('cover.html') 


@app.route('/enrique')
def enrique():
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"
    return f"<h1>ENRIQUE</h1>"


@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']

    with db.connect() as conn:
        # Execute the query and fetch all results
        data = conn.execute(f"INSERT INTO entries (guestName) VALUES ('{email}')")

    return "The email address is '" + email + "'"


def init_connection_engine():
    db_config = {
        "pool_size": 5,
        "max_overflow": 2,
        "pool_timeout": 30,  # 30 seconds
        "pool_recycle": 1800,  # 30 minutes
    }

    if os.environ.get("DB_HOST"):
        return init_tcp_connection_engine(db_config)
    else:
        return init_unix_connection_engine(db_config)


def init_tcp_connection_engine(db_config):
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]

    # Extract host and port from db_host
    host_args = db_host.split(":")
    db_hostname, db_port = host_args[0], int(host_args[1])

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_hostname,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 3306
            database=db_name,  # e.g. "my-database-name"
        ),
        **db_config
    )
    return pool


def init_unix_connection_engine(db_config):
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    cloud_sql_connection_name = os.environ["CLOUD_SQL_CONNECTION_NAME"]

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={
                "unix_socket": "{}/{}".format(
                    db_socket_dir,  # e.g. "/cloudsql"
                    cloud_sql_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            }
        ),
        **db_config
    )

    return pool


db = init_connection_engine()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
