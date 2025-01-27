import json
import requests
from datetime import datetime
from Oauth import auth, headers
from phidata import main

# Your Google API credentials file
credentials = 'credentials.json'
access_token = auth(credentials)  # Authenticate the API
headers = headers(access_token)  # Create headers to attach to the API call.

def post_to_blogger(headers, blog_id, message_content):
    '''
    Function to create a new post on Blogger.
    '''
    api_url = f'https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/'
    post_data = {
        "kind": "blogger#post",
        "title": f"AI News Update - {datetime.now().strftime('%B %d, %Y')}",
        "content": message_content
    }

    response = requests.post(api_url, headers=headers, json=post_data)
    if response.status_code in [200, 201]:
        print("Post successful!")
        print("Post URL:", response.json().get("url"))
    else:
        print(f"Failed to post. Status Code: {response.status_code}")
    print("Response JSON:", response.json())

if __name__ == '__main__':
    # Replace with your Blogger blog ID
    blog_id = "4787197814469544568"
    
    # Fetch the message content to post
    message = main()
    message_content = message['news_content']

    # Post the content to Blogger
    post_to_blogger(headers, blog_id, message_content)
