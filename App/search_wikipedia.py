import requests

def search_wikipedia(keyword):
    api_url = "http://zh.wikipedia.org/w/api.php?format=json&action=query&generator=search&gsrnamespace=0&gsrlimit=10&prop=pageimages|extracts&pilimit=max&exintro&explaintext&exsentences=3&exlimit=max&gsrsearch="
    wiki_base_url = 'https://zh.wikipedia.org/wiki/'
    response = requests.get(api_url+keyword)
    data = response.json()
    list = []
    for page in data['query']['pages'].keys():
        list.append({'title':data['query']['pages'][page]['title'],'extract':data['query']['pages'][page]['extract'],'url':wiki_base_url+data['query']['pages'][page]['title']})
    return list