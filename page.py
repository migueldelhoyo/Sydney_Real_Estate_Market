import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd

from modules.functions_ml import read_data, load_model#, download_file

def page_app_func():

    st.title(body = "Streamlit Project :robot_face:")

    st.subheader(body = "Home :house:")

    st.write("Welcome to the **Study of the residential market in Sydney (Australia)** made with **Streamlit**.")

    st.markdown("""The data for this project comes from the following website: 
                    [Kaggle (https://www.kaggle.com/datasets/mihirhalai/sydney-house-prices).""")

    st.write("""To use this app just go to the `Exploratory Data Analysis` In this section, you will have the possibility
              to choose a percentage of the data for plotting. By default, you will find the option to 
             filter the data, and you will have the choice to deactivate the filters. And you can know more
            about the data that we used to build the Machine Learning models.""")
    
    st.write("""To use the `Machine Learning Model` section, you can use the sliders to make predictions.""")

    st.write("""In the `Folium` section, you will be able to visually see the properties distributed in Sydney.
              Even in this section, you can activate filters that will affect the map visualization.""")
    
    df = read_data()
    st.write(df)

    columnas = list(df.columns)

    columnas = [col for col in columnas if col not in ['sellPrice', 'Id', 'Date', 'Year', 'Month']]

    
    fig_scatter = px.scatter(data_frame = df,
                            x          = "sellPrice",
                            y          = "propType",
                            color      = "propType",
                            opacity    = 0.5)

    st.plotly_chart(fig_scatter)


if __name__ == "__page_app_func__":
    page_app_func()