import streamlit as st
import json
import os

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
# LOAD SAMPLE DATA
# =====================================================

def load_profiles_data():
    data_path = os.path.join(
        os.path.dirname(__file__),
        "../data/user_profiles.json"
    )
    if os.path.exists(data_path):
        with open(data_path, 'r') as f:
            return json.load(f)
    return []

profiles_data = load_profiles_data()

# =====================================================
# USER DATA
# =====================================================

user_id = st.session_state.get("user_id")
username = st.session_state.get("username")

profile = get_profile(user_id)

if profile is None:
    profile = {}

stats = get_user_statistics(user_id)

# Use sample profile if available
sample_profile = next((p for p in profiles_data if p['username'] == username), None)
if sample_profile:
    profile = {**profile, **sample_profile}

# =====================================================
# PAGE HEADER
# =====================================================

st.markdown(
    """
    <h1 class='main-title'>
    👤 CREATOR PROFILE
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<div class='highlight-mystical'>
Manage your creator identity within the Empire of Continuum.
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

# =====================================================
# PROFILE SUMMARY
# =====================================================

left, right = st.columns([1, 3])

with left:
    st.markdown(f"""
    <div style='
    text-align:center;
    padding:20px;
    border:2px solid var(--purple-accent);
    border-radius:15px;
    background:rgba(26,26,46,0.8);
    '>
    <h1 style='font-size: 3rem;'>{profile.get("avatar", "🛡️")}</h1>
    <p style='color: var(--gold-primary);'>Avatar</p>
    <small style='color: #A8A8A8;'>
    Upload arrives in future update.
    </small>
    </div>
    """, unsafe_allow_html=True)

with right:
    display_name = profile.get("display_name", username)
    tagline = profile.get("tagline", "Creator of the Empire")
    bio = profile.get("bio", "No biography yet.")
    
    badge_html = ""
    if profile.get("verified"):
        badge_html = "✓ <span style='color: var(--mystic-blue-light);'>Verified</span>"
    
    st.markdown(f"""
    <div class='creator-panel' style='padding: 20px; border-left: 6px solid var(--purple-accent);'>
    <h2 style="color: var(--gold-light); margin-bottom: 5px;">
    {display_name} {badge_html}
    </h2>
    <h4 style="color: var(--purple-light); margin-bottom: 10px;">
    {tagline}
    </h4>
    <p style='color: #D8D8D8; line-height: 1.6;'>
    {bio}
    </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

# =====================================================
# STATISTICS
# =====================================================

st.subheader("📊 Creator Statistics")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("📖 Stories", profile.get("stories", 0))

with stat_col2:
    st.metric("🎨 Artwork", profile.get("artworks", 0))

with stat_col3:
    st.metric("🔖 Bookmarks", profile.get("bookmarks", 0))

with stat_col4:
    st.metric("👥 Followers", profile.get("followers", 0))

st.divider()

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 Profile Settings",
    "📖 Stories",
    "🎨 Artwork",
    "🔔 Notifications",
    "👥 Creator Directory"
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

    if st.button("💾 Save Profile", use_container_width=True):
        try:
            update_profile(
                user_id,
                display_name,
                tagline,
                location,
                website,
                portfolio,
                bio
            )
            st.success("✅ Profile updated successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Error updating profile: {str(e)}")

# =====================================================
# STORIES
# =====================================================

with tab2:

    st.subheader("📖 My Stories")

    try:
        stories = get_user_stories(user_id)
    except:
        stories = []

    if stories:
        for story in stories:
            st.markdown(f"""
            <div class='publication-card'>
            <h4 style="color: var(--gold-light);">
            {story["title"]}
            </h4>
            <div style='display: flex; gap: 15px; margin: 10px 0; font-size: 0.9rem;'>
            <span style='color: var(--purple-light);'>📚 {story["category"]}</span>
            <span style='color: var(--gold-primary);'>✓ {story["status"]}</span>
            </div>
            <small style='color: #A8A8A8;'>
            Created: {story["created_at"]}
            </small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 You have not published any stories yet. Start creating!")

# =====================================================
# ARTWORK
# =====================================================

with tab3:

    st.subheader("🎨 My Artwork")

    try:
        artworks = get_user_artworks(user_id)
    except:
        artworks = []

    if artworks:
        for artwork in artworks:
            st.markdown(f"""
            <div class='publication-card'>
            <h4 style="color: var(--gold-light);">
            {artwork["title"]}
            </h4>
            <div style='display: flex; gap: 15px; margin: 10px 0; font-size: 0.9rem;'>
            <span style='color: var(--gold-primary);'>✓ {artwork["status"]}</span>
            </div>
            <small style='color: #A8A8A8;'>
            Uploaded: {artwork["created_at"]}
            </small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🖼️ No artwork uploaded yet. Share your creations!")

# =====================================================
# NOTIFICATIONS
# =====================================================

with tab4:

    st.subheader("🔔 Notifications")

    try:
        notifications = get_notifications(user_id)
    except:
        notifications = []

    if notifications:
        for notification in notifications:
            status = (
                "✓ Read"
                if notification["read_status"]
                else "● Unread"
            )

            st.markdown(f"""
            <div class='highlight-mystical'>
            <h4 style='color: var(--gold-light); margin-bottom: 8px;'>
            {notification["title"]}
            </h4>
            <p style='color: #D8D8D8; margin-bottom: 10px;'>
            {notification["message"]}
            </p>
            <small style='color: var(--purple-light);'>
            {status}
            </small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🔔 No notifications.")

# =====================================================
# CREATOR DIRECTORY
# =====================================================

with tab5:

    st.subheader("👥 Creator Directory")

    try:
        creators = get_all_creators()
    except:
        creators = profiles_data

    if creators:
        search_term = st.text_input("Search creators...", placeholder="Filter by username or role")
        
        filtered_creators = creators
        if search_term:
            filtered_creators = [
                c for c in creators 
                if search_term.lower() in c.get('username', '').lower() or
                   search_term.lower() in c.get('role', '').lower()
            ]

        if filtered_creators:
            for creator in filtered_creators[:20]:
                badges_html = ""
                if creator.get("verified"):
                    badges_html = "✓ <span style='color: var(--mystic-blue-light);'>Verified</span>"
                
                badges_list = creator.get("badges", [])
                if badges_list:
                    badges_display = " • ".join([f"<span style='color: var(--gold-primary);'>{b}</span>" for b in badges_list])
                    badges_html += f" • {badges_display}"

                st.markdown(f"""
                <div class='epic-card'>
                <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;'>
                <div>
                <h4 style="color: var(--gold-light); margin-bottom: 5px;">
                {creator.get('avatar', '👤')} {creator["username"]} {badges_html}
                </h4>
                <div style='color: var(--purple-light); font-size: 0.9rem;'>
                {creator.get('display_name', creator['username'])}
                </div>
                </div>
                <div style='text-align: right;'>
                <div style='color: var(--gold-primary); font-weight: bold;'>{creator.get('followers', 0)}</div>
                <small style='color: #A8A8A8;'>Followers</small>
                </div>
                </div>
                <div style='display: flex; gap: 20px; font-size: 0.85rem; color: #B8B8B8;'>
                <span>📖 {creator.get('stories', 0)} stories</span>
                <span>🎨 {creator.get('artworks', 0)} works</span>
                <span>👥 {creator.get('following', 0)} following</span>
                </div>
                <small style='color: #888888; margin-top: 10px; display: block;'>
                Joined: {creator.get('joined', 'N/A')}
                </small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No creators found matching your search.")
    else:
        st.info("👥 Creator directory loading...")

# =====================================================
# FOOTER
# =====================================================

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

st.caption("⚔️ Empire of Continuum • Creator Profile System v2.0")
