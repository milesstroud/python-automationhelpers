#IMPORTS
import datetime as dt
import praw #Reddit API Package (https://praw.readthedocs.io/en/latest/index.html)
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from email.message import EmailMessage
import datetime as dt
from datetime import date


#Eail Details for Sending Email
sender_email = "stroudfake1@gmail.com"
receiver_email = "stroudfake1@gmail.com"
email_password = input("Type your EMAIL password.")
password = input("Please type your password.")


#PRAW Read Only Instance (https://praw.readthedocs.io/en/latest/getting_started/quick_start.html)
reddit = praw.Reddit(client_id = '',
                     client_secret = '',
                     user_agent = '')

#Dictionary to store all of the data retrieved
master_dict = {"title": [],
               "bodytext": []}


#Defining functions to build the master dictionary using data from each subreddit
def Pop():
    popreddit = reddit.subreddit('Popheads') #Defining subreddit of choice (first, popheads)
    popemergencies = popreddit.top(limit = 5, time_filter = 'day') #Retrieving the top 5 posts within the last 24hours
    for post in popemergencies:
        master_dict['title'].append(post.title) #Adding values for the "title" key
        master_dict['bodytext'].append(post.selftext) #Adding values for the "bodytext" key

#Repeat for Subs of Choice!
def HipHop():
    hiphopheads = reddit.subreddit('hiphopheads')
    HHHNews = hiphopheads.top(limit=5, time_filter = 'day')
    for post in HHHNews:
        master_dict['title'].append(post.title)
        master_dict['bodytext'].append(post.selftext)

def PsychRock():
    psychrock = reddit.subreddit('psychedelicrock')
    psychnews = psychrock.top(limit=5, time_filter = 'day')
    for post in psychnews:
        master_dict['title'].append(post.title)
        master_dict['bodytext'].append(post.selftext)

#Calling each function to perform their duties before creating the email
Pop()
HipHop()
PsychRock()

#Not sure this is necessary, potentially helpful to convert the dictionary to a pandas dataframe
#master_dataframe = pd.DataFrame(master_dict)




#HTML Email
msg = EmailMessage()
#Defining "day" to be the proper day of the week using datetime
if dt.datetime.today().weekday() == 0: #datetime.today() returns an integer
    day = "Monday" #Beginning with 0, the integers correspond to days of the week 0-6 (Mon-Sun)
elif dt.datetime.today().weekday() == 1:
        day = "Tuesday"
elif dt.datetime.today().weekday() == 2:
    day = "Wednesday"
elif dt.datetime.today().weekday() == 3:
        day = "Thursday"
elif dt.datetime.today().weekday() == 4:
        day = "Friday"
elif dt.datetime.today().weekday() == 5:
        day = "Saturday"
elif dt.datetime.today().weekday() == 6:
        day = "Sunday"
else:
    print("Error Fetching Date")

msg['Subject'] = '%s, %s' % (day,date.today()) #Passing the proper day of the week to the subject line of the email
msg['From'] = sender_email
msg['To'] = receiver_email

msg.set_content('This is a plain test email')
msg.add_alternative("""\
<!DOCTYPE html>
<html>
	<body>
		<h1 style="color:SlateGray;"> Daily Reddit Music News </h1>
		<br>%s: %s<br>
		<br>%s: %s<br>
		<br>%s: %s<br>
		<br>%s: %s<br>
		<br>%s: %s<br>
		<br>%s: %s<br>
		<br>%s: %s<br>
	</body>
</html>
""" % (master_dict["title"][0],master_dict["bodytext"][0],
       master_dict["title"][1], master_dict["bodytext"][1],
       master_dict["title"][2], master_dict["bodytext"][2],
       master_dict["title"][3], master_dict["bodytext"][3],
       master_dict["title"][4], master_dict["bodytext"][4],
       master_dict["title"][5], master_dict["bodytext"][5],
       master_dict["title"][6], master_dict["bodytext"][6]), subtype='html') #Filling the 15 (5 for each subreddit) stri
# ngs

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, email_password)
        server.send_message(msg)

print(master_dict)
