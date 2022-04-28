from elasticsearch import Elasticsearch
import time


class ESClient:
    def __init__(self, **kwargs):
        self.hosts = kwargs['hosts']
        self.port = kwargs['port']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.index = kwargs['index']
        self.sort_map = kwargs['sort_map']
        self.es = Elasticsearch(hosts=self.hosts,
                                http_auth=(self.user, self.password),
                                port=self.port)
        # print(self.es)

    def delete_index(self):
        return self.es.indices.delete(index=self.index)

    def put_mapping(self, body):
        self.es.indices.put_mapping(index=self.index, body=body)

    def add_sort(self, ori_query):
        sort_condition = []
        for key in self.sort_map:
            if key in ori_query and ori_query[key] != "false":
                condition = {
                    self.sort_map[key]: {
                        "order": ori_query[key]
                    }
                }
                sort_condition.append(condition)
        return sort_condition

    def search(self, query):
        raise NotImplementedError

    @staticmethod
    def time_record(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            res = func(*args, **kwargs)
            end_time = time.time()
            args[1]["search_time"] = end_time - start_time
            return res
        return wrapper

    def __del__(self):
        self.es.close()
        print("elasticsearch closed")


class IRClient(ESClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.func_map = {
            "TITLE": self.search_title
        }

    @ESClient.time_record
    def search(self, query):
        return self.func_map[query["type"]](query)

    def search_title(self, query):
        es_query = {
            "track_total_hits": "true",
            "from": query["size"]*query["from"],
            "size": query["size"],
            "query": {
                "bool": {
                    "must": [
                        {
                            "function_score": {
                                "query": {
                                    "bool": {
                                        "should": [
                                            {
                                                "match": {
                                                    "title": {
                                                        "query":
                                                            query["query"],
                                                        "boost": 2.0,
                                                        "operator": "or",
                                                        "minimum_should_match":
                                                            "85%"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }
        es_query["query"]["bool"]["filter"]\
            = self.gen_filter(query)
        es_query["query"]["bool"]["must"][0]["function_score"]["functions"]\
            = self.gen_optimizer(query)
        es_query["sort"] = self.add_sort(query)

        res = self.es.search(index=self.index, body=es_query)

        id_list = [item["_source"]["Sid"] for item in res["hits"]["hits"]]

        hit = dict()
        hit["total"] = res["hits"]["total"]["value"]
        hit["hit"] = id_list
        return hit

    def add_sort(self, ori_query):
        sort_condition = []
        for key in self.sort_map:
            if key in ori_query and ori_query[key] != "false":
                condition = {
                    self.sort_map[key]: {
                        "order": ori_query[key]
                    }
                }
                sort_condition.append(condition)
        return sort_condition

    def gen_filter(self, query):
        es_filter = []
        if query["filter_year"]:
            filter_query = {"range": {"year": {}}}
            if query["s_year"] != 0:
                filter_query["range"]["year"]["gte"] = query["s_year"]
            if query["e_year"] != 0:
                filter_query["range"]["year"]["lte"] = query["e_year"]
            es_filter.append(filter_query)
        return es_filter

    def gen_optimizer(self, query):
        es_optimizer = []
        if query["sort_by_importance"]:
            es_function = {
                "field_value_factor": {
                    "field": "importance",
                    "modifier": "log1p",
                    "missing": 1
                }
            }
            es_optimizer.append(es_function)
        return es_optimizer
