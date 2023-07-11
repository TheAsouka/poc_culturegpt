#! /usr/local/bin/python3
# Version used : python3.11.2
# -*- coding: utf-8 -*-

import streamlit as st
import openai, os, json
from dotenv import load_dotenv

load_dotenv()


def write_AI_response(response):
    with open("reponse2.txt", "w+") as f:
        f.write(response)


def txt_to_dict():
    with open("reponse2.txt", "r") as f:
        data = json.load(f)
    return data


openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("CultureGPT")

# Sélection du thème du quiz
theme = st.selectbox(
    "Sélectionnez le thème du quiz:",
    ["Histoire", "Géographie", "Science", "Art", "Technologie", "Internet"],
)
difficulty = st.select_slider(
    "Sélectionnez la difficulté:", ["Facile", "Moyen", "Difficile"]
)

system_msg = """Tu es un assistant permettant de créer des tests de culture générale dans un format de QCM sur différents thèmes et dans différentes diffcultés.
Tu retournes les questions et réponses en JSON comme ci :
[{id : 1,question : "QUESTION1",reponses : ["reponse1","reponse2","reponse3","reponse4"],correct : "reponse2"}],[{id : 2,question : "QUESTION2",reponses : ["reponse1","reponse2","reponse3","reponse4"],correct : "reponse4"}],..."""
user_msg = f"Créer un test de culture générale de 5 questions sur le thème \"{theme}\" de niveau {difficulty.lower()}.Ne répond qu'avec le JSON rien d'autre."


# Génération de la question
if st.button("Générer le quizz"):
    # Attention à utiliser ChatCompletion avec les bon paramètres (model&messages) pour utiliser GPT3.5
    # Utilisation de Completion avec des modèle GPT3 requiert différents paramètres (engine&prompt).

    """
    quizz = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=1,
        max_tokens=600,
    )
    print(quizz)
    response = quizz.choices[0].message.content.strip()
    # write_AI_response(response)"""

    data = txt_to_dict()
    st.session_state.quizz = data
    # Besoin de save les réponses de l'user dans le session_state
    with st.form("my_form"):
        score = 0
        for elements in data:
            user_rep = st.radio(f'**{elements["question"]}**', elements["reponses"])
            st.session_state.rep = user_rep
        submitted = st.form_submit_button("Confirmer")
        if submitted:
            st.success(str(score))
    print(st.session_state)
