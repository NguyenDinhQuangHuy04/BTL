from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import pandas as pd

# Hàm kiểm tra và chuyển đổi dữ liệu
def validdata(n):
    if n == '' or n is None:
        return "N/a"
    try:
        return float(n)
    except ValueError:
        return "N/a"

# Hàm lấy dữ liệu từ web 
def GetDataFromWeb(url, Xpath_player, Data_name):
    service = Service(ChromeDriverManager().install())
    driver1 = webdriver.Chrome(service=service)
    driver1.get(url)
    player_list = []
    try:
        WebDriverWait(driver1, 10).until(EC.presence_of_element_located((By.XPATH, Xpath_player)))
        table_element = driver1.find_element(By.XPATH, Xpath_player)
        html_table = table_element.get_attribute('outerHTML')
        soup = bs(html_table, 'html.parser')
        table = soup.find('table')
        if table:
            for row in table.find_all('tr'):
                cols = row.find_all('td')
                data = []
                for id, play in enumerate(cols[:-1]):
                    if id == 1:
                        a = play.text.strip().split()
                        data.append(a[1] if len(a) == 2 else play.text.strip())
                    else:
                        s = play.text.strip()
                        if id >= 4:
                            s = s.replace(",", "")
                            s = validdata(s)
                        data.append(s)
                if len(data) != 0: player_list.append(data)
    finally:
        driver1.quit()
        print("Finish " + Data_name)
    return player_list
    
# stats_standard
url = "https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats"
Xpath_player = '//*[@id="stats_standard"]'
Data_name = "Standard"
list = GetDataFromWeb(url, Xpath_player, Data_name)

player_list = []
for p in list:
    try:
        Name, Nation, Position, Team, Age = p[0:5]
        mp, starts, min = p[6:9]
        Gls, Ast, ycard, rcard = p[9:13]
        xG, xAG = p[18], p[20]
        PrgC, PrgP, PrgR = p[22:25]
        Gls90, Ast90, xG90, xAG90 = p[25], p[26], p[30], p[31]
        if min > 90:
            player_list.append([Name, Nation, Team, Position, Age, mp, starts, min, Gls, Ast, ycard, rcard, xG, xAG, PrgC, PrgP, PrgR, Gls90, Ast90, xG90, xAG90])
    except IndexError:
        break

cols_player = ['Name','Nation','Team','Position','Age','Matches Played','Starts','Min','Goals','Assists','Yellow Cards','Red Cards','xG','xAG','PrgC','PrgP','PrgR','Gls90','Ast90','xG90','xAG90']
df_player = pd.DataFrame(player_list, columns=cols_player)

# stats_keeper
url = "https://fbref.com/en/comps/9/2024-2025/keepers/2024-2025-Premier-League-Stats"
Xpath_player = '//*[@id="stats_keeper"]'
Data_name = "Keepers"
list = GetDataFromWeb(url, Xpath_player, Data_name)

keeper_list = []
for p in list:
    Name = p[0]
    Team = p[3]
    GA90, Save_perc, CS_perc, PKSave_perc = p[11], p[14], p[16], p[20]
    keeper_list.append([Name,Team,GA90, Save_perc, CS_perc, PKSave_perc])
df_keepers = pd.DataFrame(keeper_list, columns=['Name','Team','GA90', 'Save%', 'CS%', 'PK Save%'])

# stats_shooting
url = "https://fbref.com/en/comps/9/2024-2025/shooting/2024-2025-Premier-League-Stats"
Xpath_player = '//*[@id="stats_shooting"]'
Data_name = "Shooting"
list = GetDataFromWeb(url, Xpath_player, Data_name)

Shooting_list = []
for p in list:
    Name = p[0]
    Team = p[3]
    SoT_perc, SoT_90, G_Sh, Dist = p[10:14]
    Shooting_list.append([Name,Team, SoT_perc, SoT_90, G_Sh, Dist])
df_shooting = pd.DataFrame(Shooting_list, columns=['Name','Team','SoT%','SoT/90','G/Sh','Dist'])

# stats_passing
url = "https://fbref.com/en/comps/9/2024-2025/passing/2024-2025-Premier-League-Stats"
Xpath_player = '//*[@id="stats_passing"]'
Data_name = "Passing"
list = GetDataFromWeb(url, Xpath_player, Data_name)

Passing_list = []
for p in list:
    Name = p[0]
    Team = p[3]
    Cmp, Att, Cmp_perc, TotDist = p[7:11]
    sCmp_perc, mCmp_perc, lCmp_perc = p[13], p[16], p[19]
    KP, a1_3, PPA, CrsPA, PrgP = p[24:29]
    Passing_list.append([Name,Team,Cmp, Cmp_perc, TotDist, sCmp_perc, mCmp_perc, lCmp_perc, KP, a1_3, PPA, CrsPA, PrgP])
