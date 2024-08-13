from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup
import cohere
import os
class WriteBlog(BaseTool):
    name: str = "Writes a blog based on the summary of an endpoint"
    description: str = (
        "Writes a 1 page blog based on the summary of an endpoint"
    )

    def _run(self, summary: str) -> str:
        co = cohere.Client(os.environ['COHERE'])
        blog_output = co.chat(
            message=f"Write a blog post after intaking a summary of an API endpoint; Make this blog consist of an introduction, context, and conclusion. Make it look pretty using markdown. Use this summary: {summary}"
        )

        return blog_output

