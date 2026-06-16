import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_loader import load_wiki_articles
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
# LOAD SAMPLE DATA
# =====================================================

wiki_data = load_wiki_articles()

# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <h1 class='main-title'>
    📖 EMPIRE OF CONTINUUM WIKI
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<div class='highlight-mystical'>
The official encyclopedia of the Empire of Continuum.

Browse characters, factions, locations, historical events, technologies, species, organizations, and continuity documents that define the shared universe.
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

# =====================================================
# STATISTICS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"<div class='stMetric'><div style='color: var(--gold-primary); font-weight: bold;'>{len(wiki_data)}</div><div style='font-size: 0.9rem;'>Total Articles</div></div>", unsafe_allow_html=True)

with c2:
    canon_count = len([a for a in wiki_data if a.get('canon_status') == 'canon'])
    st.markdown(f"<div class='stMetric'><div style='color: #A8E6A1; font-weight: bold;'>{canon_count}</div><div style='font-size: 0.9rem;'>Canon Articles</div></div>", unsafe_allow_html=True)

with c3:
    noncanon_count = len([a for a in wiki_data if a.get('canon_status') == 'non-canon'])
    st.markdown(f"<div class='stMetric'><div style='color: #F5C89A; font-weight: bold;'>{noncanon_count}</div><div style='font-size: 0.9rem;'>Non-Canon</div></div>", unsafe_allow_html=True)

with c4:
    total_views = sum(a.get('views', 0) for a in wiki_data)
    st.markdown(f"<div class='stMetric'><div style='color: var(--purple-light); font-weight: bold;'>{total_views:,}</div><div style='font-size: 0.9rem;'>Total Views</div></div>", unsafe_allow_html=True)

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🔎 Wiki Browser",
    "✍️ Create Article",
    "⏳ Timeline",
    "🔥 Popular Articles"
])

# =====================================================
# TAB 1 - BROWSER
# =====================================================

