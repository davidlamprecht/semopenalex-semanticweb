from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://semopenalex.org/sparql")

authors_set_work_filter = set()
works_set = set()


query_base = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
PREFIX fabio: <http://purl.org/spar/fabio/> 
PREFIX dcterms: <http://purl.org/dc/terms/> 
PREFIX sp: <https://semopenalex.org/property/>
PREFIX sc: <https://semopenalex.org/class/> 
SELECT DISTINCT ?work ?citedByCount ?year { 
  ?work dcterms:creator <?AUTHORURI> .
  ?work dcterms:abstract ?abstract .
  ?work fabio:hasPublicationYear ?year .
  ?work sp:citedByCount ?citedByCount .
  FILTER (?year >= 2005)
  FILTER (?citedByCount >= 10)
}
ORDER BY DESC (?citedByCount)
LIMIT 10
"""


# Datei öffnen
i = 0
with open('.../author-list-v0.txt', 'r', encoding='utf-8') as datei:
    for zeile in datei:
        # Entferne Leerzeichen und Zeilenumbrüche am Anfang und Ende der Zeile
        zeile = zeile.strip()
        query = query_base.replace("?AUTHORURI", str(zeile))
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        
        results = sparql.query().convert()
        if results["results"]["bindings"]:
            authors_set_work_filter.add(zeile)
            for result in results["results"]["bindings"]:
                works_set.add(result["work"]["value"])

        i += 1

        if i % 100 == 0:
            print("Finished query " + str(i))
            print("Authors added: " + str(len(authors_set_work_filter)))
            print("Works added: " + str(len(works_set)))


print("All Queries done:")
print(len(authors_set_work_filter))
print(len(works_set))

with open(".../author-list-v1.txt", "w") as f:
    for author in authors_set_work_filter:
        f.write(author + "\n")
        f.flush()


with open(".../work-list-v1.txt", "w") as f:
    for works in works_set:
        f.write(works + "\n")
        f.flush()

print("Done")