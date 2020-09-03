__name__ == "graph_op"

import networkx as nx
import matplotlib.pyplot as plt
import spacy
import gensim
from gensim.models import Word2Vec, FastText
import nltk
from nltk.corpus import stopwords

all_stopwords = stopwords.words("english")
nlp = spacy.load("en_core_web_sm")
model = gensim.models.KeyedVectors.load_word2vec_format('programming-assignment/model.bin')
# model = gensim.models.KeyedVectors.load_word2vec_format('model.bin')



class Query:
    def __init__(self, text):
        self.q = text
    
    def get_entity(self):
        doc = nlp(self.q)
        for ent in doc.ents:
            return ent
    
    def get_relation(self, ent):
        text = self.q
        relation  = ""
        for w in str(ent).split(" "):
            text = text.replace(w,'')
        relation = " ".join(text.split(' ')[1:]).strip('?').strip(" ")
        return relation


class KG:

    def __init__(self):
        self.graph = nx.Graph()

    def append_to_graph(self, row):
        for i in range(0,len(row) - 2, 2):
            triple = (row[i], row[i+1], row[i+2])
            self.graph.add_node(row[i])
            self.graph.add_node(row[i+2])
            self.graph.add_edge(row[i],row[i+2], data = row[i+1])

    def draw_graph(self):
        print("plotted")
        pos = nx.spring_layout(self.graph,scale=0.001)
        nx.draw(self.graph,pos,font_size=0.001)
        plt.plot()
    
    def remove(self):
        self.graph.clear()

    def get_node_relation(self, node):
        return list(self.graph.edges(str(node), data=True))

    def get_similar_triple(self, query_relation, kg_triple_list):
        vocab = model.vocab.keys()
        similarity_max = 0
        triple_max = None
        for triple in kg_triple_list:
            relation = triple[2].get('data', ' ')
            relation = relation.split(" ") if ' ' in relation else [relation]
            relation = [w for w in relation if w in vocab and (w not in all_stopwords)]
            query =  [w for w in query_relation.split(" ") if (w in vocab) and (w not in all_stopwords)]
            similarity = model.wv.n_similarity(relation, query) if relation and query else 0
            if similarity > similarity_max:
                similarity_max = similarity
                triple_max = triple
        return (triple_max, similarity_max)
        
    def get_object(self, node, triple):
        for item in triple:
            if str(node) != item and type(item) != dict:
                return item

    def node_disambiguation(self, ent):
        nodes = self.graph.nodes
        node_list = []
        query_entity = str(ent)
        for node in self.graph.nodes:
            if len(node.split(" ")) == 2 and node.split(" ")[1] == query_entity:
                node_list.append(node)
        if len(node_list) == 0:
            node_list.append(query_entity)
        # print(node_list)
        return node_list