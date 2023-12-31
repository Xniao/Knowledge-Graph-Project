import dotenv
import os
from neo4j import GraphDatabase
from rich.progress import track
import json


dotenv.load_dotenv("./Neo4j.txt")

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

ENTITY_RESULT_FILE_PATH = "./data/node.json"
RELATION_RESULT_FILE_PATH = "./data/relation.json"

def load_entities():
    with open(ENTITY_RESULT_FILE_PATH, 'r', encoding="utf8") as file:
        return json.load(file)

def load_relations():
    with open(RELATION_RESULT_FILE_PATH, 'r', encoding="utf8") as file:
        return json.load(file)

def create_node(driver, entity):
    query = f"CREATE (:{entity['label']} {{name:'{entity['name']}', nid:{int(entity['nid'])}}})"
    # print(query)
    driver.execute_query(query, database_="neo4j")
    
    
def create_relation(driver, relation, source_nid, target_nid):
    # query = \
    # f"MATCH (e1:{relation['entity1']['label']} {{name: '{relation['entity1']['name']}'}})," + \
    # f"(e2:{relation['entity2']['label']} {{name: '{relation['entity2']['name']}'}}) " + \
    # f"CREATE (e1) - [:{relation['label']} {{isDirect: {relation['isDirect']}}}] -> (e2)"
    query = \
    f"MATCH (e1:% {{nid: {source_nid}}})," + \
    f"(e2:% {{nid: {target_nid}}}) " + \
    f"CREATE (e1) - [:{relation['label']} {{rid: {relation['rid']}}}] -> (e2)"
    print(query)
    driver.execute_query(query, database_="neo4j")

    
def create_all_nodes(driver):
    entities = load_entities()
    for entity in track(entities, description="Creating nodes..."):
        print(entity['name'])
        create_node(driver, entity)
  
def handle_nodes_relations():
    nodes = load_entities()
    res = dict()
    for node in nodes:
        res[node['nid']] = {
            "label": node['label'],
            "name": node['name'],
            "id": node['nid']
        }
    return res
  
def create_all_relations(driver):
    filter_nodes = handle_nodes_relations()
    relations = load_relations()
    for relation in track(relations, description="Creating relations..."):
        source_node, target_node = filter_nodes[relation['src_id']], filter_nodes[relation['target_id']]
        print(source_node['name'], relation['label'] ,target_node['name'])
        create_relation(driver, relation, relation['src_id'], relation['target_id'])

    
if __name__ == "__main__":
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        create_all_nodes(driver)
        create_all_relations(driver)
