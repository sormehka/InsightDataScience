import csv
import pandas as pd
import sys
import numpy as np

def parse_input(batch_file, stream_file, batch_file_fixed, stream_file_fixed): # 1. The message column contains extra commas which complicates the import with separator ','. The files were fixed using split command and saved as new csv files\  
    with open(batch_file, 'rb') as b, open(batch_file_fixed, 'wb') as bb:
        writer = csv.writer(bb, delimiter=',')
        for line in b:
            row = line.split(',', 4)
            writer.writerow(row)
    with open(stream_file, 'rb') as s, open(stream_file_fixed, 'wb') as ss:
        writer = csv.writer(ss, delimiter=',')
        for line in s:
            row = line.split(',', 4)
            writer.writerow(row)

# 2. Defining a graph class
class Graph(object):
    def _init_(self):  # Initializing a graph object with an empty dictionary
        self._graph_dict={}

    def vertices(self):  # Returns the vertices of graph (list of graph dict keys)
        return list(self._graph_dict.keys())

    def add_vertex(self,vertex): # If vertex is not already defined, a key "vertex" with an empty set  will be added to the dictionary
        if vertex not in self._graph_dict:
            self._graph_dict[vertex]=set()
            
    def add_edge(self,vertex1,vertex2): # Adding edges to vertix dictionaries 
        if not vertex1 in self._graph_dict:
            self.add_vertex(vertex1)
        if not vertex2 in self._graph_dict:
            self.add_vertex(vertex2)
        self._graph_dict[vertex1].add(vertex2)
        self._graph_dict[vertex2].add(vertex1)

    def BFS(self, start, end, trusted_depth): #Breath Frist Search algorithm to find the path between two vetices, trusted_depth represents the degree of friends network
        gp=self._graph_dict
        if not start in gp: return None
        visited = {}
        for v in gp.keys():
            visited[v] = False
        my_queue = []
        distances = []
        my_queue.append(start)
        distances.append(0)
        while len(my_queue) > 0:
            current_item = my_queue.pop()
            current_distance = distances.pop()
            visited[current_item] = True
            if current_distance > trusted_depth:
                return False
            if current_item == end:
                return True
            for neighbor in gp[current_item]:
                if visited[neighbor]:
                    continue
                my_queue.insert(0, neighbor)
                distances.insert(0, current_distance+1)
        return False

# 3. Initializing the graph class, adding vertices and edges based on the batch_payment file
def main():
    if len(sys.argv) < 7:
        print "Input error: this code requires two input files,two temporary files, and 3 output file paths"
        sys.exit(1)
    batch_file = sys.argv[1]
    stream_file = sys.argv[2] 
    batch_file_fixed=sys.argv[3]
    stream_file_fixed=sys.argv[4]
    output1 = sys.argv[5]
    output2 = sys.argv[6]
    output3 = sys.argv[7]
    
    # 1.1 Parse input files
    parse_input(batch_file, stream_file, batch_file_fixed, stream_file_fixed)
    
    # 1.2. Reading and saving the two columns id1 and id2
    df=pd.read_csv(batch_file_fixed,usecols=[1,2]).as_matrix()
    df_out=pd.read_csv(stream_file_fixed,usecols=[1,2]).as_matrix()

    graph=Graph()

    graph._init_() 

    for i in range(0,len(df)):  
        graph.add_vertex(df[i][0]) 
        graph.add_vertex(df[i][1])
        graph.add_edge(df[i][0],df[i][1])

   #  4. Writing the outputs of three features to text files 
    with open(output1,"w") as out_text: #output1-Feature1 
        trusted_depth=1
        vertices_index=graph.vertices()
        trusted=np.zeros((len(vertices_index)+1,len(vertices_index)+1))
        for i in range(0,3000): #len(df_out)):
            if not df_out[i][0] in vertices_index or not df_out[i][1] in vertices_index:
                out_text.write("unverified\n") #if not in vertices, new costumer, unverified
            elif trusted[vertices_index.index(df_out[i][0])][vertices_index.index(df_out[i][1])]==1:
                out_text.write("trusted\n") #already labeled as trusted
            elif trusted[vertices_index.index(df_out[i][0])][vertices_index.index(df_out[i][1])]==2:
                out_text.write("unverified\n") #already labeled as unverified               
            elif not graph.BFS(df_out[i][0],df_out[i][1],trusted_depth):
                out_text.write("unverified\n") #new label as unverified
                trusted[vertices_index.index(df_out[i][0])][vertices_index.index(df_out[i][1])]=2
                trusted[vertices_index.index(df_out[i][1])][vertices_index.index(df_out[i][0])]=2
            else: #new label as trusted
                out_text.write("trusted\n")
                trusted[vertices_index.index(df_out[i][0])][vertices_index.index(df_out[i][1])]=1
                trusted[vertices_index.index(df_out[i][1])][vertices_index.index(df_out[i][0])]=1
                

    with open(output2,"w") as out_text: #output2-Feature2                                                                         
        trusted_depth=2
        #Trusted matrix from feature 1. The ones are still trusted.
        for i in range(0,50): #len(df_out)):
            if not df_out[i][0] in vertices_index or not df_out[i][1] in vertices_index:
                out_text.write("unverified\n")
                
            elif trusted[vertices_index.index(df_out[i][0])][vertices_index.index(df_out[i][1])]==1:
                out_text.write("trusted\n")
                
            elif trusted[vertices_index.index(df_out[i][0])][vertices_index.index(df_out[i][1])]==3:
                out_text.write("unverified\n")
                
            elif not graph.BFS(df_out[i][0],df_out[i][1],trusted_depth):
                out_text.write("unverified\n")
                trusted[vertices_index.index(df_out[i][0])][vertices_index.index(df_out[i][1])]=3
                trusted[vertices_index.index(df_out[i][1])][vertices_index.index(df_out[i][0])]=3
                
            else:
                out_text.write("trusted\n")
                trusted[vertices_index.index(df_out[i][0])][vertices_index.index(df_out[i][1])]=1
                trusted[vertices_index.index(df_out[i][1])][vertices_index.index(df_out[i][0])]=1
                
           
    with open(output3,"w") as out_text: #output3-Feature3                                                                      
        trusted_depth=4
        for i in range(0,10): #len(df_out)):
            if not df_out[i][0] in vertices_index or not df_out[i][1] in vertices_index:
                out_text.write("unverified\n")
                
            elif trusted[vertices_index.index(df_out[i][0])][vertices_index.index(df_out[i][1])]==1:
                out_text.write("trusted\n")
                
            elif trusted[vertices_index.index(df_out[i][0])][vertices_index.index(df_out[i][1])]==4:
                out_text.write("unverified\n")
                
            elif not graph.BFS(df_out[i][0],df_out[i][1],trusted_depth):
                out_text.write("unverified\n")
                trusted[vertices_index.index(df_out[i][0])][vertices_index.index(df_out[i][1])]=4
                trusted[vertices_index.index(df_out[i][1])][vertices_index.index(df_out[i][0])]=4
            else:
                out_text.write("trusted\n")
                trusted[vertices_index.index(df_out[i][0])][vertices_index.index(df_out[i][1])]=1
                trusted[vertices_index.index(df_out[i][1])][vertices_index.index(df_out[i][0])]=1
                

if __name__ == "__main__":
    main()
