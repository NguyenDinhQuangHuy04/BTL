import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Đọc dữ liệu
df = pd.read_csv('results.csv')

# Chuyển 'N/a' thành NaN để tính toán không bị lỗi
df.replace('N/a', np.nan, inplace=True)

# Chuyển tất cả cột số thành float (nếu có thể)
for col in df.columns:
    try:
        df[col] = df[col].astype(float)
    except:
        continue

# Lọc danh sách cột số (numeric)
exclude_cols = ['Name', 'Nation', 'Team', 'Position']
numeric_cols = [col for col in df.columns if col not in exclude_cols and pd.api.types.is_numeric_dtype(df[col])]

# Top 3 cao nhất / thấp nhất

with open('top_3.txt', 'w', encoding='utf-8') as f:
    for col in numeric_cols:
        f.write(f'\n==== {col} ====\n')
        # Bỏ NaN khi sort
        top3 = df[['Name','Team',col]].dropna(subset=[col]).sort_values(by=col, ascending=False).head(3)
        bottom3 = df[['Name','Team',col]].dropna(subset=[col]).sort_values(by=col, ascending=True).head(3)

        f.write('\nTop 3 highest:\n')
        f.write(top3.to_string(index=False))
        f.write('\n\nTop 3 lowest:\n')
        f.write(bottom3.to_string(index=False))
        f.write('\n\n')

print('Đã lưu file top_3.txt')

# Tính Median, Mean, Std (all + từng team)

summary_rows = []

# Cho toàn bộ
row_all = ['all']
for col in numeric_cols:
    row_all.extend([
        df[col].median(skipna=True),
        df[col].mean(skipna=True),
        df[col].std(skipna=True)
    ])
summary_rows.append(row_all)

# Cho từng đội
teams = df['Team'].dropna().unique()

for team in teams:
    df_team = df[df['Team'] == team]
    row = [team]
    for col in numeric_cols:
        row.extend([
            df_team[col].median(skipna=True),
            df_team[col].mean(skipna=True),
            df_team[col].std(skipna=True)
        ])
    summary_rows.append(row)

# Lưu file results2.csv
columns = ['Team']
for col in numeric_cols:
    columns.extend([f'Median_{col}', f'Mean_{col}', f'Std_{col}'])

df_summary = pd.DataFrame(summary_rows, columns=columns)
df_summary.to_csv('results2.csv', index=False)

print('Đã lưu file results2.csv')

# Vẽ biểu đồ histogram (Chỉ 3 attack + 3 defense)

# Chỉ số tấn công và phòng thủ được chọn
attack_cols = ['Goals', 'Assists', 'xG']
defense_cols = ['Tkl', 'Blocks', 'Int']
selected_cols = attack_cols + defense_cols

os.makedirs('histograms', exist_ok=True)

for col in selected_cols:
    if col not in df.columns:
        print(f"Cột {col} không tồn tại trong dữ liệu — bỏ qua")
        continue

    plt.figure(figsize=(8,5))
    plt.hist(df[col].dropna(), bins=20, color='blue', alpha=0.7)
    plt.title(f'Distribution of {col} (All players)')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(f'histograms/{col}_all.png')
    plt.close()

    for team in teams:
        df_team = df[df['Team'] == team]
        plt.figure(figsize=(8,5))
        plt.hist(df_team[col].dropna(), bins=20, color='green', alpha=0.7)
        plt.title(f'Distribution of {col} ({team})')
        plt.xlabel(col)
        plt.ylabel('Frequency')
        plt.tight_layout()
        filename = f'histograms/{col}_{team.replace("/", "-")}.png'
        plt.savefig(filename)
        plt.close()

print('Đã vẽ xong histogram cho 6 chỉ số (thư mục histograms)')

# Tìm đội có giá trị cao nhất cho từng chỉ số

team_best = {}

for col in numeric_cols:
    team_avg = df.groupby('Team')[col].mean()
    best_team = team_avg.idxmax()
    best_value = team_avg.max()
    team_best[col] = (best_team, best_value)

# Lưu bảng tổng hợp đội mạnh nhất theo từng chỉ số
with open('team_best_stats.txt', 'w', encoding='utf-8') as f:
    for stat, (team, value) in team_best.items():
        f.write(f'{stat}: Best team = {team} | Avg = {value}\n')

print('Đã lưu file team_best_stats.txt (thống kê đội mạnh nhất mỗi chỉ số)')

# Xác định đội toàn diện nhất

# Tính điểm mỗi đội (số lần đứng đầu ở các chỉ số)
team_score = {}

for col in numeric_cols:
    team_avg = df.groupby('Team')[col].mean()
    best_team = team_avg.idxmax()
    if pd.notna(best_team):
        team_score[best_team] = team_score.get(best_team, 0) + 1

# Đội có điểm cao nhất
best_overall_team = max(team_score, key=team_score.get)
best_overall_score = team_score[best_overall_team]

# Ghi kết quả vào cuối file top_3.txt
with open('top_3.txt', 'a', encoding='utf-8') as f:
    f.write('\n' + '='*40 + '\n')
    f.write(f'\nĐỘI TOÀN DIỆN NHẤT (THE BEST OVERALL TEAM)\n')
    f.write(f'\n{best_overall_team} với tổng điểm {best_overall_score} (số lần đứng đầu chỉ số)\n')
    f.write('\nChi tiết điểm từng đội:\n')
    for team, score in sorted(team_score.items(), key=lambda x: x[1], reverse=True):
        f.write(f'{team}: {score} điểm\n')

print(f'Đội toàn diện nhất là {best_overall_team} (đã ghi vào top_3.txt)')