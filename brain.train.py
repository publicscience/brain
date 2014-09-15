import json
from app.brain import train

f = open('~/sliced_articles_BIG.json', 'r')
data = json.load(f)

docs = [article['text'] for article in data]
print(docs)
#train(docs)
