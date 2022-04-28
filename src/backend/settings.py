parameters = {
    "host": "10.108.17.104",

    # es
    "es_port": 9200,
    "es_user": "elastic",
    "es_password": "000000",
    "index": "citations",

    # db
    "db_port": 27017,
    "db_name": "IR",
    "doc_name": "citations"
}

sort_map = {
    "sort_by_time": "year",
    "sort_by_incite": "inCitationsCount",
    "sort_by_outcite": "outCitationsCount"
}

bool_map = {
    "true": True,
    "false": False
}
