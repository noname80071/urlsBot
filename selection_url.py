import requests

def selection_urls(file_name):
    with open('urls.txt') as f:
        for url in f:
            print(url)
            check = requests.head(url)
            print(check.status_code)
            if check.status_code != 200:
