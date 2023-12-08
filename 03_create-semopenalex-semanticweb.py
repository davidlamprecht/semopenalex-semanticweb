from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from SPARQLWrapper import SPARQLWrapper, JSON, N3


#Author Information
query_author = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    CONSTRUCT {
        ?s ?p ?o
    }
    WHERE {
        ?s ?p ?o .
        FILTER (?s = <?AUTHORURI>)      
    }
"""

#Institution Information
query_institution = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    CONSTRUCT {
        ?o ?a ?b 
    }
    WHERE {
        ?s ?p ?o .
        FILTER (?s = <?AUTHORURI>) 
        ?o rdf:type <https://semopenalex.org/class/Institution> .
        ?o ?a ?b .         
    }
"""

#Work Information
query_work = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    CONSTRUCT {
        ?s ?p ?o
    }
    WHERE {
        ?s ?p ?o .
        FILTER (?s = <?WORKURI>)      
    }
"""

#Author Position Information
query_author_position = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    CONSTRUCT {
        ?o ?a ?b 
    }
    WHERE {
        ?s ?p ?o .
        FILTER (?s = <?WORKURI>)    
        ?o rdf:type <https://semopenalex.org/class/AuthorPosition> .
        ?o ?a ?b .
    }
"""

#Concept Information
query_concept = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    CONSTRUCT {
        ?o ?a ?b 
    }
    WHERE {
        ?s ?p ?o .
        FILTER (?s = <?WORKURI>)    
        ?o rdf:type <http://www.w3.org/2004/02/skos/core#Concept> .
        ?o ?a ?b .
    }
"""

#Concept Score Information
query_concept_score = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    CONSTRUCT {
        ?o ?a ?b 
    }
    WHERE {
        ?s ?p ?o .
        FILTER (?s = <?WORKURI>)    
        ?o rdf:type <https://semopenalex.org/class/ConceptScore> .
        ?o ?a ?b .
    }
"""

#Location Information
query_location = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    CONSTRUCT {
        ?o ?a ?b 
    }
    WHERE {
        ?s ?p ?o .
        FILTER (?s = <?WORKURI>)    
        ?o rdf:type <https://semopenalex.org/class/Location> .
        ?o ?a ?b .
    }
"""

#Source Information
query_source = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    CONSTRUCT {
        ?b ?c ?d 
    }
    WHERE {
        ?s ?p ?o.
        FILTER (?s = <?WORKURI>)          
        ?o rdf:type <https://semopenalex.org/class/Location> .
        ?o ?a ?b .  
  		?b rdf:type <https://semopenalex.org/class/Source> .
        ?b ?c ?d .
    }
"""

#Publisher Information
query_publisher = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    PREFIX sp: <https://semopenalex.org/property/>
    CONSTRUCT {
       ?d ?e ?f
    }
    WHERE {
        ?s ?p ?o.
        FILTER (?s = <?WORKURI>)          
        ?o rdf:type <https://semopenalex.org/class/Location> .
        ?o ?a ?b .  
  		?b rdf:type <https://semopenalex.org/class/Source> .
        ?b sp:hasHostOrganization ?d .
  	    ?d rdf:type <https://semopenalex.org/class/Publisher> .
        ?d ?e ?f .
    }
"""

sparql = SPARQLWrapper("https://semopenalex.org/sparql")

# Initialisieren Sie den Graphen
g = Graph()

def execute_query(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(N3)
    results = sparql.query().convert()
    g.parse(data=results, format='n3')

#AUTHORURIs file
i = 0
with open('.../author-list-v1.txt', 'r') as file:
    for line in file:
        author_uri = line.strip()
        current_query_a = query_author.replace("?AUTHORURI", str(author_uri))
        execute_query(current_query_a)

        current_query_b = query_institution.replace("?AUTHORURI", str(author_uri))
        execute_query(current_query_b)

        i += 1
        if i % 100 == 0:
            print("Finished Author query " + str(i))

#WORKURIs file
i = 0
with open('.../work-list-v1.txt', 'r') as file:
    for line in file:
        work_uri = line.strip()
        current_query_a = query_work.replace("?WORKURI", str(work_uri))
        execute_query(current_query_a)

        current_query_b = query_author_position.replace("?WORKURI", str(work_uri))
        execute_query(current_query_b)

        current_query_c = query_concept.replace("?WORKURI", str(work_uri))
        execute_query(current_query_c)

        current_query_d = query_concept_score.replace("?WORKURI", str(work_uri))
        execute_query(current_query_d)

        current_query_e = query_location.replace("?WORKURI", str(work_uri))
        execute_query(current_query_e)

        current_query_f = query_source.replace("?WORKURI", str(work_uri))
        execute_query(current_query_f)

        current_query_g = query_publisher.replace("?WORKURI", str(work_uri))
        execute_query(current_query_g)

        i += 1
        if i % 100 == 0:
            print("Finished Work query " + str(i))


print("Construct Querys finished")

g.serialize(destination='.../semopenalex-semanticweb.nt', format='nt', encoding='utf-8')

print("Done")