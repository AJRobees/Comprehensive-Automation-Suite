from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json

from config import random_header,tests_dir_path
from configs import get_logger

logger = get_logger("web_scraper")

class Web_Scraper():
    def __init__(self):

        self.given_url = ""
        self.required_element = ""
        self.element_list = []

        self.header = random_header

    def scraper_collector(self,url):
        try:
            self.given_url = url 
            actual_response = requests.get(self.given_url,timeout=(3,10),allow_redirects=True,headers=self.header)
            self.response = actual_response
            self.status = self.response.status_code
            result = "Web page retrieved successfully."
            return True,result

        except requests.exceptions.ConnectionError:
            logger.error("Network connection is lost.")
            result = "Network connection is lost."
            return False,result
        except requests.exceptions.Timeout:
            logger.error("No response from website >_< .")
            result = "No response from website >_< ."
            return False,result

    def soup_maker(self):
        if self.response.ok:
            logger.info(f"Web page retrieved successfully. Code {self.status}")

            self.doc = BeautifulSoup(self.response.text,"html.parser")
            logger.info("The HTML was successfully parsed.")

        else:
                logger.warning(f"Failed to fetch from the website. Error code {self.status}")

    def search_element(self,element):
        self.element_list = []
        result_element = self.doc.find_all(element)

        if len(result_element) != 0:
            for item in result_element:
                if item.text != "":
                    self.element_list.append(item.text)

            logger.info(f"Web page {element} retrieved successfully.")
            self.required_element = element
            return self.element_list

        else:
            logger.warning("The HTML was failed to parse.")

        
    def run_scraper(self,url):
        valid,result = self.scraper_collector(url)
        if valid:
            self.soup_maker()
            return True,result
        else:
            return False,result

def save_as_json(url,search,result):

    if not tests_dir_path.exists():
        tests_dir_path.mkdir()

    if len(result)== 1:
        result = result[0]

    data = {
        "URL":url,
        "Search":search,
        "Result":result,
        "Time":datetime.now().strftime("%H-%M-%S")
    }

    file_name = f"{datetime.now().strftime('%d-%h-%Y')}_reports.json"
    file_path = tests_dir_path/file_name

    if file_path.exists():
        existing_data = []

        with open(file_path,"r",encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
        if isinstance(existing_data,dict):
            existing_data = [existing_data]

        if isinstance (data,dict):                                 # To append the dictionary note with the existing one
            existing_data.append(data)

        else:
            existing_data.extend(data)

        with open(file_path,"w",encoding="utf-8") as f:
            json.dump(existing_data,f,indent= 2)
        logger.info("Extracted data saved as json.")
    else:
        with open(file_path,"w",encoding="utf-8") as f:
            json.dump(data,f,indent= 2)
            logger.info("Extracted data saved as json.")

    