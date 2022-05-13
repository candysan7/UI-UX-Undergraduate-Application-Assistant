import streamlit as st
from apps import home, data, scholarships,reminders2 # import your app modules here

#Making a navbar
class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            st.title('Navigation Panel')
            app = st.radio(
            'Go To',
            self.apps,
            format_func=lambda app: app['title'])

        app['function']()

app = MultiApp()

# st.markdown("""
# # Multi-Page App

# This multi-page app is using the [streamlit-multiapps](https://github.com/upraneelnihar/streamlit-multiapps) framework developed by [Praneel Nihar](https://medium.com/@u.praneel.nihar). Also check out his [Medium article](https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4).

# """)

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Scholarships", scholarships.app)
app.add_app("Reminders", reminders2.app)
app.add_app("College Database", data.app)
# The main app
app.run()
