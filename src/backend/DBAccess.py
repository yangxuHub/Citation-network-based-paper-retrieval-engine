import pymongo
from bson.objectid import ObjectId
import time


class DBAccess:
    def __init__(self, **kwargs):
        hosts = kwargs["hosts"]
        port = kwargs["port"]
        db_name = kwargs["db_name"]
        doc_name = kwargs["doc_name"]
        self.sort_map = kwargs["sort_map"]
        con_str = "mongodb://{}:{}/{}".format(hosts, port, db_name)
        self.db_client = pymongo.MongoClient(con_str)
        self.db = self.db_client[db_name]
        self.doc = self.db[doc_name]

    @staticmethod
    def replace_id_view(data):
        # docs are from view so just replace "_id" with Sid
        for item in data:
            item["_id"] = item["Sid"]

    def basic_search(self, query, page_id, page_size):
        res = self.doc.find(query).skip(page_size*page_id).limit(page_size)
        return res

    def sort_search(self, query, page_id, page_size, sort_condition):
        res = self.doc.find(query).sort(sort_condition)\
            .skip(page_size*page_id).limit(page_size)
        return res

    def search_by_id(self, _id):
        db_query = {"_id": _id if isinstance(_id, ObjectId) else ObjectId(_id)}
        res = self.doc.find_one(db_query)
        return res

    def search_by_id_list(self, id_list):
        res = []
        for _id in id_list:
            res.append(self.search_by_id(_id))
        return res

    @staticmethod
    def reformat_id(data):
        if isinstance(data, list):
            for idx in range(len(data)):
                if isinstance(data[idx], ObjectId):
                    data[idx] = str(data[idx])
                else:
                    DBAccess.reformat_id(data[idx])
        elif isinstance(data, dict):
            for key in data:
                if isinstance(data[key], ObjectId):
                    data[key] = str(data[key])
                else:
                    DBAccess.reformat_id(data[key])

    @staticmethod
    def time_record(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            res = func(*args, **kwargs)
            end_time = time.time()
            if "db_time" in args[1]:
                args[1]["db_time"] += end_time - start_time
            else:
                args[1]["db_time"] = end_time - start_time
            return res
        return wrapper

    def __del__(self):
        self.db_client.close()
        print("mongodb connection closed")


class PaperAccess(DBAccess):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.func_map = {
            "TITLE": self.search_by_paper_id_list,
            "CITATIONS": self.search_by_citation_root_sid
        }

    def search_by_sid(self, sid):
        db_query = {"Sid": sid}
        res = self.doc.find_one(db_query)
        return res

    def search_by_sid_list(self, sid_list):
        res = []
        for sid in sid_list:
            res.append(self.search_by_sid(sid))
        return res

    @DBAccess.time_record
    def search(self, query):
        res = self.func_map[query["type"]](query)
        return res

    def search_by_paper_id_list(self, query):
        """
        :param query: full query
        :return:
        """
        res = self.search_by_sid_list(query["hits"]["hit"])
        # for i,data in enumerate(res):
        #     print("data {}:{}".format(i, data))
        self.reformat_id(res)
        self.replace_id_view(res)
        query["hits"]["hit"] = res
        # res = self.modify_res(query)
        return query

    def search_by_citation_root_sid(self, query):
        root_sid = query["sid"]
        depth = query["depth"]
        length = query["length"]
        res = self.search_by_sid(root_sid)
        self.reformat_id(res)
        res["_id"] = res["Sid"]
        self.shrink_citations(res, length)
        if depth > 0:
            self.append_citations(res, depth, 1, length)
        query["hit"] = res
        return query

    def append_citations(self, root, max_depth, depth, length):
        if depth <= max_depth:
            for i in range(len(root["inCitations_shrink"])):
                self.shrink_citations(root["inCitations_shrink"][i], length)
                self.append_citations(root["inCitations_shrink"][i],
                                      max_depth, depth + 1, length)
            for i in range(len(root["outCitations_shrink"])):
                self.shrink_citations(root["outCitations_shrink"][i], length)
                self.append_citations(root["outCitations_shrink"][i],
                                      max_depth, depth + 1, length)

    def shrink_citations(self, root, length):
        inCitations_total = list(
            filter(None, self.search_by_sid_list(root["inCitations"])))
        self.reformat_id(inCitations_total)
        self.replace_id_view(inCitations_total)
        if length < len(inCitations_total):
            root["inCitations_shrink"]\
                = sorted(inCitations_total,
                         key=lambda item: item["importance"],
                         reverse=True)[:length]
        else:
            root["inCitations_shrink"] \
                = inCitations_total

        outCitations_total = list(
            filter(None, self.search_by_sid_list(root["outCitations"])))
        self.reformat_id(outCitations_total)
        self.replace_id_view(outCitations_total)
        if length < len(outCitations_total):
            root["outCitations_shrink"]\
                = sorted(outCitations_total,
                         key=lambda item: item["importance"],
                         reverse=True)[:length]
        else:
            root["outCitations_shrink"] = inCitations_total
