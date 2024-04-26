from googlesearch import search
import requests
from bs4 import BeautifulSoup
import html_to_json
import ollama

def extract_content_specific_text(html_string):
    # BeautifulSoup-Objekt erstellen
    soup = BeautifulSoup(html_string, 'html.parser')
    
    # Tags, die normalerweise Content-spezifische Informationen enthalten
    content_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'span']
    
    # Extrahiere Text aus den Content-spezifischen Tags
    content_texts = [tag.get_text(separator='|') for tag in soup.find_all(content_tags)]
    for x in content_texts:
        if x in [' ','  ','   ', '    ']:
            content_texts.remove(x)

    
    # Kombiniere alle extrahierten Texte zu einem einzigen Text
    content_text = ' '.join(content_texts)
    
    return content_text


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
    num_results = 5
    search_results = google_search(query, num_results)
    for i, result in enumerate(search_results, start=1):
        response = requests.get(result, headers=headers)

        #output = html_to_json.convert(extract_content_specific_text(response.text))
        data= extract_content_specific_text(response.text)

    return data


def llama(prompt):
    response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': f'Use these Internet-Results to answer: {searcher(prompt)}, Respond in question language.',
                'role': 'user',
                'content': f'{prompt}'
            },
            ])

    output = response['message']['content']
    print(output)

llama("Was für ein Tag ist heute?")


