from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import psycopg2
import pdb
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
db = SQLAlchemy(app)


sql = 'select * from vuln'
result = db.engine.execute(sql)
names = []
for row in result:
    names.append(row[1])

print names


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
