#! /usr/local/bin/python3
# Version used : python3.11.2
# -*- coding: utf-8 -*-

import streamlit as st
import openai, os, json
from dotenv import load_dotenv
from collections import namedtuple


def load_env():
    # Charger les variables d'environnement depuis .env
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")


def init_session_state():
    # Initialiser le session_state avec des valeurs par défaut
    # session_state permet de conserver des données entre les "run" sur streamlit
    initial_state = {
        "FormSubmitter:my_form-Confirmer": False,
        "NbrQuiz": 0,
        "TotalScore": 0,
    }

    for state_variable, default_value in initial_state.items():
        if state_variable not in st.session_state:
            st.session_state[state_variable] = default_value


def archive_quiz(response):
    # Enregistre les réponses données par GPT dans un fichier texte
    with open("quiz_archive.txt", "a") as f:
        f.write(response + "\n")


def render_quiz_form(quiz):
    # Afficher le quiz sous forme de formulaire
    st.subheader(f'Quiz {quiz["theme"]} - {quiz["difficulty"]}')
    with st.form("my_form"):
        for i, question in enumerate(quiz["questions"]):
            user_rep = st.radio(
                f'**{question["question"]}**',
                question["reponses"],
                key="rep" + str(i),
            )
        # L'argument key est automatiquement enregistré dans session_state
        # "FormSubmitter:my_form-Confirmer" est automatiquement crée dans session_state
        st.form_submit_button("Confirmer")


def render_quiz_results(quiz):
    # Calculer le score et afficher les résultats du quiz
    score = 0
    st.subheader("Voici les réponses :")
    for y in range(0, len(quiz["questions"])):
        question = quiz["questions"][y]["question"]
        correct_answer = quiz["questions"][y]["correct"]
        user_rep = st.session_state["rep" + str(y)]
        if user_rep == correct_answer:
            score += 1

        st.write(f"**{question}**")
        st.write(correct_answer)
    st.success(f"Votre score est de {score}/5 bonnes réponses !")
    st.session_state["TotalScore"] += score
    st.session_state["NbrQuiz"] += 1
    st.button("OK")


def render_sidebar():
    # Affiche la barre latérale
    sidebar = st.sidebar
    sidebar.write("Nombre de quiz effectués :", st.session_state["NbrQuiz"])
    sidebar.write(
        "Score total :",
        st.session_state["TotalScore"],
        "/",
        st.session_state["NbrQuiz"] * 5,
    )


def generate_quiz(theme, difficulty):
    # Context pour le modele
    system_msg = """Tu es un assistant permettant de créer des tests de culture générale dans un format de QCM sur différents thèmes et dans différentes diffcultés.
Tu retournes les questions et réponses en JSON comme ci :
[{question : "QUESTION1",reponses : ["reponse1","reponse2","reponse3","reponse4"],correct : "reponse2"}],[{question : "QUESTION2",reponses : ["reponse1","reponse2","reponse3","reponse4"],correct : "reponse4"}],..."""
    # Prompt de l'utilisateur
    user_msg = f"Créer un test de culture générale de 5 questions sur le thème \"{theme}\" de niveau {difficulty.lower()}.Ne répond qu'avec le JSON rien d'autre."

    # Utilisation de ChatCompletion avec les bons paramètres (model&messages) pour utiliser GPT3.5
    # Utilisation de Completion (modèles GPT3) requiert différents paramètres (engine&prompt).
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        temperature=1,
        max_tokens=600,
    )

    # Affiche des données sur l'utilisation de l'API OpenAI
    print("-" * 20)
    print("id :", completion.id)
    print("model :", completion.model)
    print(completion.usage)
    print("-" * 20)

    response = completion.choices[0].message.content.strip()

    # Transformer la réponse en dictionnaire et enregistrer dans une archive
    archive_quiz(response)
    questions = json.loads(response)
    quiz = {"theme": theme, "difficulty": difficulty, "questions": questions}

    return quiz


def render_select():
    # Affiche les options de sélection et retourne les résultats associés
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

    return theme, difficulty


def run_app():
    load_env()
    init_session_state()
    render_sidebar()

    st.title("CultureGPT")
    theme, difficulty = render_select()

    if st.button("Générer le quiz"):
        try:
            quiz = generate_quiz(theme, difficulty)
            st.session_state.quiz = (
                quiz  # enregistré le dictionnaire quiz session state
            )
            render_quiz_form(quiz)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Retourne la valeur de "FormSubmitter:my_form-Confirmer" dans st.session_state si elle existe, sinon retourne False.
    # Puisque la valeur existe déjà (False), attend qu'elle soit a True.
    # Permet d'attendre que l'utilisateur clique sur "Confirmer" dans le formulaire
    if st.session_state.get("FormSubmitter:my_form-Confirmer", False):
        try:
            render_quiz_results(st.session_state.quiz)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    run_app()
