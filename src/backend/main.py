from flask import Flask
from ESClient import IRClient
from DBAccess import PaperAccess
from settings import parameters, sort_map
from ESUtils import gen_query
import json

app = Flask(__name__)

citation_es = IRClient(hosts=parameters["host"],
                       port=parameters["es_port"],
                       user=parameters["es_user"],
                       password=parameters["es_password"],
                       index=parameters["index"],
                       sort_map=sort_map)

citation_db = PaperAccess(hosts=parameters["host"],
                          port=parameters["db_port"],
                          db_name=parameters["db_name"],
                          doc_name=parameters["doc_name"],
                          sort_map=sort_map,)


@app.route('/query', methods=['GET'])
def search():
    query = gen_query()
    query["hits"] = citation_es.search(query)
    res = citation_db.search(query)
    # logger.write(gen_log(res))
    return json.dumps(res)


@app.route('/citations', methods=['GET'])
def get_citations():
    query = gen_query()
    res = citation_db.search(query)
    return json.dumps(res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
