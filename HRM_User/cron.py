import requests
from bs4 import BeautifulSoup
from pytz import timezone
from datetime import datetime
from HRM_controller import models

auth_user = 'Techforing_Ltd'
auth_code = "09345jljrksdfhhsr745h3j4w8dd9fs"
url = 'https://rumytechnologies.com/rams/json_api'
todays_date = datetime.now(timezone('Asia/Dhaka')).today().date().strftime('%Y-%m-%d')

data = {
    "operation": "fetch_log",
    "auth_user": auth_user,
    "auth_code": auth_code,
    "start_date": todays_date,
    "end_date": todays_date
}


def attendance_data():
    pass


def create_holiday():
    year = datetime.now().year
    url = f'https://www.officeholidays.com/countries/bangladesh/{year}'

    ### Web Scraping ###
    full_page = requests.get(url)
    full_page = full_page.content
    soup = BeautifulSoup(full_page, "html.parser")

    holidays = soup.find_all('tr', {'class': ['country', 'govt']})

    for holiday in holidays:
        day = holiday.find_all('td')[2].find('a').text
        h_date = holiday.find_all('td')[1].find('time')['datetime']
        models.HolidayModel.objects.get_or_create(holiday_name=day, holiday_date=h_date)
