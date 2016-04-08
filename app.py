#!/usr/bin/env python
from bottle import route, error, post, get, run, static_file, abort, redirect, response, request, template
import sys,urlparse,json
import wiki


@route('/index.html')
def index():
	redirect("/")

@route('/query.html')
def index():
	redirect("/query")

@route('/')
def home():
	return template('assets/index.html',name=request.environ.get('REMOTE_ADDR'))

@route('/query')
def search():
	query = request.query['q']
	print query
	return template('assets/query.html',name=request.environ.get('REMOTE_ADDR') ,query = query )

@get("/search")
def search():
	query = request.query['query']
	response.headers['Content-Type'] = 'text/javascript'
	return "callback("+json.dumps(wiki.search(query))+")"

@post("/autosuggest")
def autosuggest():
	entity=None
	data = request.body.readline()
	if not data:
		abort(400, 'No data received')
	else:
		entity = dict(urlparse.parse_qs(data))
	#print entity
	return json.dumps([{"label":entity["q"][0],"value":entity["q"][0]}])

# Static Routes
@get('/assets/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='assets/js')

@get('/assets/<filename:re:.*\.css>')
def stylesheets(filename):
	return static_file(filename, root='assets/css')

@get('/assets/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='assets/img')

@get('/assets/<filename:re:.*\.(eot|ttf|woff|woff2|svg)>')
def fonts(filename):
	return static_file(filename, root='assets/fonts')

@get('/assets/<filename:re:.*\.(json)>')
def json_assets(filename):
	return static_file(filename, root='assets/json')

@get('/fonts/<filename:re:.*\.(eot|ttf|woff|woff2|svg)>')
def fonts(filename):
	return static_file(filename, root='assets/fonts')

run(host='0.0.0.0', port=sys.argv[1], debug=True)
