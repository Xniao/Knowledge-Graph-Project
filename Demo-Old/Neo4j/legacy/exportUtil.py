import json

IMPORT_FILE_PATH = "E:/Programming/KnowledgeGraphProject/Entity/topic.json"
ENTITY_RESULT_FILE_PATH = "E:/Programming/KnowledgeGraphProject/Neo4j/entity.json"
RELATION_RESULT_FILE_PATH = "E:/Programming/KnowledgeGraphProject/Neo4j/relation.json"

def load_topic():
    with open(IMPORT_FILE_PATH, 'r', encoding="utf8") as file:
        return json.load(file)


def load_entities():
    with open(ENTITY_RESULT_FILE_PATH, 'r', encoding="utf8") as file:
        return json.load(file)
    
def load_relations():
    with open(RELATION_RESULT_FILE_PATH, 'r', encoding="utf8") as file:
        return json.load(file)

def dfs_topic(topic: dict):
    if topic == None:
        return []
    result = []
    result.append(dict(
        name=topic['subject'],
        link=topic['link'],
        label=topic['label']
    ))
    if topic.get("items"):
        for item in topic.get("items"):
            result.extend(dfs_topic(item))
    if topic.get("contents"):
        for content in topic.get("contents"):
            result.append(dict(
                name=content,
                label="知识点" 
            ))
    return result


def export_entities():
    topics = load_topic()
    entities = []
    for topic in topics:
        entities.extend(dfs_topic(topic))
    with open(ENTITY_RESULT_FILE_PATH, 'w', encoding='utf8') as file:
        json.dump(entities, file, indent=2, ensure_ascii=False)
    print(len(entities))


def get_children(root: dict):
    if root == None:
        return []
    result = []
    if root.get('items'):
        for item in root['items']:
            result.append(dict(
                subject=item['subject'],
                label=item['label']
            ))
            result.extend(get_children(item))
    if root.get('contents'):
        contents = [dict(subject=content,label="知识点") 
                    for content in root['contents']]
        result.extend(contents)
    return result


def dfs_relation(root: dict):
    # Create relation for the root and its children.
    if root == None:
        return []
    relations = []
    children = get_children(root)
    for child in children:
        relation1 = dict(
            label="包含",
        )
        relation2 = dict(
            label="属于",
        )
        entity1 = dict(
            name=root['subject'],
            label=root['label']
        )
        entity2 = dict(
            name=child['subject'],
            label=child['label'],
        )
        relation1['entity1'] = entity1
        relation1['entity2'] = entity2
        relation2['entity1'] = entity2
        relation2['entity2'] = entity1
        isDirect = False
        if root.get('items'):
            isDirect = child['subject'] in {item['subject'] for item in root.get('items')}
        if root.get('contents'):
            isDirect = isDirect or child['subject'] in root.get('contents')
        relation1['isDirect'] = isDirect
        relation2['isDirect'] = isDirect
        relations.append(relation1)
        relations.append(relation2)
        relations.extend(dfs_relation(child))
    return relations

# Basic contains and belong relationship
def export_simple_relations():
    topics = load_topic()
    relations = []
    for topic in topics:
        relations.extend(dfs_relation(topic))
    print(relations)
    with open(RELATION_RESULT_FILE_PATH, 'w', encoding='utf8') as file:
        json.dump(relations, file, indent=2, ensure_ascii=False)


def main():

    pass


if __name__ == "__main__":
    export_simple_relations()
