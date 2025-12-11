import streamlit as st
from streamlit_gsheets import GSheetsConnection
import numpy as np
import pandas as pd


#title
st.title("Welcome to a Car Enthusiast's Survey.")
st.markdown("**Please fill out all of the information below :D**")


con = st.connection("gsheets", type=GSheetsConnection)
current= con.read(worksheet='Data')

#creating fields to choose from
age_ranges = ['<18',
              '18-30',
              '30-45',
              '45-60',
              '>60']
#creation of the survey questions
with st.form(key='Car_survey'):
    city = st.text_input("Enter City")
    state = st.text_input("Enter State")
    age = st.selectbox("Enter Age Range", options=age_ranges)
    st.text("Please input the number of how important these aspects in a sports car are below")
    speed = st.slider("Straight Line Speed",min_value=0, max_value=10, value=1)
    handling = st.slider("Handling/Suspension",min_value=0, max_value=10, value=1)
    visuals = st.slider("Visual Aestetics",min_value=0, max_value=10, value=1)
    feel = st.slider("Driving Response/Feeling",min_value=0, max_value=10, value=1)
    project_ideas = st.text_input("What is your current/next project car")
    new_car = st.text_area("Would you buy a new sports car from the lot?")
    cost = st.slider("How much money would you spend on a new sports car (2020-Present)", 0,250000,step=1000)
    submit = st.form_submit_button("Submit")
    if submit:
        if not city or not state or not cost:
            st.warning("Please fill out all of the information ")
        else:
            st.write("Thanks for submitting!")
            new_data = pd.DataFrame(
                [
                    {
                    'City': city,
                    'State': state,
                    'Age': age,
                    'Speed': speed,
                    'Handling': handling,
                    'Visual': visuals,
                    'Feeling': feel,
                    'Project_idea': project_ideas,
                    'New_Car': new_car,
                    'Cost_for_new': cost,

                    }
                ]
            )
            updated = pd.concat([current, new_data], ignore_index=True)
            con.update(worksheet = 'Data', data = updated)
            st.success("Yippie")