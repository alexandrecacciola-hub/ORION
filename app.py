import streamlit as st
import google.generativeai as genai
import PIL.Image
import urllib.parse
import os

# --- CONFIGURATION GLOBALE ---
NOM_SITE = "ORION"
VERSION = "3.6 PRO"

st.set_page_config(page_title=f"{NOM_SITE} | L'Excellence Immobilière", layout="wide", page_icon="✨")

# --- BRANDING & DESIGN (CSS) ---
def apply_branding():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,700&family=Inter:wght@400;600;700&display=swap');
        .stApp {{ background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; font-family: 'Inter', sans-serif; }}
        
        h1, h2, h3 {{ font-family: 'Playfair Display', serif !important; color: #ffb800 !important; font-weight: 700; }}
        
        /* TOUTES LES SOUS-RUBRIQUES : Playfair Display & Doré */
        .sub-header {{
            font-family: 'Playfair Display', serif !important;
            color: #ffb800 !important;
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 20px;
            margin-top: 15px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        
        .hero-section {{
            text-align: center;
            padding: 80px 20px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 20px;
            margin-bottom: 40px;
            border: 1px solid rgba(255, 184, 0, 0.1);
        }}
        
        .cta-button {{
            background: linear-gradient(90deg, #ffb800 0%, #f59e0b 100%);
            color: #0f172a !important;
            padding: 18px 40px;
            border-radius: 10px;
            font-weight: 800;
            text-decoration: none;
            font-size: 1.2rem;
            display: inline-block;
            margin-top: 20px;
            transition: 0.3s;
        }}
        
        .result-box {{
            background-color: rgba(255, 255, 255, 0.04);
            border-left: 5px solid #ffb800;
            padding: 25px;
            border-radius: 0 15px 15px 0;
            font-family: 'Inter', sans-serif;
            line-height: 1.7;
            color: #f1f5f9;
            white-space: pre-wrap;
        }}

        .stButton>button {{
            background: linear-gradient(90deg, #ffb800 0%, #f59e0b 100%);
            color: #0f172a; font-weight: 800; text-transform: uppercase;
            border-radius: 8px; padding: 12px; width: 100%; border: none;
        }}
    </style>
    """, unsafe_allow_html=True)

apply_branding()

# --- GESTION DE LA SESSION ---
if "auth_state" not in st.session_state:
    st.session_state.auth_state = False

# --- FONCTION DE CONNEXION ---
def login_form():
    st.markdown('<div class="sub-header" style="text-align:center;">Accès Membre Premium</div>', unsafe_allow_html=True)
    with st.form("login_form"):
        user = st.text_input("Identifiant")
        pwd = st.text_input("Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter")
        if submit:
            if user in st.secrets["passwords"] and pwd == st.secrets["passwords"][user]:
                st.session_state.auth_state = True
                st.rerun()
            else:
                st.error("Identifiants incorrects.")

# --- NAVIGATION PRINCIPALE ---
if not st.session_state.auth_state:
    # --- PAGE D'ACCUEIL ---
    menu_accueil = st.sidebar.selectbox("Navigation", ["🏠 Accueil", "🔐 Se connecter"])
    
    if menu_accueil == "🏠 Accueil":
        st.markdown(f"""
        <div class="hero-section">
            <h1>L'outil intelligent au service de l'Excellence Immobilière</h1>
            <p style="font-size:1.3rem; color:#94a3b8; max-width:800px; margin: 20px auto;">
                ORION accompagne les agents d'exception dans la rédaction, l'analyse et la stratégie au quotidien. 
                Gagnez en productivité et en prestige.
            </p>
            <a href="TON_LIEN_STRIPE_ICI" class="cta-button">DÉCOUVRIR LES OFFRES PREMIUM</a>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="sub-header" style="font-size:1.2rem;">📢 Marketing</div>', unsafe_allow_html=True)
            st.write("Annonces de luxe et posts réseaux sociaux générés instantanément.")
        with c2:
            st.markdown('<div class="sub-header" style="font-size:1.2rem;">⚖️ Expertise</div>', unsafe_allow_html=True)
            st.write("Analyse flash de diagnostics techniques et aide à l'estimation précise.")
        with c3:
            st.markdown('<div class="sub-header" style="font-size:1.2rem;">🤝 Matching</div>', unsafe_allow_html=True)
            st.write("Algorithme de correspondance entre vos mandats et vos acquéreurs.")
            
    else:
        login_form()

else:
    # --- INTERFACE PRO (MEMBRES) ---
    with st.sidebar:
        st.markdown(f"<h2>✨ {NOM_SITE}</h2>", unsafe_allow_html=True)
        page = st.radio("OUTILS MÉTIER", [
            "📢 Pack Marketing", "⚖️ Expertise", "🤝 Matching", "📋 Check-lists", "✉️ Modèles"
        ])
        st.markdown("---")
        if st.button("Déconnexion"):
            st.session_state.auth_state = False
            st.rerun()

    # --- CONFIGURATION API ---
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    except:
        st.error("Clé API manquante.")
        st.stop()

    # --- LOGIQUE DES PAGES ---
    if page == "📢 Pack Marketing":
        st.title(f"✨ {NOM_SITE} | Marketing")
        tab1, tab2 = st.tabs(["📢 GÉNÉRATEUR D'ANNONCE", "🤝 COMPTE-RENDU DE VISITE"])
        
        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('<div class="sub-header">Le Bien</div>', unsafe_allow_html=True)
                ton = st.selectbox("Style*", ["Luxe", "Pro", "Chaleureux"])
                type_b = st.text_input("Type de bien*", placeholder="Ex: Loft")
                surf = st.text_input("Surface (m²)*")
                chambres = st.text_input("Chambres*")
                annee = st.text_input("Année de construction")
            with col2:
                st.markdown('<div class="sub-header">Localisation</div>', unsafe_allow_html=True)
                lieu = st.text_input("Lieu*", placeholder="Ville, quartier")
                prix = st.text_input("Prix (€)*")
                taxe = st.text_input("Taxe foncière (€)")
                charges = st.text_input("Charges (€/mois)")
            with col3:
                st.markdown('<div class="sub-header">Médias & Contact</div>', unsafe_allow_html=True)
                img = st.file_uploader("Photo", type=["jpg", "png"])
                dpe = st.text_input("Classe DPE")
                atouts = st.text_area("Atouts*", height=68)
                choc = st.text_input("Argument N°1*")
                contact = st.text_input("Contact*")
                
            if st.button("✨ GÉNÉRER LE PACK"):
                model = genai.GenerativeModel('gemini-flash-latest')
                prompt = f"Expert immo. Rédige pack: {type_b}, {surf}m2, {chambres} ch, {lieu}, {prix}€. {atouts}. Style: {ton}."
                res = model.generate_content([prompt, PIL.Image.open(img)] if img else [prompt])
                st.markdown(f'<div class="result-box">{res.text}</div>', unsafe_allow_html=True)

    elif page == "⚖️ Expertise":
        st.title(f"⚖️ {NOM_SITE} | Expertise")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="sub-header">Analyse Technique</div>', unsafe_allow_html=True)
            doc = st.file_uploader("Scanner un diagnostic", type=["jpg", "png"])
            if st.button("🔍 ANALYSER"):
                if doc:
                    model = genai.GenerativeModel('gemini-flash-latest')
                    res = model.generate_content(["Points d'alerte de ce diagnostic.", PIL.Image.open(doc)])
                    st.markdown(f'<div class="result-box">{res.text}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="sub-header">Aide à l\'Estimation</div>', unsafe_allow_html=True)
            data = st.text_area("Détails du bien et du secteur")
            if st.button("📊 ARGUMENTAIRE PRIX"):
                model = genai.GenerativeModel('gemini-flash-latest')
                res = model.generate_content(f"Argumentaire pro pour justifier un prix : {data}")
                st.markdown(f'<div class="result-box">{res.text}</div>', unsafe_allow_html=True)
    
    # ... (Les autres pages Matching, Check-lists, Modèles conservent la même logique)
