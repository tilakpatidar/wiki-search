def getWikiIndex():
    return "wiki_module1"
def getWikiDoc():
    return "doc"
def getGeneralIndex():
    return "nutch"
def getGeneralDoc():
    return "doc"
def getNewsIndex():
    return "news"
def getNewsDoc():
    return "news"
def getWikiQuery(wiki_query):
  return {
  "size": 10,
  "partial_fields": {
    "results": {
      "include": ["body", "box", "_id", "website", "external_links", "page_views"]
    }
  },
  "highlight": {
    "fields": {
      "body": {
        "fragment_size": 400
      }
    }
  },
  "query": {
    "multi_match": {
      "minimum_should_match": "50%",
      "query": wiki_query,
      "fields": ["search^10", "home_page^5", "redirect_search_*^5", "c_*^1", "body^2", "external_links^5"],
      "type": "cross_fields"
    }
  }
}

def getClusterURL():
    return 'http://192.168.101.5:9200/nutch/doc/_search_with_clusters'
def getClusterQuery(query):
  return {
  "size": 100,
  "search_request": {
    "fields": ["url","title","meta_description","host"],
    "query": {
      "multi_match": {
        "query": query,
        "fields": ["title^5","meta_description^5","content","host^5","url^5"],
        "type": "cross_fields"

      }
    },
    "filter": {
      "bool": {
        "must_not": [{
          "term": {
            "host": "en.wikipedia.org"
          }
        }, {
          "term": {
            "host": "pixabay.com"
          }
        }]
      }
    },

    "size": 100
  },
  "minimum_should_match": "75%",
  "query_hint": query,
  "field_mapping": {
    "title": ["fields.title", "fields.content"]
  }
}
def getRequiredFields(typee):
	dic={"general":["title","meta_description","url","type","content"],"news":["url","title","meta_description","body","host","img"]}
	return dic[typee]
def getGeneralQuery(query):
  return {
  "size": 10,
  "fields": ["url","title","meta_description","host","content","type"],
  "query": {
    "multi_match": {
      "minimum_should_match": "100%",
      "query": query,
      "fields": ["title^4", "meta_description^2", "content", "host^4", "url^4"],
      "type": "cross_fields"
    }
  },
  "filter": {
    "bool": {
      "must_not": [{
        "term": {
          "host": "en.wikipedia.org"
        }
      }, {
        "term": {
          "host": "thinkstockphotos.in"
        }
      }, {
        "term": {
          "host": "github.com"
        }
      }]
    }
  }
}

def getNewsQuery(query):
  return {
  "size": 100,
  "sort": ["_score"],
  "fields": ["url","title","meta_description","body","host","img"],
  "query": {
    "multi_match": {
      "minimum_should_match": "100%",
      "query": query,
      "fields": ["url","host^2","title^2","body","meta_description^2"],
      "type":"cross_fields"
    }
  },
  "filter": {
    "bool": {
      "must_not": [{
        "term": {
          "host": "en.wikipedia.org"
        }
      }, {
        "term": {
          "host": "thinkstockphotos.in"
        }
      }, {
        "term": {
          "host": "github.com"
        }
      }, {
        "term": {
          "host": "pixabay.com"
        }
      }]
    }
  }
}
