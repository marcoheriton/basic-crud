import streamlit as st
import pandas as pd
import re
import psycopg2 as psy
from sqlalchemy import text
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
#from vega_datasets import data
import altair as alt


# Initialize connection.
conn = st.connection("postgresql", type="sql",autocommit=True)


def is_valid_email(email):
    # Define the regular expression for a valid email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Use re.match to check if the email matches the regex
    if re.match(email_regex, email):
        return True
    else:
        return False

def insert_data(email,animal):
    with conn.session as session:
        session.execute(text(f"insert into mytable (name, pet) values ('{email}','{animal}')"))
        session.commit()



def main():
    st.title("Escolha o seu animal preferido")

    with st.form(key='form', clear_on_submit=True):
        menu=["Escolha","Resultado"]
        choice=st.sidebar.selectbox("Menu",menu)

        if choice == "Escolha":
            email = st.text_input("digite seu email")
            animal = st.radio("Qual seu animal favorito?",[":dog: Cachorro",":cat: Gato"])
            if animal == ":dog: Cachorro":
                animal = "Cachorro"
            else:
                animal = "Gato" 
            botao = st.form_submit_button(label='enviar')
            if is_valid_email(email):
                if botao and email is not None:
                    dados = conn.query("Select * from mytable")

                    for row in dados.itertuples():
                        if email == row.name:
                            st.warning("Já existe registro do seu email na pesquisa!")
                            return False
                        else:
                            insert_data(email, animal)
                            st.success("Escolha enviada com sucesso!")
            else:
                st.warning("O campo email está vazio ou não é um email válido")

        if choice == "Resultado":
            st.write("Aba Resultado")
            visualizar = st.form_submit_button(label="Visualizar")
            if visualizar:
                df = conn.query('select count(*) as votes, pet from mytable group by pet')
                
                fig, ax = plt.subplots()  
                ax.pie(df['votes'], labels=df['pet'], autopct='%1.1f%%', startangle=90)
                ax.axis('equal')
                st.markdown('## Gráfico com Resultado da Pesquisa')
                st.pyplot(fig)

                                                                                                                         
if __name__=='__main__':
    main()