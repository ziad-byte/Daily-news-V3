import requests
from bs4 import BeautifulSoup
import json
import re

# Function to fetch articles based on heuristics
def fetch_articles(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # Extract the page title
        page_title = soup.title.string.strip() if soup.title else 'No title found'

        # Attempt to find article containers
        articles = soup.find_all('article')
        if not articles:
            # Fallback: Look for divs with common article-related classes
            articles = soup.find_all('div', class_=re.compile(r'(post|article|entry|news|story)', re.I))

        if not articles:
            print("No articles found on this page.")
            return

        results = []

        for article in articles:
            # Extract the title
            title_tag = article.find(re.compile('h[1-6]'))
            title = title_tag.get_text(strip=True) if title_tag else 'No title found'

            # Extract the link
            link_tag = article.find('a', href=True)
            link = link_tag['href'] if link_tag else 'No link found'

            # Extract the description
            description_tag = article.find('p')
            description = description_tag.get_text(strip=True) if description_tag else 'No description found'

            article_data = {
                "Page Title": page_title,
                "Link": link,
                "Title": title,
                "Description": description
            }
            results.append(article_data)

        # Display the results
        for result in results:
            print(json.dumps(result, indent=4))
            print('-' * 40)

        # Save to JSON file
        with open('articles_output.json', 'w', encoding='utf-8') as outfile:
            json.dump(results, outfile, indent=4, ensure_ascii=False)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")

if __name__ == "__main__":
    url = input("Enter the URL of the website: ")
    fetch_articles(url)
