
import json
import requests
from bs4 import BeautifulSoup

#Example Plugin
def run(parameters):
    try:
        # Load Parameters
        query = parameters.get('query')
        max_results = parameters.get('max_results', 5)
        timeout = parameters.get('timeout', 90)
        
        # Logic Goes Here
        response = requests.get('https://www.google.com/search?q=' + query, timeout=timeout)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for link in soup.find_all('a')[:max_results]: # Truncate the response to the first 5 links
            links.append(link.get('href'))
        
        # Return Status
        return json.dumps(links)
    except Exception as e:
        return "The assistant timed out: " + str(e)