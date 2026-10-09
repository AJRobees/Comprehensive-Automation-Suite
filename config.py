from pathlib import Path
from fake_useragent import UserAgent

project_path = Path(__file__).parent

tests_dir_path = project_path/"tests"
report_dir_path = project_path/"reports"

ua = UserAgent()
random_header = {"User-Agent":ua.random}          # Generates a random, valid browser string

