import json
import os

COUNT = 0

def dfs(node):
    global COUNT
    if node == None:
        return
    if type(node) == str:
        COUNT += 1
        print(node)
        return
    COUNT += 1
    print(node['name'])
    for item in node['items']:
        dfs(item)

def main():
    with open('..\\data\\textbooks.json', 'r', encoding='utf-8') as file:
        textbooks = json.load(file)
    for textbook in textbooks:
        dfs(textbook)
    global COUNT
    print(COUNT)

if __name__ == '__main__':
    main()