import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    #Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    
    #---------------------first pull--------------------------------#


    # read from red planet site
    url="https://redplanetscience.com/"
    browser.visit(url)

    #set up HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    
    #locate article title and news
     #Extract the article title and paragraph
    news_title = news_soup.body.find("div", class_="content_title").text.strip()
    news_p = news_soup.body.find("div", class_="article_teaser_body").text.strip()

    #---------------------Second Pull---------------------------------#

    #Use splinter to find  image url
    url2="https://spaceimages-mars.com/"
    browser.visit(url2)

    #set up HTML parser
    html2=browser.html
    #beautiful soup object
    image_soup = soup(html2, "html.parser")

    #Parse the htlm for image source("src")
    image = image_soup.body.find("img", class_="headerimage")["src"]
    #extract url for image
    feature = url2 + image
    

    #-----------------------Third Pull---------------------------------#

    #mars facts table
    url3= "https://galaxyfacts-mars.com/"
    mars_table = pd.read_html(url3)
    #read the first table
    table= mars_table[0]
    #make the first row the column headers
    headers = table.iloc[0]
    df = pd.DataFrame(table.values[1:], columns=headers)
    #set the first row as the index
    df.set_index("Mars - Earth Comparison")

    #extract html code from table
    df_html = df.to_html()

    #------------------------Forth Pull--------------------------------#
    #visit the hemispheres website
    url4= "https://marshemispheres.com/"
    browser.visit(url4)
    
    hemis_html = browser.html
    hemis_soup = soup(hemis_html, 'html.parser')

    # 2. Create a list to hold the images and titles.
    image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    items = hemis_soup.find_all("div",class_='item')

    for item in items:
        hemisphere = {}
#       print(f"https://marshemispheres.com/{item.find('a')['href']}")
        browser.visit(f"https://marshemispheres.com/{item.find('a')['href']}")
        
        hemi_html = browser.html
        hemi_soup = soup(hemi_html, 'html.parser')


        hemisphere["title"] = hemi_soup.find('h2', class_='title').text
        hemisphere["image"] = f"https://marshemispheres.com/{hemi_soup.find('img', class_='wide-image')['src']}"
    
        image_urls.append(hemisphere)

    browser.quit()

    mars_df = {
        "News_Title": news_title,
        "News_Snipit": news_p,
        "Featured_Image": feature,
        "Mars_Facts": df_html,
        "Hemisphere_Images": image_urls
    }

    return mars_df

if __name__ == "__main__":
    # execute only if run as a script
    print(scrape())  

