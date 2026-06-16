import streamlit as st

from services.story_service import (
    get_approved_stories,
    get_story,
    search_stories,
    get_stories_by_category,
    get_story_categories,
    increment_story_view,
    bookmark_story,
    like_story,
    get_most_liked_stories,
    get_most_viewed_stories
)

# =====================================================
# ACCESS CONTROL
# =====================================================

if not st.session_state.get("logged_in", False):
    st.warning(
        "Please login to access the Story Library."
    )
    st.stop()

# =====================================================
# SESSION STATE
# =====================================================

if "selected_story_id" not in st.session_state:
    st.session_state.selected_story_id = None

# =====================================================
# HEADER
# =====================================================

st.title("📚 Empire Story Library")

st.markdown("""
<div class='highlight-mystical'>
Explore stories, lore, character profiles, worldbuilding documents and comics created by the Empire of Continuum community.
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

# =====================================================
# FEATURED SECTION
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🔥 Most Liked")

    top_liked = get_most_liked_stories(5)

    if top_liked:

        for story in top_liked:

            st.markdown(f"""
            <div class='epic-card'>
            <h4 style='color: var(--gold-light); margin-bottom: 8px;'>{story['title']}</h4>
            <div style='color: var(--purple-light); font-size: 0.9rem; margin-bottom: 8px;'>By {story['author_name']}</div>
            <div style='display: flex; gap: 15px; font-size: 0.85rem; color: var(--gold-primary);'>
            <span>❤️ {story['likes']}</span>
            <span>👁️ {story['views']}</span>
            </div>
            </div>
            """)

    else:
        st.info("No stories yet.")

with col2:

    st.subheader("👁️ Most Viewed")

    top_viewed = get_most_viewed_stories(5)

    if top_viewed:

        for story in top_viewed:

            st.markdown(f"""
            <div class='epic-card'>
            <h4 style='color: var(--gold-light); margin-bottom: 8px;'>{story['title']}</h4>
            <div style='color: var(--purple-light); font-size: 0.9rem; margin-bottom: 8px;'>By {story['author_name']}</div>
            <div style='display: flex; gap: 15px; font-size: 0.85rem; color: var(--gold-primary);'>
            <span>❤️ {story['likes']}</span>
            <span>👁️ {story['views']}</span>
            </div>
            </div>
            """)

    else:
        st.info("No stories yet.")

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

# =====================================================
# SEARCH SECTION
# =====================================================

st.subheader("🔎 Search Library")

search_col, filter_col = st.columns([3, 1])

with search_col:

    search_term = st.text_input(
        "Search by title or content",
        placeholder="Search stories..."
    )

with filter_col:

    category_filter = st.selectbox(
        "Category",
        ["All"] + get_story_categories()
    )

# =====================================================
# STORY LIST
# =====================================================

st.subheader("📖 Available Stories")

results = []

if search_term:

    results = search_stories(
        search_term,
        category_filter
    )

elif category_filter != "All":

    results = get_stories_by_category(
        category_filter
    )

else:

    results = get_approved_stories()

if not results:

    st.info(
        "No stories found."
    )

# =====================================================
# STORY GRID
# =====================================================

for story in results:

    with st.container():

        st.markdown(f"""
        <div class='publication-card'>
        <h4 style='color: var(--gold-light); margin-bottom: 8px;'>{story['title']}</h4>
        <div style='color: var(--purple-light); font-size: 0.9rem; margin-bottom: 10px;'>By {story['author_name']}</div>
        <div style='display: flex; gap: 15px; font-size: 0.85rem; color: #B8B8B8;'>
        <span>📚 {story['category']}</span>
        <span>❤️ {story['likes']}</span>
        <span>👁️ {story['views']}</span>
        </div>
        </div>
        """)

        if st.button(
            f"Read Story #{story['id']}",
            key=f"read_{story['id']}"
        ):
            st.session_state.selected_story_id = (
                story["id"]
            )
            st.rerun()

# =====================================================
# STORY READER
# =====================================================

if st.session_state.selected_story_id:

    story = get_story(
        st.session_state.selected_story_id
    )

    if story:

        increment_story_view(
            story["id"]
        )

        st.divider()

        st.header(
            story["title"]
        )

        st.caption(
            f"By {story['author_name']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Category",
                story["category"]
            )

        with col2:

            st.metric(
                "Likes",
                story["likes"]
            )

        with col3:

            st.metric(
                "Views",
                story["views"]
            )

        st.divider()

        st.markdown(
            story["content"]
        )

        st.divider()

        # ============================================
        # INTERACTIONS
        # ============================================

        action1, action2, action3 = st.columns(3)

        with action1:

            if st.button(
                "❤️ Like",
                key=f"like_{story['id']}"
            ):

                result = like_story(
                    st.session_state.user_id,
                    story["id"]
                )

                if result:
                    st.success(
                        "Story liked."
                    )
                else:
                    st.warning(
                        "Already liked."
                    )

                st.rerun()

        with action2:

            if st.button(
                "🔖 Bookmark",
                key=f"bookmark_{story['id']}"
            ):

                result = bookmark_story(
                    st.session_state.user_id,
                    story["id"]
                )

                if result:
                    st.success(
                        "Bookmarked."
                    )
                else:
                    st.warning(
                        "Already bookmarked."
                    )

        with action3:

            if st.button(
                "⬅ Back to Library"
            ):

                st.session_state.selected_story_id = None
                st.rerun()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("📚 Story Library")

    st.write(
        "Browse approved stories from across the Empire."
    )

    st.divider()

    st.write(
        f"Logged in as: **{st.session_state.username}**"
    )

    st.write(
        f"Role: **{st.session_state.role}**"
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Empire of Continuum • Story Library v1.0"
)
from services.story_service import (
    get_story_statistics,
    get_story,
    get_approved_stories,
    
)
