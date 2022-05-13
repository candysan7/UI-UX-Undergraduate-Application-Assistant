import streamlit as st
import pymysql
import pandas as pd
from datetime import date
from apps import qadd

def app():
    #Define the main page of website
    def main_page():

        #Sidebar
        st.sidebar.title("Feedback")
        st.sidebar.info(
            "This an open source project completed for USC DSCI 551 and we are very open to any **feedback** you have. You are more than welcome welcome to **contribute** your "
            "questions, concerns, and suggestions at "
            "[email](andyxian@usc.edu) or at our "
            "[github](https://github.com/candysan7). "
            # REFERENCE ----- (https://github.com/MarcSkovMadsen/awesome-streamlit). "
        )
        st.sidebar.title("About Us")
        st.sidebar.info(
            """
            This app is maintained by [Andy Xiang](https://www.linkedin.com/in/andy-xiang/) and [Preston Fong](https://www.linkedin.com/in/preston-fong-91686a128/). 
            Please feel free to reach out to us if you have any questions. 
            You can learn more about instiution at [www.usc.edu](https://www.usc.edu/).
        """)

        #Main Page
        st.title('Scholarship Search Engine and Tracker!')

        #builing form
        act = st.selectbox('Do You Have an ACT Score?', ['','Yes', 'No'])
        if act == 'Yes': 
            act = st.number_input('Enter Your ACT Score', 0, 36)
        else:
            act = 0
        major = st.selectbox('What is your major?', ['','Agriculture','Teaching', 'Math', 'Science', 'Engineering', 'Arts', 'History', 'Social Sciences', 'Veterinary' , 'Music', 'Other'])
        additionals = st.multiselect('Are you in any of the following groups?', ['','Homeless','Adopted/Foster Child/Orphan','Single Parent Household', 'LGBTQ+', 'First Generation', ' Immigrant', 'Native American', 'Female'])
        activism = st.selectbox('Have you engaged in activism?',['','Yes','No'])
        community = st.selectbox('Have you participated in community service?',['','Yes','No'])

        if st.button('Search Scholarship!'):
            if major == '' or activism == '' or community == '': 
                st.error('Form is incomplete')

            else:
                db = pymysql.connections.Connection(host='applicationhelper.cdmmorqiqhka.us-east-1.rds.amazonaws.com', user ='admin', password ='Dsci-551', database='applicationhelper')
                cursor = db.cursor()
                query = "SELECT DISTINCT * from scholarships WHERE " + qadd.qadd(additionals, major, act,  activism, community)
                cursor.execute(query)
                st.session_state['data'] = cursor.fetchall()
                st.session_state.runpage = results_page
                st.experimental_rerun()

    #Results page
    def results_page():
        #Query Database
        # st.write(st.session_state['query'])
        #Start Writing Page
        #Sidebar
        st.sidebar.title("Feedback")
        st.sidebar.info(
            "This an open source project completed for USC DSCI 551 and we are very open to any **feedback** you have. You are more than welcome welcome to **contribute** your "
            "questions, concerns, and suggestions at "
            "[email](andyxian@usc.edu) or at our "
            "[github](https://github.com/candysan7). "
            # REFERENCE ----- (https://github.com/MarcSkovMadsen/awesome-streamlit). "
        )
        st.sidebar.title("About Us")
        st.sidebar.info(
            """
            This app is maintained by [Andy Xiang](https://www.linkedin.com/in/andy-xiang/) and [Preston Fong](https://www.linkedin.com/in/preston-fong-91686a128/). 
            Please feel free to reach out to us if you have any questions. 
            You can learn more about instiution at [www.usc.edu](https://www.usc.edu/).
        """)
        if len(st.session_state['data']) == 0:
            st.sub('We could not find any scholarships for you.')
        else:
            st.header('Scholarship Results')

            #Method Section
            method = st.selectbox('How would you like to be notified?', ['','Email', 'Text'])
            if method == 'Email':
                email = st.text_input('Enter your Email')
            if method == 'Text':
                phone = st.text_input('Enter your Mobile Phone Number')

            #Display Results
            for item in st.session_state['data']:
                header = '[' + item[1] + '](' + item[7] + ')'
                st.subheader(header)
                with st.form(key=str(item[0])):
                    col1, col2 = st.columns(2)
                    deadline = 'Deadline: ' + item[4]
                    award = 'Award: $' + str(item[2])
                    col1.write(deadline)
                    col1.write(award)
                    rdate = col2.date_input('Set Reminder Date')
                    rdate = str(rdate.strftime("%#m/%#d/%Y"))

                    #Submit the reminder form
                    if col2.form_submit_button('Add to Reminders'):
                        if method == 'Email':
                            if '@' not in email or '.' not in email:
                                st.error('Email is invalid')
                            else:
                                db = pymysql.connections.Connection(host='applicationhelper.cdmmorqiqhka.us-east-1.rds.amazonaws.com', user ='admin', password ='Dsci-551', database='applicationhelper')
                                cursor = db.cursor()
                                query = 'INSERT INTO reminders (date_to_send,due_date,name,description,phone,email,method) VALUES ("' + rdate + '","' + item[4] + '","' +  item[1] + '", "" , "" , "' +  email + '","email");'
                                cursor.execute(query)
                                db.commit()
                                st.success('Successfully added into reminders!')
                        if method == 'Text':
                            if len(phone) != 10:
                                st.error('Phone Number is invalid')
                            else:
                                try:
                                    db = pymysql.connections.Connection(host='applicationhelper.cdmmorqiqhka.us-east-1.rds.amazonaws.com', user ='admin', password ='Dsci-551', database='applicationhelper')
                                    cursor = db.cursor()
                                    str(phone)
                                    query = 'INSERT INTO reminders (date_to_send,due_date,name,description,phone,email,method) VALUES ("' + rdate + '","' + item[4] + '","' +  item[1] + '" ,"" , ' + phone + ',"","phone");'
                                    cursor.execute(query)
                                    db.commit()
                                    st.success('Successfully added into reminders!')
                                except:
                                    st.error('Phone Number is invalid')
                        if method == '':
                                st.error('No Method')
                    with st.expander('Details:'):
                        st.write(item[6])
        #Return button
        if st.button('Return to Form'):
            st.session_state.runpage = main_page
            st.experimental_rerun()


    #Setup session states and run session
    if 'runpage' not in st.session_state:
        st.session_state.runpage = main_page
        st.experimental_rerun()

    if 'page' not in st.session_state or st.session_state.page != 'scholarships':
        st.session_state.page = 'scholarships'
        st.session_state.runpage = main_page
        st.experimental_rerun()

    else:
        st.session_state.runpage()



