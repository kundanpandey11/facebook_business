import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from .create_html_posts2 import save_html_post, get_post_element_from_pages

import time 
from decouple import config 
import json 

from textblob import TextBlob
import plotly.offline as opy
import plotly.graph_objs as go

email = "kundan.k.pandey02@gmail.com"
password = "Cogitoergosum25"









amitabh = "https://www.facebook.com/amitabhbachchan"

ger_wholesale = "https://www.facebook.com/GERwholesale"
virat = "https://www.facebook.com/virat.kohli"

page_url = 'https://www.facebook.com/pages/?category=your_pages'
page1_url = "https://www.facebook.com/profile.php?id=100090231663199"
page2_url = "https://www.facebook.com/profile.php?id=100089498875309"
george_page_url  = "https://www.facebook.com/profile.php?id=102531858594913"



def get_all_page_url(username, home_url=page_url, index=1):
    
    option = Options()
    # option.add_argument("--headless")
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_argument("--disable-notifications")
    option.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver  = webdriver.Chrome("./chromedriver.exe", options=option)

    url = 'https://www.facebook.com/'
    # request_url = requests.get(url)

    driver.get(url)
    time.sleep(1)
    # post_list_div = "//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']/div[2]"
    page_url_xpath = "//div[@class='x1d52u69']/div[{}]/a"
    # view_all_comments_xpath = "//div[@class='x1i10hfl xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1a2a7pz x6s0dn4 xi81zsa x1iyjqo2 xs83m0k xsyo7zv xt0b8zv']"
    page_url_list = []
    page_url_dict = {}
    time.sleep(50)
    # wait = WebDriverWait(driver, 100)
    # wait.until(EC.url_to_be(home_url))
    driver.get(home_url)

    driver.find_element(By.XPATH,"//div[@class='x1d52u69']/div[last()]").click() # go to last div and click to reveal all pages 
    # global num_pages 
    num_pages = driver.find_elements(By.XPATH, "//div[@class='x1d52u69']/div") # get total count of pages 
    
    if index <= len(num_pages): # print urls of all the pages
        driver.find_element(By.XPATH, page_url_xpath.format(index)).click()
        if index >=4:
            time.sleep(1)
        page_url = driver.current_url
        page_url_list.append(page_url)
        print(page_url) # to see if the id of the page is displayed
        return get_all_page_url(driver, home_url, index=1+index)
    
    else: 
        page_url_dict['page_urls'] = page_url_list
        json_object = json.dumps(page_url_dict, indent=4) # works 
        with open('{}_page_url.json'.format(username), 'w', encoding='utf-8') as json_file:
            json_file.write(json_object)
        page_url_list
        
        print(page_url_dict)
        print('done!')
        driver.quit()
        return json_file


    
