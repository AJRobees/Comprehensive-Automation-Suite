"""
Web scraping module for retrieving and extracting HTML content.

This module requests web pages, parses their HTML using BeautifulSoup,
extracts text from specified HTML elements, and saves extracted results
as JSON reports. It also logs relevant scraping events and errors.
"""

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json

from config import random_header,report_dir_path
from configs import get_logger

logger = get_logger("web_scraper")

class Web_Scraper():
    """
    Retrieve web pages and extract text from selected HTML elements.

    The class manages the request process, HTML parsing, and extraction
    of text content from elements specified by the caller.
    """

    def __init__(self):
        """
        Initialize the scraper's state and request headers.

        Set up attributes for the target URL, requested HTML element,
        extracted results, and randomized user-agent header.
        """

        self.given_url = ""
        self.required_element = ""
        self.element_list = []

        self.header = random_header

    def scraper_collector(self,url):
        """
        Request a web page and handle connection-related failures.

        Args:
        url: The URL of the web page to retrieve.

        Returns:
        A tuple containing a success flag and a status message.

        Logs connection and timeout errors when they occur.
        """

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
        """
        Parse the retrieved HTML response using BeautifulSoup.

        If the response is successful, create a parsed HTML document
        and log the result. Otherwise, log a warning about the failed request.
        """

        if self.response.ok:
            logger.info(f"Web page retrieved successfully. Code {self.status}")

            self.doc = BeautifulSoup(self.response.text,"html.parser")
            logger.info("The HTML was successfully parsed.")

        else:
                logger.warning(f"Failed to fetch from the website. Error code {self.status}")

    def search_element(self,element):
        """
        Extract non-empty text from matching HTML elements.

        Args:
        element: The HTML tag name to search for, such as "p" or "h1".

        Returns:
        A list of extracted text strings if matching elements contain
        non-empty text; otherwise, returns None.

        Updates the selected element and logs the extraction result.
        """

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
        """
        Retrieve a web page and prepare its HTML for parsing.

        Args:
        url: The URL of the web page to retrieve.

        Returns:
        A tuple containing a success flag and a status message.
        Returns a failure flag and error message if retrieval fails.
        """

        valid,result = self.scraper_collector(url)
        if valid:
            self.soup_maker()
            return True,result
        else:
            return False,result

def save_as_json(url,search,result):
    """
    Save extracted web-scraping results to a dated JSON report.

    Args:
    url: The URL from which the data was extracted.
    search: The HTML element or search criterion used.
    result: The extracted result or collection of results.

    Creates the reports directory if needed and appends the new
    record to the current day's report when a report already exists.
    Logs successful saves.
    """

    if not report_dir_path.exists():
        report_dir_path.mkdir()

    if len(result)== 1:
        result = result[0]

    data = {
        "URL":url,
        "Search":search,
        "Result":result,
        "Time":datetime.now().strftime("%H-%M-%S")
    }

    file_name = f"{datetime.now().strftime('%d-%h-%Y')}_reports.json"
    file_path = report_dir_path/file_name

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

    