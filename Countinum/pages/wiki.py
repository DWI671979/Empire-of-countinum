import streamlit as st

from services.wiki_service import (
    create_article,
    get_article,
    get_articles,
    get_articles_by_type,
    search_articles,
    get_article_types,
    increment_article_view,
    get_wiki_statistics,
    get_timeline_events,
    get_popular_articles
)

# =====================================================
# ACCESS CONTROL
# =====================================================

if not st.session_state.get("logged_in", False):
    st.warning(
        "Please login to access the Continuity Wiki."
    )
    st.stop()

# =====================================================
# SESSION STATE
# =====================================================

if "selected_wiki_article" not in st.session_state:
    st.session_state.selected_wiki_article = None

# =====================================================
# HEADER
# =====================================================

st.title("📖 Empire of Continuum Wiki")

st.markdown("""
The official encyclopedia of the Empire of Continuum.

Browse characters, factions, locations, historical
events, technologies, species, organizations, and
continuity documents that define the shared universe.
""")

st.divider()

# =====================================================
# STATISTICS
# =====================================================

stats = get_wiki_statistics()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Articles",
        stats["total_articles"]
    )

with c2:
    st.metric(
        "Canon",
        stats["canon_articles"]
    )

with c3:
    st.metric(
        "Non-Canon",
        stats["noncanon_articles"]
    )

with c4:
    st.metric(
        "Views",
        stats["total_views"]
    )

st.divider()

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Wiki Browser",
    "Create Article",
    "Timeline",
    "Popular Articles"
])

# =====================================================
# TAB 1 - BROWSER
# =====================================================

with tab1:

    st.subheader(
        "🔎 Search Encyclopedia"
    )

    search_term = st.text_input(
        "Search"
    )

    article_type = st.selectbox(
        "Filter by Type",
        ["All"] + get_article_types()
    )

    if search_term:

        articles = search_articles(
            search_term
        )

    elif article_type != "All":

        articles = get_articles_by_type(
            article_type
        )

    else:

        articles = get_articles()

    st.divider()

    if not articles:

        st.info(
            "No articles found."
        )

    for article in articles:

        canon_badge = (
            "🟢 Canon"
            if article["canon_status"] == "canon"
            else "🟡 Non-Canon"
        )

        st.markdown(f"""
### {article['title']}

Type: **{article['article_type']}**

Status: **{canon_badge}**
""")

        if st.button(
            f"View Article #{article['id']}",
            key=f"wiki_{article['id']}"
        ):

            st.session_state.selected_wiki_article = (
                article["id"]
            )

            st.rerun()

        st.divider()

# =====================================================
# ARTICLE VIEWER
# =====================================================

if st.session_state.selected_wiki_article:

    article = get_article(
        st.session_state.selected_wiki_article
    )

    if article:

        increment_article_view(
            article["id"]
        )

        st.divider()

        st.header(
            article["title"]
        )

        st.caption(
            f"Author: {article['author_name']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Type",
                article["article_type"]
            )

        with col2:

            st.metric(
                "Status",
                article["canon_status"]
            )

        st.divider()

        st.markdown(
            article["content"]
        )

        st.divider()

        if st.button(
            "⬅ Return to Wiki"
        ):

            st.session_state.selected_wiki_article = None
            st.rerun()

# =====================================================
# TAB 2 - CREATE ARTICLE
# =====================================================

with tab2:

    st.subheader(
        "✍ Create New Wiki Article"
    )

    title = st.text_input(
        "Article Title"
    )

    article_type = st.selectbox(
        "Article Type",
        get_article_types()
    )

    canon_status = st.selectbox(
        "Canon Status",
        [
            "non-canon",
            "canon"
        ]
    )

    content = st.text_area(
        "Article Content",
        height=450
    )

    if st.button(
        "Submit Article"
    ):

        if not title.strip():

            st.error(
                "Title required."
            )

        elif not content.strip():

            st.error(
                "Content required."
            )

        else:

            article_id = create_article(
                title=title,
                article_type=article_type,
                content=content,
                author_id=st.session_state.user_id,
                canon_status=canon_status
            )

            st.success(
                f"""
Article submitted successfully.

Article ID:
{article_id}
"""
            )

            st.balloons()

# =====================================================
# TAB 3 - TIMELINE
# =====================================================

with tab3:

    st.subheader(
        "⏳ Continuity Timeline"
    )

    timeline_events = get_timeline_events()

    if not timeline_events:

        st.info(
            "No timeline events available."
        )

    for event in timeline_events:

        status = (
            "🟢 Canon"
            if event["canon_status"] == "canon"
            else "🟡 Non-Canon"
        )

        st.markdown(f"""
### {event['event_title']}

**Date:** {event['event_date']}

**Era:** {event['era']}

**Status:** {status}
""")

        st.write(
            event["description"]
        )

        st.divider()

# =====================================================
# TAB 4 - POPULAR ARTICLES
# =====================================================

with tab4:

    st.subheader(
        "🔥 Most Viewed Articles"
    )

    popular_articles = get_popular_articles()

    if not popular_articles:

        st.info(
            "No articles available."
        )

    for article in popular_articles:

        st.markdown(f"""
### {article['title']}

Type:
{article['article_type']}

Status:
{article['canon_status']}

Views:
{article['views']}
""")

        st.divider()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header(
        "📚 Encyclopedia"
    )

    st.write(
        f"Logged in as "
        f"**{st.session_state.username}**"
    )

    st.divider()

    st.markdown("""
### Article Types

- Characters
- Locations
- Factions
- Organizations
- Species
- Technology
- Historical Events
- Lore Articles
- Timeline Entries
- Continuity Documents

### Canon Guide

🟢 Canon

Official continuity

🟡 Non-Canon

Community submissions
""")

# =====================================================
# QUICK NAVIGATION
# =====================================================

with st.sidebar:

    st.subheader(
        "Quick Browse"
    )

    for item in get_article_types():

        st.write(
            f"• {item}"
        )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Empire of Continuum • Continuity Wiki v1.0"
)