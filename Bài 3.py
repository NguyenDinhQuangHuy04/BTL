import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Đọc và tiền xử lý dữ liệu
try:
    df = pd.read_csv('result.csv')
    
    # Chuyển đổi cột Minutes sang số (xử lý cả trường hợp có dấu phẩy)
    df['Minutes'] = df['Minutes'].astype(str).str.replace(',', '').astype(float)
    
    # Lọc cầu thủ có trên 90 phút
    df = df[df['Minutes'] > 90]
    players = df['Name'].tolist()
    print(f"Có {len(players)} cầu thủ đủ điều kiện (>90 phút)")
    
    # In kiểm tra 5 dòng đầu
    print("\nKiểm tra dữ liệu Minutes:")
    print(df['Minutes'].head())
    
except Exception as e:
    print(f"Lỗi khi đọc file: {e}")
    exit()

# Hàm crawl giá trị chuyển nhượng (giữ nguyên như trước)
def get_transfer_value(player_name):
    # ... (phần này giữ nguyên code gốc của bạn)
    pass

# Thu thập dữ liệu (giữ nguyên)
transfer_values = {}
for player in players:
    value = get_transfer_value(player)
    if value is not None:
        transfer_values[player] = value
    print(f"Đã xử lý {player}: {value if value else 'N/A'}")

# Thêm cột giá trị và lưu file
df['TransferValue(m)'] = df['Name'].map(transfer_values)
df.to_csv('players_with_transfer_values.csv', index=False)

print("\nĐã hoàn thành thu thập dữ liệu!")