def get_comments_form_page_url(page_url, name, post_count):
    option = Options()
    option.add_argument("--headless")
    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    option.add_argument("--disable-notifications")
    option.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver  = webdriver.Chrome("./chromedriver.exe", options=option)
    url = 'https://www.facebook.com/'
    # request_url = requests.get(url)

    driver.get(url)
    time.sleep(1)

    username_field = driver.find_element(By.NAME, 'email')
    username_field.send_keys(email)
    password_field = driver.find_element(By.NAME, 'pass')
    password_field.send_keys(password)
    login_button = driver.find_element(By.CSS_SELECTOR,'button[type="submit"]')
    login_button.click()
    time.sleep(20)

    # jsonfile =  open('data.json', "r+", encoding="utf-8")
    # file_data = json.load(jsonfile)
    file_data = {}

    driver.get(page_url)
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(4)
    post_list_div = driver.find_elements(
        By.XPATH, 
        "//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']/div[2]/div"
        )
    print("Total post count: ",len(post_list_div))
    page_name_path  = "//div[@class='x1e56ztr x1xmf6yo']"
    page_name = driver.find_element(By.XPATH, page_name_path).text

    file_data["page_name"] = page_name
    file_data[page_url] = []

    print(page_name)

    for i in range(1, post_count+1):
    # try: 
    # entire xpath of clickable span 
        post_div_path = f"//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']/div[2]/div[{i}]"
        post_div = driver.find_element(By.XPATH, post_div_path)
        actions = ActionChains(driver)
        actions.move_to_element(post_div).perform()
        view_comment = post_div.find_element(By.XPATH, f"(//span[contains(text(), 'View more comments')])[position()={i}]")
        actions.move_to_element(view_comment).perform()
        time.sleep(5)

        view_comment.click()

        print('clicked')
        time.sleep(2)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)
        all_li_count = driver.find_elements(By.XPATH, "//div[@class='xwya9rg x11i5rnm x1e56ztr x1mh8g0r xh8yej3']/div/div[2]/ul/li")
        length_all_li  = len(all_li_count)+1
        print("total comments {}".format(len(all_li_count)))
        all_comments = []
        comment_count = 1
        while comment_count <= 20:
            
            try:
                # every next 50 comments there is "view more comments"
                if (comment_count + 10)%50 == 0:
                    open_more_comments = driver.find_element(By.XPATH, "//div[@class='xwya9rg x11i5rnm x1e56ztr x1mh8g0r xh8yej3']/div/div[2]/div[2]/div/div/span")
                    actions.move_to_element(open_more_comments).perform()
                    time.sleep(2)
                    open_more_comments.click()
                    
                time.sleep(1)
                all_li = driver.find_element(By.XPATH, f"//div[@class='xwya9rg x11i5rnm x1e56ztr x1mh8g0r xh8yej3']/div/div[2]/ul/li[{comment_count}]/div/div/div[2]/div/div/div/div/div/div/div")
                driver.execute_script("arguments[0].scrollIntoView();", all_li)
                time.sleep(1)
                comment = all_li.text
                if comment == "Top fan":
                    all_li = driver.find_element(By.XPATH, f"//div[@class='xwya9rg x11i5rnm x1e56ztr x1mh8g0r xh8yej3']/div/div[2]/ul/li[{comment_count}]/div/div/div[2]/div/div/div/div/div/div/div[2]")
                    # print('top fan as comment ')
                    driver.execute_script("arguments[0].scrollIntoView();", all_li) # make the division visible 
                    # arguments[0].scrollIntoView();
                    # actions.move_to_element(all_li).perform()
                    time.sleep(1)
                    comment = all_li.text
                    print("top fan: {} {} ".format(comment, comment_count))
                all_comments.append(comment)
                # comment = all_li.find_element(By.XPATH, "//div[@class='x1lliihq xjkvuk6 x1iorvi4']").text
                print(comment, comment_count)
                # comment_count += 1
            except Exception as e:
                print("Couldn't get above comment!", comment_count)
                time.sleep(2)
            # print(comment)
            comment_count +=1
        page_info  = {
        "post_count": "post_{}".format(i),
        "comments": all_comments, 
        "comment_count": length_all_li,
        }

        file_data[page_url].append(page_info)
        # terminate the post popup screen
        driver.find_element(By.XPATH, "//div[@class='x1d52u69 xktsk01']/div").click() 
        time.sleep(1)
    time.sleep(2)
    json_object = json.dumps(file_data)
    jsonfile = open(f'JSON/{name}_data.json', 'a', encoding='utf-8')
    jsonfile.write(json_object)
    jsonfile.close()

    driver.quit()


def create_graph(json_file):
    open
    for c in com:
        comment_id = []
        comment_string = TextBlob(c['message'])
        comments_polarity = comment_string.sentiment.polarity
        if comments_polarity > 0.0:
            positive_sentiment += 1
        elif comments_polarity < 0.0:
                
            negative_sentiment += 1
        else:
            
            neutral_sentiment += 1
        comment_id += [c['id']]
    
    value = [negative_sentiment, neutral_sentiment, positive_sentiment]
    names = ['Negative Comments', 'Neutral Comments', 'Positive Comments']
    account_name = get_account_name(page_id, page_access_token)
    try: 
        post_title = get_post_name_from_commentid(c['id'], account_data=accounts_posts_json['data'])
    except BaseException: 
        post_title = "NO COMMENTS YET" 
    
    if sum(value) != 0:  
        trace1 = go.Bar(x=names, y=value )
        data=go.Data([trace1])
        layout=go.Layout(title=post_title, xaxis={'title':'Comments'}, yaxis={'title':'Count'})
        figure=go.Figure(data=data,layout=layout, ) 
        figure.update_traces(marker_color=['red', 'blue', 'green'])             
        div = figure.to_html(
            full_html=False, default_height=400, 
            default_width=500,
            config=dict(displayModeBar=False))
        contain_div += [div]

    context = {
        'graphs': contain_div[:10],
        'account_name':account_name,
    }
    return context
        


# get_comments_form_page_url(amitabh) 






                               
                               
                               
                               
