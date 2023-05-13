from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
import json


# redirect to all the pages 
# create html file for first post from all the pages 
# home_url = 'https://www.facebook.com/pages/?category=your_pages'
post_list_div = "//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']/div[2]"
page_url_xpath = "//div[@class='x1d52u69']/div[{}]/a"
view_all_comments_xpath = "//div[@class='x1i10hfl xjbqb8w xjqpnuy xa49m3k xqeqjp1 x2hbi6w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xdl72j9 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli xexx8yu x18d9i69 xkhd6sd x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x3nfvp2 x1q0g3np x87ps6o x1a2a7pz x6s0dn4 xi81zsa x1iyjqo2 xs83m0k xsyo7zv xt0b8zv']"
page_url_list = []
page_url_dict = {}

def save_html_post( driver, home_url, index=1):
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
        return save_html_post(driver, home_url, index=1+index)
    
    else: 
        page_url_dict['page_urls'] = page_url_list
        json_object = json.dumps(page_url_dict, indent=4) # works 
        with open('data.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json_object)
        page_url_list
        
        print(page_url_dict)
        print('done!')
    
    # driver.find_element(By.XPATH, view_all_comments_xpath).click()
    # print('clicked on view more comments')

    # with open('firstPagePost.html', 'w', encoding='utf8') as file:
    #     source_data = driver.page_source
    #     bs_data = BeautifulSoup(source_data, 'html.parser')
    #     file.write(str(bs_data.prettify()))
    #     print(f'written: html file ')
    

    
def get_post_element_from_pages(page_url, driver, post_no):
    jsonfile =  open('data.json', "r+", encoding="utf-8")
    file_data = json.load(jsonfile)

    file_data[page_url] = []

    
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
    # page_likes = driver.find_element(By.XPATH, "//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w x6s0dn4 xyamay9']/span/a[1]").text
    # page_followers = driver.find_element(By.XPATH, "//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 xdt5ytf x2lah0s x193iq5w x6s0dn4 xyamay9']/span/a[2]").text

    # file_data["page_name"] = page_name
    # file_data['page_likes'] = page_likes
    # file_data['page_followers'] = page_followers
    print(page_name)

    for i in range(1, post_no+1):
    
        # try: 
        # entire xpath of clickable span 
        post_div = f"//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']/div[2]/div[{i}]"
        find_post_div = driver.find_element(By.XPATH, post_div)
        actions = ActionChains(driver)
        actions.move_to_element(find_post_div).perform()
        post_name_div = find_post_div.find_element(By.XPATH, "//div[@class='xzsf02u xngnso2 xo1l8bm x1qb5hxa']")
        actions.move_to_element(post_name_div).perform()
        post_name = post_name_div.text
        print("Post name: {}".format(post_name))
        # actions.move_to_element(find_post_name)
        all_post_comment_view  = f"//div[@class='x9f619 x1n2onr6 x1ja2u2z xeuugli xs83m0k x1xmf6yo x1emribx x1e56ztr x1i64zmx xjl7jj x19h7ccj xu9j1y6 x7ep2pv']/div[2]/div[{i}]/div[@class='x1yztbdb x1n2onr6 xh8yej3 x1ja2u2z']/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[5]/div/div/div[2]/div[4]/div/div[2]/span"
        time.sleep(5)
        driver.find_element(By.XPATH, all_post_comment_view).click()
        print('clicked')
        time.sleep(2)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        all_li = driver.find_elements(By.XPATH, "//div[@class='xwya9rg x11i5rnm x1e56ztr x1mh8g0r xh8yej3']/div/div[2]/ul/li")
        # ul = div_over_ul.find_element(By.TAG_NAME, 'ul')
        # all_li = ul.find_element(By.TAG_NAME, 'li[1]')
        # print("Post Name: {}".format(post_name))
        print("total comments {}".format(len(all_li)))
        all_comments = []
        for al in range(1, len(all_li)+1):
            time.sleep(1)
            all_li = driver.find_element(By.XPATH, f"//div[@class='xwya9rg x11i5rnm x1e56ztr x1mh8g0r xh8yej3']/div/div[2]/ul/li[{al}]/div/div/div[2]/div/div/div/div/div/div/div")
            # all_li = driver.find_element(By.XPATH, f"//div[@class='xwya9rg x11i5rnm x1e56ztr x1mh8g0r xh8yej3']/div/div[2]/ul/li[{i}]")
            actions.move_to_element(all_li).perform()
            time.sleep(1)
            comment = all_li.text
            all_comments.append(comment)
            # comment = all_li.find_element(By.XPATH, "//div[@class='x1lliihq xjkvuk6 x1iorvi4']").text
            # print(comment)
        print(all_comments)

        page_info  = {
        "post_count": "post_{}".format(i),
        "comments": all_comments, 
        "comment_count": 6,

        }
        # x[page_url].append(page_info)
        # file_data.append(x)
        file_data[page_url].append(page_info)
        

        
        # with open(f"HTML/post_html{i}.html".format(post_no), 'w', encoding='utf-8') as file:
        #     source_data = driver.page_source
        #     bs_data = BeautifulSoup(source_data, 'html.parser')
        #     file.write(str(bs_data.prettify()))

        #     time.sleep(4)
            # terminate the post popup screen
        driver.find_element(By.XPATH, "//div[@class='x1d52u69 xktsk01']/div").click() 

        # except Exception as e:
    jsonfile.seek(0)
      #     print("There was an error finding the posts")
    json.dump(file_data, jsonfile, indent=4)
    jsonfile.close()
        # time.sleep(10)
        # return get_post_element_from_pages(page_url, driver, post_no=1+post_no)
        
