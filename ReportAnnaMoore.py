import openai

import time
import mysql.connector
import base64
import csv
import requests
import ftplib

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import os

assistant_id = st.secrets["OPENAI_ASSISTANT"]
db_host = st.secrets["DB_HOST"]
db_port = st.secrets["DB_PORT"]
db_name =  st.secrets["DB_NAME"]
db_user =  st.secrets["DB_USER"]
db_password =  st.secrets["DB_PASSWORD"]

client = openai
count = 0

csv_file_path = 'maquines_informe_5.csv'

if os.path.exists(csv_file_path):
  os.remove(csv_file_path)
else:
  print("The file does not exist")

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

st.set_page_config(page_title="rurAIctive Gallery by partners",page_icon="✅",layout="wide")

openai.api_key = st.secrets["auto_pau"]

l1 = ['xdominguez', 'dyumi']
lc = ['arehman','dbatista','ccastillo','alasurashvili','dmajdoub','aelahyani','egonçalves',
'fgueye','sjaved','mkaur','imerino','ynawaz','kpacheco','zrehman','yrivera','jsaavedra','asegura','dsena','asingh',
'rtrinidad','iyucra','czambrana','djimenez','mbarahona']
listcaptions =[]
listimages = []
# Disable the submit button after it is clicked

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def disable():
    if nom != '' and nom in l1:
        st.session_state.disabled = True
        st.session_state.start_chat = True
        st.session_state.disabled = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
    else:
        if nom != '':
            st.sidebar.write(":red[Aquest usuari no existeix]")

def enable():
    if "disabled" in st.session_state and st.session_state.disabled == True:
        st.session_state.disabled = False
        st.session_state.messages = []  # Clear the chat history
        st.session_state.start_chat = False  # Reset the chat state
        st.session_state.thread_id = None


# Initialize disabled for form_submit_button to False
if "disabled" not in st.session_state:
    st.session_state.disabled = False

with st.sidebar.form("usuari_form"):
  nom = st.text_input("Escriu la teva identificació 👇",disabled=st.session_state.disabled, key=1)
  submit_button = st.form_submit_button(label="Veure Informe",disabled=st.session_state.disabled, on_click=disable)

  if submit_button and nom != '' and nom in l1:
        st.session_state.disabled = True
        st.session_state.start_chat = True
        st.session_state.disabled = True
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id


st.title("rurAIctive Gallery by partners")

st.sidebar.button("Exit",on_click=enable)

if st.session_state.start_chat:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4-1106-preview"
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Crea una conexión con la base de datos
        conn = mysql.connector.connect(host=db_host, port=db_port, database=db_name, user=db_user,
                                                       password=db_password)

        # Crea un cursor para ejecutar comandos SQL
        cur = conn.cursor()

        # Ejecuta una consulta SQL
        sql = "SELECT * FROM teclaCOMIC WHERE tema = '5555555'"
        cur.execute(sql)

        # Obtiene los resultados de la consulta
        results_database = cur.fetchall()
        if results_database:
            # New empty list called 'result'. This will be written to a file.
            result = list()

            # The row name is the first entry for each entity in the description tuple.
            column_names = list()
            for i in cur.description:
                column_names.append(i[0])

            result.append(column_names)
            for row in results_database:
                result.append(row)

            # Write result to file.
            with open(csv_file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in result:
                    csvwriter.writerow(row)

        else:
            sys.exit("No rows found for query: {}".format(sql))

        conn.commit()

        # Cierra la conexión con la base de datos
        cur.close()
        conn.close()

        # read csv from a URL
        @st.experimental_memo
        def get_data() -> pd.DataFrame:
            return pd.read_csv(csv_file_path)


        df = get_data()
        # top-level filters
        #user_filter = st.selectbox("Escull un usuari", pd.unique(df["idc"]))
        # create two columns for charts
        st.markdown("### Dades Generals")
        st.dataframe(df, width=1800, column_order=("descripcio"),
                     column_config={"descripcio": "Description"})

        st.markdown("### Gallery")
        for i in range(len(df['url'])):
            if df['url'][i]:
                df['url'][i] = "https://www.xavidominguez.com/tecla/"+str(df['url'][i])
                #st.write(df['infografia'][i])
                listimages.append(str(df['url'][i]))
                listcaptions.append(df['descripcio'][i])

        st.image(listimages,caption=listcaptions,width=200,output_format="JPEG")
else:
    st.write("Afegeix les teves dades i clica en 'Veure Informe'.")