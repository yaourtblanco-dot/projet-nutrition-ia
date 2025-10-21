# app.py

import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Assistant Nutrition IA", page_icon="💪")

# --- TITRE DE L'APPLICATION ---
st.title("💪 Assistant Nutrition IA")
st.subheader("Générez vos idées de repas en un clic")

# --- CONNEXION À L'API GEMINI ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except AttributeError:
    st.error("Clé API Google non trouvée. Veuillez la configurer dans .streamlit/secrets.toml")
    st.stop() 

model = genai.GenerativeModel('gemini-1.5-flash') 

# --- CORPS DE L'APPLICATION ---
col1, col2, col3 = st.columns(3)

with col1:
    poids = st.number_input("Votre poids (kg)", min_value=30, max_value=200, value=110)
with col2:
    objectif = st.selectbox("Votre objectif", ["Perte de poids", "Maintien", "Prise de masse"])
with col3:
    allergies = st.text_input("Allergies (ex: noix, lactose)", placeholder="Aucune")

if st.button("Générer mon plan", type="primary"):
    with st.spinner("L'IA prépare vos repas..."):

        prompt = f"""
        Tu es un nutritionniste sportif expert.
        Mon profil est le suivant :
        - Poids actuel : {poids} kg
        - Objectif : {objectif}
        - Allergies : {allergies}

        Ta mission :
        Propose-moi 3 idées de repas (Petit-déjeuner, Déjeuner, Dîner)
        qui soient simples, rapides à préparer, et adaptées à mon objectif.

        Formatte ta réponse en Markdown :
        - Un titre pour chaque repas (ex: ### 🥞 Petit-déjeuner).
        - Une liste à puces pour les ingrédients.
        - Une courte phrase pour la préparation.
        - N'ajoute pas d'introduction ou de conclusion, donne juste les repas.
        """

        try:
            response = model.generate_content(prompt)
            st.subheader("💡 Voici vos suggestions de repas :")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Une erreur est survenue avec l'API : {e}")
