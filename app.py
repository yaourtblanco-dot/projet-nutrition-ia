# app.py
import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Assistant Nutrition IA",
    page_icon="🥑",
    layout="centered"
)

# --- CONNEXION À L'API GEMINI ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Assure-toi que c'est le bon nom de modèle que tu as trouvé dans AI Studio
    model = genai.GenerativeModel('gemini-2.5-flash-image') 
except Exception as e:
    st.error(f"Erreur de configuration de l'API : {e}")
    st.stop()

# --- TITRE DE L'APPLICATION ---
st.title("🥑 Assistant Nutrition IA")
st.caption("Remplissez vos informations pour générer un plan de repas personnalisé.")

# --- SECTION DES INPUTS UTILISATEUR ---
with st.container(border=True):
    st.subheader("Votre Profil", anchor=False)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        poids = st.number_input("Votre poids (kg)", min_value=30, max_value=200, value=110, key="poids_input")
    with col2:
        objectif = st.selectbox("Votre objectif", ["Perte de poids", "Maintien", "Prise de masse"], key="objectif_input")
    with col3:
        allergies = st.text_input("Allergies", placeholder="Aucune", key="allergies_input")

# Ajoute un petit espace vertical
st.write("") 

# --- BOUTON DE GÉNÉRATION ---
if st.button("Générer mon plan", type="primary", use_container_width=True):
    
    with st.spinner("L'IA prépare vos repas..."):
        
        # --- PROMPT POUR L'IA ---
        prompt = f"""
        Tu es un nutritionniste sportif expert.
        Mon profil est le suivant :
        - Poids actuel : {poids} kg
        - Objectif : {objectif}
        - Allergies : {allergies}

        Ta mission :
        Propose-moi 3 idées de repas (Petit-déjeuner, Déjeuner, Dîner)
        qui soient simples, rapides à préparer, et adaptées à mon objectif.

        Formatte ta réponse en Markdown de manière très épurée et professionnelle.
        - Un titre pour chaque repas (ex: ### Petit-déjeuner).
        - Une liste à puces pour les ingrédients.
        - Une courte phrase pour la préparation.
        - **N'ajoute AUCUN emoji, ni dans les titres ni dans le texte.**
        - N'ajoute pas d'introduction ou de conclusion, donne juste les repas.
        """
        
        # --- GÉNÉRATION ET AFFICHAGE DE LA RÉPONSE ---
        try:
            response = model.generate_content(prompt)
            st.subheader("Plan de Repas Recommandé", divider="blue")
            st.markdown(response.text)
        
        except Exception as e:
            st.error(f"Une erreur est survenue avec l'API : {e}")
