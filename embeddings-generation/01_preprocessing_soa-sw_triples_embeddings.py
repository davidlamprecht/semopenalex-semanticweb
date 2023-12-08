''' 
Preprocessing script to tranform soa-sw.nt to input files for knowedle graph embedding models.
Input file: soa-sw.nt
Output files: triples_input_embeddings.txt, entity_mapping.txt and relation_mapping.txt
'''
import rdflib
from rdflib import Graph, URIRef
import numpy as np

# Erstellen Sie ein Graph-Objekt
graph = rdflib.Graph()

# Laden Sie die .nt-Datei in den Graphen


file_path = ".../soa-sw.nt"

graph.parse(file_path, format="nt")

# Anzahl der Tripel im Graphen ausgeben
print(f"Der Graph enthält {len(graph)} Tripel.")


class_list = [
    URIRef("https://semopenalex.org/class/Work"),
    URIRef("https://semopenalex.org/class/Author"),
    URIRef("https://semopenalex.org/class/Institution"),
    URIRef("https://semopenalex.org/class/Source"),
    URIRef("http://www.w3.org/2004/02/skos/core#Concept"),
    URIRef("https://semopenalex.org/class/Publisher"),
    URIRef("https://semopenalex.org/class/Location")
]



pred_list = [ 
    URIRef("http://purl.org/spar/cito/cites"),
    URIRef("https://semopenalex.org/property/hasRelatedWork"), 
    URIRef("https://semopenalex.org/property/hasLocation"), 
    URIRef("https://semopenalex.org/property/hasPrimaryLocation"), 
    URIRef("https://semopenalex.org/property/hasBestOaLocation"), 
    URIRef("https://semopenalex.org/property/hasSource"),
    URIRef("https://semopenalex.org/property/hasHostOrganization"),
    URIRef("https://semopenalex.org/property/hasParentPublisher"),
    URIRef("https://semopenalex.org/property/hasConcept"),
    URIRef("http://purl.org/dc/terms/creator"), 
    URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),  
    URIRef("http://www.w3.org/ns/org#memberOf"),                 
    URIRef("https://semopenalex.org/property/hasAssociatedInstitution"),
    URIRef("http://www.w3.org/2004/02/skos/core#broader"),
    URIRef("http://www.w3.org/2004/02/skos/core#related")
]



# Initialisierung der Zähler und Wörterbücher
entity_counter = 0
relation_counter = 0
entity_dict = {}
relation_dict = {}

triples = []

# Iteration über die Tripel im Graphen
for s, p, o in graph:
    # Wenn das Prädikat rdf:type ist, überprüfen wir, ob das Objekt o in der Klassenliste ist
    if p == URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"):
        if o not in class_list:
            continue
    else:
        # Wenn das Prädikat nicht rdf:type ist, prüfen wir die Klasse des Objekts und des Subjects
        # Erhalte alle Typen der Objekte und Subjects
        o_classes = [obj for obj in graph.objects(o, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"))]
        s_classes = [obj for obj in graph.objects(s, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"))]

        # Überspringe, wenn das Objekt oder das Subject keine Klasse in der Klassenliste hat
        if type(o) is URIRef and not any(oc in class_list for oc in o_classes):
            continue
        if type(s) is URIRef and not any(sc in class_list for sc in s_classes):
            continue

    # Überspringe Literale und Prädikate, die nicht in der Liste sind
    if type(o) is not URIRef or p not in pred_list:
        continue

    # Überprüfung und Zuordnung der Entitäten und Beziehungen
    if s not in entity_dict and s not in class_list:
        entity_dict[s] = entity_counter
        entity_counter += 1

    if o not in entity_dict and o not in class_list:
        entity_dict[o] = entity_counter
        entity_counter += 1

    if p not in relation_dict:
        relation_dict[p] = relation_counter
        relation_counter += 1

    # Prüfe ob Subjekt, Prädikat und Objekt im Mapping sind, bevor wir das Tripel hinzufügen
    if s in entity_dict and p in relation_dict and o in entity_dict:
        triples.append((entity_dict[s], relation_dict[p], entity_dict[o]))

# Speichern der Tripel in eine Textdatei
np.savetxt('.../triples.txt', triples, fmt='%i')

# Speichern der Zuordnung von Entitäten und Beziehungen in Textdateien
with open('.../entity_mapping.txt', 'w') as f:
    for key, value in entity_dict.items():
        f.write('%s\t%i\n' % (str(key), value))

with open('.../relation_mapping.txt', 'w') as f:
    for key, value in relation_dict.items():
        f.write('%s\t%i\n' % (str(key), value))
