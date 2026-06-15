import streamlit as st

st.title("Profile")

st.info(
    "Profile system implementation arrives in Stage 2B."
)
import streamlit as st

from services.profile_service import (
    get_profile,
    update_profile,
    get_user_statistics,
    get_user_stories,
    get_user_artworks,
    get_notifications,
    get_all_creators
)

# =====================================================
# ACCESS CONTROL
# =====================================================

if not st.session_state.get("logged_in", False):
    st.warning("Please login to access your profile.")
    st.stop()

# =====================================================
# USER DATA
# =====================================================

user_id = st.session_state.get("user_id")
username = st.session_state.get("username")

profile = get_profile(user_id)

if profile is None:
    st.error("Unable to load profile.")
    st.stop()

stats = get_user_statistics(user_id)

# =====================================================
# PAGE HEADER
# =====================================================

st.markdown("""
<div style="
padding:20px;
border:2px solid #D4AF37;
border-radius:15px;
background:#111111;
margin-bottom:20px;
">
<h1 style="
color:#D4AF37;
margin-bottom:5px;
">
👤 Creator Profile
</h1>

<p>
Manage your creator identity within the Empire of Continuum.
</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# PROFILE SUMMARY
# =====================================================

left, right = st.columns([1, 3])

with left:

    st.markdown("""
    <div style="
    text-align:center;
    padding:20px;
    border:2px solid #8B0000;
    border-radius:15px;
    background:#111111;
    ">
    <h2>🛡️</h2>
    <p>Avatar System</p>
    <small>
    Uploads arrive in a future stage.
    </small>
    </div>
    """, unsafe_allow_html=True)

with right:

    st.markdown(f"""
    <div style="
    padding:20px;
    border-left:5px solid #D4AF37;
    background:#111111;
    ">
    <h2 style="color:#D4AF37;">
    {profile.get("display_name", username)}
    </h2>

    <h4 style="color:#8B0000;">
    {profile.get("tagline", "Creator")}
    </h4>

    <p>
    {profile.get("bio", "No biography yet.")}
    </p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# STATISTICS
# =====================================================

st.subheader("📊 Creator Statistics")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Stories",
        stats["stories"]
    )

with c2:
    st.metric(
        "Artwork",
        stats["artworks"]
    )

with c3:
    st.metric(
        "Bookmarks",
        stats["bookmarks"]
    )

with c4:
    st.metric(
        "Followers",
        stats["followers"]
    )

st.divider()

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Profile Settings",
    "Stories",
    "Artwork",
    "Notifications",
    "Creator Directory"
])

# =====================================================
# PROFILE SETTINGS
# =====================================================

with tab1:

    st.subheader("Edit Profile")

    display_name = st.text_input(
        "Display Name",
        value=profile.get("display_name", "")
    )

    tagline = st.text_input(
        "Creator Tagline",
        value=profile.get("tagline", "")
    )

    location = st.text_input(
        "Location",
        value=profile.get("location", "")
    )

    website = st.text_input(
        "Website",
        value=profile.get("website", "")
    )

    portfolio = st.text_input(
        "Portfolio Link",
        value=profile.get("portfolio", "")
    )

    bio = st.text_area(
        "Biography",
        value=profile.get("bio", ""),
        height=200
    )

    if st.button("💾 Save Profile"):

        update_profile(
            user_id,
            display_name,
            tagline,
            location,
            website,
            portfolio,
            bio
        )

        st.success(
            "Profile updated successfully."
        )

        st.rerun()

# =====================================================
# STORIES
# =====================================================

with tab2:

    st.subheader("📖 My Stories")

    stories = get_user_stories(user_id)

    if stories:

        for story in stories:

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
            Category: {story["category"]}
            </p>

            <p>
            Status: {story["status"]}
            </p>

            <small>
            Created:
            {story["created_at"]}
            </small>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info(
            "You have not published any stories yet."
        )

# =====================================================
# ARTWORK
# =====================================================

with tab3:

    st.subheader("🎨 My Artwork")

    artworks = get_user_artworks(user_id)

    if artworks:

        for artwork in artworks:

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

            <p>
            Status:
            {artwork["status"]}
            </p>

            <small>
            Uploaded:
            {artwork["created_at"]}
            </small>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info(
            "No artwork uploaded yet."
        )

# =====================================================
# NOTIFICATIONS
# =====================================================

with tab4:

    st.subheader("🔔 Notifications")

    notifications = get_notifications(user_id)

    if notifications:

        for notification in notifications:

            status = (
                "🟢 Read"
                if notification["read_status"]
                else "🔴 Unread"
            )

            st.markdown(f"""
            <div style="
            border-left:4px solid #D4AF37;
            background:#111111;
            padding:15px;
            margin-bottom:10px;
            ">
            <h4>
            {notification["title"]}
            </h4>

            <p>
            {notification["message"]}
            </p>

            <small>
            {status}
            </small>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info(
            "No notifications."
        )

# =====================================================
# CREATOR DIRECTORY
# =====================================================

with tab5:

    st.subheader("👥 Creator Directory")

    creators = get_all_creators()

    if creators:

        for creator in creators:

            st.markdown(f"""
            <div style="
            border:1px solid #333333;
            padding:15px;
            border-radius:10px;
            background:#111111;
            margin-bottom:10px;
            ">
            <h4 style="color:#D4AF37;">
            {creator["username"]}
            </h4>

            <p>
            Role:
            {creator["role"]}
            </p>

            <small>
            Joined:
            {creator["created_at"]}
            </small>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info(
            "No creators found."
        )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Empire of Continuum • Creator Profile System v1.0"
)