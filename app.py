from flask import Flask, jsonify, request, Response
from elasticsearch import Elasticsearch
import psycopg2, json
from db import Session
from models import Entry
import pdb


app = Flask(__name__)


@app.route('/api/entries', methods=["GET", "POST"])
def list_entries():
    if request.method == 'POST':
        data = json.loads(request.data)
        cve_id = data.get('cve_id')
        cvss_score = data.get('cvss_score')
        version = data.get('version')
        description = data.get('description')
        product_name = data.get('product_name')

        session = Session()
        entry = Entry(cve_id=cve_id, cvss_score=cvss_score, version=version, description=description, product_name=product_name)
        session.add(entry)
        session.commit()

        return 'ok'

    else:
        session = Session()
        entries = session.query(Entry).all()
        return Response(json.dumps(
            [{"title": x.title, "content": x.content} for x in entries]),
                        mimetype='application/json')


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
