"""
Shared configuration settings for the automation suite.

This module defines the project directory paths, test and report
locations, and a randomized User-Agent header for web requests.
"""

from pathlib import Path
from fake_useragent import UserAgent

# Root directory of the project.
project_path = Path(__file__).parent
# Directory used to store test-related files.
tests_dir_path = project_path/"tests"
# Directory used to store generated reports.
report_dir_path = project_path/"reports"


# User-Agent generator used to create browser-identifying headers.
ua = UserAgent()
# HTTP request header containing a randomly generated User-Agent.
random_header = {"User-Agent":ua.random}        
