import dotenv
import os
from neo4j import GraphDatabase
import exportUtil
from rich.progress import track

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
dotenv.load_dotenv("Neo4j-48a6b976-Created-2023-12-18.txt")

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

def create_node(driver, entity):
    if entity.get("link"):
        query = f"CREATE (:{entity['label']} {{name:'{entity['name']}',link:'{entity['link']}'}})"
    else:
        query = f"CREATE (:{entity['label']} {{name:'{entity['name']}'}})"
    driver.execute_query(query, database_="neo4j")
    
    
def create_relation(driver, relation):
    query = \
    f"MATCH (e1:{relation['entity1']['label']} {{name: '{relation['entity1']['name']}'}})," + \
    f"(e2:{relation['entity2']['label']} {{name: '{relation['entity2']['name']}'}}) " + \
    f"CREATE (e1) - [:{relation['label']} {{isDirect: {relation['isDirect']}}}] -> (e2)"
    # print(query)
    driver.execute_query(query, database_="neo4j")

    
def create_all_nodes(driver):
    entities = exportUtil.load_entities()
    for entity in track(entities, description="Creating nodes..."):
        print(entity['name'])
        create_node(driver, entity)
  
  
def create_all_relations(driver):
    relations = exportUtil.load_relations()
    for relation in track(relations, description="Creating relations..."):
        print(relation['entity1']['name'], relation['label'] ,relation['entity2']['name'])
        create_relation(driver, relation)

    
if __name__ == "__main__":
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        # create_all_nodes(driver)
        create_all_relations(driver)