df_Passing = pd.DataFrame(Passing_list, columns=['Name','Team','Cmp','Cmp%','TotDist','Short Cmp%','Med Cmp%','Long Cmp%','KP','1/3','PPA','CrsPA','PrgP'])

# stats_gca
url = "https://fbref.com/en/comps/9/2024-2025/gca/2024-2025-Premier-League-Stats"
Xpath_player = '//*[@id="stats_gca"]'
Data_name = "GCA"
list = GetDataFromWeb(url, Xpath_player, Data_name)

GCA_list = []
for p in list:
    Name = p[0]
    Team = p[3]
    SCA, SCA90, GCA, GCA90 = p[7], p[8], p[16], p[17]
    GCA_list.append([Name,Team,SCA,SCA90,GCA,GCA90])
df_GCA = pd.DataFrame(GCA_list, columns=['Name','Team','SCA','SCA90','GCA','GCA90'])

# stats_defense
url = "https://fbref.com/en/comps/9/2024-2025/defense/2024-2025-Premier-League-Stats"
Xpath_player = '//*[@id="stats_defense"]'
Data_name = "Defense"
list = GetDataFromWeb(url, Xpath_player, Data_name)

Defense_list = []
for p in list:
    Name = p[0]
    Team = p[3]
    Tkl, TklW, Att, Lost, Blocks, Sh, Pass, Int = p[7], p[8], p[13], p[16], p[17], p[18], p[19], p[20]
    Defense_list.append([Name,Team,Tkl,TklW,Att,Lost,Blocks,Sh,Pass,Int])
df_defense = pd.DataFrame(Defense_list, columns=['Name','Team','Tkl','TklW','Att','Lost','Blocks','Sh','Pass','Int'])

# stats_possession
url = "https://fbref.com/en/comps/9/2024-2025/possession/2024-2025-Premier-League-Stats"
Xpath_player = '//*[@id="stats_possession"]'
Data_name = "Possession"
list = GetDataFromWeb(url, Xpath_player, Data_name)

Possession_list = []
for p in list:
    Name = p[0]
    Team = p[3]
    Touches, DefPen, Def3rd, Mid3rd, Att3rd, AttPen = p[7:13]
    Att, Succ_perc, Tkld_perc = p[13], p[15], p[17]
    Carries, ProDist, ProgC, a1_3, CPA, Mis, Dis = p[18:25]
    Rec, PrgR = p[25:27]
    Possession_list.append([Name,Team,Touches,DefPen,Def3rd,Mid3rd,Att3rd,AttPen,Att,Succ_perc,Tkld_perc,Carries,ProDist,ProgC,a1_3,CPA,Mis,Dis,Rec,PrgR])
df_possession = pd.DataFrame(Possession_list, columns=['Name','Team','Touches','Def Pen','Def 3rd','Mid 3rd','Att 3rd','Att Pen','Att','Succ%','Tkld%','Carries','ProDist','ProgC','1/3','CPA','Mis','Dis','Rec','PrgR'])

# stats_misc
url = "https://fbref.com/en/comps/9/2024-2025/misc/2024-2025-Premier-League-Stats"
Xpath_player = '//*[@id="stats_misc"]'
Data_name = "Misc"
list = GetDataFromWeb(url, Xpath_player, Data_name)

Misc_list = []
for p in list:
    Name = p[0]
    Team = p[3]
    Fls, Fld, Off, Crs, Recov, Won, Lost, Won_perc = p[10:14] + p[18:22]
    Misc_list.append([Name,Team,Fls,Fld,Off,Crs,Recov,Won,Lost,Won_perc])
df_misc = pd.DataFrame(Misc_list, columns=['Name','Team','Fls','Fld','Off','Crs','Recov','Won','Lost','Won%'])

# Merge tất cả lại
dataframes = [df_keepers,df_shooting,df_Passing, df_GCA,df_defense,df_possession, df_misc]
df_merged = df_player
for df in dataframes:
    df_merged = pd.merge(df_merged,df, on = ['Name','Team'], how = 'left')

# Sắp xếp và lưu
df_merged['First Name'] = df_merged['Name'].apply(lambda x: x.split()[0])
df_sorted = df_merged.sort_values(by=['First Name', 'Age'], ascending=[True, False])
df_sorted = df_sorted.drop(columns=['First Name'])
df_sorted.to_csv('results.csv', index=False, na_rep='N/a')

print('Du lieu da duoc luu vao file results.csv')