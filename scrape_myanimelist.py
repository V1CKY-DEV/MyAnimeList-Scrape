from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import threading
firefox_profile = webdriver.FirefoxProfile()
# Set preferences to disable images, stylesheets, JavaScript, and Flash
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('permissions.default.stylesheet', 2)
firefox_profile.set_preference("stylesheet.enabled", False);
firefox_profile.set_preference("javascript.enabled", False);
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
driver = webdriver.Firefox(firefox_profile=firefox_profile)

# Define the order of the letters to be scraped

order = ['.', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
#current_num is used to declare the page no for pagination
current_num = 0
count = 0
# Loop through each letter in the order and scrape the anime data.these letter are used in url to get all anime by letter
for letter in order:
    #while loop is used for the page increment to loop with same letter but different page.
    while True:
        current_letter = letter
        if current_num == 0 :
            #if the current num is 0 only add letter
            url_in = f"https://myanimelist.net/anime.php?letter={letter}"
        elif current_num > 0 :
            #if current_num is greater then 0 add current number with the same letter
            url_in = f"https://myanimelist.net/anime.php?letter={letter}&show={current_num}"
        driver.get(url_in)
        #this breaker is a error 404 recognizer 
        breaker = driver.find_elements(By.CSS_SELECTOR, '.error404')
        #if breaker got the error 404 page it will break the for loop and make the current num 0 to start the numbering from beginning 
        if breaker:
            current_num = 0
            break
            
        else:
            #else this is going to increase the current num by 50 because myanimelist have 50 anime data per page 
            current_num+=50
        urls = []
        #element gets all anime in the page
        elements = driver.find_elements(By.CSS_SELECTOR, '.hoverinfo_trigger.fw-b.fl-l')
        #this extract all urls in the elements and put in the urls
        urls.extend([result.get_attribute("href") for result in elements])
        file_path = ''
        #this if statement check the letter so that if it is dot it should be changed to letter instead of symbol
        if letter == '.' :
            #this creates a json file for dot symbol. 
            file_path = 'database/dot.json'
        else:
            # this creates a json file with the letter this loop is using
            file_path = f'database/{letter}.json'
        #this for loop use urls one by one to get information out the page 
        for url in urls:
            count+=1
            driver.get(url)
            #Data - Information
            Data = driver.find_elements(By.CSS_SELECTOR, '.spaceit_pad')
            #This loop gives all additional information
            #Streaming - broadcasters
            Streaming = driver.find_elements(By.CLASS_NAME, 'broadcasts')
            #Data2 - Addition information
            Data2 = driver.find_elements(By.XPATH, '//*[@id="content"]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[3]/td/table/tbody')
            list_data = {}
            #Eng_title  - English title is out of data because not all series have English titles
            Eng_title = driver.find_elements(By.CLASS_NAME, 'title-english')
            #Jap-title  - Japanese title is out of data because not all series have English titles
            Jap_title = driver.find_elements(By.CLASS_NAME, 'title-name')
            
            list_data = {}
            # this condition checks if English Title Exists
            if Eng_title:
                #this update the list_data with English Titles
                list_data[count] = {"English_Title" :  Eng_title[0].text}
            else:
                #this update the list_data with Englsih Title and add N/A to it
                list_data[count] = {"English_Title" :  'N/A'}
            
            characters_data = driver.find_elements(By.CSS_SELECTOR, '.h3_characters_voice_actors')
            #this declares character in the list_data
            list_data[count]['characters'] = {}
            # this condition checks if the character database Exists
            if characters_data:
                lister = []
                for c in characters_data:
                    lister.append(c.text)
                    #this update the list_data with Characters
                list_data[count]['characters'].update({"Name":lister})
            #this update the list_data with Japanglish
            list_data[count].update({"English_Japanese":  Jap_title[0].text})
            Data = [element for element in Data if element.text.strip() != '']
            if Streaming:
                stream = str(Streaming[0].text)
                stream = stream.replace('May be unavailable in your region.', "")
                stream = stream.split()
                stream = ",".join(stream)
                #this update the list_data with Broadcasters
                list_data[count] = {"Streaming" :  stream}
            
            #This loop split the data to fit the json format
            for list in Data:
                temp = str(list.text).strip()
                if ':' in temp:
                    str1 , str2 = temp.split(':', maxsplit=1)
                    #if condition to remove some of the data which i didn't need. you can remove the if statement
                    if str1 not in ['Japanese', 'Synonyms', 'Favorites', 'Members', 'Score', 'Source', 'Licensors', 'Producers']:
                        if str1  or str2 != " ":
                            item_dict = {str1.strip(): str2.strip()}
                            #this update the list_data with Information
                            list_data[count].update(item_dict)
            
            #This loop split the data to fit the json format
            for list in Data2:
                temp = str(list.text).strip()
                if ':' in temp:
                    str1 , str2 = temp.split(':', maxsplit=1)
                    #if condition to remove some of the data which i didn't need. you can remove the if statement
                    if str1 not in ['Adaptation', 'Side story', 'Spin-off', 'Members', 'Other']:
                        if str1  or str2 != " ":
                            item_dict = {str1.strip(): str2.strip()}
                            #this update the list_data with Additional Information
                            list_data[count].update(item_dict)



            if os.path.isfile(file_path):
                # If the file exists, open it in append mode and write the new anime dictionary to it
                with open(file_path, "a") as f:
                    json.dump(list_data, f)
                    f.write("\n") # Add a newline character to separate the JSON objects in the file
            else:
            # If the file does not exist, create it and write the new anime dictionary to it as a JSON array
                with open(file_path, "w") as f:
                    json.dump([list_data], f)
# quit the browser we didn't quit the driver before because we are using the same driver but different urls always so it will be like one browser changing urls
driver.quit()
