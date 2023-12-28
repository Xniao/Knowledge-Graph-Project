import dotenv
import os
from os.path import exists
from neo4j import GraphDatabase
from rich.progress import track
import json, jieba
from flask import Flask, redirect
dotenv.load_dotenv("/home/hyl/paper/tmp/Knowledge-Graph-Project/Demo-Old/Neo4j/Neo4j-48a6b976-Created-2023-12-18.txt")

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

ENTITY_RESULT_FILE_PATH = "/home/hyl/paper/tmp/Knowledge-Graph-Project/data/node.json"
RELATION_RESULT_FILE_PATH = "/home/hyl/paper/tmp/Knowledge-Graph-Project/data/relation.json"

# 导入自定义词表
def save_and_load_worddict():
    if not exists('/home/hyl/paper/tmp/Knowledge-Graph-Project/words.txt'):	
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

        with open('/home/hyl/paper/tmp/Knowledge-Graph-Project/words.txt', 'w', encoding='utf-8') as f:
            for k, v in word_dic.items():
                f.write(k + ' ' + str(v) + '\n')
    jieba.load_userdict('/home/hyl/paper/tmp/Knowledge-Graph-Project/words.txt')

def pre_handle_search():
    pass

def search(driver, query):
    seg_list = jieba.lcut(query)
    print(query)
    for entity in seg_list:
        # 此条语句查询该node的所有子节点 - 直接关系
        send_q1 = f'MATCH (a:% {{name:"{entity}"}}) - [r:{"包含"}] -> (b) RETURN a,r, b'
        # print(send_q1)
        ans = driver.execute_query(send_q1, database_="neo4j")
        # 此条语句查询该node的所有父节点 - 直接关系
        send_q2 = f'MATCH (a) - [r:{"包含"}] -> (b:% {{name:"{entity}"}}) RETURN a,r, b'
        # print(send_q2)
        ans = driver.execute_query(send_q2, database_="neo4j")
 

# 创建应用实例
app = Flask(__name__)
# 视图函数（路由）
@app.route('/user/<username>')
def say_hello(username):
	# return '<h1>Hello %s !<h1>' % username
	return redirect('https://www.baidu.com')



# 启动实施（只在当前模块运行）
if __name__ == '__main__':
    save_and_load_worddict()
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        search(driver, '常用逻辑用语')
