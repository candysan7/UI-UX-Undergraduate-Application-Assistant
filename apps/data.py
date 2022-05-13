import pandas as pd
import numpy as np
import streamlit as st
import time 
import pymysql
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


def app():
    st.header('California Colleges Database')

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


    db = pymysql.connections.Connection(host='applicationhelper.cdmmorqiqhka.us-east-1.rds.amazonaws.com', user ='admin', password ='Dsci-551', database='applicationhelper')
    cursor = db.cursor()
    college_select_query = "SELECT * from appcolleges"
    # query = ''' SELECT * from appcolleges WHERE Weighted GPA >''' + str(gpa_lower
    cursor.execute(college_select_query)
    data = cursor.fetchall()
    column_names = ["id","University_name","Average_SAT","Average_ACT","Weighted_GPA","Admision_rate","Type","Early_Action","Regular_Deadline","Average_Cost","Average_Cost_after_aid","Graduation_rate"]
    full_resultdf = pd.DataFrame(data ,columns=column_names)
    full_resultdf = full_resultdf.drop(['id'],axis=1)
    # full_resultdf = full_resultdf.drop(['Index'],axis=1)
    
    # full_resultdf = full_resultdf.drop(['Index'],axis=1)
    # st.table(full_resultdf)
    # AgGrid(full_resultdf)

    ####SOURCE: https://towardsdatascience.com/make-dataframes-interactive-in-streamlit-c3d0c4f84ccb
    gb = GridOptionsBuilder.from_dataframe(full_resultdf)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gridOptions = gb.build()

    grid_response = AgGrid(
        full_resultdf,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=False,
        theme='blue', #Add theme color to the table
        enable_enterprise_modules=True,
        height=650, 
        width='100%',
        reload_data=True
    )
