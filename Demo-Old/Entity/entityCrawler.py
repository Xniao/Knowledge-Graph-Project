from bs4 import BeautifulSoup as Soup
import requests
import os
import json
import re

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

KB_URL = "https://kb.kmath.cn/kbase/"
TOPIC_RESULT_FILE_PATH = "./topic.json"
ENTITY_RESULT_FILE_PATH = "./entity.json"
COUNT = 0
FILTER_WORDS = set(
    ['定义', '性质', '记忆技巧', '引入',
     '意义', '证明', '总结', '求法', '推广1',
     '推广', '应用','例题', '牛刀小试']
)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0'
}

def get_soup_object(target_url):
    response = requests.get(target_url, headers=HEADERS)
    assert response.status_code == 200
    return Soup(response.text, "html.parser", from_encoding="utf-8")


def get_topic_titles(topic_url):
    soup = soup = get_soup_object(topic_url)
    # Find title in markdown text
    markdown_text = soup.select_one("textarea")
    if markdown_text == None:
        return []
    titles = [re.sub(r"#+", '', title).strip()
              for title in markdown_text.text.split("\n") 
              if title.startswith("#")]
    titles = [title for title in titles if title not in FILTER_WORDS]
    global COUNT
    COUNT += len(titles)
    # for title in titles:
    #     print(title)
    return titles


def dfs_topic(topic, level):
    if topic == None:
        return None
    subject = topic.find_next('a')
    parent = subject.parent
    subject_link = KB_URL + subject['href']
    global COUNT
    COUNT += 1
    print('\t' * level, subject.text, subject_link)
    result = dict(
        subject=subject.text,
        link=subject_link,
        # By default
        label="知识点"
    )
    contents = get_topic_titles(subject_link)
    if len(contents) > 0:
        result['contents'] = contents
        result['label'] = "专题"
    # This topic is a topic
    if parent.has_attr('class'):
        items = topic.find_next(class_="items")
        result['label'] = "专题"
        if items: 
            result['items'] = []
            for item in items:
                result['items'].append(dfs_topic(item, level+1))    
    return result


def crawl_topics():
    soup = get_soup_object(KB_URL)
    # Search the high school math part
    topics = soup.select("#ctl00_body_lbl1 > .kb") + soup.select("#ctl00_body_lbl2 > .kb")
    result = []
    [result.append(dfs_topic(topic,0)) for topic in topics]
    print(COUNT)
    with open(TOPIC_RESULT_FILE_PATH, 'w', encoding='utf8') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)


def dfs_entity(topic: dict):
    result = []
    if topic == None:
        return result
    result.append(topic['subject'])
    if topic.get('contents'):
        result.extend(topic['contents'])
    if topic.get('items'):
        items = topic['items']
        [result.extend(dfs_entity(item)) for item in items]
    return result


def get_entity():
    topics = []
    entities = []
    with open(TOPIC_RESULT_FILE_PATH, 'r', encoding='utf8') as file: 
        topics = json.load(file)
    for topic in topics:
        entities.extend(dfs_entity(topic))
    print(entities)
    with open(ENTITY_RESULT_FILE_PATH, 'w', encoding='utf8') as file:
        json.dump(entities, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # get_topic_titles("https://kb.kmath.cn/kbase/detail.aspx?id=90")
    crawl_topics()
    get_entity()
