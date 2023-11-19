import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pickle
from modules.functions_ml import read_data, read_data_gr


def eda():


    df = read_data()
    df_static = df.copy()
    df_gr = read_data_gr()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title("Exploratory Data Analysis :bar_chart:")

    type_graphics = st.sidebar.radio(label = "",
                        options = ("Default","Boxplot", "Heatmap", "Subplots Scatterplot"),
                        index = 0,
                        disabled = False,
                        horizontal = False,
                        )
    if type_graphics == "Default":
        colsp1, colsp2 = st.columns(2)
        with colsp1:
            show_filters = st.checkbox("Disable filters/Enable filters")
        with colsp2:    
            porcent = st.radio(label = "%",
                        options = (25, 50, 75, 100),
                        index = 0,
                        disabled = False,
                        horizontal = True,
                        )
            
            df =df.sample(frac = porcent / 100)
            df_filtered = df.copy()
        
        

        # Pestañas
        
        if show_filters:
            

            # Contenido de la primera columna
            col1, col2 = st.columns([1,4])
            with col1:
                
                coordinate_options = ['sellPrice', 'propType','suburb', 'Season', 'bath', 'bed' ]
                y_options = coordinate_options
                y_coord = st.selectbox(label = "Coordenada Y",
                                                options = y_options)
                
                coordinate_options = ['propType','suburb', 'Season', 'bath', 'bed', 'sellPrice'  ]
                x_options = coordinate_options
                x_coord = st.selectbox(label = "Coordenada X",
                                                options = x_options)
            
            with col2:   
                tab1, tab2, tab3, tab4 = st.tabs(["Bar Graphic", "Violin Graphic", "Scatter Graphic", "Pie Graphic"])
            
            
            #Bar Graphic
            fig_bar = px.bar(df, x= x_coord, y= y_coord)

            # Violin Graphic
            fig_violin = px.violin(df, x= x_coord, y= y_coord)

            # Scatter Graphic
            fig_scatter = px.scatter(df, x= x_coord, y= y_coord)

            # Pie Graphic
            df_group = df.groupby(by = x_coord).agg({x_coord : ["count"]})
            df_group.columns = [f"{x_coord} Count"]
            df_group.reset_index(inplace = True)

            fig_pie = px.pie(df_group, names= x_coord, values= f"{x_coord} Count", title = "Solo se usará Coordenada X")

            tab1.plotly_chart(figure_or_data = fig_bar, use_container_width = True)
            tab2.plotly_chart(figure_or_data = fig_violin, use_container_width = True)
            tab3.plotly_chart(figure_or_data = fig_scatter, use_container_width = True)
            tab4.plotly_chart(figure_or_data = fig_pie, use_container_width = True)
        
                

        else:
            
            #suburb
            suburb_options = ["All"] + sorted(list(df_filtered["suburb"].unique()))
            suburbs = st.multiselect(label="Suburb", 
                                            options=suburb_options, 
                                            default='All')
            
            suburb_options = ["All"] + sorted(list(df_filtered["suburb"].unique()))
            df_filtered = df_filtered[df_filtered["suburb"].isin(suburbs)] if 'All' not in suburbs else df_filtered
            
            if len(suburbs) == 0:
                suburbs = 'All'

            coordinate_options = [ 'sellPrice','propType', 'Season', 'bath', 'bed', 'suburb']
            y_options = coordinate_options
            y_coord = st.sidebar.selectbox(label = "Coordenada Y",
                                            options = y_options)
            
            coordinate_options = ['propType','suburb', 'Season', 'bath', 'bed', 'sellPrice']
            x_options = coordinate_options
            x_coord = st.sidebar.selectbox(label = "Coordenada X",
                                            options = x_options)  
                
                
            
            # Divide la pantalla en dos columnas
            col1, col2, col3 = st.columns([1,5,1])

            # Contenido de la primera columna
            with col1:
                # Year
                year_options = ["All"] + list(df["Year"].unique())
                year = st.selectbox(label = "Year",
                                            options = year_options)

                df_filtered = df[df["Year"] == year] if year != "All" else df

            
                
                # Season
                season_options = ["All"] + list(df_filtered["Season"].unique())
                season = st.selectbox(label = "Season",
                                            options = season_options)
                
                df_filtered = df_filtered[df_filtered["Season"] == season] if season != "All" else df_filtered

                
                
                #propType

                propType_options = ["All"] + list(df_filtered["propType"].unique())
                
                propType = st.selectbox(label= "Type", 
                                                options=propType_options)
                
                df_filtered = df_filtered[df_filtered["propType"] == propType] if propType != "All" else df_filtered
            
            with col3:   
                col4, col5 = st.columns(([2,1]))

                with col4:
                # Bed
                    bed_options = list(df_filtered["bed"].unique())

                    bed = st.number_input(label = "Bedroom",
                                        min_value = 1,
                                        max_value = max(bed_options),
                                        value = 1,
                                        step = 1)
                    # Bath

                    bath_options = list(df_filtered["bath"].unique())

                    bath = st.number_input(label = "Bathroom",
                                        min_value = 1,
                                        max_value = max(bath_options),
                                        value = 1,
                                        step = 1)
                    #Car
                    car_options = list(df_filtered["car"].unique())
                    car = st.number_input(label     = "Space car",
                                    min_value = 1,
                                    max_value = max(car_options),
                                    value     = 1)
                    
                    df_filtered = df_filtered[(df_filtered["car"] == car)]
                with col5:
                    signs_bed_mapping = {"<=": "<=", "==": "==", "=>": ">="}
                    signs_bed = st.select_slider(label="",
                                                options=["<=", "==", "=>"],
                                                value="==")
                    sign_bed_operator = signs_bed_mapping[signs_bed]

                    

                    # Obtener el signo seleccionado por el usuario para la columna 'bath'
                    signs_bath_mapping = {"<=": "<=", "==": "==", "=>": ">="}
                    signs_bath = st.select_slider(label=" ",
                                                options=["<=", "==", "=>"],
                                                value="==")
                    sign_bath_operator = signs_bath_mapping[signs_bath]


           
                    #car
                    signs_car_mapping = {"<=": "<=", "==": "==", "=>": ">="}
                    signs_car = st.select_slider(label="  ",
                                                options=["<=", "==", "=>"],
                                                value="==")
                    
                    sign_car_operator = signs_car_mapping[signs_car]

                    # Filtrar el DataFrame
                    df_filtered = df[(eval(f"df['bed'] {sign_bed_operator} bed")) & (eval(f"df['bath'] {sign_bath_operator} bath") & (eval(f"df['car'] {sign_car_operator} car")))]

                    
            # Contenido de la segunda columna
            with col2:

                # Pestañas
                tab1, tab2, tab3, tab4 = st.tabs(["Bar Graphic", "Violin Graphic", "Scatter Graphic", "Pie Graphic"])
                
                
                
                # Bar Chart
                df_group = df_filtered.groupby(by = "propType").agg({"propType" : ["count"]})
                df_group.columns = ["PropType Count"]
                df_group.reset_index(inplace = True)

                fig_bar = px.bar(data_frame = df_filtered,
                                x          = x_coord,
                                y          = y_coord,
                                color      = x_coord,
                                text_auto  = True)

                # Scatter Plot
                fig_scatter = px.scatter(data_frame = df_filtered,
                                        x          = x_coord,
                                        y          = y_coord,
                                        color      = x_coord,
                                        opacity    = 0.5)
                
                # Pie Chart
                df_group = df_filtered.groupby(by = x_coord).agg({x_coord : ["count"]})
                df_group.columns = [f"{x_coord} Count"]
                df_group.reset_index(inplace = True)

                fig_pie = px.pie(df_group, names= x_coord, values= f"{x_coord} Count", title = "Solo se usará Coordenada X")
                
                # Violin Plot
                fig_violin = px.violin(data_frame = df_filtered,
                                        x          = x_coord,
                                        y          = y_coord,
                                        color      = x_coord,)
                
                
                tab1.plotly_chart(figure_or_data = fig_bar, use_container_width = True)
                tab2.plotly_chart(figure_or_data = fig_violin, use_container_width = True)
                tab3.plotly_chart(figure_or_data = fig_scatter, use_container_width = True)
                tab4.plotly_chart(figure_or_data = fig_pie, use_container_width = True)
           
    elif type_graphics == 'Boxplot':
            
        df_numeric = df_static.select_dtypes(include=['number'])
        df_numeric = df_numeric.drop('Id', axis=1)
        numeric_list = list(df_numeric.columns)
        
        sns.set_style("darkgrid")

        for col in numeric_list:
            plt.figure(figsize=(10, 5))
            sns.boxplot(x=df_static[col])
            plt.title(f'Boxplot de {col}')
            st.pyplot()
            
         
    
    elif type_graphics == 'Heatmap':
        
        st.write('We can find slight correlations between sellPrice and bed, sellPrice and bath, and bed and bath. This means that, in general, houses with more bedrooms and bathrooms tend to have a higher selling price.')
        st.write('There is a positive correlation, albeit weaker, between sellPrice and year. This means that, in general, newer houses tend to have a higher selling price.')
        st.write('On the other hand, there is no significant correlation between sellPrice and month. This means that the month in which a house is sold does not have a significant impact on its selling price.')

        df_numeric = df_gr.select_dtypes(include=['number'])
        numeric_list = list(df_numeric.columns)   
        corr_matrix_numerica = df_gr[numeric_list].corr()

        plt.figure(figsize=(12, 8))
        sns.heatmap(corr_matrix_numerica, annot=True, cmap="coolwarm", linewidths=.5)
        plt.title("Heatmap de correlación entre columnas numéricas")
        plt.show()
        st.pyplot()

    elif type_graphics == 'Subplots Scatterplot':

        st.write("As we had seen in the correlations, those with a positive correlation, although an upward direction can be seen in relation to the price, is not so clear in some cases, and those with a negative correlation have a downward direction.")

        # Creamos subplots para cada variable por separado
        num_cols = ['postalCode', 'bed', 'bath', 'car', 'Year']

        # Configuramos el tamaño de la figura y el número de filas y columnas de subplots
        filas, columnas = 5, 2
        fig, axes = plt.subplots(filas, columnas, figsize=(12, 20))
        fig.subplots_adjust(hspace=0.5)

        # Iterando creamos los gráficos
        for i, col in enumerate(num_cols[:5]):
            #Gráfico de cada variable por separado
            sns.histplot(data=df_gr, x=col, ax=axes[i, 0])
            axes[i, 0].set_title(f'{col}')
            axes[i, 0].set_xlabel(col)
            axes[i, 0].set_ylabel('Frecuencia')

            #Gráfico de dispersión cruzando la variable con "sellPrice"
            sns.scatterplot(data=df_static, x=col, y='sellPrice', ax=axes[i, 1])
            axes[i, 1].set_title(f'{col} vs. sellPrice')
            axes[i, 1].set_xlabel(col)
            axes[i, 1].set_ylabel('sellPrice')
            plt.xticks(rotation=45)

        # Mostrar los gráficos pair plot
        plt.xticks(rotation=45)
        st.pyplot()

        pair_plot = sns.pairplot(df_static, diag_kind='kde')
        st.pyplot(pair_plot)

if __name__ == "__eda__":

    eda()