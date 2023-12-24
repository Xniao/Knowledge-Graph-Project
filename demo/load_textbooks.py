import json
import os

def main():
    with open('..\\data\\textbooks.json', 'r', encoding='utf-8') as file:
        textbooks = json.load(file)
    for textbook in textbooks:
        print(textbook)
    pass

if __name__ == '__main__':
    main()