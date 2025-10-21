# app.py

import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION DE LA PAGE ---
# CHANGÉ : J'ai remplacé l'emoji par un icône "shortcode" plus propre (un avocat)
# et j'ai mis layout="centered" pour que ce soit plus net sur grand écran.
st.set_page_config(
    page_title="Assistant Nutrition IA",
    page_icon="🥑",
    layout="centered"
)

# --- CONNEXION À L'API GEMINI ---
# (Pas de changement ici, on cache la connexion)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash-image') # Le nom de ton modèle
except Exception as e:
    # Affiche une erreur claire si la clé n'est pas trouvée ou si le modèle plante
    st.error(f"Erreur de configuration de l'API : {e}")
    st.stop() # Arrête l'appli

# --- TITRE DE L'APPLICATION ---
# CHANGÉ : J'ai enlevé l'emoji du titre.
st.title("Assistant Nutrition IA")

# CHANGÉ : J'ai remplacé le "subheader" par un "caption" plus discret et pro.
st.caption("Remplissez vos informations pour générer un plan de repas personnalisé.")

# CHANGÉ : J'ai ajouté un séparateur visuel propre.
st.divider()

# --- CORPS DE L'APPLICATION ---
# (Pas de changement sur la structure des colonnes, elle est ergonomique)
col1, col2, col3 = st.columns(3)

with col1:
    poids = st.number_input("Votre poids (kg)", min_value=30, max_value=200, value=110)
with col2:
    objectif = st.selectbox("Votre objectif", ["Perte de poids", "Maintien", "Prise de masse"])
with col3:
    allergies = st.text_input("Allergies (ex: noix, lactose)", placeholder="Aucune")

# (Le bouton reste le même, `type="primary"` est une bonne pratique)
if st.button("Générer mon plan", type="primary"):
    
    with st.spinner("L'IA prépare vos repas..."):
        
        # --- LE PROMPT (L'INSTRUCTION PERSONNALISÉE) ---
        # CHANGÉ : C'est la partie la plus importante !
        # J'ai demandé à l'IA de ne PAS utiliser d'emojis.
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

        # --- APPEL À L'IA ---
        try:
            response = model.generate_content(prompt)
            
            # CHANGÉ : J'ai ajouté un séparateur avant la réponse.
            st.divider()
            
            # CHANGÉ : J'ai enlevé l'emoji "💡" du sous-titre.
            st.subheader("Voici vos suggestions de repas :")
            st.markdown(response.text)
        
        except Exception as e:
            st.error(f"Une erreur est survenue avec l'API : {e}")
