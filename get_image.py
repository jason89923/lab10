import sqlite3
import matplotlib.pyplot as plt

# 使用 matplotlib 內建的 'ggplot' 樣式美化圖表
plt.style.use('ggplot')

# 連接到 SQLite 數據庫
conn = sqlite3.connect('../lab09/temperature.db')
cursor = conn.cursor()

# 從數據庫中擷取數據 (請確定資料表與欄位名稱正確)
cursor.execute('SELECT time, temperature FROM temperature_table')
data = cursor.fetchall()

# 關閉數據庫連接
conn.close()

# 分離 x 和 y 數據
x_data = [row[0] for row in data]
y_data = [row[1] for row in data]

# 建立一個較大的繪圖畫布，以增進可讀性
plt.figure(figsize=(10, 6))

# 繪製摺線圖：調整線條顏色、粗細和標記樣式
plt.plot(x_data, y_data, marker='o', color='steelblue', linewidth=2, markersize=6)

# 設定標題與軸標籤字型大小
plt.title('Line Chart from Temperature Data', fontsize=16, fontweight='bold')
plt.xlabel('Time', fontsize=14)
plt.ylabel('Temperature', fontsize=14)

# 若時間軸標籤過長，可考慮旋轉以方便閱讀
plt.xticks(rotation=45)

# 顯示格線
plt.grid(True, linestyle='--', alpha=0.7)

# 調整版面以避免標籤重疊
plt.tight_layout()

# 儲存圖表(解析度300 dpi)
plt.savefig('temperature.png', dpi=300)

# 如需在程式執行環境中顯示圖表，可加入：
# plt.show()
