import dotenv
import os
from os.path import exists
from neo4j import GraphDatabase
from rich.progress import track
import json, jieba
from flask import Flask, redirect
from search_wikipedia import search_wikipedia

dotenv.load_dotenv("../Demo-Old/Neo4j/Neo4j-48a6b976-Created-2023-12-18.txt")
URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

ENTITY_RESULT_FILE_PATH = "../data/node.json"
RELATION_RESULT_FILE_PATH = "../data/relation.json"
WORDS_TEXT_FILE_PATH = "../data/words.txt"

# 导入自定义词表
def save_and_load_worddict():
    if not exists(WORDS_TEXT_FILE_PATH):	
        word_dic = {}
        with open(ENTITY_RESULT_FILE_PATH, 'r', encoding="utf8") as f:
            nodes = json.load(f)
            
        with open(ENTITY_RESULT_FILE_PATH, 'r', encoding="utf8") as f:
            relations = json.load(f)

        for node in nodes:
            if node['label'] in word_dic:
                word_dic[node['label']] += 1
            else:
                word_dic[node['label']] = 1

            if node['name'] in word_dic:
                word_dic[node['name']] += 1
            else:
                word_dic[node['name']] = 1

        for relation in relations:
            if relation['label'] in word_dic:
                word_dic[relation['label']] += 1
            else:
                word_dic[relation['label']] = 1

        with open(WORDS_TEXT_FILE_PATH, 'w', encoding='utf-8') as f:
            for k, v in word_dic.items():
                f.write(k + ' ' + str(v) + '\n')
    jieba.load_userdict(WORDS_TEXT_FILE_PATH)

def pre_handle_search():
    pass

# 定义排序函数，以r列表的长度为关键字
def sort_key(record):
    return len(record['r'])



def post_handle_result(records):
    # 按照r列表的长度从大到小进行排序
    sorted_records = sorted(records, key=sort_key, reverse=True)
    # print(sorted_records)
    res_dict = {
        "textbook": None,
        "chapter": None,
        "special1": None,
        "special2": None, 
        "knowledge-topic": None
    }
    chinese2eng_dict = {
        "知识点": "knowledge-topic",
        "章节": "chapter",
        "专题": "special",
        "教科书": "textbook"
    }
    
    for rn in sorted_records:
        node_label = list(rn['a'].labels)[0]
        node_name = rn['a']['name']
        
        if node_label not in "专题":
            res_dict[chinese2eng_dict[node_label]] = node_name
        else:
            if res_dict["special1"] is None:
                res_dict['special1'] = node_name
            else:
                res_dict['special2'] = node_name
    last_b_label = list(sorted_records[-1]['b'].labels)[0]
    last_b_name = sorted_records[-1]['b']['name']
    if last_b_label not in "专题":
        res_dict[chinese2eng_dict[last_b_label]] = last_b_name
    else:
        if res_dict["special1"] is None:
            res_dict['special1'] = last_b_name
        else:
            res_dict['special2'] = last_b_name
    return res_dict

def search(query):
    save_and_load_worddict()
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
    seg_list = jieba.lcut(query)
    result = []
    for entity in seg_list:
        print(entity)
        # 此条语句查询该node的所有子节点 - 直接关系
        # send_q1 = f'MATCH (a:% {{name:"{entity}"}}) - [r:{"包含"}] -> (b) RETURN a,r, b'
        # print(send_q1)
        # ans = driver.execute_query(send_q1, database_="neo4j")
        # print(ans)
        # 此条语句查询该node的所有父节点 - 包含关系

        #判断实体是否不是教科书, False表示是教科书，True表示不是教科书
        query_entity = driver.execute_query(f'MATCH (a{{name:"{entity}"}}) RETURN a', database_="neo4j")
        flag = False
        if len(query_entity[0]) == 0:
            continue
        for q in query_entity[0]:
            if list(q['a'].labels)[0] != '教科书':
                flag = True
                break
        if flag == True:
            send_q2 = f'MATCH (a) - [r:{"包含"} *1..10] -> (b:% {{name:"{entity}"}}) RETURN a,r, b'
            print(send_q2)
            ans = driver.execute_query(send_q2, database_="neo4j")
            location = post_handle_result(ans[0])
            print(location)
            dict = {}
            dict['isTextbook'] = False
            location['level'] = 0
            for key in location.keys():
                if location[key] != None:
                    location['level'] =  location['level'] + 1
            dict['wikipedia'] = search_wikipedia(entity)
            dict['location'] = location
            dict['entity'] = entity
            result.append(dict)
        else:
            textbook = {}
            knowledge = []
            query_textbook = f'MATCH (a{{name:"{entity}"}}) RETURN a'
            result_textbook = driver.execute_query(query_textbook, database_="neo4j")
            textbook['nid'] = result_textbook[0][0]['a']['nid']
            textbook['name'] = result_textbook[0][0]['a']['name']
            textbook['num'] = 0
            textbook['label'] = '教科书'
            knowledge.append(textbook)
            index = 0
            while True:
                search = knowledge[index]['nid']
                if knowledge[index]['label'] == '知识点':
                    index = index + 1
                    if(index == len(knowledge)):
                        break
                    continue
                query = f'MATCH (a{{nid:{search}}}) - [r:{"包含"}] -> (b) RETURN b'
                result_query = driver.execute_query(query, database_="neo4j")
                for an in result_query[0]:
                    knowledge.append({'nid':an['b']['nid'],'name':an['b']['name'],'num':0,'label':list(an['b'].labels)[0]})
                    knowledge[index]['num'] = knowledge[index]['num'] + 1
                index = index + 1
                if(index == len(knowledge)):
                    break
            dict = {}
            dict['isTextbook'] = True
            dict['entity'] = entity
            dict['knowledge'] = knowledge
            result.append(dict)
    return json.dumps(result)