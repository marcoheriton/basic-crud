import streamlit as st
import pandas as pd
import re
import psycopg2 as psy
from sqlalchemy import text
import matplotlib.pyplot as plt
import numpy as np
import altair as alt


# Initialize connection.
conn = st.connection("postgresql", type="sql",autocommit=True)
#with conn.session as session:
#    session.execute(text(f"CREATE TABLE IF NOT EXISTS mytable (name VARCHAR(80), pet VARCHAR(8))"))
    


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


existeemail = False
st.title("Escolha o seu animal preferido")

email = st.text_input("digite seu email")
animal = st.radio("Qual seu animal favorito?",[":dog: Cachorro",":cat: Gato"])
if animal == ":dog: Cachorro":
    animal = "Cachorro"
else:
    animal = "Gato" 

botao = st.button(label='enviar')
if is_valid_email(email):
   if botao and email is not None:
        dados = conn.query("Select * from mytable")
        for row in dados.itertuples():
            if email == row.name:
                existeemail = True
                st.warning("Já existe registro do seu email na pesquisa!")
                continue
                            
        if not existeemail:
            insert_data(email, animal)
            st.success("Escolha enviada com sucesso!")
            existeemail=False
   else:
    st.warning("O campo email está vazio ou não é um email válido")
           
