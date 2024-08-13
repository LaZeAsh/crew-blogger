from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup
import cohere 
import os

class ResearchLink(BaseTool):
    name: str = "Endpoint Researcher"
    description: str = (
        "Research the given Cohere endpoint and provide a 10 bullet point summary of what it does"
    )

    def _run(self, link: str) -> str:
        co = cohere.Client(os.environ['COHERE'])
        response = requests.get(link)
        text = ""
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            text = soup.get_text(separator='\n')

        else:
            return "Failed to retrieve website"
        
        result = co.chat(
            message=f"Summarize this API endpoint usage into 10 bulletpoints max {text}"
        )

        return result
