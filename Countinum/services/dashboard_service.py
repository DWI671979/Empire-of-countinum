import json
from pathlib import Path

from database.database import get_connection


FEATURED_PATH = Path("data/featured.json")
ANNOUNCEMENTS_PATH = Path("data/announcements.json")


def get_platform_stats():

    conn = get_connection()

    users = conn.execute(
        "SELECT COUNT(*) AS count FROM users"
    ).fetchone()["count"]

    stories = conn.execute(
        "SELECT COUNT(*) AS count FROM stories"
    ).fetchone()["count"]

    artworks = conn.execute(
        "SELECT COUNT(*) AS count FROM artworks"
    ).fetchone()["count"]

    conn.close()

    return {
        "users": users,
        "stories": stories,
        "artworks": artworks
    }


def get_featured_content():

    if not FEATURED_PATH.exists():
        return {}

    with open(FEATURED_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def get_announcements():

    if not ANNOUNCEMENTS_PATH.exists():
        return []

    with open(
        ANNOUNCEMENTS_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def get_recent_stories(limit=5):

    conn = get_connection()

    rows = conn.execute("""
    SELECT title,
           category,
           created_at
    FROM stories
    ORDER BY id DESC
    LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    return rows


def get_recent_artworks(limit=5):

    conn = get_connection()

    rows = conn.execute("""
    SELECT title,
           created_at
    FROM artworks
    ORDER BY id DESC
    LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    return rows
import streamlit as st
from services.dashboard_service import (
    get_platform_stats,
    get_featured_content,
    get_announcements,
    get_recent_stories,
    get_recent_artworks
)

st.set_page_config(
    page_title="Empire Dashboard",
    page_icon="⚔️",
    layout="wide"
)

# ----------------------------------------
# ACCESS CONTROL
# ----------------------------------------

if not st.session_state.get("logged_in", False):
    st.warning("Please login to access the Empire Dashboard.")
    st.stop()

# ----------------------------------------
# LOAD DATA
# ----------------------------------------

stats = get_platform_stats()
featured = get_featured_content()
announcements = get_announcements()
recent_stories = get_recent_stories()
recent_artworks = get_recent_artworks()

# ----------------------------------------
# HERO SECTION
# ----------------------------------------

st.markdown("""
<div style="
padding:40px;
border:2px solid #D4AF37;
border-radius:15px;
background:linear-gradient(135deg,#111111,#1a1a1a);
margin-bottom:25px;
text-align:center;
">
<h1 style="
color:#D4AF37;
font-size:3rem;
margin-bottom:10px;
">
⚔️ EMPIRE OF CONTINUUM ⚔️
</h1>

<h3 style="
color:#8B0000;
margin-bottom:20px;
">
Forge Worlds • Create Legends • Shape Continuity
</h3>

<p style="
color:#f5f5f5;
font-size:1.1rem;
">
A collaborative universe where writers, artists and worldbuilders
create living continuities together.
</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------
# USER WELCOME
# ----------------------------------------

username = st.session_state.get("username", "Creator")

st.markdown(f"""
<div style="
padding:20px;
border-left:5px solid #8B0000;
background:#111111;
margin-bottom:20px;
">
<h3 style="color:#D4AF37;">
Welcome back, {username}
</h3>

<p>
Continue building the Empire and help shape the future of the Continuum.
</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------------------
# PLATFORM STATS
# ----------------------------------------

st.subheader("📊 Empire Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Registered Creators",
        stats["users"]
    )

with col2:
    st.metric(
        "Stories Published",
        stats["stories"]
    )

with col3:
    st.metric(
        "Artwork Uploaded",
        stats["artworks"]
    )

st.divider()

# ----------------------------------------
# FEATURED SECTION
# ----------------------------------------

st.subheader("⭐ Featured Content")

featured_story = featured.get("featured_story", {})
featured_artwork = featured.get("featured_artwork", {})
featured_creator = featured.get("featured_creator", {})
canon_event = featured.get("latest_canon_event", {})

col1, col2 = st.columns(2)

with col1:

    st.markdown(f"""
    <div style="
    border:2px solid #D4AF37;
    padding:20px;
    border-radius:10px;
    background:#111111;
    min-height:250px;
    ">
    <h3 style="color:#D4AF37;">
    📖 Featured Story
    </h3>

    <h4>
    {featured_story.get("title","No Story")}
    </h4>

    <p>
    <b>Author:</b>
    {featured_story.get("author","Unknown")}
    </p>

    <p>
    {featured_story.get("description","")}
    </p>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div style="
    border:2px solid #8B0000;
    padding:20px;
    border-radius:10px;
    background:#111111;
    min-height:250px;
    ">
    <h3 style="color:#D4AF37;">
    🎨 Featured Artwork
    </h3>

    <h4>
    {featured_artwork.get("title","No Artwork")}
    </h4>

    <p>
    <b>Artist:</b>
    {featured_artwork.get("artist","Unknown")}
    </p>

    <p>
    {featured_artwork.get("description","")}
    </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

col3, col4 = st.columns(2)

with col3:

    st.markdown(f"""
    <div style="
    border:2px solid #D4AF37;
    padding:20px;
    border-radius:10px;
    background:#111111;
    min-height:220px;
    ">
    <h3 style="color:#D4AF37;">
    👑 Creator Spotlight
    </h3>

    <h4>
    {featured_creator.get("name","Unknown")}
    </h4>

    <p>
    <b>Role:</b>
    {featured_creator.get("role","Creator")}
    </p>

    <p>
    {featured_creator.get("bio","")}
    </p>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown(f"""
    <div style="
    border:2px solid #8B0000;
    padding:20px;
    border-radius:10px;
    background:#111111;
    min-height:220px;
    ">
    <h3 style="color:#D4AF37;">
    🕰 Latest Canon Event
    </h3>

    <h4>
    {canon_event.get("title","No Event")}
    </h4>

    <p>
    {canon_event.get("description","")}
    </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ----------------------------------------
# ANNOUNCEMENTS
# ----------------------------------------

st.subheader("📢 Empire Announcements")

if announcements:

    for announcement in announcements:

        st.markdown(f"""
        <div style="
        padding:15px;
        border-left:4px solid #D4AF37;
        background:#111111;
        margin-bottom:15px;
        ">
        <h4 style="color:#D4AF37;">
        {announcement.get("title","Announcement")}
        </h4>

        <p>
        {announcement.get("content","")}
        </p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("No announcements available.")

st.divider()

# ----------------------------------------
# RECENT CONTENT
# ----------------------------------------

left, right = st.columns(2)

# ----------------------------------------
# STORIES
# ----------------------------------------

with left:

    st.subheader("📚 Recent Stories")

    if recent_stories:

        for story in recent_stories:

            st.markdown(f"""
            <div style="
            border:1px solid #333333;
            padding:15px;
            border-radius:10px;
            background:#111111;
            margin-bottom:10px;
            ">
            <h4 style="color:#D4AF37;">
            {story["title"]}
            </h4>

            <p>
            Category:
            {story["category"]}
            </p>

            <small>
            Published:
            {story["created_at"]}
            </small>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("No stories have been published yet.")

# ----------------------------------------
# ARTWORK
# ----------------------------------------

with right:

    st.subheader("🎨 Recent Artwork")

    if recent_artworks:

        for artwork in recent_artworks:

            st.markdown(f"""
            <div style="
            border:1px solid #333333;
            padding:15px;
            border-radius:10px;
            background:#111111;
            margin-bottom:10px;
            ">
            <h4 style="color:#D4AF37;">
            {artwork["title"]}
            </h4>

            <small>
            Uploaded:
            {artwork["created_at"]}
            </small>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("No artwork has been uploaded yet.")

st.divider()

# ----------------------------------------
# QUICK ACTIONS
# ----------------------------------------

st.subheader("⚡ Quick Actions")

action1, action2, action3, action4 = st.columns(4)

with action1:
    st.button(
        "📖 Publish Story",
        use_container_width=True,
        disabled=True
    )

with action2:
    st.button(
        "🎨 Upload Artwork",
        use_container_width=True,
        disabled=True
    )

with action3:
    st.button(
        "📚 Open Wiki",
        use_container_width=True,
        disabled=True
    )

with action4:
    st.button(
        "🤝 Collaboration Hub",
        use_container_width=True,
        disabled=True
    )

st.caption(
    "These features will become active as future stages are implemented."
)