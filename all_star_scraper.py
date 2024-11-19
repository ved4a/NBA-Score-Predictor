import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.basketball-reference.com/allstar/NBA_{}.html"

START_YEAR = 2000
END_YEAR = 2023

all_stars = []
