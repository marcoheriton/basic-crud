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

botao_v = st.button(label="Visualizar")

if botao_v:
    df = conn.query('select count(*) as votes, pet from mytable group by pet')
    fig, ax = plt.subplots()  
    ax.pie(df['votes'], labels=df['pet'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.markdown('## Gráfico com Resultado da Pesquisa')
    st.pyplot(fig)
