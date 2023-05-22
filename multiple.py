import requests
from bs4 import BeautifulSoup
import pandas as pd

def books():
    base_url = 'http://books.toscrape.com/catalogue/page-'
    newbook_list = []
    
    # Define the headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
        'Referer': 'https://www.google.com',
        'DNT': '1',
        'Accept-Language': 'en-US,en;q=0.9',
        'Padding': '0'
    }
    
    for page in range(1, 51):
        url = base_url + str(page) + '.html'
        r = requests.get(url, headers=headers)
        souper = BeautifulSoup(r.text, 'html.parser')
        
        boz = souper.find_all('li', class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")
        
        for bo in boz:
            full_namez = bo.find('h3').contents[-1]['title'].strip()
            pricez = bo.find('div', class_='product_price').find('p', class_='price_color').text.replace('Â£', '')
            currency = bo.find('div', class_='product_price')('p')[0].text[1]
            availablez = bo.find('div', class_='product_price').find('p', class_='instock availability').text.strip()
            book_url = 'http://books.toscrape.com/catalogue/' + bo.find('h3').find('a')['href']
            img_url = 'http://books.toscrape.com/' + bo.find('div', class_='image_container').find('img')['src']
            
            bookz = {
                'Title': full_namez,
                'Currency': currency,
                'Price': pricez,
                'Availability': availablez,
                'URL': book_url,
                'Img_URL': img_url
            } 

            newbook_list.append(bookz)
    
    new_df = pd.DataFrame(newbook_list)
    new_df['Price'] = pd.to_numeric(new_df.Price)
    return new_df

# Calling the function
book_data = books()
# print(book_data)

# save to csv
book_data.to_csv('book_data.csv', index=False)