# UI-UX-Undergraduate-Application-Assistant
A UI / UX Project of an app that will serve as a resource by providing college application information, deadlines, scholarship details, and other vital information for prospective undergraduate students. 

# [Website](https://share.streamlit.io/prestonfong/scholarship-assistant/main/app.py?fbclid=IwAR0e_99w8BK0gDXqSer3_14z9UUBNVmL22cAjUaviHSHW2l0_cLOMOonCho)

### Topic 
Students can input their personal and academic information to see their recommended colleges as well as their eligible scholarships. We have also built in a reminder feature that can allow users to set phone or email reminders of upcoming deadlines. The purpose of our project and web application is so that we can help underserved high school applicants better be informed and ready to apply to colleges in California.  

### Motivation 
The US has almost 500 students for every guidance counselor. This means that the majority of students are not receiving the necessary help they need to understand the college application process. In fact, the lack of guidance for college admissions disproportionately affects low-income, first-generation, and minority students. Our app will be able to help underserved students apply for colleges by providing the necessary information, resources, and guidance.

As two students who recently graduated from California universities, we understand the challenges of applying and navigating the college application process. The information is overwhelming and many underprivileged students do not have the resources to know which colleges to apply to. Thus, we decided to build a web application that can consolidate all that information and help with the undergraduate application process. 

### Components & Main Functions 
1.	College Predictor Form 
The primary function and feature of this web application is so that high school students can input their academic information and our program will provide them with the recommended universities that they should apply to. We have collected data on over 45 California private and public universities and developed an algorithm that considers your GPA, SAT, ACT, and merit awards when providing your college recommendation. We have considered adding in elements such as race, gender, first-generation status, or socioeconomic statuses, but we did not have sufficient data to develop an algorithm that can consider these factors. Once the algorithm has matched the student with schools, the student will be able to set a customized reminder for each school.
2.	Scholarship Form & Database 
We have also built a form for users to determine which scholarships they would be eligible to apply for. Users would have to quickly provide some personal and demographic information to see which scholarship they are eligible for. The user would be redirected to the results page and see all the scholarships given their eligibility criteria. Similarly, they will be able to set reminders here.
3.	College Database 
One of the by-products of creating a college predictor form was developing an entirely well-formatted database on university freshmen admission data. Users can view this table on our webpage and make informed decisions by themselves. We were able to collect critical data features for 2022 such as Early Action deadlines, average GPA, average cost after aid, etc. Users would then be able to easier compare certain features of colleges against colleges more visually. We believe this database would be very useful for guidance counselors, prospective undergraduate students, and education administrators. 
4.	Email & Text Reminders
The web application is able to send push notifications and email reminders to students when an upcoming college or scholarship deadline is approaching. The user has the ability to set the reminder date as well as remove the reminder. We have built a friendly UI feature that allows users to see all the existing reminders and remove any additional reminders. 

### Data Flow
We would first gather the data through web-scraping or manual searching. After cleaning the data, we would upload our data onto Amazon RDS, which is our cloud database. We used Python and SQL to extract the data from the cloud database and would convert it to a data frame or the proper data structure so that we properly display the data in a user-friendly format. The user would then input their personal and academic information and our program would use the inputted data to filter our cloud databases and display their unique results. We have tested our data flow and programs for bugs and have tried to improve the user experience. 