with tab1:

    st.subheader("Search Encyclopedia")

    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input(
            "Search articles by title or content",
            placeholder="Type to search..."
        )

    with col2:
        article_type = st.selectbox(
            "Filter by Type",
            ["All Types"] + list(set(a.get('article_type', 'Unknown') for a in wiki_data))
        )

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    # Filter articles
    filtered_articles = wiki_data.copy()
    
    if search_term:
        filtered_articles = [
            a for a in filtered_articles 
            if search_term.lower() in a.get('title', '').lower() or 
               search_term.lower() in a.get('excerpt', '').lower()
        ]

    if article_type != "All Types":
        filtered_articles = [a for a in filtered_articles if a.get('article_type') == article_type]

    if not filtered_articles:
        st.info("📭 No articles found matching your search.")
    else:
        st.markdown(f"**Found {len(filtered_articles)} article(s)**")
        
        for article in filtered_articles:
            canon_badge = (
                "<span class='badge-canon'>🟢 Canon</span>"
                if article.get("canon_status") == "canon"
                else "<span class='badge-noncanon'>🟡 Non-Canon</span>"
            )

            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.markdown(f"<div style='text-align: center; font-size: 2rem;'>📄</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
<div class='epic-card'>
<h4 style='color: var(--gold-light); margin-bottom: 8px;'>{article['title']}</h4>
<div style='color: var(--purple-light); font-size: 0.9rem; margin-bottom: 8px;'>
{article['article_type']} • {canon_badge}
</div>
<p style='color: #E8E8E8; margin-bottom: 12px;'>{article['excerpt']}</p>
<div style='display: flex; gap: 15px; font-size: 0.85rem; color: var(--gold-primary);'>
<span>👁️ {article.get('views', 0):,} views</span>
<span>❤️ {article.get('likes', 0)} likes</span>
<span>✍️ {article['author']}</span>
</div>
</div>
                """, unsafe_allow_html=True)

            if st.button(
                f"Read Full Article",
                key=f"wiki_{article['id']}"
            ):
                st.session_state.selected_wiki_article = article["id"]
                st.rerun()

# =====================================================
# ARTICLE VIEWER
# =====================================================

if st.session_state.selected_wiki_article:
    article = next(
        (a for a in wiki_data if a["id"] == st.session_state.selected_wiki_article),
        None
    )

    if article:
        st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"<h2 style='color: var(--gold-light);'>{article['title']}</h2>", unsafe_allow_html=True)
            st.caption(f"✍️ By {article['author']}")

        with col2:
            canon_text = "Canon" if article.get("canon_status") == "canon" else "Community Submission"
            st.markdown(f"<div class='badge-canon' style='text-align: center;'>{canon_text}</div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div style='text-align: center; background: rgba(26,26,46,0.8); padding: 10px; border-radius: 8px;'><div style='font-size: 1.5rem; color: var(--gold-primary);'>{article.get('views', 0):,}</div><div style='font-size: 0.8rem;'>Views</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

        st.markdown(f"**Type:** {article['article_type']} | **Tags:** {', '.join(article.get('tags', []))}")
        
        st.markdown(f"""
<div class='highlight-mystical'>
{article['content']}
</div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("👁️ Views", f"{article.get('views', 0):,}")
        with c2:
            st.metric("❤️ Likes", f"{article.get('likes', 0)}")
        with c3:
            st.metric("📝 Type", article['article_type'])

        st.divider()

        if st.button("⬅️ Back to Wiki"):
            st.session_state.selected_wiki_article = None
            st.rerun()

# =====================================================
# TAB 2 - CREATE ARTICLE
# =====================================================

with tab2:

    st.subheader("✍️ Create New Wiki Article")

    title = st.text_input("Article Title", placeholder="Enter article title")

    article_type = st.selectbox(
        "Article Type",
        ["Characters", "Locations", "Factions", "Organizations", "Species", "Technology", "Historical Events", "Lore Articles", "Timeline Entries", "Continuity Documents"]
    )

    canon_status = st.selectbox(
        "Canon Status",
        ["non-canon", "canon"],
        help="Canon status is typically assigned by the Continuity Council after review"
    )

    content = st.text_area(
        "Article Content",
        height=450,
        placeholder="Write your article content here..."
    )

    if st.button("📜 Submit Article", use_container_width=True):

        if not title.strip():
            st.error("Title required.")
        elif not content.strip():
            st.error("Content required.")
        else:
            try:
                article_id = create_article(
                    title=title,
                    article_type=article_type,
                    content=content,
                    author_id=st.session_state.user_id,
                    canon_status=canon_status
                )
                st.success(f"✅ Article submitted successfully!\n\nArticle ID: {article_id}")
                st.balloons()
            except Exception as e:
                st.error(f"Error submitting article: {str(e)}")

# =====================================================
# TAB 3 - TIMELINE
# =====================================================

with tab3:

    st.subheader("⏳ Continuity Timeline")

    st.markdown("""
<div class='highlight-mystical'>
The official timeline consists of seven major ages that have shaped the Empire of Continuum:
</div>
    """, unsafe_allow_html=True)

    timeline_items = [
        {"era": "Age of Emergence", "period": "The First Dawn", "description": "The founding of the first civilizations and emergence of sentient beings"},
        {"era": "Age of Building", "period": "Expansion Era", "description": "Rapid expansion and development of technologies and societies"},
        {"era": "Age of Enlightenment", "period": "Renaissance", "description": "Cultural and magical renaissance across all known worlds"},
        {"era": "Age of Shadows", "period": "The Great Conflict", "description": "The devastating conflict that nearly ended the Continuum"},
        {"era": "Age of Recovery", "period": "Reconstruction", "description": "Healing and rebuilding after the great conflict"},
        {"era": "Age of Balance", "period": "Current Era", "description": "The ongoing age of peace and cooperation"},
        {"era": "Age of Convergence", "period": "The Prophecy", "description": "The prophesied final age when all timelines converge"},
    ]

    for i, event in enumerate(timeline_items, 1):
        st.markdown(f"""
<div class='epic-card'>
<h4 style='color: var(--gold-light);'>{i}. {event['era']}</h4>
<div style='color: var(--purple-light); font-size: 0.9rem; margin-bottom: 8px;'>{event['period']}</div>
<p style='color: #E8E8E8;'>{event['description']}</p>
</div>
        """, unsafe_allow_html=True)

# =====================================================
# TAB 4 - POPULAR ARTICLES
# =====================================================

with tab4:

    st.subheader("🔥 Most Viewed & Liked Articles")

    sorted_articles = sorted(wiki_data, key=lambda x: (x.get('views', 0), x.get('likes', 0)), reverse=True)[:5]

    if not sorted_articles:
        st.info("No articles available yet.")
    else:
        for idx, article in enumerate(sorted_articles, 1):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
<div class='publication-card'>
<h4 style='color: var(--gold-light); margin-bottom: 8px;'>#{idx} - {article['title']}</h4>
<div style='display: flex; gap: 20px; font-size: 0.9rem; margin-bottom: 8px;'>
<span style='color: var(--purple-light);'>{article['article_type']}</span>
<span style='color: var(--gold-primary);'>✍️ {article['author']}</span>
</div>
<div style='display: flex; gap: 20px; font-size: 0.85rem; color: #B8B8B8;'>
<span>👁️ {article.get('views', 0):,} views</span>
<span>❤️ {article.get('likes', 0)} likes</span>
</div>
</div>
                """, unsafe_allow_html=True)

            with col2:
                if st.button("View", key=f"popular_{article['id']}"):
                    st.session_state.selected_wiki_article = article["id"]
                    st.rerun()

# =====================================================
# FOOTER
# =====================================================

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

st.caption("⚔️ Empire of Continuum • Continuity Wiki v2.0 • Powered by Epic Fantasy Design")
