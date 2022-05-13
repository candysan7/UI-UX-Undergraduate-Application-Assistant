import pandas as pd
import streamlit as st
import time 
import pymysql
import pandas as pd


def app():
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

        # CSS to inject contained in a string
        hide_dataframe_row_index = """
                    <style>
                    .row_heading.level0 {display:none}
                    .blank {display:none}
                    </style>
                    """
        # Inject CSS with Markdown
        st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)



        #Main Page
        st.title('College Recommender and Tracker!')

        #Input Form
        gpa = st.number_input("Enter Your Weighted GPA", min_value=0.0, max_value=5.0, step=1e-2, format="%.2f")
        sat = st.selectbox('Do You Have an SAT Score?', ['','Yes', 'No'])
        if sat == 'Yes': 
            sat = st.number_input('Enter Your SAT Score', 0, 1600)
            act = 'No'
        if sat == 'No':
            act = st.selectbox('Do You Have an ACT Score?', ['','Yes', 'No'])
            if act == 'Yes': 
                act = st.number_input('Enter Your ACT Score', 0, 36)
        city =st.text_input('City')
        zip_code = st.text_input('Zip Code')
        regional = st.selectbox('Have You Won Any Regional Awards?',['','Yes','No'])
        if regional == 'Yes':
            regional_slider = st.select_slider('Number of Regional Awards Won', ['1', '2', '3','4','5','6','7'])
        national = st.selectbox('Have You Won Any National Awards?',['','Yes','No'])
        if national == 'Yes':
            national_slider = st.select_slider('Number of National Awards Won', ['1', '2', '3','4','5','6','7'])
        if regional == 'No' or national == 'No': 
            regional_slider = 0 
            national_slider = 0 
        if st.button('Find My Colleges!'):
            if gpa == 0 or sat == '' or regional == '' or national == '': 
                st.error('Form is Incomplete')
            else:
                #Matching Algorithm
                gpasat = 0
                gpaact = 0
                if sat == 'Yes': 
                    gpasat = 3.2 + (sat - 900)*.0014
                    gpa = (gpa + gpasat)/2
                if act == 'Yes':    
                    gpaact = 3.2 + (act - 19)*.06
                    gpa = (gpa + gpasat)/2
                gpa_upper = gpa + 0.5 + int(regional_slider)*0.25 + int(national_slider)*0.05
                gpa_lower = gpa - 0.5 + int(regional_slider)*0.25 + int(national_slider)*0.05
                query = "SELECT * from appcolleges WHERE Weighted_GPA> "+ str(gpa_lower) + " AND Weighted_GPA< " + str(gpa_upper) + " LIMIT 5"
                db = pymysql.connections.Connection(host='applicationhelper.cdmmorqiqhka.us-east-1.rds.amazonaws.com', user ='admin', password ='Dsci-551', database='applicationhelper')
                cursor = db.cursor()
                cursor.execute(query)
                data = cursor.fetchall()
                st.session_state['data'] = data
                st.session_state.runpage = results_page
                st.experimental_rerun()

        #### DISAYING RESULTS #### 
    def results_page():
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
            st.header('Sorry, we could not find a match for you.')
        else:
            results = st.title('Here are your top matches:')

            #Method Section
            method = st.selectbox('How would you like to be notified?', ['','Email', 'Text'])
            if method == 'Email':
                email = st.text_input('Enter your Email')
            if method == 'Text':
                phone = st.text_input('Enter your Mobile Phone Number')


            for item in st.session_state['data']:
                st.subheader(item[1].replace("/n", ' '))
                with st.form(key=str(item[0])):
                    col1, col2 = st.columns(2)
                    stype = 'Type : ' + item[6]
                    try:
                        early =  'Early Action Deadline: ' + item[7]
                    except:
                        continue
                    regular = 'Regular Decision Deadline: ' + item[8]
                    cost = 'Average Cost: ' + item[9]
                    grad = 'Graduation Rate: ' + item[11]
                    col1.write(stype)
                    if len(item[7]) >  2:
                        col1.write(early)
                    col1.write(regular)
                    col1.write(cost)
                    col1.write(grad)
                    rdate = col2.date_input('Set Reminder Date')
                    rdate = str(rdate.strftime("%#m/%#d/%Y"))
                    deadline = col2.selectbox('Which Deadline?', ['','Early Action', 'Regular Decision'])
                    if deadline == 'Early Action':
                        deadlinedate = item[7]
                    else:
                        deadlinedate = item[8]
                    if col2.form_submit_button('Add to Reminders'):
                        if deadline == 'Early Action' and len(item[7]) < 2:
                            st.error('No Early Action')
                        elif deadline == '': 
                            st.error('Form Incomplete')
                        elif method == 'Email':
                                if '@' not in email or '.' not in email:
                                    st.error('Email is invalid')
                                else:
                                    db = pymysql.connections.Connection(host='applicationhelper.cdmmorqiqhka.us-east-1.rds.amazonaws.com', user ='admin', password ='Dsci-551', database='applicationhelper')
                                    cursor = db.cursor()
                                    query = 'INSERT INTO reminders (date_to_send,due_date,name,description,phone,email,method) VALUES ("' + rdate + '","' + deadlinedate + '","' +  item[1] + '","' + deadline + '","","' +  email + '","email");'
                                    cursor.execute(query)
                                    db.commit()
                                    st.success('Successfully added into reminders!')
                        elif method == 'Text':
                            if len(phone) != 10:
                                st.error('Phone Number is invalid')
                            else:
                                try:
                                    db = pymysql.connections.Connection(host='applicationhelper.cdmmorqiqhka.us-east-1.rds.amazonaws.com', user ='admin', password ='Dsci-551', database='applicationhelper')
                                    cursor = db.cursor()
                                    str(phone)
                                    query = 'INSERT INTO reminders (date_to_send,due_date,name,description,phone,email,method) VALUES ("' + rdate + '","' + deadlinedate + '","' +  item[1] + '" ,"' + deadline + '" , ' + phone + ',"","phone");'
                                    cursor.execute(query)
                                    db.commit()
                                    st.success('Successfully added into reminders!')
                                except:
                                    st.error('Phone Number is invalid')
                        elif method == '':
                            st.error('No Email or Phone Number')
                            

        #Return button
        if st.button('Return to Form'):
            st.session_state.runpage = main_page
            st.experimental_rerun() 

        
    #Setup session states and run session
    if 'runpage' not in st.session_state:
        st.session_state.runpage = main_page
        st.experimental_rerun()

    if 'page' not in st.session_state or st.session_state.page != 'home':
        st.session_state.page = 'home'
        st.session_state.runpage = main_page
        st.experimental_rerun()

    else:
        st.session_state.runpage()