from srmse import db
import queries
import re,json,os
from srmse import nutch
es = db.getES()
WIKI_MAPPING=json.loads(open("./wiki/infobox_mapping.json","r").read())
WIKI_KEYS_DEL=["^(wikt|voy|mw|display|commons|species|type|small|align|width|expiry|imageSize|source|row)$","^.$"]



def getTopLinks(TOP_LINKS):
	results=es.mget(index="nutch",doc_type="doc",body=TOP_LINKS)["docs"]
	results.reverse()
	return results


def search(query):
	dic=queries.getWikiQuery(query)
	res=es.search(index=queries.getWikiIndex(),doc_type=queries.getWikiDoc(),body=dic)
	li=res["hits"]["hits"]
	if len(li)==0:
		#empty results
		WIKI_RESULT=[]
		return
	d=[]
	homepages=[]
	extern=[]
	lii=[]
	ranked={}
	ranks=[]
	for indexx,i in enumerate(li):
		#sort according to page views
		try:
			count=i["fields"]["results"][0]["page_views"]
			if count in ranked:
				ranked[count]=str(ranked[count])+"###SPLIT###"+str(indexx)
			else:
				ranked[count]=str(indexx)
				ranks.append(count)
		except KeyError as e:
			pass
	ranks.sort()
	ranks.reverse()
	for rr in ranks:
		item=ranked[rr]
		if "###SPLIT###" in item:
			splits=item.split("###SPLIT###")
			for s in splits:
				lii.append(res["hits"]["hits"][int(s)])
			pass
		else:
			lii.append(res["hits"]["hits"][int(item)])
			
	for i in lii:
		info={}
		url=""
		external_links=[]
		hp=""
		title=""
		body=""
		image = []
		try:
			tmp_info=i["fields"]["results"][0]["box"]
			t={}
			for key in tmp_info:
				b=False
				for r in WIKI_KEYS_DEL:
					c=re.match(r,key)
					if c is not None:
						b=True
						break
				if b:
					continue
				if key in WIKI_MAPPING:
					t[WIKI_MAPPING[key]]=tmp_info[key]
				else:
					t[key]=tmp_info[key]
			
				
			info=t
		except KeyError:
			info={}
		try:
			url=i["_id"]
		except KeyError:
			url=""
		try:
			external_links=i["fields"]["results"][0]["external_links"]
		except KeyError:
			external_links=[]
		try:
			hp=i["fields"]["results"][0]["home_page"]
		except KeyError:
			hp=""
		try:
			title=url.split("/")[-1]
		except KeyError:
			title=""
		try:
			body=i["highlight"]["body"][0]
		except KeyError:
			body=""
		try:
			image = i["fields"]["results"][0]["image"]
		except KeyError:
			image=[]
		d.append({"infobox":info,
			"url":url,
			"title":title,
			"body":body
		})
		TOP_LINKS={"docs":[]}
		for e in external_links:
			u=e.replace("http://","http://").replace("https://","http://")
			#searching with both http:// and https://
			TOP_LINKS["docs"].append({"_id":nutch.getId(u),"_source":["url","title","host","type","meta_description","content"]})
			TOP_LINKS["docs"].append({"_id":nutch.getId(u.replace("http://","https://")),"_source":["url","title","host","type","meta_description","content"]})
		h=hp.replace("http://","http://").replace("https://","http://")
		#searching with both http:// and https://
		TOP_LINKS["docs"].append({"_id":nutch.getId(h),"_source":["url","title","host","type","meta_description","content"]})
		TOP_LINKS["docs"].append({"_id":nutch.getId(h.replace("http://","https://")),"_source":["url","title","host","type","meta_description","content"]})
		TOP_LINKS_TMP = getTopLinks(TOP_LINKS)
		for r in TOP_LINKS_TMP:
			if r["found"]:
				r["_source"]["content"]=r["_source"]["content"][0:300]
				d.append(r["_source"])
	return d
