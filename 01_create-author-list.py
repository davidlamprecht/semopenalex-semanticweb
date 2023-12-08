from SPARQLWrapper import SPARQLWrapper, JSON


sparql = SPARQLWrapper("https://semopenalex.org/sparql")

query = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX fabio: <http://purl.org/spar/fabio/> 
PREFIX dcterms: <http://purl.org/dc/terms/> 
PREFIX sp: <https://semopenalex.org/property/>
PREFIX sc: <https://semopenalex.org/class/> 
SELECT DISTINCT ?author ?worksCount { 
  ?work sp:hasConcept <https://semopenalex.org/concept/C2129575> .
  ?work dcterms:creator ?author .
  ?author sp:worksCount ?worksCount .
}
"""

authors_set = set()
sparql.setReturnFormat(JSON)

sparql.setQuery(query)
    

results = sparql.query().convert()

for result in results["results"]["bindings"]:
    works_count = int(result["worksCount"]["value"])

    if 3 <= works_count <= 200:
        author_uri = result["author"]["value"]
        authors_set.add(author_uri)


print(len(authors_set))

#save authors_set to text file
with open(".../author-list-v0.txt", "w") as f:
    for author in authors_set:
        f.write(author + "\n")
