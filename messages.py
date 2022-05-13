import pandas as pd
from datetime import date
from twilio.rest import Client
import yagmail
import pymysql
import pandas as pd
import time


#Composes the message for the email/text
def compose(reminders):
    message = 'This is a reminder for the following:'
    for reminder in reminders:
        message += '\n' + reminder[0] + ' ' + reminder[1] + ' due on ' + reminder[2]
    return message
    
while True:
    #twilio info this cost about 1 cent feel free to test as much as you want. There is like $20 of credit in the account
    account_sid = 'ACf66f7695c009e9bbbe519101b053b246'
    auth_token = '6d673228c678d6c9e49c33c503368b05'
    client = Client(account_sid, auth_token)

    #connect to data base
    db = pymysql.connections.Connection(host='applicationhelper.cdmmorqiqhka.us-east-1.rds.amazonaws.com', user ='admin', password ='Dsci-551', database='applicationhelper')


    #today's date. This is how we know what to send
    today = date.today().strftime("%m/%d/%Y")

    #grab the data from SQL 
    query = 'select * from reminders WHERE date_to_send = "' + str(today) + '";'
    df = pd.read_sql(query, db, index_col='id')
    print(df)
    # df = pd.DataFrame(data, index=['date to send', 'due date', 'name', 'description', 'phone', 'email', 'method'])

    text = {}
    mail = {}

    #Creates entry for each unique phone number/email This is so that if someone signed up for a lot of reminders, it is consolidated into one message
    for index, row in df.iterrows():
        if row['method'] == 'phone':
            try:
                text[row['phone']].append([row['name'], row['description'], row['due_date']])
            except:
                text[row['phone']] = [[row['name'], row['description'], row['due_date']]]
        elif row['method'] == 'email':
            try:
                mail[row['email']].append([row['name'], row['description'], row['due_date']])
            except:
                mail[row['email']] = [[row['name'], row['description'], row['due_date']]]
    # print(text)
    # print(mail)         

    #send text message
    for number, items in text.items():
        message = compose(items)
        message = client.messages \
                        .create(
                            body=message,
                            from_='+17472943425',
                            to='+1' + str(number)
                        )
        print(message.sid)

    #send email
    for email, items in mail.items():
        message = compose(items)

        yag = yagmail.SMTP('dsci551reminders@gmail.com', 'Dsci-551')
        yag.send(
            to=email,
            subject="College Application reminders",
            contents=message, 
        )
    #sleep one day
    time.sleep(60*60*24)