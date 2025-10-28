import streamlit as st
from utils.theme import theme_css

st.session_state.setdefault("theme_mode", "auto")
st.markdown(theme_css(st.session_state["theme_mode"]), unsafe_allow_html=True)

# Initialize session state
if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "I am from Thales", "I am a Professor", "I am a Student"]
PASSWORDS = {
    "I am from Thales": "thales",
    "I am a Professor": "professor",
    "I am a Student": "student"
}

def login():
    st.title("Robberies in Mexico City Around Metro Stations")
    st.logo("images/logo.png", icon_image="images/logo.png")
    st.header("Log in")
    role = st.selectbox("Who are you?", ROLES)

    if role:
        password = st.text_input("Enter password", type="password")
        if st.button("Log in"):
            if password == PASSWORDS.get(role):
                st.session_state.role = role
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")

def logout():
    st.header("Log out")
    if st.button("Log out"):
        st.session_state.role = None
        st.success("Logged out successfully.")
        st.rerun()

# If not logged in, show login screen directly
if st.session_state.role is None:
    login()
else:
    # Define pages based on role
    role = st.session_state.role

    logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
    settings = st.Page("settings.py", title="Settings", icon=":material/settings:")

    visualization = st.Page(
        "Visualization/visualization.py",
        title="Dashboard",
        icon=":material/help:",
        default=(role == "Requester"),
    )
    maps = st.Page(
        "Visualization/maps.py",
        title="Maps",
        icon=":material/help:",
        default=(role == "Requester"),
    )
    maps2 = st.Page(
        "Visualization/maps2.py",
        title="Other maps",
        icon=":material/help:",
        default=(role == "Requester"),
    )
    ml = st.Page(
        "ml/ml_analysis.py",
        title="Machine Learning",
        icon=":material/healing:",
        default=(role == "I am a Professor"),
    )
    eda = st.Page(
        "EDA/eda.py",
        title="Exploratory Data Analysis",
        icon=":material/person_add:",
        default=(role == "I am from Thales"),
    )
    chat = st.Page(
        "ollama/chatview.py",
        title="Chat with Ollama",
        icon=":material/chat:"
        default=(role == "I am a Student"),
    )

    account_pages = [logout_page, settings]
    visualization_pages = [visualization, maps, maps2]
    ml_pages = [ml]
    eda_pages = [eda]
    chat_pages = [chat]

    page_dict = {
    "EDA": eda_pages,
    "Chat with Ollama": chat_pages,
    "Visualization": visualization_pages,
    "Machine Learning": ml_pages
    }

    st.title("Robberies in Mexico City Around Metro Stations")
    st.logo("images/logo.png", icon_image="images/logo.png")

    pg = st.navigation({"Account": account_pages} | page_dict)
    pg.run()