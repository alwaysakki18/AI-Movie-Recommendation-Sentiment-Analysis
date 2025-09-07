import requests
from bs4 import BeautifulSoup
import re
import time
import random

class IMDBScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def get_movie_reviews(self, movie_title, max_reviews=50):
        search_url = f"https://www.imdb.com/find?q={movie_title.replace(' ', '+')}&s=tt"
        
        try:
            response = requests.get(search_url, headers=self.headers)
            if response.status_code != 200:
                print(f"Search request failed with status code {response.status_code}")
                return []
            soup = BeautifulSoup(response.content, 'html.parser')
            
            result = soup.find('td', class_='result_text')
            if not result or not result.a:
                print("No search result found for movie:", movie_title)
                return []
            
            movie_link = result.a.get('href')
            if not movie_link:
                print("No movie link found in search result.")
                return []
            movie_id = movie_link.split('/')[2]
            
            reviews_url = f"https://www.imdb.com/title/{movie_id}/reviews"
            response = requests.get(reviews_url, headers=self.headers)
            if response.status_code != 200:
                print(f"Reviews request failed with status code {response.status_code}")
                return []
            soup = BeautifulSoup(response.content, 'html.parser')
            
            reviews = []
            review_containers = soup.find_all('div', class_='text', attrs={'class': 'show-more__control'})
            if not review_containers:
                print("No reviews found for movie:", movie_title)
            
            for container in review_containers[:max_reviews]:
                review_text = container.get_text(strip=True)
                if review_text and len(review_text) > 10:
                    reviews.append(review_text)
            
            time.sleep(random.uniform(1, 3))
            return reviews
        
        except Exception as e:
            print(f"Error scraping IMDB: {e}")
            return []