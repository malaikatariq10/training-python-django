import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class Scrapping:
    def __init__(self,url):

        self.cleaned_quotes: List[Dict[str, str]] = []
        self.scrape_data(url)

    def scrape_data(self, url: str) -> None:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data from {url}: {e}")
            return

        try:
            soup = BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"Failed to parse HTML: {e}")
            return

        print(f" Fetched data from {url}")
        print("========")

        for block in soup.find_all("div", class_="quote"):
            try:
                quote_text = block.find("span", class_="text").text.strip()
                author = block.find("small", class_="author").text.strip()
                tags = [tag.text.strip() for tag in block.find_all("a", class_="tag")]

                self.cleaned_quotes.append({
                    "quote": quote_text,
                    "author": author,
                    "tags": tags
                })
            except AttributeError:
                print("Skipping a quote block due to missing elements.")
            except Exception as e:
                print(f"Error processing a quote block: {e}")

    def display_quotes(self) -> None:
        for item in self.cleaned_quotes:
            print(f"{item['quote']}")
            print(f"— {item['author']}")
            print(f"Tags: {', '.join(item['tags'])}")
            print("-" * 40)

    def searchByTags(self, tags: List[str]):
        results = []
        for item in self.cleaned_quotes:
            if any(tag.lower() in (t.lower() for t in item['tags']) for tag in tags):
                results.append(item)

        if results:
            for quote in results:
                print(f"{quote['quote']}")
                print(f"— {quote['author']}")
                print(f"Tags: {', '.join(quote['tags'])}")
                print("-" * 40)
        else:
            print("No quotes found for the given tags.") 

    def searchByAuthor(self, author: str):
        results = []
        for item in self.cleaned_quotes:
            if author.lower() in item["author"].lower():
                results.append(item)

        if results:
            for quote in results:
                print(f"{quote['quote']}")
                print(f"— {quote['author']}")
                print(f"Tags: {', '.join(quote['tags'])}")
                print("-" * 40)
        else:
            print("No quotes found for this author.")
    def searchByQuote(self, quote: str):
        results = []
        for item in self.cleaned_quotes:
            if quote.lower() in item["quote"].lower():
                results.append(item)

        if results:
            for quote in results:
                print(f"{quote['quote']}")
                print(f"— {quote['author']}")
                print(f"Tags: {', '.join(quote['tags'])}")
                print("-" * 40)
        else:
            print("No quotes found for this author.")


if __name__ =="__main__":
    s=Scrapping("https://quotes.toscrape.com/")
    s.searchByTags(["humor","OBVIOUS","edison"])

