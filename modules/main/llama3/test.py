from googlesearch import search
import requests
from bs4 import BeautifulSoup
import html_to_json
import ollama



def searcher(query):
    def google_search(query, num_results=5):
        results = []
        for result in search(query, num_results=num_results):
            results.append(result)
        return results

    data = {}
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


    # Beispielverwendung:
    query = "Wetter kaiserslautern"
    num_results = 5
    search_results = google_search(query, num_results)
    for i, result in enumerate(search_results, start=1):
        response = requests.get(result, headers=headers)
        output = html_to_json.convert(response.text)
        data[result] = output

    return data


def llama(prompt):
    response = ollama.chat(model='llama3', messages=[
            {
                'role': 'system',
                'content': f'{searcher(prompt)}',
                'role': 'user',
                'content': f'{prompt}'
            },
            ])

    output = response['message']['content']
    print(output)

llama("Wie ist das Wetter in kaiserslautern?")


