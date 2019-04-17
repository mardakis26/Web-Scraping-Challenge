from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import json
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

#Mars News

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "lxml")
    
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

#NASA JPL site and scrape the image URL

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    html2 = browser.html
    soup2 = BeautifulSoup(html2, "lxml")

    results2 = soup2.find("article", class_="carousel_item")
    image_url= results2["style"].split("'")
    img_url_tot = image_url[1]
    img_url_full = "https://www.jpl.nasa.gov" + img_url_tot

#Mars twitter

    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)

    html3 = browser.html
    soup3 = BeautifulSoup(html3, "lxml")

    results3 = soup3.find("ol", class_="stream-items js-navigable-stream")
    mars_weather  = results3.find("p", class_= "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    mars_weather =mars_weather.replace("pic.twitter.com/awJfx8w2YE"," ")

#Mars facts site and scrape the table data

    url4 = "https://space-facts.com/mars/"
    
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns = ["Category","Measurement"]
    df = df.set_index("Category")
    df_html = df.to_html()

#Mars Hemispheres
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url9)

    html5 = browser.html
    soup5 = BeautifulSoup(html5, "html.parser")

    results5 = soup5.find_all("div", class_="description")
    
    hemi_image_url = []

    for result in results5:
        res_link = result.find("a")
        res_href = res_link["href"]
        title = result.find("h3").text
        url6 = "https://astrogeology.usgs.gov"+ res_href
        browser.visit(url6)
        html6 = browser.html
        soup6 = BeautifulSoup(html6, "html.parser")
        image_link = soup6.find("a", target="_blank")
        href = image_link["href"]
        hemi_image_url.append({"title":title, "image_url":href})

    mars_data = {
        "latest_news_title":news_title,
        "latest_news_story":news_p,
        "featured_image":img_url_full,
        "current_weather":mars_weather,
        "mars_facts":df_html,
        "mars_hemispheres":hemi_image_url
    }

    browser.quit()

    return mars_data