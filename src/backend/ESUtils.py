from flask import request
from settings import bool_map


def reformat_title(args):
    args["from"] = int(args["from"])
    args["size"] = int(args["size"])

    args["filter_year"] = bool_map[args["filter_year"]]
    args["sort_by_importance"] = bool_map[args["sort_by_importance"]]
    args["s_year"] = int(args["s_year"])
    args["e_year"] = int(args["e_year"])


def reformat_citaions(args):
    args["depth"] = int(args["depth"])
    args["length"] = int(args["length"])


reformat_map = {
    "TITLE": reformat_title,
    "CITATIONS": reformat_citaions
}


def gen_query():
    res = {}
    args = request.args
    for key in args:
        res[key] = args[key]
    reformat_map[res["type"]](res)
    # print("query", json.dumps(res, indent=1))
    return res
