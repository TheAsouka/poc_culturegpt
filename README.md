# CultureGPT

CultureGPT est une application web qui génère des quiz de culture générale sur différents thèmes à l'aide du modèle GPT-3.5 d'OpenAI. Différents thèmes sont proposés et le niveau de difficulté peut être choisi entre facile, moyen, et difficile.

## Objectif du projet

Ce projet est un POC permettant de se familiariser avec [Streamlit](https://docs.streamlit.io/) et la bibliothèque [openai](https://github.com/openai/openai-python) pour l'interraction avec un modèle d'IA.
Il permet également de faire du prompt engineering, un processus essentiel pour diriger et affiner les performances du modèle IA. Cela implique la conception créative de prompts pour guider le modèle d'IA à produire les réponses souhaitées.

## Installation

1. Cloner le dépôt :  
`$ git clone https://github.com/TheAsouka/poc_culturegpt.git`  
`$ cd poc_culturegpt`

2. Installer les dépendances:  
`$ pip install -r requirements.txt`

## Utilisation

1. Créez un fichier .env à la racine du projet avec votre clé [API OpenAI](https://platform.openai.com/account/api-keys) :  
`OPENAI_API_KEY="sk-..."`

2. Lancez l'application avec Streamlit :  
`$ streamlit run src/app.py`  
Vous pouvez maintenant naviguer dans l'application via le navigateur web.

3. Utiliser sans API :  
Une archive de quiz a été crée pour permettre d'essayer l'application sans la connecter à l'API OpenAI.  
Pour ce faire commenter les lignes **93** à **110**, créer une variable **response** de type **str** avec l'un des quiz (entre `[]`) du fichier **quiz_archive.txt**

## Fonctionnement
L'application utilise la technologie GPT-3.5 pour générer des questions et réponses basées sur le thème et la difficulté choisie par l'utilisateur. Les questions sont générées sous forme de QCM (Question à Choix Multiples). Une fois que l'utilisateur a terminé le quiz, le score est calculé et affiché.
En moyenne pour un quiz de 5 questions un total de 500 tokens est utilisé.
Le prompt utilise **163** tokens.  
Le cout de génération d'un quiz est approximativement de :  
```((0.0015/1000)*163) + ((0.002/1000)*350) = 0.0009445$``

## Améliorations possibles

1. **Prompt** : Améliorer le prompt pour répondre aux erreurs eventuelles.
2. **Interface utilisateur** : L'interface utilisateur pourrait être améliorée pour être plus conviviale et attrayante. Donner également la possibilité à l'utilisateur de soumettre son propre thème (attention aux attaques type prompt injection)  
3. **Gestion des erreurs** : Une meilleure gestion des erreurs pourrait être mise en place pour s'assurer que l'application continue de fonctionner même si une erreur se produit lors de la génération du quiz.
4. **Historique des quiz** : Une fonctionnalité pourrait être ajoutée pour permettre à l'utilisateur de consulter ses quiz précédents et leurs scores respectifs.
5. **Support multilingue** : L'application pourrait être améliorée pour supporter plusieurs langues.
6. **Système de paiement** : Intégrer un système de micro-paiement (en cryptomonnaies évidemment) pour que l'utilisateur participe au coût de génération du quiz.

## Limites
Une limitation notable est la redondance des questions générées par le modèle d'IA. 
Il est possible que les utilisateurs rencontrent des questions similaires ou même identiques lors de l'accomplissement de plusieurs quiz. Attention il est aussi propable que les réponses aux questions ne soient pas exactes. (ex : "Quel est le plus grand désert du monde ?" "Antarctique"...)

## Image
<img src="https://github.com/TheAsouka/poc_culturegpt/blob/main/img/capture.png">  