from py4j.java_gateway import DEFAULT_ADDRESS
from pyspark import SparkConf, SparkContext, TaskContext, StorageLevel
from pyspark.sql import SparkSession
import pymongo
from tqdm import tqdm
from operator import add
import math
import json

PART = 500
MONGOURI = 'mongodb://10.108.17.104:27017/IR.citations'

myconf = SparkConf()\
    .set("spark.local.dir", "/home1/public_place/tmp,/home3/public_place/tmp")\
    .set("spark.driver.memory", "100G")\
    .set("spark.driver.maxResultSize", "100G")\
    .set("spark.executor.heartbeatInterval", "60s")\
    .set("spark.network.timeout", "600s")
spark = SparkSession.builder\
                    .config(conf=myconf)\
                    .getOrCreate()

data = spark.read.format("com.mongodb.spark.sql.DefaultSource")\
    .option("uri", MONGOURI).load().repartition(PART).rdd

print('data loading finish\n')
'''
data 格式
Sid，_id，importance，inCitations,inCitationsCount，outCitations，outCitationsCount，title，year
'''

# x: (sid, (list, score))


def calc_contribs(x):
    tot = len(x[1][0])
    for y in x[1][0]:
        yield (y, x[1][1] / tot)


def calc_scores(x):
    alpha = 1 / math.log10(10 + 2021 - x[1][2])
    return alpha * x[0], [x[1][0], x[1][1], x[1][2], x[1][3], x[1][4], x[1][5], x[1][6]]


links = data.map(lambda x: (x[0], x[5])).persist(
    StorageLevel.DISK_ONLY)  # (sid, list)
ranks = links.map(lambda x: (x[0], 1.0))  # (sid, rank)
tags = data.map(lambda x: (x[0], (int(x[4]), int(x[6]), int(x[8]), x[3], x[5], x[7])))\
    .persist(StorageLevel.DISK_ONLY)  # (sid, (in_degree, out_degree, year, in, out, title))
base = tags.filter(lambda x: x[1][0] == 0 and x[1][1] > 0).map(
    lambda x: (x[0], 0.15)).persist(StorageLevel.DISK_ONLY)  # (sid, 0.15)
empty = tags.filter(lambda x: x[1][0] + x[1][1]
                    == 0).map(lambda x: (x[0], 0))  # (sid, 0)

for i in range(10):
    # (sid, (list, rank)) => (new_sid, new_rank)
    contribs = links.join(ranks).flatMap(calc_contribs)
    ranks = contribs.reduceByKey(add).mapValues(
        lambda rank: 0.85 * rank + 0.15)
    ranks = ranks.union(base).coalesce(PART)

# (sid, (rank, (in_degree, out_degree, year, in, out, title))) => (sid, (score, in_degree, out_degree, year, in, out, title))
scores = ranks.union(empty).join(tags).mapValues(calc_scores)


def save_jsonl(part):
    pid = TaskContext().partitionId()
    f = open('./tmp_ir/part_{}.jsonl'.format(pid), 'w')
    for raw in part:
        sid, payload = raw
        record = {
            'Sid': sid,
            'importance': payload[0],
            'inCitations': payload[4],
            'inCitationsCount': payload[1],
            'outCitations': payload[5],
            'outCitationsCount': payload[2],
            'title': payload[6],
            'year': payload[3]
        }
        f.write('{}\n'.format(json.dumps(record)))
    f.close()


scores.foreachPartition(save_jsonl)
