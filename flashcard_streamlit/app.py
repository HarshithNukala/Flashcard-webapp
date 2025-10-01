import streamlit as st
import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:5001"
st.set_page_config(
    page_title="Flashcards App",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"  # Changed from "collapsed" to "expanded"
)

# Hide sidebar completely
st.markdown(
    """
    <style>
    /* Sidebar styling - keep existing */
    [data-testid="collapsedControl"] {
        display: block !important;
    }
    [data-testid="stSidebar"] {
        display: block !important;
        background-color: #f8f9fa !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-color: #2c3e50 !important;
        background-image: none !important;
    }
    [data-testid="stSidebar"] .css-1d391kg {
        background-color: #2c3e50 !important;
    }
    
    /* Sidebar text and elements styling - keep existing */
    [data-testid="stSidebar"] .element-container {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown h4,
    [data-testid="stSidebar"] .stMarkdown h5,
    [data-testid="stSidebar"] .stMarkdown h6 {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: #ffffff !important;
    }
    
    /* Sidebar buttons styling - keep existing */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #34495e !important;
        color: #ffffff !important;
        border: 1px solid #5a6c7d !important;
        border-radius: 6px !important;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #4a5f7a !important;
        border-color: #667eea !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    /* Primary buttons in sidebar - keep existing */
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background-color: #e74c3c !important;
        color: #ffffff !important;
        border: 1px solid #c0392b !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background-color: #c0392b !important;
        border-color: #a93226 !important;
    }
    
    /* Sidebar metrics styling - keep existing */
    [data-testid="stSidebar"] .metric-container {
        background-color: #34495e !important;
        border-radius: 8px !important;
        padding: 10px !important;
        margin: 5px 0 !important;
    }
    [data-testid="stSidebar"] [data-testid="metric-container"] {
        background-color: #34495e !important;
        border-radius: 8px !important;
        padding: 10px !important;
        margin: 5px 0 !important;
        border: 1px solid #5a6c7d !important;
    }
    [data-testid="stSidebar"] [data-testid="metric-container"] label {
        color: #bdc3c7 !important;
        font-size: 0.8rem !important;
    }
    [data-testid="stSidebar"] [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    
    /* Custom user info card - keep existing */
    .user-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        margin-bottom: 1rem !important;
        text-align: center !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }
    .user-info h3 {
        margin: 0 0 0.5rem 0 !important;
        font-size: 1.1em !important;
        color: white !important;
    }
    .user-info p {
        margin: 0 !important;
        font-size: 0.9em !important;
        opacity: 0.9 !important;
        color: white !important;
    }
    
    /* Sidebar dividers - keep existing */
    [data-testid="stSidebar"] hr {
        border-color: #5a6c7d !important;
        margin: 1rem 0 !important;
    }
    
    /* Main content styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* UPDATED: Dark theme deck cards styling */
    .deck-card {
        border: 1px solid #4a5568;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        height: 200px;
        transition: transform 0.3s, box-shadow 0.3s;
        position: relative;
        color: #ffffff;
    }
    .deck-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
        border-color: #667eea;
    }
    .deck-card h3 {
        color: #ffffff;
        margin: 0 0 10px 0;
        font-size: 1.2em;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    .deck-card .description {
        color: #cbd5e0;
        font-size: 0.9em;
        line-height: 1.4;
        margin-bottom: 15px;
        height: 60px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }
    .deck-card .stats {
        color: #a0aec0;
        font-size: 0.8em;
        margin-bottom: 15px;
        font-weight: 500;
        background: rgba(255,255,255,0.1);
        padding: 4px 8px;
        border-radius: 12px;
        display: inline-block;
    }
    
    /* UPDATED: Dark theme flashcard styling */
    .flashcard-grid {
        border: 1px solid #4a5568;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        height: 180px;
        transition: transform 0.3s, box-shadow 0.3s;
        position: relative;
        color: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .flashcard-grid:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(118, 75, 162, 0.15);
        border-color: #764ba2;
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
    }
    .flashcard-header {
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 10px;
        font-size: 1em;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        background: rgba(102, 126, 234, 0.2);
        padding: 4px 8px;
        border-radius: 8px;
        display: inline-block;
    }
    .flashcard-question {
        color: #e2e8f0;
        font-size: 0.9em;
        line-height: 1.4;
        height: 80px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        margin-bottom: 10px;
    }
    
    /* Enhanced button styling for cards */
    .stButton > button {
        border-radius: 6px;
        transition: all 0.2s;
        font-weight: 500;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Main page metrics styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    [data-testid="metric-container"] label {
        color: #ffffff !important;
        font-weight: 500;
    }
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #ffffff !important;
        font-weight: 700;
    }
    
    /* Grid container */
    .grid-container {
        margin: 1rem 0;
    }
    
    /* Enhanced expander styling */
    [data-testid="stExpander"] {
        border: 1px solid #4a5568;
        border-radius: 8px;
        background-color: #2d3748;
    }
    [data-testid="stExpander"] summary {
        background-color: #2d3748;
        color: #ffffff;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background-color: #1a202c;
        color: #ffffff;
        border-radius: 0 0 8px 8px;
    }
    
    /* Form styling */
    .stForm {
        background-color: #2d3748;
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #4a5568;
    }
    
    /* Navigation styles */
    .sidebar-nav {
        margin: 1rem 0;
    }
    .nav-button {
        width: 100%;
        margin: 0.2rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Session State Management
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'selected_deck' not in st.session_state:
    st.session_state.selected_deck = None

# API Helper Functions
def api_request(method, endpoint, data=None, headers=None):
    """Make API requests with error handling"""
    url = f"{API_BASE_URL}{endpoint}"
    default_headers = {"Content-Type": "application/json"}
    
    if st.session_state.token:
        default_headers["Authorization"] = f"Bearer {st.session_state.token}"
    
    if headers:
        default_headers.update(headers)
    
    try:
        if method == "GET":
            response = requests.get(url, headers=default_headers)
        elif method == "POST":
            response = requests.post(url, json=data, headers=default_headers)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=default_headers)
        elif method == "DELETE":
            response = requests.delete(url, headers=default_headers)
        
        if response.status_code == 401:
            st.session_state.authenticated = False
            st.session_state.token = None
            st.rerun()
        
        return response
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to server. Make sure your Express server is running on port 5001.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Authentication Functions
def login(email, password):
    """Login user"""
    data = {"email": email, "password": password}
    response = api_request("POST", "/api/auth/login", data)
    
    if response and response.status_code == 200:
        result = response.json()
        st.session_state.token = result.get('token')
        st.session_state.authenticated = True
        get_user_info()
        st.session_state.current_page = 'dashboard'
        st.success("Login successful!")
        st.rerun()
    elif response:
        st.error("Invalid email or password")
    
def register(username, password, email):
    """Register new user"""
    data = {"name": username, "password": password, "email": email}
    response = api_request("POST", "/api/auth/register", data)
    
    if response and response.status_code == 201:
        st.success("Registration successful! Please login.")
        return True
    elif response:
        try:
            error = response.json().get('message', 'Registration failed')
            st.error(error)
        except:
            st.error("Registration failed")
    return False

def get_user_info():
    """Get current user info"""
    response = api_request("GET", "/api/auth/me")
    if response and response.status_code == 200:
        st.session_state.user = response.json()

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.current_page = 'login'
    st.session_state.selected_deck = None
    st.success("Logged out successfully!")
    st.rerun()
    
# Deck Functions
def get_decks():
    """Get all decks for the current user"""
    response = api_request("GET", "/api/decks")
    if response and response.status_code == 200:
        return response.json()
    return []

def create_deck(name, description):
    """Create a new deck"""
    data = {"name": name, "description": description}
    response = api_request("POST", "/api/decks", data)
    
    if response and response.status_code == 201:
        st.success("Deck created successfully!")
        return True
    elif response:
        st.error("Failed to create deck")
    return False

def update_deck(deck_id, name, description):
    """Update an existing deck"""
    data = {"name": name, "description": description}
    response = api_request("PUT", f"/api/decks/{deck_id}", data)
    
    if response and response.status_code == 200:
        st.success("Deck updated successfully!")
        return True
    elif response:
        st.error("Failed to update deck")
    return False

def delete_deck(deck_id):
    """Delete a deck"""
    response = api_request("DELETE", f"/api/decks/{deck_id}")
    
    if response and response.status_code == 200:
        st.success("Deck deleted successfully!")
        return True
    elif response:
        st.error("Failed to delete deck")
    return False

# Flashcard Functions
def get_flashcards(deck_id):
    """Get all flashcards for a deck"""
    response = api_request("GET", f"/api/flashcards/{deck_id}")
    if response and response.status_code == 200:
        return response.json()
    return []

def create_flashcard(deck_id, question, answer, card_type="QNA", options=None):
    """Create a new flashcard with support for MCQ"""
    data = {
        "question": question,
        "answer": answer,
        "type": card_type
    }
    
    if card_type == "MCQ" and options:
        data["options"] = options
    
    response = api_request("POST", f"/api/flashcards/{deck_id}", data)
    
    if response and response.status_code == 201:
        st.success("Flashcard created successfully!")
        return True
    elif response:
        st.error("Failed to create flashcard")
    return False

def update_flashcard(flashcard_id, question, answer, card_type="QNA", options=None):
    """Update an existing flashcard with MCQ support"""
    data = {
        "question": question,
        "answer": answer,
        "type": card_type
    }
    
    if card_type == "MCQ" and options:
        data["options"] = options
    
    response = api_request("PUT", f"/api/flashcards/{flashcard_id}", data)
    
    if response and response.status_code == 200:
        st.success("Flashcard updated successfully!")
        return True
    elif response:
        st.error("Failed to update flashcard")
    return False

def delete_flashcard(flashcard_id):
    """Delete a flashcard"""
    response = api_request("DELETE", f"/api/flashcards/{flashcard_id}")
    
    if response and response.status_code == 200:
        st.success("Flashcard deleted successfully!")
        return True
    elif response:
        st.error("Failed to delete flashcard")
    return False

# UI Components

def render_sidebar():
    """Render sidebar with user info and logout"""
    if st.session_state.authenticated and st.session_state.user:
        with st.sidebar:
            # User Info Section
            st.markdown(
                f"""
                <div class="user-info">
                    <h3>👋 Welcome!</h3>
                    <p>{st.session_state.user.get('Name', 'user')}</p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.markdown("---")
            
            # Navigation
            st.markdown("### 📱 Navigation")
            
            if st.button("🏠 Dashboard", key="nav_dashboard", use_container_width=True):
                st.session_state.current_page = 'dashboard'
                st.rerun()
            
            if st.button("📚 My Decks", key="nav_decks", use_container_width=True):
                st.session_state.current_page = 'decks'
                st.rerun()
            
            if st.button("➕ Create Deck", key="nav_create", use_container_width=True):
                st.session_state.current_page = 'create_deck'
                st.rerun()
            
            st.markdown("---")
            
            # App Info
            st.markdown("### ℹ️ App Info")
            if st.session_state.user:
                decks = get_decks()
                total_cards = sum([len(get_flashcards(deck.get('_id'))) for deck in decks])
                
                st.metric("Total Decks", len(decks))
                st.metric("Total Cards", total_cards)
            
            st.markdown("---")
            
            # Logout Button
            st.markdown("### 🚪 Account")
            if st.button("🚪 Logout", key="sidebar_logout", type="primary", use_container_width=True):
                logout()


def render_auth_page():
    """Render authentication page"""
    st.markdown('<div class="main-header"><h1 style="color: white; margin: 0;">📚 Flashcards App</h1></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.subheader("Login")
            username = st.text_input("Email", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", type="primary", use_container_width=True):
                if username and password:
                    login(username, password)
                else:
                    st.error("Please enter both username and password")
        
        with tab2:
            st.subheader("Register")
            reg_username = st.text_input("Username", key="reg_username")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Register", type="primary", use_container_width=True):
                if reg_username and reg_email and reg_password and reg_confirm:
                    if reg_password == reg_confirm:
                        register(reg_username, reg_password, reg_email)
                    else:
                        st.error("Passwords don't match")
                else:
                    st.error("Please fill in all fields")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_header():
    """Render simplified app header"""
    st.markdown('<div class="main-header"><h1 style="color: white; margin: 0;">📚 Flashcards App</h1></div>', unsafe_allow_html=True)

def render_dashboard():
    """Render main dashboard with grid layout"""
    render_header()
    
    # Quick Actions (simplified since navigation is now in sidebar)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.metric("📚 Your Decks", len(get_decks()))
    
    with col2:
        decks = get_decks()
        total_cards = sum([len(get_flashcards(deck.get('_id'))) for deck in decks])
        st.metric("🗃️ Total Cards", total_cards)
    
    with col3:
        if st.button("🎯 Quick Study", use_container_width=True, disabled=True):
            st.info("Study mode coming soon!")
    
    st.markdown("---")
    
    # Recent Decks in Grid
    st.subheader("Your Recent Decks")
    decks = get_decks()
    
    if decks:
        # Display decks in grid format (3 columns)
        recent_decks = decks[:6]  # Show max 6 recent decks
        
        for i in range(0, len(recent_decks), 3):
            cols = st.columns(3)
            
            for j, col in enumerate(cols):
                if i + j < len(recent_decks):
                    deck = recent_decks[i + j]
                    
                    with col:
                        # Custom HTML card
                        card_html = f"""
                        <div class="deck-card">
                            <h3>{deck.get('name', 'Untitled')}</h3>
                            <div class="description">{deck.get('description', 'No description')}</div>
                            <div class="stats">📚 {len(get_flashcards(deck.get('_id')))} cards</div>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        # Action button
                        if st.button("Open Deck", key=f"open_dash_{deck.get('_id')}", type="primary", use_container_width=True):
                            st.session_state.selected_deck = deck
                            st.session_state.current_page = 'flashcards'
                            st.rerun()
    else:
        st.info("You haven't created any decks yet. Use the sidebar to create your first deck!")

def render_decks_page():
    """Render decks management page with grid layout"""
    render_header()
    
    st.subheader("📚 My Decks")
    
    if st.button("➕ Create New Deck", type="primary"):
        st.session_state.current_page = 'create_deck'
        st.rerun()
    
    st.markdown("---")
    
    decks = get_decks()
    
    if decks:
        # Display decks in grid format (3 columns)
        for i in range(0, len(decks), 3):
            cols = st.columns(3)
            
            for j, col in enumerate(cols):
                if i + j < len(decks):
                    deck = decks[i + j]
                    
                    with col:
                        # Custom HTML card
                        card_html = f"""
                        <div class="deck-card">
                            <h3>{deck.get('name', 'Untitled')}</h3>
                            <div class="description">{deck.get('description', 'No description')}</div>
                            <div class="stats">📚 {len(get_flashcards(deck.get('_id')))} cards</div>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        # Action buttons in columns
                        btn_col1, btn_col2 = st.columns(2)
                        
                        with btn_col1:
                            if st.button("📖", key=f"open_{deck.get('_id')}", help="Open Deck", use_container_width=True):
                                st.session_state.selected_deck = deck
                                st.session_state.current_page = 'flashcards'
                                st.rerun()
                        
                        with btn_col2:
                            if st.button("✏️", key=f"edit_{deck.get('_id')}", help="Edit Deck", use_container_width=True):
                                st.session_state.edit_deck = deck
                                st.session_state.current_page = 'edit_deck'
                                st.rerun()
                        
                        # Delete button (full width)
                        if st.button("🗑️ Delete", key=f"delete_{deck.get('_id')}", type="secondary", use_container_width=True):
                            if st.session_state.get(f"confirm_delete_{deck.get('_id')}", False):
                                delete_deck(deck.get('_id'))
                                st.rerun()
                            else:
                                st.session_state[f"confirm_delete_{deck.get('_id')}"] = True
                                st.warning("Click delete again to confirm")
    else:
        st.info("You haven't created any decks yet.")

def render_create_deck_page():
    """Render create deck page"""
    render_header()
    
    st.subheader("➕ Create New Deck")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("create_deck_form"):
            deck_name = st.text_input("Deck Name", placeholder="Enter deck name...")
            deck_description = st.text_area("Description", placeholder="Enter deck description...")
            
            submitted = st.form_submit_button("Create Deck", type="primary", use_container_width=True)
            
            if submitted:
                if deck_name:
                    if create_deck(deck_name, deck_description):
                        st.session_state.current_page = 'decks'
                        st.rerun()
                else:
                    st.error("Please enter a deck name")

def render_edit_deck_page():
    """Render edit deck page"""
    render_header()
    
    st.subheader("✏️ Edit Deck")
    st.markdown("---")
    
    deck = st.session_state.get('edit_deck')
    if deck:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("edit_deck_form"):
                deck_name = st.text_input("Deck Name", value=deck.get('name', ''))
                deck_description = st.text_area("Description", value=deck.get('description', ''))
                
                submitted = st.form_submit_button("Update Deck", type="primary", use_container_width=True)
                
                if submitted:
                    if deck_name:
                        if update_deck(deck.get('_id'), deck_name, deck_description):
                            st.session_state.current_page = 'decks'
                            st.rerun()
                    else:
                        st.error("Please enter a deck name")

def render_flashcards_page():
    """Render flashcards page with improved MCQ support and answer hiding"""
    render_header()
    
    deck = st.session_state.selected_deck
    if not deck:
        st.error("No deck selected")
        st.session_state.current_page = 'dashboard'
        st.rerun()
        return
    
    st.subheader(f"📚 {deck.get('name', 'Untitled Deck')}")
    if deck.get('description'):
        st.write(deck.get('description'))
    
    # Add new flashcard form with dynamic fields
    with st.expander("➕ Add New Flashcard"):
        # Initialize session state for card type if not exists
        if 'new_card_type' not in st.session_state:
            st.session_state.new_card_type = "QNA"
        
        # Card type selection
        card_type = st.selectbox(
            "Card Type",
            options=["QNA", "MCQ"],
            index=0 if st.session_state.new_card_type == "QNA" else 1,
            key="card_type_selector",
            format_func=lambda x: "Question & Answer" if x == "QNA" else "Multiple Choice Question"
        )
        
        # Update session state when card type changes
        if card_type != st.session_state.new_card_type:
            st.session_state.new_card_type = card_type
            st.rerun()
        
        # Question input
        question = st.text_area(
            "Question", 
            key="new_flashcard_question", 
            placeholder="Enter your question here..."
        )
        
        # Dynamic fields based on card type
        if card_type == "QNA":
            # Traditional Q&A format
            answer = st.text_area(
                "Answer", 
                key="new_flashcard_answer", 
                placeholder="Enter the answer..."
            )
        else:  # MCQ format
            st.write("**Multiple Choice Options:**")
            col1, col2 = st.columns(2)
            
            with col1:
                option_a = st.text_input("Option A", key="new_mcq_option_a", placeholder="First option...")
                option_c = st.text_input("Option C", key="new_mcq_option_c", placeholder="Third option...")
            
            with col2:
                option_b = st.text_input("Option B", key="new_mcq_option_b", placeholder="Second option...")
                option_d = st.text_input("Option D", key="new_mcq_option_d", placeholder="Fourth option...")
            
            # Correct answer selection
            correct_answer = st.selectbox(
                "Correct Answer",
                options=["A", "B", "C", "D"],
                key="new_mcq_correct",
                help="Select which option is the correct answer"
            )
        
        # Submit button
        if st.button("Add Flashcard", type="primary"):
            if not question.strip():
                st.error("Please enter a question")
            elif card_type == "QNA":
                if not answer.strip():
                    st.error("Please enter an answer")
                else:
                    if create_flashcard(deck.get('_id'), question, answer, card_type):
                        # Clear fields on success
                        st.session_state.new_flashcard_question = ""
                        st.session_state.new_flashcard_answer = ""
                        st.rerun()
            else:  # MCQ
                options = [
                    st.session_state.get("new_mcq_option_a", "").strip(),
                    st.session_state.get("new_mcq_option_b", "").strip(),
                    st.session_state.get("new_mcq_option_c", "").strip(),
                    st.session_state.get("new_mcq_option_d", "").strip(),
                ]
                
                if sum(bool(opt) for opt in options) < 2:
                    st.error("Please enter at least 2 options for multiple choice")
                elif not options[ord(correct_answer) - ord("A")]:
                    st.error("The correct answer option cannot be blank")
                else:
                    mcq_answer = f"Correct Answer: {correct_answer}"
                    if create_flashcard(deck.get('_id'), question, mcq_answer, card_type, options):
                        # Clear all fields on success
                        st.session_state.new_flashcard_question = ""
                        st.session_state.new_mcq_option_a = ""
                        st.session_state.new_mcq_option_b = ""
                        st.session_state.new_mcq_option_c = ""
                        st.session_state.new_mcq_option_d = ""
                        st.rerun()
    
    st.markdown("---")
    
    # Display flashcards in grid
    flashcards = get_flashcards(deck.get('_id'))
    
    if flashcards:
        st.subheader(f"Flashcards ({len(flashcards)})")
        
        # Display flashcards in grid format (2 columns for better readability)
        for i in range(0, len(flashcards), 2):
            cols = st.columns(2)
            
            for j, col in enumerate(cols):
                if i + j < len(flashcards):
                    card = flashcards[i + j]
                    
                    with col:
                        # Custom HTML card with type indicator
                        question_preview = card.get('question', 'No question')[:100]
                        if len(card.get('question', '')) > 100:
                            question_preview += "..."
                        
                        card_type = card.get('type', 'QNA')
                        type_icon = "🔤" if card_type == "MCQ" else "❓"
                        type_label = "MCQ" if card_type == "MCQ" else "Q&A"
                        
                        card_html = f"""
                        <div class="flashcard-grid">
                            <div class="flashcard-header">{type_icon} Card {i + j + 1} ({type_label})</div>
                            <div class="flashcard-question">{question_preview}</div>
                        </div>
                        """
                        st.markdown(card_html, unsafe_allow_html=True)
                        
                        # Action buttons
                        btn_col1, btn_col2, btn_col3 = st.columns(3)
                        
                        with btn_col1:
                            view_key = f"view_{card.get('_id')}"
                            if st.button("👁️", key=view_key, help="View Card", use_container_width=True):
                                st.session_state[f"show_card_{card.get('_id')}"] = True
                                st.rerun()
                        
                        with btn_col2:
                            if st.button("✏️", key=f"edit_card_{card.get('_id')}", help="Edit Card", use_container_width=True):
                                st.session_state.edit_flashcard = card
                                st.session_state.show_edit_form = True
                                st.rerun()
                        
                        with btn_col3:
                            if st.button("🗑️", key=f"delete_card_{card.get('_id')}", help="Delete Card", type="secondary", use_container_width=True):
                                if st.session_state.get(f"confirm_delete_card_{card.get('_id')}", False):
                                    delete_flashcard(card.get('_id'))
                                    st.rerun()
                                else:
                                    st.session_state[f"confirm_delete_card_{card.get('_id')}"] = True
                                    st.warning("Click again to confirm")
                        
                        # Show full card details if requested
                        if st.session_state.get(f"show_card_{card.get('_id')}", False):
                            with st.expander("Card Details", expanded=True):
                                st.write("**Question:**")
                                st.write(card.get('question', 'No question'))
                                
                                if card.get('type') == 'MCQ':
                                    # MCQ Interactive Mode
                                    options = card.get('options', [])
                                    correct_answer_text = card.get('answer', '')
                                    correct_letter = "A"
                                    
                                    if 'Correct Answer:' in correct_answer_text:
                                        correct_letter = correct_answer_text.split('Correct Answer: ')[1].strip()
                                    
                                    user_choice_key = f"user_mcq_choice_{card.get('_id')}"
                                    user_choice = st.session_state.get(user_choice_key)
                                    
                                    if user_choice is None:
                                        # Show options as buttons for selection
                                        st.write("**Choose your answer:**")
                                        
                                        for idx, option in enumerate(options):
                                            if option:  # Only show non-empty options
                                                letter = chr(65 + idx)  # A, B, C, D
                                                if st.button(f"{letter}. {option}", key=f"{user_choice_key}_{letter}", use_container_width=True):
                                                    st.session_state[user_choice_key] = letter
                                                    st.rerun()
                                    else:
                                        # Show result and all options
                                        st.write(f"**Your choice:** {user_choice}")
                                        
                                        if user_choice == correct_letter:
                                            st.success("✅ Correct!")
                                        else:
                                            st.error(f"❌ Incorrect! The correct answer is {correct_letter}")
                                        
                                        st.write("**All Options:**")
                                        for idx, option in enumerate(options):
                                            if option:  # Only show non-empty options
                                                letter = chr(65 + idx)
                                                if letter == correct_letter:
                                                    st.markdown(f"**✅ {letter}. {option}** (Correct Answer)")
                                                else:
                                                    st.write(f"{letter}. {option}")
                                        
                                        # Reset button
                                        if st.button("🔄 Try Again", key=f"reset_mcq_{card.get('_id')}"):
                                            st.session_state.pop(user_choice_key, None)
                                            st.rerun()
                                
                                else:
                                    # QNA Mode - Hide answer until revealed
                                    show_answer_key = f"show_answer_{card.get('_id')}"
                                    
                                    if not st.session_state.get(show_answer_key, False):
                                        # Show blurred answer
                                        st.markdown(
                                            f"""
                                            <div style="
                                                filter: blur(8px);
                                                background-color: #2c3e50;
                                                padding: 10px;
                                                border-radius: 5px;
                                                color: #888;
                                                user-select: none;
                                                margin: 10px 0;
                                            ">
                                                {card.get('answer', 'No answer')}
                                            </div>
                                            """,
                                            unsafe_allow_html=True
                                        )
                                        
                                        if st.button("👁️ Show Answer", key=f"reveal_{card.get('_id')}", type="primary"):
                                            st.session_state[show_answer_key] = True
                                            st.rerun()
                                    else:
                                        # Show revealed answer
                                        st.write("**Answer:**")
                                        st.success(card.get('answer', 'No answer'))
                                        
                                        if st.button("🙈 Hide Answer", key=f"hide_{card.get('_id')}"):
                                            st.session_state[show_answer_key] = False
                                            st.rerun()
                                
                                # Close button
                                if st.button("✖️ Close", key=f"close_{card.get('_id')}"):
                                    st.session_state[f"show_card_{card.get('_id')}"] = False
                                    # Clear any MCQ selections when closing
                                    user_choice_key = f"user_mcq_choice_{card.get('_id')}"
                                    st.session_state.pop(user_choice_key, None)
                                    show_answer_key = f"show_answer_{card.get('_id')}"
                                    st.session_state.pop(show_answer_key, None)
                                    st.rerun()
        
        # Edit flashcard form
        if st.session_state.get('show_edit_form', False):
            card = st.session_state.get('edit_flashcard')
            if card:
                st.markdown("---")
                st.subheader("Edit Flashcard")
                
                with st.form("edit_flashcard_form"):
                    # Card type (read-only for editing)
                    current_type = card.get('type', 'QNA')
                    st.write(f"**Card Type:** {'Multiple Choice Question' if current_type == 'MCQ' else 'Question & Answer'}")
                    
                    new_question = st.text_area("Question", value=card.get('question', ''))
                    
                    if current_type == 'MCQ':
                        st.write("**Multiple Choice Options:**")
                        current_options = card.get('options', ['', '', '', ''])
                        # Ensure we have 4 options
                        while len(current_options) < 4:
                            current_options.append('')
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            option_a = st.text_input("Option A", value=current_options[0] if len(current_options) > 0 else "")
                            option_c = st.text_input("Option C", value=current_options[2] if len(current_options) > 2 else "")
                        
                        with col2:
                            option_b = st.text_input("Option B", value=current_options[1] if len(current_options) > 1 else "")
                            option_d = st.text_input("Option D", value=current_options[3] if len(current_options) > 3 else "")
                        
                        # Extract current correct answer
                        current_answer = card.get('answer', '')
                        current_correct = 'A'  # default
                        if 'Correct Answer:' in current_answer:
                            current_correct = current_answer.split('Correct Answer: ')[1].strip()
                        
                        correct_answer = st.selectbox(
                            "Correct Answer",
                            options=["A", "B", "C", "D"],
                            index=["A", "B", "C", "D"].index(current_correct) if current_correct in ["A", "B", "C", "D"] else 0
                        )
                    else:
                        new_answer = st.text_area("Answer", value=card.get('answer', ''))
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.form_submit_button("Update Flashcard", type="primary"):
                            if new_question:
                                if current_type == 'MCQ':
                                    options = [opt.strip() for opt in [option_a, option_b, option_c, option_d] if opt.strip()]
                                    if len(options) >= 2:
                                        mcq_answer = f"Correct Answer: {correct_answer}"
                                        update_flashcard(card.get('_id'), new_question, mcq_answer, current_type, options)
                                        st.session_state.show_edit_form = False
                                        st.rerun()
                                    else:
                                        st.error("Please enter at least 2 options")
                                else:
                                    if new_answer:
                                        update_flashcard(card.get('_id'), new_question, new_answer, current_type)
                                        st.session_state.show_edit_form = False
                                        st.rerun()
                                    else:
                                        st.error("Please enter an answer")
                            else:
                                st.error("Please enter a question")
                    
                    with col2:
                        if st.form_submit_button("Cancel"):
                            st.session_state.show_edit_form = False
                            st.rerun()
    
    else:
        st.info("This deck doesn't have any flashcards yet. Add your first flashcard above!")


# Main App Logic
def main():
    """Main application logic"""
    if not st.session_state.authenticated:
        render_auth_page()
    else:
        # Render sidebar for authenticated users
        render_sidebar()
        
        current_page = st.session_state.current_page
        
        if current_page == 'dashboard':
            render_dashboard()
        elif current_page == 'decks':
            render_decks_page()
        elif current_page == 'create_deck':
            render_create_deck_page()
        elif current_page == 'edit_deck':
            render_edit_deck_page()
        elif current_page == 'flashcards':
            render_flashcards_page()
        else:
            render_dashboard()

if __name__ == "__main__":
    main()
