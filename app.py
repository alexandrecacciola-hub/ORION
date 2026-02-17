import os
import streamlit as st
import google.generativeai as genai
import PIL.Image
import urllib.parse

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="ImmoIA Pro | L'Excellence Immobilière", 
    layout="wide", 
    page_icon="💎"
)

# --- BRANDING & CSS PERSONNALISÉ ---
def apply_branding():
    st.markdown("""
    <style>
        /* Importation d'une police moderne */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Fond dégradé Midnight Blue */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }

        /* Carte de contenu (les onglets) */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 12px;
        }

        .stTabs [data-baseweb="tab"] {
            height: 45px;
            border-radius: 8px;
            background-color: transparent;
            color: #94a3b8;
            border: none;
            font-weight: 600;
        }

        .stTabs [aria-selected="true"] {
            background-color: #ffb800 !important; /* Couleur Or/Jaune */
            color: #0f172a !important;
        }

        /* Champs de saisie stylisés */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            background-color: #1e293b !important;
            color: white !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            transition: 0.3s;
        }

        .stTextInput input:focus {
            border-color: #ffb800 !important;
            box-shadow: 0 0 0 1px #ffb800 !important;
        }

        /* Bouton Principal - Style Or */
        .stButton>button {
            background: linear-gradient(90deg, #ffb800 0%, #f59e0b 100%);
            color: #0f172a;
            border: none;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-radius: 8px;
            padding: 15px;
            transition: transform 0.2s;
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(251, 191, 36, 0.4);
            color: #000;
        }

        /* Bouton Email - Style Emeraude */
        .email-button {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 14px;
            background: #10b981;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            margin-top: 15px;
            transition: 0.3s;
        }
        .email-button:hover { background: #059669; }

        .obligatoire { color: #ffb800; font-size: 0.8rem; font-style: italic; }
        
        /* Personnalisation des titres */
        h1, h2, h3 {
            background: linear-gradient(to right, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
    </style>
    """, unsafe_allow_html=True)

apply_branding()

# --- CONFIGURATION API ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    else:
        st.error("⚠️ Clé API manquante dans .streamlit/secrets.toml")
        st.stop()
except Exception as e:
    st.error(f"Erreur de configuration : {e}")
    st.stop()

# --- BARRE LATÉRALE ---
with st.sidebar:
    # On vérifie si le fichier existe pour éviter le message d'erreur rouge
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        # Si le fichier est manquant, on affiche un logo temporaire stylé
        st.markdown("""
            <div style='text-align: center; padding: 10px; border: 2px solid #ffb800; border-radius: 10px;'>
                <h2 style='color: #ffb800; margin:0;'>💎 ImmoIA Pro</h2>
                <p style='font-size: 0.8rem; color: #94a3b8;'>Logo introuvable</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("🚀 Version 1.2 | Licence Premium")
    st.write("Compte : **Alexandre Immo**")
    st.write("Statut : **Connecté**")
# --- SYSTÈME D'ONGLETS ---
tab1, tab2 = st.tabs(["📢 GÉNÉRATEUR D'ANNONCE & PACK RS", "🤝 COMPTE-RENDU DE VISITE"])

# ==============================================================================
# ONGLET 1 : GÉNÉRATEUR D'ANNONCE
# ==============================================================================
with tab1:
    st.markdown('<span class="obligatoire">* Mentions obligatoires</span>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Structure")
        ton_choisi = st.selectbox("Style*", ["Luxe & Élégant", "Professionnel & Concis", "Chaleureux & Familial", "Urgent & Bonne Affaire"])
        type_bien = st.text_input("Type de bien*", placeholder="Ex: Loft contemporain")
        surface = st.text_input("Surface (m²)*", placeholder="Ex: 120")
        chambres = st.text_input("Nombre de chambres*", placeholder="Ex: 3")
        annee_construction = st.text_input("Année", placeholder="Ex: 2022")

    with col2:
        st.subheader("Localisation")
        lieu = st.text_input("Lieu*", placeholder="Ex: Paris 8ème")
        prix = st.text_input("Prix (€)*", placeholder="Ex: 1450000")
        taxe_fonciere = st.text_input("Taxe foncière", placeholder="Ex: 2100")
        charges = st.text_input("Charges / mois", placeholder="Ex: 450")

    with col3:
        st.subheader("Marketing")
        image_telechargee = st.file_uploader("Photo du bien", type=["jpg", "jpeg", "png"])
        dpe = st.text_input("DPE", placeholder="Ex: A")
        atouts = st.text_area("Points forts*", placeholder="Cuisine d'architecte, terrasse plein sud...", height=100)
        point_fort_unique = st.text_input("Argument Choc*", placeholder="Vue panoramique sur la Seine")
        infos_contact = st.text_input("Contact*", placeholder="Alexandre - 06 12 34 56 78")

    if st.button("✨ GÉNÉRER LE PACK MARKETING COMPLET"):
        if not all([type_bien, surface, chambres, lieu, prix, atouts, point_fort_unique, infos_contact]):
            st.warning("⚠️ Remplissez les champs obligatoires.")
        else:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt_marketing = f"Expert marketing luxe. Rédige un pack complet : Annonce premium + Post FB + Post Instagram avec 20 hashtags + Tweet. Bien: {type_bien} à {lieu}, {surface}m2, {chambres}ch. Prix: {prix}€. Atouts: {atouts}. Argument phare: {point_fort_unique}. Contact: {infos_contact}. Style: {ton_choisi}."
                inputs = [prompt_marketing]
                if image_telechargee: inputs.append(PIL.Image.open(image_telechargee))
                with st.spinner("Conception de votre campagne digitale..."):
                    response = model.generate_content(inputs)
                st.success("✅ Votre pack est prêt !")
                st.code(response.text, language="markdown")
            except Exception as e:
                st.error(f"Erreur : {e}")

# ==============================================================================
# ONGLET 2 : COMPTE-RENDU DE VISITE
# ==============================================================================
with tab2:
    st.subheader("L'Assistant Diplomate")
    st.write("Transformez vos impressions de terrain en rapports clients irréprochables.")
    col_cr1, col_cr2 = st.columns(2)
    with col_cr1:
        nom_vendeur = st.text_input("Propriétaire", placeholder="Mme Lefebvre")
        nom_visiteur = st.text_input("Visiteur", placeholder="Famille Gomez")
        email_dest = st.text_input("Email client", placeholder="client@vendeur.fr")
    with col_cr2:
        notes_brutes = st.text_area("Notes de visite*", placeholder="Il a aimé la vue mais déteste le carrelage. Budget trop court de 15k€.", height=125)
    
    if st.button("📝 GÉNÉRER LE RAPPORT"):
        if not notes_brutes:
            st.warning("⚠️ Saisissez vos notes.")
        else:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt_cr = f"Agent immo expert. Transforme ces notes en rapport diplomatique et bienveillant pour {nom_vendeur} suite à la visite de {nom_visiteur}. Notes : {notes_brutes}"
                with st.spinner("Analyse diplomatique..."):
                    response_cr = model.generate_content(prompt_cr)
                    texte_rapport = response_cr.text
                st.success("✅ Rapport diplomatique prêt !")
                st.code(texte_rapport, language="markdown")
                sujet_mail = urllib.parse.quote(f"Suivi de visite - {nom_visiteur}")
                corps_mail = urllib.parse.quote(texte_rapport)
                st.markdown(f'<a href="mailto:{email_dest}?subject={sujet_mail}&body={corps_mail}" class="email-button">📧 Envoyer par Email</a>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erreur : {e}")