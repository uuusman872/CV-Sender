import tabula as tb
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import contentmanager, encoders
import CONSTANTS

# Import all the important libraries

def read_pdf_file():
    # tb.convert_into("1657827244782.pdf", "output.csv", output_format="csv", pages='all')
    df = pd.read_csv("output.csv")
    return df



hr_emails = []
df = read_pdf_file()
for web in df.CONTACT:
    if isinstance(web, str):
        if "," in web:
            for i in web.split(","):
                if "@" in i:
                    hr_emails.append(str.strip(i))
        else:
            if "@" in web:
                if '/' in web:
                    web = web.replace('/', "")
                hr_emails.append(str.strip(web))


# This function will convert the html template and send it to email to make your email look pretty
def read_template(template_name):
    with open(template_name, 'r') as file:
        content = file.read()
        return content


def sendEmail(email, password, send_to, body, file_name, file_path):
    fromaddr = email
    toaddr = send_to
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "I am a developer who needs a job"
    # Change the template name here if requried
    body = read_template("index.html")
    msg.attach(MIMEText(body, 'html'))
    filename = file_name
    attachment = open(file_path, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


def main():
    # finally we can send email to all the hrs of comapny we extracted
    for mail in hr_emails:
        try:
            print(f"Sending Your cv to {mail}")
            sendEmail(CONSTANTS.EMAIL, CONSTANTS.PASSWORD, mail, "Full Stack Developer", "mycv.pdf", "MuhammadUsman.pdf")
        except:
            print(f"Unable to send to {mail}")



# make sure that u have your cv in the project folder 

# U need to also set up your gmail for smtp follow the instruction on link
# https://www.youtube.com/watch?v=qpAI5qZR9ms