import streamlit as st

from database.schema import initialize_database
from auth.register import register_user
from auth.login import authenticate_user

initialize_database()

st.set_page_config(
    page_title="Empire of Continuum",
    page_icon="⚔️",
    layout="wide"
)

with open("css/manga_theme.css") as css:
    st.markdown(
        f"<style>{css.read()}</style>",
        unsafe_allow_html=True
    )

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

st.markdown(
    """
    <h1 class='main-title'>
    EMPIRE OF CONTINUUM
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class='subtitle'>
    Forge Worlds • Create Legends • Shape Continuity
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

if not st.session_state.logged_in:

    login_tab, register_tab = st.tabs(
        ["Login", "Register"]
    )

    with login_tab:

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Enter Empire"):

            user = authenticate_user(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_id = user["id"]
                st.session_state.username = user["username"]
                st.session_state.role = user["role"]

                st.success("Welcome back.")
                st.rerun()

            else:
                st.error("Invalid credentials")

    with register_tab:

        username = st.text_input(
            "Username"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button("Create Account"):

            if password != confirm:
                st.error(
                    "Passwords do not match."
                )

            elif len(password) < 8:
                st.error(
                    "Password must contain at least 8 characters."
                )

            else:

                success, message = register_user(
                    username,
                    email,
                    password
                )

                if success:
                    st.success(message)

                else:
                    st.error(message)

else:

    st.success(
        f"Logged in as {st.session_state.username}"
    )

    st.info(
        "Use the left sidebar to navigate between pages."
    )

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()