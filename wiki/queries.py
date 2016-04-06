def getWikiIndex():
    return "wiki_module"
def getWikiDoc():
    return "doc"
def getWikiQuery(wiki_query):
  return {
  "size": 2,
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
      "minimum_should_match": "100%",
      "query": wiki_query,
      "fields": ["search^10", "home_page^5", "redirect_search_*^5", "c_*^1", "body^2", "external_links^5"],
      "type": "cross_fields"
    }
  }
}


def getRequiredFields(typee):
	dic={"general":["title","meta_description","url","type","content"],"news":["url","title","meta_description","body","host","img"]}
	return dic[typee]
