curl -X DELETE localhost:9200/citations
curl -H 'Content-Type: application/json' -X PUT 'localhost:9200/citations?pretty' -d'
{
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "Sid": { "type": "keyword" },
      "title": { "type": "text" },
      "year": {"type": "short"},
      "inCitationsCount" : {"type" : "integer", "index" : false},
      "outCitationsCount" : {"type" : "integer", "index" : false},
      "importance": {"type": "double"}
    }
  }
}'
