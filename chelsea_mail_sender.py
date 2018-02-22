import smtplib 
from email_content import email_info

def send_email(formatted_time,teams_text):
	# formatting the email
	msg = 'Subject: Match Alert!\n' + formatted_time + '\r\n' + teams_text
	smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(email_info.from_email, email_info.from_email_password)
	smtpObj.sendmail(email_info.from_email, email_info.to_email, msg)
	smtpObj.quit()
	print('mail sent')