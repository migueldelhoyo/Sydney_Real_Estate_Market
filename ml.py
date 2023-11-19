import streamlit as st
import numpy as np
import pandas as pd
from modules.functions_ml import read_data, load_model

def ml():
    st.subheader(body="Machine Learning Model :robot_face:")

    st.markdown(body="""Use the sidebar to test our models. 
                We have built a model to find out the price of property in Syndey.""")

    st.title("Streamlit App")

    # Cargar el modelo y los escaladores específicos para el tipo de propiedad seleccionado
    df = read_data()

    prop_Type = st.selectbox("Select Type Properity", df['propType'].unique())

    model, x_scaler, encode_prop, adam_model = load_model()

    # Barra lateral para ingresar datos
    year = st.slider("Year", min_value=2000, max_value=2030, step=1)
    
    bed = st.slider("Bed", min_value=1, max_value=50, step=1)
    bath = st.slider("Bath", min_value=1, max_value=50, step=1)
    car = st.slider("car", min_value=1, max_value=50, step=1)
    suburb = st.selectbox("Select Suburb", df['suburb'].unique())
    filtered_df = df[df['suburb'] == suburb]
    # Barra lateral para seleccionar postalCode basado en el suburb seleccionado
    postalcode = st.selectbox("Select Postalcode", filtered_df['postalCode'].unique())

    # Aplicar el codificador cargado a los nuevos datos
    propType_encoded = int(encode_prop.transform([[prop_Type]]))

    #Season
    season_options = ['Autumn','Spring','Summer','Winter']
    season = st.radio("When do you want to sell the property?", season_options)
    season_mapping = {
    'Autumn': 0,
    'Spring': 0,
    'Summer': 0,
    'Winter': 0}

    season_mapping[season] = 1

    # Crear un DataFrame con los datos del usuario
    data = pd.DataFrame(
        {'postalCode': [postalcode], 'bed': [bed], 'bath': [bath], 'car': [car], 'Year': [year], 'propType-encoded': [propType_encoded],
         'Season_autumn': season_mapping['Autumn'],'Season_spring': season_mapping['Spring'],
        'Season_summer': season_mapping['Summer'],'Season_winter': season_mapping['Winter']})

    tab1, tab2 = st.tabs(['XGBoost', 'Neural Network'])
    
    # Escalar los datos
    data_scaled = x_scaler.transform(data)

    # Predicción XGBoost
    prediction = model.predict(data_scaled)

    #Predicción Red Neuronal
    prediction_neural = adam_model.predict(data_scaled)
    
    # Mostrar la predicción
    tab1.header('Sales Price Prediction through XGBoost')
    tab1.markdown(f'# ${prediction[0]:,.2f}')
    st.write(data)

    
    
    tab2.header('Sales Price Prediction through Neural Network')
    tab2.markdown(f'# ${prediction_neural[0,0]:,.2f}')
        


if __name__ == "__ml__":

    ml()