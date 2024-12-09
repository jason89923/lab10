import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# 在此填入你的Gmail地址與應用程式密碼
email_address = "max0605123789@gmail.com"
app_password = "auvs jqaw madz rpjk"  # 應用程式密碼
Subject = "嵌入式系統第XX組"
body = "尊敬的老師您好：\
\n\n　　請恕學生冒昧來信。附件中附上一張圖片，圖中展示了特定時段內的氣溫變化關係。透過該圖表，您可以清楚地看到各時間點的溫度起伏，以利了解趨勢並進行相關分析。\
若您對此資料有任何意見或需要進一步說明，敬請指教。學生必將竭誠配合與改進。\
\n\n敬請\
\n  道安"

# 收件者 (不可修改)
to_email = "embedding20240909@gmail.com"

# 建立郵件主體
message = MIMEMultipart()
message["From"] = email_address
message["To"] = to_email
message["Subject"] = Subject  # 標題

# 郵件文字內容
message.attach(MIMEText(body, "plain"))

# 讀取圖片並建立附件
with open("temperature.png", "rb") as f:
    img_data = f.read()
    image_attachment = MIMEImage(img_data)
    image_attachment.add_header('Content-Disposition', 'attachment; filename="image.jpg"')
    message.attach(image_attachment)

# 使用Gmail的SMTP_SSL通道連線至465埠
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    # 使用應用程式密碼登入
    server.login(email_address, app_password)
    # 寄出郵件
    server.sendmail(email_address, to_email, message.as_string())

print("信件已成功寄出！")
