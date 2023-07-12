#! /usr/local/bin/python3
# Version used : python3.11.2
# -*- coding: utf-8 -*-

import streamlit as st
import openai, os, json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def archive_quiz(response):
    with open("quiz_archive.txt", "a") as f:
        f.write(response + "\n")


def response_to_dict(response):
    data = json.loads(response)
    return data


# Initialisation session_state
def init_session_state():
    if "FormSubmitter:my_form-Confirmer" not in st.session_state:
        st.session_state["FormSubmitter:my_form-Confirmer"] = False

    if "NbrQuiz" not in st.session_state:
        st.session_state["NbrQuiz"] = 0

    if "TotalScore" not in st.session_state:
        st.session_state["TotalScore"] = 0


init_session_state()


# Création front
st.title("CultureGPT")


# Sélection thème et difficulté du quiz
theme = st.selectbox(
    "**Sélectionnez le thème du quiz:**",
    [
        "Histoire",
        "Géographie",
        "Science",
        "Art",
        "Technologie",
        "Internet",
        "France",
        "Culture populaire",
    ],
)
difficulty = st.select_slider(
    "**Sélectionnez la difficulté:**", ["Facile", "Moyen", "Difficile"]
)

# Context pour le modele
system_msg = """Tu es un assistant permettant de créer des tests de culture générale dans un format de QCM sur différents thèmes et dans différentes diffcultés.
Tu retournes les questions et réponses en JSON comme ci :
[{question : "QUESTION1",reponses : ["reponse1","reponse2","reponse3","reponse4"],correct : "reponse2"}],[{question : "QUESTION2",reponses : ["reponse1","reponse2","reponse3","reponse4"],correct : "reponse4"}],..."""
# Prompt de l'utilisateur
user_msg = f"Créer un test de culture générale de 5 questions sur le thème \"{theme}\" de niveau {difficulty.lower()}.Ne répond qu'avec le JSON rien d'autre."


# Création de la sidebar
with st.sidebar:
    side_nbrqquiz = st.write("Nombre de quiz effectués :", st.session_state["NbrQuiz"])
    side_totalscore = st.write(
        "Score total :",
        st.session_state["TotalScore"],
        "/",
        st.session_state["NbrQuiz"] * 5,
    )


# Evite l'erreur 'data' not defined
# Gestion d'erreur à améliorer
data = []

# Génération du quiz
st.warning("Attention ça coute des sous (mais pas beaucoup).")
if st.button("Générer le quiz"):
    # Attention à utiliser ChatCompletion avec les bon paramètres (model&messages) pour utiliser GPT3.5
    # Utilisation de Completion avec des modèle GPT3 requiert différents paramètres (engine&prompt).
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=1,
        max_tokens=600,
    )
    print("-" * 20)
    print("id :", completion.id)
    print("model :", completion.model)
    print(completion.usage)
    print("-" * 20)

    response = completion.choices[0].message.content.strip()

    archive_quiz(response)
    data = response_to_dict(response)

# Affichage des questions et choix dans un formulaire
if len(data) != 0:
    st.session_state.quiz = data
    st.subheader(f"Quiz {theme} - {difficulty}")
    # Besoin de save les réponses de l'user dans le session_state
    # Fais automatiquement via l'argument key du radio (widget)
    with st.form("my_form"):
        i = 0
        for elements in data:
            user_rep = st.radio(
                f'**{elements["question"]}**',
                elements["reponses"],
                key="rep" + str(i),
            )
            i += 1
        submitted = st.form_submit_button("Confirmer")
        # "FormSubmitter:my_form-Confirmer" est automatiquement créer dans session_state


if st.session_state["FormSubmitter:my_form-Confirmer"] is True:
    score = 0
    st.subheader("Voici les réponses :")
    for y in range(0, 5):
        question = st.session_state["quiz"][y]["question"]
        correct_answer = st.session_state["quiz"][y]["correct"]
        user_rep = st.session_state["rep" + str(y)]
        if user_rep == correct_answer:
            score += 1

        st.write(f"**{question}**")
        st.write(correct_answer)
    st.success(f"Votre score est de {score}/5 bonnes réponses !")
    st.session_state["TotalScore"] += score
    st.session_state["NbrQuiz"] += 1
    st.button("OK")
