from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import threading
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('permissions.default.stylesheet', 2)
firefox_profile.set_preference("stylesheet.enabled", False);
firefox_profile.set_preference("javascript.enabled", False);
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
driver = webdriver.Firefox(firefox_profile=firefox_profile)
order = ['.', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
current_num = 0
count = 0
for letter in order:
    while True:
        current_letter = letter
        if current_num == 0 :
            url_in = f"https://myanimelist.net/anime.php?letter={letter}"
        elif current_num > 0 :
            url_in = f"https://myanimelist.net/anime.php?letter={letter}&show={current_num}"
        driver.get(url_in)
        breaker = driver.find_elements(By.CSS_SELECTOR, '.error404')
        if breaker:
            current_num = 0
            break
            
        else:
            current_num+=50
        urls = []
        elements = driver.find_elements(By.CSS_SELECTOR, '.hoverinfo_trigger.fw-b.fl-l')
        urls.extend([result.get_attribute("href") for result in elements])
        file_path = ''
        if letter == '.' :
            file_path = 'database/dot.json'
        else:
            file_path = f'database/{letter}.json'
        
        for url in urls:
            count+=1
            driver.get(url)
            Data = driver.find_elements(By.CSS_SELECTOR, '.spaceit_pad')
            Streaming = driver.find_elements(By.CLASS_NAME, 'broadcasts')
            Data2 = driver.find_elements(By.XPATH, '//*[@id="content"]/table/tbody/tr/td[2]/div[1]/table/tbody/tr[3]/td/table/tbody')
            list_data = {}
            Eng_title = driver.find_elements(By.CLASS_NAME, 'title-english')
            Jap_title = driver.find_elements(By.CLASS_NAME, 'title-name')
            
            list_data = {}
            
            if Eng_title:
                list_data[count] = {"English_Title" :  Eng_title[0].text}
            else:
                list_data[count] = {"English_Title" :  'N/A'}
            characters_data = driver.find_elements(By.CSS_SELECTOR, '.h3_characters_voice_actors')
            list_data[count]['characters'] = {}
            if characters_data:
                lister = []
                for c in characters_data:
                    lister.append(c.text)
                list_data[count]['characters'].update({"Name":lister})
            list_data[count].update({"English_Japanese":  Jap_title[0].text})
            Data = [element for element in Data if element.text.strip() != '']
            if Streaming:
                stream = str(Streaming[0].text)
                stream = stream.replace('May be unavailable in your region.', "")
                stream = stream.split()
                stream = ",".join(stream)
                list_data[count] = {"Streaming" :  stream}
            
        
            for list in Data:
                temp = str(list.text).strip()
                if ':' in temp:
                    str1 , str2 = temp.split(':', maxsplit=1)
                    if str1 not in ['Japanese', 'Synonyms', 'Favorites', 'Members', 'Score', 'Source', 'Licensors', 'Producers']:
                        if str1  or str2 != " ":
                            item_dict = {str1.strip(): str2.strip()}
                            list_data[count].update(item_dict)
            for list in Data2:
                temp = str(list.text).strip()
                if ':' in temp:
                    str1 , str2 = temp.split(':', maxsplit=1)
                    if str1 not in ['Adaptation', 'Side story', 'Spin-off', 'Members', 'Other']:
                        if str1  or str2 != " ":
                            item_dict = {str1.strip(): str2.strip()}
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
# quit the browser
driver.quit()
