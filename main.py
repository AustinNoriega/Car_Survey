import streamlit as st
from sqlalchemy.sql import text
import numpy as np

#title
st.title("Welcome to a Car Enthusiast's Survey.")
st.markdown("**Please fill out all of the information below :D**")


con = st.connection('Data_db', type= 'sql')

#creating fields to chose from
ideals = ['Horsepower',
          'Track Times',
          'Track Additions (Track Suspension, Carbon Ceramic Breaks, etc...)',
          'Lightweight',
          'Aerodynamics']

age_ranges = ['<18',
              '18-30',
              '30-45',
              '45-60',
              '>60']
#creation of the survey questions
with st.form(key='Car_survey'):
    city = st.text_input("Enter City")
    state = st.text_input("Enter State")
    age = st.multiselect("Enter Age Range", options=age_ranges)
    speed = st.slider("Straight Line Speed",min_value=0, max_value=10, value=1)
    handling = st.slider("Handling/Suspension",min_value=0, max_value=10, value=1)
    visuals = st.slider("Visual Aestetics",min_value=0, max_value=10, value=1)
    feel = st.slider("Driving Response/Feeling",min_value=0, max_value=10, value=1)
    project_ideas = st.text_input("What is your current/next project car")
    new_car = st.text_area("Would you buy a new sports car from the lot?")
    cost = st.slider("How much money would you spend on a new sports car (2020-Present)", 0,500000,step=1000)
    submit = st.form_submit_button("Submit")
    if submit:
        if not city or not state or not cost:
            st.warning("Please fill out all of the information ")
        else:
            st.write("Thanks for submitting!")
            with con.session as s:
                s.execute(text("CREATE TABLE IF NOT EXISTS cars (ID INTEGER,City TEXT,State TEXT, Age FLOAT, Speed INTEGER, Handling Integer, Visual INTEGER, Feeling INTEGER, Project_idea TEXT, "
                               "New_car TEXT, Cost_for_new INTEGER,PRIMARY KEY(ID AUTOINCREMENT));"))

                s.execute(text("INSERT INTO cars (City, State, Age, Speed, Handling, Visual, Feeling, Project_idea, New_car,Cost_for_new) VALUES (:city, :state, :age, :speed,"
                               " :handling, :visual, :feeling, :project_idea, :new_car, :cost_for_new);"),
                    params = dict(city = city, state = state, age = age, speed = speed, handling = handling, visual = visuals, feeling = feel, project_idea = project_ideas, cost_for_new = cost,  new_car = new_car)),
                s.commit()
            df = con.query("select * from cars", ttl = 0 )
            st.dataframe(df)