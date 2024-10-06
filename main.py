import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Google Sheets API setup
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1m4BktefQ3vCY3NtOhWoLc7rb9aKOMJXKR_qwAjo15oE"
sheet = client.open_by_key(sheet_id).sheet1

def listenerCount(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    listener_div = soup.find('div', class_='card-footer d-block text-muted')

    if listener_div:
        listeners_text = listener_div.get_text(strip=True)
        listeners_number = listeners_text.split(' ')[0]
        return int(listeners_number)
    
    return None

def record_listeners():
    url = "http://dir.xiph.org/search?q=wcfm"
    listeners = listenerCount(url)

    if listeners is not None:
        print(f"Number of listeners: {listeners}")

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        next_row = len(sheet.get_all_values()) + 1
        sheet.update(f'A{next_row}', [[listeners, timestamp]])
    else:
        print("Could not find the number of listeners.")
record_listeners()
