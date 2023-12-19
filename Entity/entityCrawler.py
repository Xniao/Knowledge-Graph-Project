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

def get_topic_titles(topic_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0'
    }
    response = requests.get(topic_url, headers=headers)
    assert response.status_code == 200
    html_doc = response.text
    soup = Soup(html_doc, "html.parser", from_encoding="utf-8")
    # All title
    markdown_text = soup.select_one("textarea")
    if markdown_text == None:
        return []
    titles = [re.sub(r"#+", '', title).strip()
              for title in markdown_text.text.split("\n") 
              if title.startswith("#")]
    titles = [title for title in titles if title not in FILTER_WORDS]
    global COUNT
    COUNT += len(titles)
    for title in titles:
        print(title)
    return titles


def dfs_topic(topic, level):
    if topic == None:
        return None
    subject = topic.find_next('a')
    parent = subject.parent
    subject_link = KB_URL + subject['href']
    global COUNT
    COUNT += 1
    # print('\t' * level, subject.text, subject_link)
    result = dict(
        subject=subject.text,
        link=subject_link,
    )
    contents = get_topic_titles(subject_link)
    if len(contents) > 0:
        result['contents'] = contents
    if parent.has_attr('class'):
        items = topic.find_next(class_="items")
        if items: 
            result['items'] = []
            for item in items:
                result['items'].append(dfs_topic(item, level+1))
    return result


def main():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0'
    }
    response = requests.get(KB_URL, headers=headers)
    assert response.status_code == 200
    html_doc = response.text
    soup = Soup(html_doc, "html.parser", from_encoding="utf-8")
    # Search the high school math part
    topics = soup.select("#ctl00_body_lbl1 > .kb") + soup.select("#ctl00_body_lbl2 > .kb")
    result = []
    for topic in topics:
        subject = topic.find_next(class_="subject").find_next('a')
        subject_link = KB_URL + subject['href']
        global COUNT
        COUNT += 1
        # print(subject.text, KB_URL + subject['href'])
        topic_result = dict(
            subject=subject.text,
            link=subject_link,
        )
        contents = get_topic_titles(subject_link)
        if len(contents) > 0:
            topic_result['contents'] = contents
        items = topic.find_next(class_="items")
        if items:
            topic_result['items'] = []
            for item in items:
                topic_result['items'].append(dfs_topic(item, 1))
        result.append(topic_result)
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
        for item in items:
          result.extend(dfs_entity(item))  
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
    get_entity()
