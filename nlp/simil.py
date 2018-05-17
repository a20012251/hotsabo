import json
import gensim

articlesData = json.loads(open('articlesData.json').read())

from nltk.tokenize import word_tokenize

tokenList = [] #lista total de tokens

###Creacion de corpus y tf_idf de todas las publicaciones
for item in articlesData:
    item["_values"]["tokens"] = word_tokenize(item["_values"]["content"])
    for w in item["_values"]["tokens"]:
        w.lower()
    tokenList.append(item["_values"]["tokens"])

mainDict = gensim.corpora.Dictionary(tokenList)

mainCorpus = [mainDict.doc2bow(tokenItem) for tokenItem in tokenList]
mainTf_idf = gensim.models.TfidfModel(mainCorpus)

mainSims = gensim.similarities.Similarity('/home/nosabo/Documents/Coding/Python/my_project/',
                                            mainTf_idf[mainCorpus],num_features=len(mainDict))


###Encontrar publicaciones similares y agregar un nuevo
### campo con la lista de publicaciones similares
for item in articlesData:
    query = mainTf_idf[mainDict.doc2bow(item["_values"]["tokens"])]
    item["_values"]["similares"] = []
    item["_values"]["isNews"] = 0
    for index, percent in enumerate(mainSims[query]):
        if (percent > 0.4):
            item["_values"]["similares"].append(index)


###Utilizar las siguientes dos lineas para mostrar los grupos
### de noticias de cada publicacion:
for pub in articlesData:
    print(pub["_values"]["noticias"])

###Crear archivo JSON:
with open('newArticlesData.json', 'w') as outfile:
    json.dump(articlesData, outfile, indent=4)
