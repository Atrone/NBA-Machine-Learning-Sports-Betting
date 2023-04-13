import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Run the shell script
from email.mime.text import MIMEText

# For cmd.exe (Command Prompt)
subprocess.run(["cmd.exe", "/c", "job.bat"], check=True)

# Email settings
from_email = "blockbits30@gmail.com"
to_email = "anthony.teixeira55@gmail.com"
subject = "Python script output"
body = "Please find the attached output.txt file."
smtp_server = "smtp.gmail.com"
smtp_port = 587  # or 465, depending on your server
smtp_user = "blockbits30@gmail.com"
smtp_password = os.environ.get("emailpwd")

# Compose email
msg = MIMEMultipart()
msg["From"] = from_email
msg["To"] = to_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

# Attach the output file
filename = "output.txt"
attachment = open(filename, "rb")
part = MIMEBase("application", "octet-stream")
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename= {filename}")
msg.attach(part)

# Send email
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(smtp_user, smtp_password)
text = msg.as_string()
server.sendmail(from_email, to_email, text)
server.quit()

print("Email sent successfully.")
