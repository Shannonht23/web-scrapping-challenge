from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd



def scrape():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    big_dict = {}


    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')



    #display the current title content
    content_title= slide_elem.select_one('div.content_title')




    # Use the parent element to find the first a tag and save it as `news_title`

    news_title = content_title.text

    big_dict['news_title'] = news_title



    # Use the parent element to find the paragraph text
    news_p = slide_elem.select_one('div.article_teaser_body')
    news_p = news_p.text
    
    big_dict['news_paragraph'] = news_p


    # ## JPL Space Images Featured Image

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    browser.links.find_by_partial_text('FULL IMAGE').click()



    # Parse the resulting html with soup
    s=soup(browser.html,'html.parser')






    # find the relative image url
    img_url_rel= s.find_all('img', class_='headerimage')
    img_url_rel = img_url_rel[0].get('src')





    # Use the base url to create an absolute url
    img_url=f'{url}/{img_url_rel}'

    big_dict['img_url'] = img_url


    # ## Mars Facts



    # Use `pd.read_html` to pull the data from the Mars-Earth Comparison section
    # hint use index 0 to find the table
    df =pd.read_html('https://galaxyfacts-mars.com/')
    df = df[0]






    #adding headers and a index: 

    df=df.set_axis(['Description','Mars','Earth'], axis=1, inplace =False)
    df=df.set_index('Description')






    #representaion of a table


    big_dict['mars_facts'] = df.to_html(classes='table table-striped')


    # ## Hemispheres





    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Get a list of all of the hemispheres
    links = browser.find_by_css('div.description a.product-item')

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        
        
        # We have to find the elements on each loop to avoid a stale element exception
        links=browser.find_by_css('div.description a.product-item')
        link=links[i]
        browser.visit(link['href'])
        html2 = browser.html
        s2 = soup(html2, 'html.parser')
        page_dict= {}
        
        # Next, we find the Sample image anchor tag and extract the href
        
        a=s2.find_all('a')
        for i in a:
            if(i.string =='Sample'):
                page_dict['img_url'] = 'https://marshemispheres.com/'+i['href']
            
        # Get Hemisphere title
        t =s2.find('h2', class_='title')
        page_dict['title'] =t.text
        
        # Append hemisphere object to list
        hemisphere_image_urls.append(page_dict)
        
        # Finally, we navigate backwards
        
        browser.back()
    


        
    big_dict['hemisphere'] = hemisphere_image_urls 




    browser.quit()
    return big_dict

