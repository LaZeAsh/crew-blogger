from crewai_tools import BaseTool
import requests
from bs4 import BeautifulSoup
import os

class UploadMedium(BaseTool):
    name: str = "MediumUploader"
    description: str = (
        "Uploads the inputted blog to medium.com"
    )

    def _run(self, blog_content: str) -> str:

        # Your Medium integration token
        TOKEN = os.environ['MEDIUM']
        # Base URL for Medium API
        BASE_URL = 'https://api.medium.com/v1'

        # Headers including the authorization token
        headers = {
            'Authorization': f'Bearer {TOKEN}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Get user ID
        response = requests.get(f'{BASE_URL}/me', headers=headers)
        response_data = response.json()

        user_id = response_data['data']['id']

        # Blog post data
        post_data = {
            'title': 'NEW Cohere API Endpoint',
            'contentFormat': 'markdown',  # can be 'html' or 'markdown'
            'content': blog_content,
            'publishStatus': 'public'  # can be 'draft', 'public', or 'unlisted'
        }

        # Publish the post
        response = requests.post(f'{BASE_URL}/users/{user_id}/posts', headers=headers, json=post_data)
        response_data = response.json()

        if response.status_code == 201:
            print(f"Blog post published successfully: {response_data['data']['url']}")
            return response_data['data']['url']
        else:
            print(f"Failed to publish blog post: {response_data}")
            return response_data
