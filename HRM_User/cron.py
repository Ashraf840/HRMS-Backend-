import requests
from pytz import timezone
from datetime import datetime

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
