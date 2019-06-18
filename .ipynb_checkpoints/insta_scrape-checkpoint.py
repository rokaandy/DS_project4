# code taken from jnawjux with permission from owner:
# https://github.com/jnawjux/web_scraping_corgis/blob/master/insta_scrape.py

from time import sleep
from random import random
import re
from selenium.webdriver import Chrome
from urllib.request import urlretrieve
from uuid import uuid4

def get_posts(hashtag, n):
    """Collect images and hashtags from the n newest posts with the given hashtag"""
    url = f'https://www.instagram.com/explore/tags/{hashtag}/'
    browser = Chrome()
    browser.get(url)
    posts = []
    while len(posts) < n:
        images = [img.get_attribute('src') for img in browser.find_elements_by_css_selector('article img')]
        links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
        post_url = 'https://www.instagram.com/p/'
        posts = list(filter(lambda link: post_url in link, links))
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
        # Pause for 3 to 8 seconds before continuing
        sleep(3 + (random() * 5))
    else:
        # Create a list of pairs of post links and image links
        posts = [{'post_link': posts[n], 'image_link': images[n]} for n in range(len(posts))]
        for post in posts:
            uuid = uuid4()
            urlretrieve(post['image_link'], f'data/{hashtag}/{uuid}.jpg')
            post['hashtags'] = get_hashtags(post['post_link'])
            post['image'] = f'{uuid}.jpg'
            # Pause for 3 to 8 seconds before continuing
            sleep(3 + (random() * 5))
    return posts
    
def insta_details(urls):
    """Take a post url and return post details"""
    browser = Chrome()
    post_details = []
    for link in urls:
        browser.get(link)
        try:
        # This captures the standard like count. 
            likes = browser.find_element_by_partial_link_text(' likes').text
        except:
        # This captures the like count for videos which is stored
            view_id = '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/span'
            likes = browser.find_element_by_xpath(view_id).text
        age = browser.find_element_by_css_selector('a time').text
        xpath_c = '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li[1]/div/div/div'
        comment = browser.find_element_by_xpath(xpath_c).text
        post_details.append({'link': link, 'likes/views': likes, 'age': age, 'comment': comment})
        sleep(3 + (random() * 5))
    return post_details  

def find_hashtags(comment):
    """Find hastags used in comment and return them"""
    hashtags = re.findall('#[A-Za-z]+', comment)
    return hashtags

# def get_hashtags(post_url):
#     """Fetches all the hashtags from a post"""
#     browser = Chrome()
#     browser.get(post_url)
#     comments_html = browser.find_elements_by_css_selector('span')
#     all_hashtags = []
#     for comment in comments_html:
#         hashtags = re.findall('#[A-Za-z]+', comment.text)
#         if len(hashtags) > 0:
#             all_hashtags.extend(hashtags)
#     return list(set(all_hashtags))

def get_hashtags(lol):
    """Dummy function for testing purposes"""
    return ['lol']