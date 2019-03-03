from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pandas as pd
import time

def init_browser():

    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=True)

def scrape_info():

    browser = init_browser()
    
    url = "https://mars.nasa.gov/news"

    browser.visit(url)

    time.sleep(1)

    soup = BeautifulSoup(browser.html, 'lxml')

    title = soup.find('div', class_='content_title').text

    paragraph = soup.find('div', class_="article_teaser_body").text

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    
    browser.visit(url)

    browser.click_link_by_partial_text("FULL IMAGE")

    time.sleep(2)

    browser.click_link_by_partial_text("more info")

    soup = BeautifulSoup(browser.html, 'lxml')

    image = soup.find("figure", class_="lede")

    featured_url = "https://www.jpl.nasa.gov" + image.a['href']

    weather_url = "https://twitter.com/marswxreport?lang=en"

    browser.visit(weather_url)

    soup = BeautifulSoup(browser.html, 'lxml')

    tweet = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text

    tweet = tweet.replace('\n', '')

    facts_url = "https://space-facts.com/mars"

    table = pd.read_html(facts_url)

    df = table[0]

    html_table = df.to_html(index=False)

    html_table = html_table.replace('\n', '')
    
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(hemisphere_url)

    soup = BeautifulSoup(browser.html, 'lxml')

    # hemisphere = []
    # img_url = [] 

    results = soup.find_all('div', class_="description")

    # for result in results:
    #     hemisphere.append(result.h3.text)
    #     browser.visit("https://astrogeology.usgs.gov" + result.a["href"])
    #     time.sleep(2)
    #     img_url.append(BeautifulSoup(browser.html, "html.parser").find("div", class_="downloads").a["href"])
    #     time.sleep(2)

    hemisphere = []

    for result in results:
        title = result.h3.text
        browser.visit("https://astrogeology.usgs.gov" + result.a["href"])
        time.sleep(2)
        img_url = BeautifulSoup(browser.html, "html.parser").find("div", class_="downloads").a["href"]
        dictionary = {"hemi_title": title, "img_url": img_url}
        hemisphere.append(dictionary)
        time.sleep(2)
    
    mars = {}
    
    mars["paragraph"] = paragraph

    mars["news_title"] = title

    mars["featured_img_url"] = featured_url

    mars["weather_tweet"] = tweet

    mars["facts_table"] = html_table

    # mars["hemisphere"] = {"hemi_title": hemisphere, "img_url": img_url}
    mars["hemisphere"] = hemisphere

    browser.quit

    return mars