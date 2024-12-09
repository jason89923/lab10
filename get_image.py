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

# 固定Y軸範圍為0~100
y_min = 0
y_max = 100

# 設定圖片尺寸
img_width = 800
img_height = 600

# 建立白色背景的圖片
img = Image.new("RGB", (img_width, img_height), "white")
draw = ImageDraw.Draw(img)

# 留一些邊界空間
padding_left = 50
padding_right = 50
padding_top = 50
padding_bottom = 50

plot_width = img_width - padding_left - padding_right
plot_height = img_height - padding_top - padding_bottom

# 將溫度數據縮放至圖表範圍內(0~100)
def scale_temp_to_y(temp):
    # y座標0在上方，所以要反轉
    if y_max == y_min:
        return img_height//2
    return padding_top + plot_height - int((temp - y_min)/(y_max - y_min)*plot_height)

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

# 載入字型(若無法載入，則使用預設)
title_font = None
label_font = None
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
    label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
except:
    pass

# 繪製標題
draw.text((img_width//2 - 100, 10), "Temperature Over Time", fill="black", font=title_font)

# 加入Y軸標籤(刻度)
# 例如每20度一個刻度：0, 20, 40, 60, 80, 100
y_ticks = [0, 20, 40, 60, 80, 100]
for val in y_ticks:
    y_pos = scale_temp_to_y(val)
    # 繪製刻度線
    draw.line((padding_left-5, y_pos, padding_left, y_pos), fill="black")
    # 繪製刻度值
    draw.text((padding_left-45, y_pos-7), f"{val}", fill="black", font=label_font)

# 加入X軸標籤(刻度)
num_x_ticks = min(len(times), 6)  # 最多顯示6個X刻度
if len(times) > 1:
    step = (len(times)-1) / (num_x_ticks-1)
else:
    step = 1

for i in range(num_x_ticks):
    idx = int(round(i*step))
    x_pos = padding_left + idx*x_step
    # 繪製刻度線
    draw.line((x_pos, img_height - padding_bottom, x_pos, img_height - padding_bottom+5), fill="black")
    # 顯示時間(可依需求格式化)
    time_label = str(times[idx])
    draw.text((x_pos-20, img_height - padding_bottom + 10), time_label, fill="black", font=label_font)

# 將圖片儲存成檔案
img.save("temperature.png")

print("圖片已生成：temperature.png")
