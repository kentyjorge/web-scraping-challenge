#move scraping from notebook to python
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# scrape all sites to pass to app
def scrape():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = bs(html, 'html.parser')

    # Add try/except for error handling
    try:
        titles = news_soup.find('div', class_='content_title').text
        teaser_text = news_soup.find('div', class_='article_teaser_body').text

    except AttributeError:
        return None, None

    
    # mars news end

    # feature image start
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    html = browser.html
    soup = bs(html, 'html.parser')
    image_path= soup.find('img', class_='headerimage fade-in')['src']
    image_path

    featured_image_url = image_url + image_path
    #feature image scrap end

    # mars facts start
    fact_url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(fact_url)
    mars_facts_df = tables[1]
    mars_facts_df.head()

    mars_facts_df = mars_facts_df.set_index(0)
    mars_facts_df = mars_facts_df.transpose()
    mars_facts_df.reset_index(inplace = True, drop = True)
    mars_facts_html = mars_facts_df.to_html()
    mars_facts_html.replace('\n','')

    mars_facts_df.to_html("mars_facts.html")
    #mars facts end

    # hemisphere image start
    hemi_page_url = "https://marshemispheres.com/"
    browser.visit(hemi_page_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    mars_images = []
    image_section = soup.find('div', class_='collapsible results')
    unique_image = soup.find_all('div',class_='item')

    for i in unique_image:

        header = i.find('h3').text
        hemi_image_url = i.find('a')['href']
        hemi_image_full_url = hemi_page_url + hemi_image_url

        html = browser.html
        soup = bs(html, 'html.parser')

        mars_images.append({"title": header, "image url": hemi_image_full_url})
    #hemisphere image scrape end

    browser.quit()
    #dictionary to store all results and reutn dictionary
    mars_scraped_dict = {
        "title" : titles,
        "teaser" : teaser_text,
        "feature image" : featured_image_url,
        "mars details" : mars_facts_html,
        "mars pictures" : mars_images
    }

    return mars_scraped_dict
