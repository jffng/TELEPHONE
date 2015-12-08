import json, urllib, unirest, re
from sys import argv
from random import randint
from clarifai.client import ClarifaiApi
api = ClarifaiApi()

f_name = argv[1]
matcher = re.compile('([^n\/]\w+)')

results = api.tag_images([open(f_name)])

results = results['results'][0]['result']['tag']['classes']

titles = []

for r in results: 
	encoded_tag = urllib.quote(r.lower(), '')
	# print encoded_tag
	uri = 'http://conceptnet5.media.mit.edu/data/5.4/c/en/' + encoded_tag

	limit = 10

	response = unirest.get(uri,
		headers= {
			"Accept": "text/plain"
		},
		params={
			'limit': limit
	})
	try: 
		for e in response.body['edges']:
			matches = matcher.findall(e['uri'])
			for m in matches:
				if len(m) > 25:
					titles.append(m.replace('_', ' '))
	except:
		print ' '

print titles[randint(0,len(titles) - 1)]