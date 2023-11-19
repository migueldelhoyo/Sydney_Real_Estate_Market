import streamlit as st

from page import page_app_func
from ml import ml
from eda import eda
from folium_page import folium_function
# from about import about

from modules.functions_ml import PAGE_CONFIG

st.set_page_config(**PAGE_CONFIG)

def main():

    menu = ["Main App", "Exploratory Data Analysis", "Machine Learning Model", "Folium"]

    page = st.sidebar.selectbox(label = "Menu", options = menu)
    
    if page == "Main App":

        page_app_func()

        pass

    elif page == "Exploratory Data Analysis":
        
        eda()
        pass

    elif page == "Machine Learning Model":

        ml()

        pass

    elif page == "Folium":

        folium_function()

        pass


if __name__ == "__main__":
    main()