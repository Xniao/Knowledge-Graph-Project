from bs4 import BeautifulSoup as Soup
import requests
import os
import json

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

KB_URL = "https://kb.kmath.cn/kbase/"
RESULT_FILE_PATH = "./topic.json"
COUNT = 0


def dfs_topic(topic, level):
    if topic == None:
        return None
    subject = topic.find_next('a')
    parent = subject.parent
    print('\t' * level, subject.text, KB_URL + subject['href'])
    global COUNT
    COUNT += 1
    result = dict(
        subject=subject.text,
        link=KB_URL + subject['href']
    )
    # Is a topic
    if parent.has_attr('class'):
        # print(parent['class'])
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
    topics = soup.select("#ctl00_body_lbl2 > .kb")
    result = []
    global COUNT
    for topic in topics:
        subject = topic.find_next(class_="subject").find_next('a')
        print(subject.text, KB_URL + subject['href'])
        COUNT += 1
        topic_result = dict(
            subject=subject.text,
            link=KB_URL + subject['href']
        )
        items = topic.find_next(class_="items")
        if items:
            topic_result['items'] = []
            for item in items:
                topic_result['items'].append(dfs_topic(item, 1))
        result.append(topic_result)
    print(result)
    print(COUNT)
    with open(RESULT_FILE_PATH, 'w', encoding='utf8') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
