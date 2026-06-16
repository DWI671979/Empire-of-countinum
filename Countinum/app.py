import streamlit as st

import database.schema
import auth.register
from auth.login import authenticate_user

# ✅ FIX 1: Initialize the database and create all tables on startup
database.schema.create_tables()

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

        st.markdown("""
        <div class='highlight-mystical'>
        Welcome back, creator. Enter the Empire.
        </div>
        """, unsafe_allow_html=True)

        email = st.text_input(
            "Email",
            key="login_email",
            placeholder="your@email.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
            placeholder="Enter your password"
        )

        if st.button("⚔️ Enter Empire", use_container_width=True):

            user = authenticate_user(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_id = user["id"]
                st.session_state.username = user["username"]
                st.session_state.role = user["role"]

                st.success("✅ Welcome back, creator.")
                st.rerun()

            else:
                st.error("❌ Invalid credentials")

    with register_tab:

        st.markdown("""
        <div class='highlight-mystical'>
        Forge your identity in the Empire.
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input(
            "Creator Name",
            placeholder="Choose your creator name"
        )

        email = st.text_input(
            "Email",
            placeholder="your@email.com"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="At least 8 characters"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm your password"
        )

        if st.button("⚔️ Create Account", use_container_width=True):

            if password != confirm:
                st.error(
                    "❌ Passwords do not match."
                )

            elif len(password) < 8:
                st.error(
                    "❌ Password must contain at least 8 characters."
                )

            else:

                success, message = auth.register.register_user(
                    username,
                    email,
                    password
                )

                if success:
                    st.success(f"✅ {message}")
                    st.balloons()

                else:
                    st.error(f"❌ {message}")

else:

    st.success(
        f"⚔️ Logged in as **{st.session_state.username}**"
    )

    st.markdown("""
    <div class='epic-card'>
    Use the left sidebar to navigate the Empire and create legendary content.
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout", use_container_width=True):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = ""
        st.session_state.role = ""

        st.rerun()
