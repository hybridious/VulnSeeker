from flask import Flask, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
import psycopg2, json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'
db = SQLAlchemy(app)

import pdb

@app.route('/api/search', methods=['POST'])
def search():
    res = []
    es = Elasticsearch()
    data = json.loads(request.data)

    search_body = {
        "query": {
            "query_string": {
                "query": data.get('search')
            }
        }
    }


    for x in es.search(body=search_body).get('hits').get('hits'):
        _src = x.get('_source')
        entry = {'id' : x.get('_id')}
        entry.update(_src)
        res.append(entry)
    return json.dumps(res)

"""
    #keywords = str(request.form['keywords']).split()
    keywords = ['2014']
    vulns= []
    #TODO: Heavily ugly - need refactor when i'll get client need
    for keyword in keywords:
        print "toto2"
        sql = "select * from vuln;"
        print sql
        result = db.engine.execute(sql)
        for row in result:
            vulns.append(row[0])
    pdb.set_trace()
    return jsonify(vuln=vulns)

#get_alert_by_id(client_id)
"""

if __name__ == '__main__':
    app.run()
