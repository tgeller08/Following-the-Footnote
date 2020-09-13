import pandas as pd

nodes = ["Gordie","Sarah","Davida","Talya"]

def merge(list1, list2): 
      
    merged_list = tuple(zip(list1, list2))  
    return merged_list 
       

indices = []
i = 0
for x in nodes:
	indices.append(i)
	i+=1

foo2 = merge(indices, nodes)

print(foo2)

foo3 = list(foo2)


df_nodes = pd.DataFrame(foo3, columns = ['ID','Author'])


print(df_nodes)

df = df_nodes.rename(columns={'ID': 'SOURCE', 'Author': 'Target'})

print(df)




'''

edge1 = {

"START_AUTHOR_INDEX": 5, 
"START_TITLE": 5, 
"END_AUTHOR_INDEX": 5, 
"END_TITLE": 5

}

edge2 = {

"START_AUTHOR_INDEX": 5, 
"START_TITLE": 5, 
"END_AUTHOR_INDEX": 5, 
"END_TITLE": 5

}

edges = [edge1, edge2]



foo = []

for edge in edges:
	foo1 = []
	for x in edge:
		foo1.append(edge[x])
	foo.append(foo1)

	
df_edges = pd.DataFrame(foo, columns = ['START_AUTHOR_INDEX','START_TITLE','END_AUTHOR_INDEX','END_TITLE'])

print(df_edges)
'''






