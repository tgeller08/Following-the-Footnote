from refextract import extract_references_from_url #IMPORT REFERENCE EXTRACTING PACKAGE
import urllib #import urllib to parse queries for url use
import re #IMPORT REGEX PACKAGE FOR Y/N INPUT
from googlesearch import search #google search python package
import webbrowser #package that opens webpages for review
import os #import os package for file_paths
import pandas as pd


nodes = [] #DECLARE GLOBALS FOR GRAPH STORAGE
edges = []

def main(): #MAIN FUNCTION (IMPLEMENTED)
    start_author = "C. F. von Weizsacker" #PROVIDE INFORMATION OF THE FIRST SOURCE
    start_title = "The Structure of Physics"
    add_node(parse(start_author), start_title, True) #add initial node
    start_url = "http://library.uc.edu.kh/userfiles/pdf/41.The%20structure%20of%20physics.pdf"
    explore_references(start_url, parse(start_author), start_title) #Start exploring!
    terminate() #once done exploring as far as desired write graph to outfile

def explore_references(url, author, title): #RECURSIVE REFERENCE EXPLORATION FUNCTION (IMPLEMENTED)
    references = extract_references_from_url(url) #get references from url
    reverse = reversed(references) #initialize reversed copy of references to iterate over
    original_length = len(references) #store number of references for deletion
    i = 0 #initialize counter variable i to keep track of current index in reverse

    for reference in reverse: #iterate over reversed reference list
        if not 'author' in list(reference.keys()): #if the reference has no offer (invalid)
            del references[original_length - 1 - i] #remove that reference (notice reverse not changed)
        i += 1 #increment i
    for reference in references: #for each valid reference
        true_author = parse(reference['author'][0]) #parse the author
        next_title = get_title(reference) #get title of reference
        add_node(true_author, next_title, False) #add new node for that reference's author
        add_edge(nodes.index(next(node for node in nodes if node["Label"] == author)), nodes.index(next(node for node in nodes if node["Label"] == true_author))) #add edge from current node to this reference's new node
    cont = get_yes_no("Explore all valid references?") #get yes no input for whether program should continue down tree
    if cont: #if user says program should continue down tree
        for reference in references: #for each valid reference
            true_author = parse(reference['author'][0]) #parse the author
            next_title = get_title(reference) #get title of reference
            q = get_queries(reference) #Store list of search queries associated with reference
            new_url = find_pdf(q) #Get a pdf url from the list of queries (google search and web scrape)
            if new_url != "FAILURE":
                explore_references(new_url, true_author, next_title) #explore new pdf if found
            else:
                print("NO PDF FOUND FOR THIS DOCUMENT, MOVING ON") #
        return #once done exploring all the references as far as desired end the function
    else: #if shouldn't continue further down tree
        return #done exploring that node

def get_queries(reference): #GET LIST OF SEARCH QUERIES FROM REFERENCE KEY VALUE PAIRS (TODO)
    queries = [reference['raw_ref'][0] + ' .pdf', reference['raw_ref'][0] + reference['author'][0] + ' .pdf'] #the whole reference + .pdf, and the whole reference w the author again + .pdf
    #TODO implement function that generates list of good queries from the reference key value pairs
    #Experiment on google and see what works
    return queries

def find_pdf(queries): #GET PDF URL FROM LIST OF QUERIES (TODO)
    for query in queries: #for each query in the list
        print(query)
        q = urllib.parse.quote_plus(query) #parse the query
        results = search(q, tld="com", num=10, stop=10, pause=2)
        for j in results: #get 10 results (have to wait 2 secs between each search so no block)
            print(j)
            if ".pdf" in j[-4:]: #if the last 4 chars are .pdf
                webbrowser.open(j) #open the page in the browser
                done = get_yes_no("Is this what you're looking for?") #ask the user if this is the right thing
                if done: #if they say yes return that url
                    return j
    return "FAILURE" #if no url approved then return failure, no pdf found for this doc, sample change

def get_title(reference): #GET TITLE OF ARTICLE FROM REFERENCE KEY VALUE PAIRS (TODO)
    title = reference['raw_ref'][0]
    #TODO Implement function that gets titles from references for edges
    #NOTE: Title doesn't have to be actual title just some sort of identifying info
    return title

def add_node(author, title, is_root): #ADD NODE TO LIST (IMPLEMENTED)
    #EXAMPLE_NODE {"ID": 0, "Label": "Ben", "titles": [{"title": "Ben's Atrocious Neuroimaging Paper", "citations": 1}, {"title": Ben's Sad Sad Spanish Paper", "citations": 0}]}
    for node in nodes: #for each node
        if node["Label"] == author: #if the author already as a node
            for title_ in node["titles"]:
                if title_["title"] == title:
                    title_["citations"] = title_["citations"] + 1
                    return
            node["titles"].append({"title": title, "citations": 1})
            return
    if is_root:
        nodes.append({"ID": len(nodes), "Label": author, "titles": [{"title": title, "citations": 0}]}) #otherwise append new node for author to the node list
    else:
        nodes.append({"ID": len(nodes), "Label": author, "titles": [{"title": title, "citations": 1}]}) #otherwise append new node for author to the node list

def add_edge(start_author_index, end_author_index): #ADD EDGE TO LIST (IMPLEMENTED)
    for edge in edges:
        if edge["Source"] == start_author_index and edge["Target"] == end_author_index:
            edge["Weight"] = edge["Weight"] + 1
            return
    new_edge = {"Source": start_author_index, "Target": end_author_index, "Weight": 1}
    edges.append(new_edge) #Add edge to the list

def get_yes_no(question): #FUNCTION THAT GETS YES/NO INPUT FROM USER AND RETURNS BOOL (IMPLEMENTED)
    str = input(f"{question} (y/n) ") #get input from user in terminal
    if re.search("^y(es)?$", str, re.IGNORECASE): #if it's Y, y, Yes, or yes return true
        return True
    elif re.search("^no?$", str, re.IGNORECASE): #if it's N, n, No, or no return false
        return False
    elif re.search("^q(uit)?$", str, re.IGNORECASE): #q, Q, quit, Quit
        terminate()
    else: #otherwise run function again to get valid yes/no input
        return get_yes_no(question)

def parse(reference_author): #FUNCTION THAT FORMATS AUTHOR FROM REFERENCES CONSISTENTLY (TODO)
    true_author = reference_author
    #TODO Authors may appear differently in different explore_references
    #Parse the author appearing in the reference so no author gets multiple nodes
    return true_author


def terminate(): #FUNCTION THAT WRITES GRAPH TO OUTFILE THEN EXITS PROGRAM (TODO)

    gephi_ready_nodes = [node.values() for node in nodes] #get the values for each node
    cols = nodes[0].keys() #get the keys for each node (headers in csv)

    df_nodes = pd.DataFrame(gephi_ready_nodes, columns = cols) #Make a dataframe with node data
    print(df_nodes)
    cwd = os.getcwd()
    df_nodes.to_csv(f'{cwd}/nodes.csv', index = False)

    #EDGES OUTFILE STUFF
    gephi_ready_edges = [edge.values() for edge in edges]
    edge_cols = edges[0].keys()


    df_edges = pd.DataFrame(gephi_ready_edges, columns = edge_cols)
    df_edges.to_csv(f'{cwd}/edges.csv', index = False)



    exit(0) #exit success

main()
