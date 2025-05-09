from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unicodedata

# Mở trình duyệt
driver = webdriver.Chrome()
main_data = []
header_saved = False
header = []

# Lặp qua các trang chuyển nhượng Premier League
for page in range(1, 23):
    if page == 1:
        url = 'https://www.footballtransfers.com/us/players/uk-premier-league'
    else:
        url = f'https://www.footballtransfers.com/us/players/uk-premier-league/{page}'
    
    driver.get(url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, 'table'))
    )
    
    html = driver.page_source
    soup = bs(html, 'html.parser')
    table_link = soup.find('table')
    
    if table_link:
        if not header_saved:
            header_link = table_link.find('thead', class_='m-hide')
            if header_link:
                header = [th.text.strip() for th in header_link.find_all('th')]
                header_saved = True

        players = table_link.find_all('tr')
        for player in players:
            row = []

            # Cột Skill / Pot
            skill = player.find('div', class_='table-skill__skill')
            pot = player.find('div', class_='table-skill__pot')
            if skill and pot and skill.text.strip() and pot.text.strip():
                row.append(skill.text.strip() + '/' + pot.text.strip())
            else:
                row.append('N/A')

            # Tên cầu thủ
            name = player.find('span', class_='d-none')
            row.append(name.text.strip() if name and name.text.strip() else 'N/A')

            # Tuổi
            age = player.find('td', class_='m-hide age')
            row.append(age.text.strip() if age and age.text.strip() else 'N/A')

            # CLB
            team = player.find('span', class_='td-team__teamname')
            row.append(team.text.strip() if team and team.text.strip() else 'N/A')

            # Giá trị chuyển nhượng
            price = player.find('td', class_='text-center')
            row.append(price.text.strip() if price and price.text.strip() else 'N/A')

            # Lưu lại nếu có tên cầu thủ
            if row[1] != 'N/A':
                main_data.append(row)

    time.sleep(2)

driver.quit()

# Lưu file CSV tạm thời
if main_data and header:
    transfer_df_raw = pd.DataFrame(main_data, columns=header)
    transfer_df_raw = transfer_df_raw[transfer_df_raw['Skill / pot'] != 'N/A']
    transfer_df_raw = transfer_df_raw.drop(columns=['Skill / pot'])
    transfer_df_raw = transfer_df_raw.rename(columns={'ETV': 'Price'})
    transfer_df_raw.to_csv('temp_value.csv', index=False)

# Hàm chuẩn hóa tên cầu thủ
def normalize_name(name):
    if pd.isna(name):
        return ''
    name = name.strip()
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
    return name.lower()

# Đọc dữ liệu thống kê cầu thủ từ file result.csv
stats_df = pd.read_csv('result.csv')

# Đổi tên một số cầu thủ cho khớp
transfer_df = pd.read_csv('temp_value.csv')
transfer_df['Player'] = transfer_df['Player'].replace({
    'Rasmus Winther Højlund': 'Rasmus Højlund',
    'Idrissa Gueye': 'Idrissa Gana Gueye',
    'Manuel Ugarte': 'Manuel Ugarte Ribeiro',
    'Omari Giraud-Hutchinson': 'Omari Hutchinson',
    'Rayan Aït Nouri': 'Rayan Ait-Nouri',
    'Heung-min Son': 'Son Heung-min',
    'Victor Kristiansen': 'Victor Bernth Kristiansen'
})

# Chuẩn hóa tên để so sánh
stats_df['_Player_'] = stats_df['Name'].apply(normalize_name)
transfer_df['_Player_'] = transfer_df['Player'].apply(normalize_name)

# Chuyển đổi phút thi đấu và lọc theo điều kiện > 900 phút
stats_df['Min'] = stats_df['Minutes'].astype(str).str.replace(',', '').astype(float)
player_to_keep = stats_df[stats_df['Min'] > 900]['_Player_'].tolist()

# Lọc danh sách giá trị chuyển nhượng tương ứng
transfer_df = transfer_df[transfer_df['_Player_'].isin(player_to_keep)]
transfer_df = transfer_df.drop(columns=['_Player_'])

# Lưu kết quả cuối cùng
transfer_df.to_csv('transfer_value.csv', index=False)