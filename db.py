from flask_mysqldb import MySQL
from config import DB_NAME, USERNAME, PASSWORD

mysql = MySQL()

def init_db(app):
    app.config["MYSQL_DB"] = DB_NAME
    app.config["MYSQL_USER"] = USERNAME
    app.config["MYSQL_PASSWORD"] = PASSWORD
    app.config["MYSQL_HOST"] = "localhost"
    app.config["MYSQL_PORT"] = 3306

    mysql.init_app(app)
    return mysql
