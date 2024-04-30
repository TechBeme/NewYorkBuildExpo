import requests
import pandas as pd
import json
from bs4 import BeautifulSoup



# API request
url = 'https://newyorkbuildexpo2024.expofp.com/data/data.js'
response = requests.get(url)
content = response.text

# Cleaning the content to get only the JSON
json_str = content.replace('var __data = ', '')
data = json.loads(json_str)

# Creating a dictionary to map category IDs to their names
category_map = {category['id']: category['name'] for category in data['categories']}

results = []
for exhibitor in data['exhibitors']:
    description_html = exhibitor.get('description')
    description_text = BeautifulSoup(description_html, 'html.parser').get_text() if description_html else None

    # Mapping category IDs to names
    category_ids = exhibitor.get('categories', [])
    category_names = [category_map.get(int(id), "") for id in category_ids]

    results.append({
        'Name': exhibitor.get('name'),
        'Categories': ', '.join(category_names),
        'Country': exhibitor.get('country'),
        'Address': exhibitor.get('address'),
        'City': exhibitor.get('city'),
        'State': exhibitor.get('state'),
        'Zip': exhibitor.get('zip'),
        'Email': exhibitor.get('email'),
        'Phone': exhibitor.get('phone1'),
        'Website': exhibitor.get('website'),
        'Linkedin': exhibitor.get('linkedin'),
        'Instagram': exhibitor.get('instagram'),
        'Twitter (X)': exhibitor.get('twitter'),
        'Facebook': exhibitor.get('facebook'),
        'Youtube': exhibitor.get('youtube'),
        'Preview': exhibitor.get('videoUrl'),
        'Description': description_text,
        })
    
df = pd.DataFrame(results)
df.to_excel("Exhibitors.xlsx", index=False)
print("Data successfully exported to Exhibitors.xlsx.")