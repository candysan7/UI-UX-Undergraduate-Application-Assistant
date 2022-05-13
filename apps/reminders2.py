import streamlit as st
import pymysql
import pandas as pd
from datetime import date

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
        st.title('Reminders Tracker')
        with st.form(key='bkey'):
            email = st.text_input('Enter your email')
            phone = st.text_input('Enter your Mobile Phone Number')

            #Make Query
            if st.form_submit_button('Submit'):
                if  ('@' not in email or '.' not in email) and  (len(phone) != 10 or phone.isdigit() == False):
                    st.error('Form is incomplete')
                else:
                    if len(phone) == 10 and ('@' in email or '.' in email):
                        query = 'SELECT DISTINCT * FROM reminders WHERE phone = ' + phone + ' or email = "' + email + '";'
                    elif len(phone) != 10:
                        query = 'SELECT DISTINCT * FROM reminders WHERE email = "' + email + '";'
                    else:
                        query = 'SELECT DISTINCT * FROM reminders WHERE phone = ' + phone + ';'
                    st.session_state['query'] = query
                    st.session_state.runpage = results_page
                    st.experimental_rerun()


    def results_page():
        #sidebar
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
        #Query Database
        db = pymysql.connections.Connection(host='applicationhelper.cdmmorqiqhka.us-east-1.rds.amazonaws.com', user ='admin', password ='Dsci-551', database='applicationhelper')
        cursor = db.cursor()
        cursor.execute(st.session_state['query'])
        data = cursor.fetchall()

        #Make page page
        if len(data) == 0:
            st.title('You have no reminders set up')
            st.subheader('Checkout the Colleges and Scholarship page to set up reminders')
        else:
            st.title('Your Reminders!')
            for item in data:
                st.markdown("""---""")
                st.subheader(item[3])
                col1, col2, col3 = st.columns(3)
                send = 'Reminder Date: ' + item[1]
                due = 'Due Date: ' + item[2]
                method = 'Method: ' + item[7]
                col1.write(send)
                col2.write(due)
                col3.write(method)
                if col3.button('Remove', key=str(item[0])):
                    query = 'DELETE FROM reminders WHERE id = '+ str(item[0]) + ';'
                    cursor.execute(query)
                    db.commit()
                    st.success('Successfully removed from reminders')
        #Return button
        if st.button('Return to Form'):
            st.session_state.runpage = main_page
            st.experimental_rerun()            

    if 'runpage' not in st.session_state:
        st.session_state.runpage = main_page
        st.experimental_rerun()

    if 'page' not in st.session_state or st.session_state.page != 'reminders':
        st.session_state.page = 'reminders'
        st.session_state.runpage = main_page
        st.experimental_rerun()

    else:
        st.session_state.runpage()