import streamlit as st
import google.generativeai as genai
import PIL.Image
import os

# --- CONFIGURATION GLOBALE ---
NOM_SITE = "ORION"
VERSION = "3.6 PRO"

st.set_page_config(
    page_title=f"{NOM_SITE} | L'Excellence Immobilière", 
    layout="wide", 
    page_icon="✨"
)

# --- BRANDING & DESIGN (CSS) ---
def apply_branding():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Inter:wght@400;600;700&display=swap');
        .stApp {{ background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; font-family: 'Inter', sans-serif; }}
        h1, h2, h3 {{ font-family: 'Playfair Display', serif !important; color: #ffb800 !important; font-weight: 700; }}
        .sub-header {{ font-family: 'Playfair Display', serif !important; color: #ffb800 !important; font-size: 1.6rem; font-weight: 700; margin-bottom: 20px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3); }}
        .hero-section {{ text-align: center; padding: 60px 20px; background: rgba(255, 255, 255, 0.03); border-radius: 20px; margin-bottom: 30px; border: 1px solid rgba(255, 184, 0, 0.1); }}
        .result-box {{ background-color: rgba(255, 255, 255, 0.04); border-left: 5px solid #ffb800; padding: 25px; border-radius: 0 15px 15px 0; white-space: pre-wrap; }}
        .stButton>button {{ background: linear-gradient(90deg, #ffb800 0%, #f59e0b 100%); color: #0f172a; font-weight: 800; border-radius: 8px; width: 100%; border: none; }}
    </style>
    """, unsafe_allow_html=True)

apply_branding()

# --- GESTION DE LA SESSION ---
if "auth_state" not in st.session_state:
    st.session_state.auth_state = False

def login_form():
    st.markdown('<div class="sub-header" style="text-align:center;">Accès Membre Premium</div>', unsafe_allow_html=True)
    with st.form("login_form"):
        user = st.text_input("Identifiant")
        pwd = st.text_input("Mot de passe", type="password")
        if st.form_submit_button("Se connecter"):
            if user in st.secrets["passwords"] and pwd == st.secrets["passwords"][user]:
                st.session_state.auth_state = True
                st.rerun()
            else:
                st.error("Identifiants incorrects.")

# --- NAVIGATION ---
if not st.session_state.auth_state:
    menu_accueil = st.sidebar.selectbox("Navigation", ["🏠 Accueil", "🔐 Se connecter"])
    
    if menu_accueil == "🏠 Accueil":
        st.markdown("""
        <div class="hero-section">
            <h1>L'outil intelligent au service de l'Excellence Immobilière</h1>
            <p style="font-size:1.3rem; color:#94a3b8; max-width:800px; margin: 20px auto;">
                ORION accompagne les agents d'exception dans la rédaction, l'analyse et la stratégie au quotidien. 
                Gagnez en productivité et en prestige.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Bouton Stripe sécurisé (Remplace par ton vrai lien Stripe)
        st.link_button("🔥 DÉCOUVRIR LES OFFRES PREMIUM", "https://buy.stripe.com/TON_LIEN_STRIPE", use_container_width=True, type="primary")
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="sub-header" style="font-size:1.2rem;">📢 Marketing</div>', unsafe_allow_html=True)
            st.write("Annonces et posts réseaux sociaux générés en 30 secondes.")
        with c2:
            st.markdown('<div class="sub-header" style="font-size:1.2rem;">⚖️ Expertise</div>', unsafe_allow_html=True)
            st.write("Analyse flash de diagnostics et aide à l'estimation précise.")
        with c3:
            st.markdown('<div class="sub-header" style="font-size:1.2rem;">🤝 Matching</div>', unsafe_allow_html=True)
            st.write("Correspondance intelligente entre vos mandats et acquéreurs.")
    else:
        login_form()
else:
    # --- INTERFACE PRO ---
    with st.sidebar:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.markdown(f"<h2>✨ {NOM_SITE}</h2>", unsafe_allow_html=True)
        
        st.markdown("---")
        page = st.radio("OUTILS MÉTIER", ["📢 Pack Marketing", "⚖️ Expertise", "🤝 Matching", "📋 Check-lists", "✉️ Modèles"])
        st.markdown("---")
        if st.button("Déconnexion"):
            st.session_state.auth_state = False
            st.rerun()

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    except:
        st.error("Clé API manquante dans les Secrets.")
        st.stop()

    # --- LOGIQUE DES OUTILS ---
    if page == "📢 Pack Marketing":
        st.title("📢 Pack Marketing")
        col1, col2 = st.columns(2)
        with col1:
            type_b = st.text_input("Type de bien (ex: Villa)")
            lieu = st.text_input("Localisation")
        with col2:
            prix = st.text_input("Prix")
            atouts = st.text_area("Points forts")
        
        if st.button("GÉNÉRER LE PACK"):
            model = genai.GenerativeModel('gemini-1.5-flash')
            res = model.generate_content(f"Rédige une annonce de luxe pour : {type_b} à {lieu} pour {prix}. Atouts: {atouts}")
            st.markdown(f'<div class="result-box">{res.text}</div>', unsafe_allow_html=True)

    elif page == "⚖️ Expertise":
        st.title("⚖️ Expertise")
        doc = st.file_uploader("Scanner un diagnostic", type=["jpg", "png"])
        if st.button("ANALYSER"):
            if doc:
                model = genai.GenerativeModel('gemini-1.5-flash')
                res = model.generate_content(["Analyse les points d'attention :", PIL.Image.open(doc)])
                st.markdown(f'<div class="result-box">{res.text}</div>', unsafe_allow_html=True)
    
    # ... Les autres pages suivent la même structure simple ...
