import requests

def search_wikipedia(keyword):
    api_url = "http://zh.wikipedia.org/w/api.php?format=json&action=query&generator=search&gsrnamespace=0&gsrlimit=10&prop=pageimages|extracts&pilimit=max&exintro&explaintext&exsentences=3&exlimit=max&gsrsearch="
    wiki_base_url = 'https://zh.wikipedia.org/wiki/'
    response = requests.get(api_url+keyword)
    data = response.json()
    result = {}
    result['list'] = []
    for page in data['query']['pages'].keys():
        result['list'].append({'title':data['query']['pages'][page]['title'],'extract':data['query']['pages'][page]['extract'],'url':wiki_base_url+data['query']['pages'][page]['title']})
    return result

print(search_wikipedia('对称变换'))