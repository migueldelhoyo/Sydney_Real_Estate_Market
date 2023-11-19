import pandas as pd
import pickle
import base64
import sklearn

PAGE_CONFIG = {"page_title"             : "Residential market in Sydney Model - Streamlit",
                "page_icon"             : ":house:",
                "layout"                : "wide",
                "initial_sidebar_state" : "expanded"}

def read_data():

    df = pd.read_csv(filepath_or_buffer = r"C:\Users\Duchement\Documents\HackABoss\Clases\Actualizado 2\Proyecto Final\sources\Sydney_limpio.csv")

    return df

def read_data_gr():
    df_gr = pd.read_csv(filepath_or_buffer = r"C:\Users\Duchement\Documents\HackABoss\Clases\Actualizado 2\Proyecto Final\sources\Sydney_cd.csv")

    return df_gr



def load_model():

    with open(file = r"C:\Users\Duchement\Documents\HackABoss\Clases\Actualizado 2\Proyecto Final\sources\modelo_xgb_optimizado.pkl", mode = "br") as file:
        model = pickle.load(file)

    with open(file = r"C:\Users\Duchement\Documents\HackABoss\Clases\Actualizado 2\Proyecto Final\sources\scaler_X.pkl", mode = "br") as file:
        x_scaler = pickle.load(file)
    
    with open(file = r"C:\Users\Duchement\Documents\HackABoss\Clases\Actualizado 2\Proyecto Final\sources\ordinal_encoder.pkl", mode = "br") as file:
        encode_prop = pickle.load(file)

    with open(file = r"C:\Users\Duchement\Documents\HackABoss\Clases\Actualizado 2\Proyecto Final\sources\Adam_best_model.pkl", mode = "br") as file:
        adam_model = pickle.load(file)

    return model, x_scaler, encode_prop, adam_model