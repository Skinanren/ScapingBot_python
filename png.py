import requests

url = 'https://slavneobrazy.cz/obr/webp/6676.webp'
url1 = 'https://www.craftfineart.com/fine-art-prints/turner-william/religious'
url2 = 'https://slavneobrazy.cz/obr/webp/5464.webp'

filename = url2.split('/')[-1]
r = requests.get(url, allow_redirects=True)
open(filename, 'wb').write(r.content)