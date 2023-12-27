import markdown2
from bs4 import BeautifulSoup
import json
import os

#全局节点id号
node_id = 1

#全局关系id号
relation_id = 1

#教科书名称
textbook = {}
#当前标题名，分三级一个一个读取，第三级可能没有
current_h1 = {}
current_h2 = {}
current_h3 = {}

#节点列表
node=[]

#关系列表
relation = []
# 解析Markdown文本
markdown_text = ""

markdown_list = os.listdir("data")

for md in markdown_list: 
    with open("data/"+md,"r",encoding='utf-8') as f:
        markdown_text = f.read();
    print(md)
    html = markdown2.markdown(markdown_text)
    soup = BeautifulSoup(html, "html.parser")
    textbook = {}
    current_h1 = {}
    current_h2 = {}
    current_h3 = {}
    for item in soup.children:
        #先确定是否有textbook，没有则是第一个标签
        if textbook == {}:
            textbook = {'name':item.string,'id':node_id}
            #添加节点
            node.append({'label':'教科书','nid':node_id,'name':textbook['name'],'grade':''})
            node_id = node_id + 1
            continue
        else:
            if item.name == 'h1':
                current_h1 = {}
                current_h2 = {}
                current_h3 = {}
                current_h1 = {'name':item.string[item.string.find(' ')+1:],'id':node_id}
                #添加节点
                node.append({'label':'章节','nid':node_id,'name':current_h1['name']})
                node_id = node_id + 1
                
                #添加关系
                relation.append({'label':'属于','src_id':current_h1['id'],'target_id':textbook['id'],'rid':relation_id})
                relation_id = relation_id + 1

                relation.append({'label':'包含','src_id':textbook['id'],'target_id':current_h1['id'],'rid':relation_id})
                relation_id = relation_id + 1
            elif item.name == 'h2':
                current_h3 = {}
                current_h2 = {'name':item.string[item.string.find(' ')+1:],'id':node_id}
                #添加节点
                node.append({'label':'专题','nid':node_id,'name':current_h2['name']})
                node_id = node_id + 1

                relation.append({'label':'属于','src_id':current_h2['id'],'target_id':current_h1['id'],'rid':relation_id})
                relation_id = relation_id + 1

                relation.append({'label':'包含','src_id':current_h1['id'],'target_id':current_h2['id'],'rid':relation_id})
                relation_id = relation_id + 1

                relation.append({'label':'间接属于','src_id':current_h2['id'],'target_id':textbook['id'],'rid':relation_id})
                relation_id = relation_id + 1

                relation.append({'label':'间接包含','src_id':textbook['id'],'target_id':current_h1['id'],'rid':relation_id})
                relation_id = relation_id + 1
            elif item.name == 'h3':
                current_h3 = {'name':item.string[item.string.find(' ')+1:],'id':node_id}
                #添加节点
                node.append({'label':'专题','nid':node_id,'name':current_h3['name']})
                node_id = node_id + 1

                relation.append({'label':'属于','src_id':current_h3['id'],'target_id':current_h2['id'],'rid':relation_id})
                relation_id = relation_id + 1

                relation.append({'label':'包含','src_id':current_h2['id'],'target_id':current_h3['id'],'rid':relation_id})
                relation_id = relation_id + 1

                relation.append({'label':'间接属于','src_id':current_h3['id'],'target_id':current_h1['id'],'rid':relation_id})
                relation_id = relation_id + 1

                relation.append({'label':'间接包含','src_id':current_h1['id'],'target_id':current_h3['id'],'rid':relation_id})
                relation_id = relation_id + 1

                relation.append({'label':'间接属于','src_id':current_h3['id'],'target_id':textbook['id'],'rid':relation_id})
                relation_id = relation_id + 1

                relation.append({'label':'间接包含','src_id':textbook['id'],'target_id':current_h3['id'],'rid':relation_id})
                relation_id = relation_id + 1
            elif item.name == 'ul':
                for k in item.children:
                    if(k.string == '\n'):
                        continue
                    id = node_id
                    node.append({'label':'知识点','nid':node_id,'name':k.string if k.string!=None else list(k.strings)[0][0:-1]})
                    node_id = node_id + 1

                    relation.append({'label':'间接属于','src_id':id,'target_id':textbook['id'],'rid':relation_id})
                    relation_id = relation_id + 1

                    relation.append({'label':'间接包含','src_id':textbook['id'],'target_id':id,'rid':relation_id})
                    relation_id = relation_id + 1

                    relation.append({'label':'间接属于','src_id':id,'target_id':current_h1['id'],'rid':relation_id})
                    relation_id = relation_id + 1

                    relation.append({'label':'间接包含','src_id':current_h1['id'],'target_id':id,'rid':relation_id})
                    relation_id = relation_id + 1

                    if current_h3 == {}:
                        relation.append({'label':'属于','src_id':id,'target_id':current_h2['id'],'rid':relation_id})
                        relation_id = relation_id + 1

                        relation.append({'label':'包含','src_id':current_h2['id'],'target_id':id,'rid':relation_id})
                        relation_id = relation_id + 1
                    else:
                        relation.append({'label':'属于','src_id':id,'target_id':current_h3['id'],'rid':relation_id})
                        relation_id = relation_id + 1

                        relation.append({'label':'包含','src_id':current_h3['id'],'target_id':id,'rid':relation_id})
                        relation_id = relation_id + 1

                        relation.append({'label':'间接属于','src_id':id,'target_id':current_h2['id'],'rid':relation_id})
                        relation_id = relation_id + 1

                        relation.append({'label':'间接包含','src_id':current_h2['id'],'target_id':id,'rid':relation_id})
                        relation_id = relation_id + 1

with open("node.json",'w',encoding='utf-8') as f:
  f.write(json.dumps(node, ensure_ascii=False, indent=2))

with open("relation.json",'w',encoding='utf-8') as f:
  f.write(json.dumps(relation, ensure_ascii=False, indent=2))