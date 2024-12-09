import sqlite3
from PIL import Image, ImageDraw, ImageFont

# 從資料庫中取得資料
conn = sqlite3.connect('../lab09/temperature.db')
cursor = conn.cursor()
cursor.execute('SELECT time, temperature FROM temperature_table')
data = cursor.fetchall()
conn.close()

if not data:
    print("資料庫無資料，無法繪製圖表。")
    exit()

times = [row[0] for row in data]
temps = [row[1] for row in data]

max_temp = max(temps)
min_temp = min(temps)

# 設定圖片尺寸
img_width = 800
img_height = 600

# 建立白色背景的圖片
img = Image.new("RGB", (img_width, img_height), "white")
draw = ImageDraw.Draw(img)

# 簡單計算點的座標
# 留一些邊界空間
padding_left = 50
padding_right = 50
padding_top = 50
padding_bottom = 50

plot_width = img_width - padding_left - padding_right
plot_height = img_height - padding_top - padding_bottom

# 將溫度數據縮放至圖表範圍內
def scale_temp_to_y(temp):
    if max_temp == min_temp:
        return img_height//2
    # y座標0在上方，所以要反轉
    return padding_top + plot_height - int((temp - min_temp)/(max_temp - min_temp)*plot_height)

# 將每個點在X軸均勻分佈
x_step = plot_width / (len(temps) - 1) if len(temps) > 1 else 0

points = []
for i, t in enumerate(temps):
    x = padding_left + i*x_step
    y = scale_temp_to_y(t)
    points.append((x, y))

# 繪製座標軸 (簡易版)
# X 軸
draw.line((padding_left, img_height - padding_bottom, img_width - padding_right, img_height - padding_bottom), fill="black")
# Y 軸
draw.line((padding_left, padding_top, padding_left, img_height - padding_bottom), fill="black")

# 繪製折線
for i in range(len(points) - 1):
    draw.line((points[i], points[i+1]), fill="blue", width=2)

# 繪製標題及標籤 (需要字體檔案，如無可省略或使用系統預設)
# 若環境中無法指定字型路徑，可不使用字型參數
title_font = None
try:
    # 試圖使用一個系統字體 (可自行調整路徑)
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
except:
    pass

draw.text((img_width//2 - 100, 10), "Temperature Over Time", fill="black", font=title_font)

# 將圖片儲存成檔案
img.save("temperature.png")

print("圖片已生成：temperature.png")
