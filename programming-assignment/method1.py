import networkx
import csv
from graph_op import KG, Query

'''
Algorithm:
1. Identify entities and relation in the query
2. take all the triplets containing the 
3. get word2vec of relation and find similarity
4. assign the object of highest entity
'''

def qa(q,G):
    query = Query(q)
    ent = str(query.get_entity())
    query_relation = query.get_relation(str(ent))
    ent = ent.lower()
    obj = None
    similarity_max = 0
    for entity in G.node_disambiguation(ent):
        kg_relation = G.get_node_relation(entity)
        one_hope_answer = G.get_similar_triple(query_relation, kg_relation)
        similarity = one_hope_answer[1]
        if similarity > similarity_max:
            similarity_max = similarity
            obj = G.get_object(entity, one_hope_answer[0])
    print("Query is: " + q)
    print("Answer is: " + str(obj))
# design the KG graph
G = KG()


Dev_qlist = ["What is the place of birth of Tom Hanks?",
"What is the number of children of Tom Cruise?",
"Who are the siblings of Travolta?", 
"What was the name of Hepburn at birth?", 
"Who was the father of Katharine Hepburn?",
"What is the date of birth of Ron Howard?",
"What is the hair color of Ron Weasley?",
"Who did the soundtrack for Lord of the Rings?",
"Who composed the score for Harry Potter?",
"Who was Robin Williams married to?"]

test_qlist = ["What is the birth place of Tom Hanks?",
"Who is married to Tom Cruise?",
"What was the occupation of John Travolta?",
"How many children did Audrey Hepburn have?",
"Where was Katharine Hepburn born?",
"What is the hair color of Ron Howard?",
"Who performed as Ron Weasley in the movies?",
"Where was Howard Shore educated at?",
"Who was the son of John Williams?",
"How did Robin Williams die?"]

# Construct KG
with open('programming-assignment/toy-kg.tsv') as f:
    rd = f.read()
f.close()
rd = rd.split('\n')
for row in rd:
    row = row.lower().rstrip('\t').split('\t')
    G.append_to_graph(row)

# print("-----------------------DEV set ------------------------------")
for q in Dev_qlist:
    qa(q, G)

print("-----------------------Test set-------------------------------")
# for q in test_qlist:
#     qa(q, G)




# G.draw_graph()
# f.close()
