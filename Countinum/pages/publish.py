import streamlit as st
import json
import os

from services.story_service import (
    create_story,
    get_story_categories
)

# =====================================================
# ACCESS CONTROL
# =====================================================

if not st.session_state.get("logged_in", False):
    st.warning(
        "Please login to publish content."
    )
    st.stop()

# =====================================================
# LOAD SAMPLE DATA
# =====================================================

def load_publications_data():
    data_path = os.path.join(
        os.path.dirname(__file__),
        "../data/publications.json"
    )
    if os.path.exists(data_path):
        with open(data_path, 'r') as f:
            return json.load(f)
    return []

publications_data = load_publications_data()

# =====================================================
# PAGE CONFIG
# =====================================================

st.markdown(
    """
    <h1 class='main-title'>
    🖋️ PUBLISH TO THE EMPIRE
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown("""
<div class='highlight-mystical'>
Submit stories, lore articles, comics, character profiles and worldbuilding documents for moderation and eventual publication within the Empire of Continuum.
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

# =====================================================
# USER INFO
# =====================================================

user_id = st.session_state.get("user_id")
username = st.session_state.get("username")

st.success(
    f"📝 Publishing as: **{username}**"
)

# =====================================================
# CATEGORY LIST
# =====================================================

try:
    categories = get_story_categories()
except:
    categories = ["Novel", "Short Story", "Comic", "Lore Article", "Character Profile", "Worldbuilding Document"]

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "📤 Story Submission",
    "📚 Published Works",
    "📋 Publishing Guidelines"
])

# =====================================================
# SUBMISSION TAB
# =====================================================

with tab1:

    st.subheader("Submit New Content")

    title = st.text_input(
        "Title",
        placeholder="Enter the title of your work..."
    )

    category = st.selectbox(
        "Category",
        categories
    )

    synopsis = st.text_area(
        "Synopsis",
        height=120,
        placeholder="Brief overview of your work.",
        help="Provide a compelling summary to attract readers."
    )

    content = st.text_area(
        "Content",
        height=500,
        placeholder="Paste your full work here...",
        help="Paste your complete work for publication review."
    )

    copyright_confirmation = st.checkbox(
        "✓ I confirm that I own this work or have permission to publish it."
    )

    canon_confirmation = st.checkbox(
        "✓ I understand that submission does not automatically make this work canon."
    )

    # -----------------------------------------
    # WORD COUNT
    # -----------------------------------------

    word_count = len(
        content.split()
    ) if content else 0

    st.info(
        f"📊 Word Count: **{word_count}** words"
    )

    # -----------------------------------------
    # SUBMIT BUTTON
    # -----------------------------------------

    if st.button(
        "📜 Submit for Moderation",
        use_container_width=True
    ):

        errors = []

        if not title.strip():
            errors.append("✗ Title is required.")

        if not synopsis.strip():
            errors.append("✗ Synopsis is required.")

        if not content.strip():
            errors.append("✗ Content is required.")

        if len(content) < 100:
            errors.append("✗ Content must be at least 100 characters long.")

        if not copyright_confirmation:
            errors.append("✗ Copyright confirmation required.")

        if not canon_confirmation:
            errors.append("✗ Canon acknowledgement required.")

        # Display errors
        if errors:
            for error in errors:
                st.error(error)
        else:
            try:
                story_id = create_story(
                    title=title,
                    author_id=user_id,
                    category=category,
                    content=content
                )

                st.success(f"""
✅ **Submission received!**

📝 Story ID: {story_id}

Your work has entered the moderation queue. You will be notified of the review status in your notifications.
                """)
                st.balloons()
            except Exception as e:
                st.error(f"Error submitting story: {str(e)}")

# =====================================================
# PUBLISHED WORKS
# =====================================================

with tab2:

    st.subheader("📚 Latest Published Works")

    # Filter by status
    status_filter = st.segmented_control(
        "Filter by Status",
        ["All", "Published", "Pending", "Canon"],
        default="All"
    )

    filtered_pubs = publications_data
    
    if status_filter == "Published":
        filtered_pubs = [p for p in publications_data if p.get("status") == "published"]
    elif status_filter == "Pending":
        filtered_pubs = [p for p in publications_data if p.get("status") == "pending"]
    elif status_filter == "Canon":
        filtered_pubs = [p for p in publications_data if p.get("canon_status") == "canon"]

    if not filtered_pubs:
        st.info("📭 No publications found.")
    else:
        for pub in filtered_pubs[:15]:
            status_badge = ""
            if pub.get("status") == "pending":
                status_badge = "🟡 Pending Review"
            elif pub.get("status") == "published":
                status_badge = "🟢 Published"
            
            canon_badge = "🟢 Canon" if pub.get("canon_status") == "canon" else "⭐ Community"

            st.markdown(f"""
<div class='publication-card'>
<div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;'>
<div style='flex: 1;'>
<h4 style='color: var(--gold-light); margin-bottom: 8px;'>{pub['title']}</h4>
<div style='color: var(--purple-light); font-size: 0.9rem;'>✍️ by {pub['author']}</div>
</div>
<div style='text-align: right;'>
<div style='color: var(--gold-primary); font-weight: bold; font-size: 0.95rem;'>{status_badge}</div>
</div>
</div>

<div style='display: flex; gap: 12px; margin-bottom: 12px; font-size: 0.85rem;'>
<span style='background: rgba(168,85,247,0.2); padding: 4px 12px; border-radius: 12px; color: var(--purple-light);'>{pub['category']}</span>
<span style='background: rgba(212,175,55,0.2); padding: 4px 12px; border-radius: 12px; color: var(--gold-primary);'>{canon_badge}</span>
<span style='color: #A8A8A8;'>📖 {pub['word_count']:,} words</span>
</div>

<p style='color: #D8D8D8; margin-bottom: 10px;'>{pub['excerpt']}</p>

<div style='display: flex; gap: 20px; font-size: 0.85rem; color: #B8B8B8;'>
<span>❤️ {pub.get('likes', 0)} likes</span>
<span>👁️ {pub.get('views', 0):,} views</span>
<span>🔖 {pub.get('bookmarks', 0)} bookmarks</span>
<span>📅 {pub['published_date']}</span>
</div>
</div>
            """, unsafe_allow_html=True)

# =====================================================
# GUIDELINES TAB
# =====================================================

with tab3:

    st.subheader("📋 Empire Publishing Standards")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
### ✅ Content Quality

All submissions should:
- Be readable and engaging
- Use proper grammar and spelling
- Have clear formatting
- Remain consistent with chosen themes
- Demonstrate originality and creativity

### 📂 Allowed Categories

- Novel
- Short Story
- Comic
- Lore Article
- Character Profile
- Worldbuilding Document
        """)

    with col2:
        st.markdown("""
### 🔒 Copyright & Rights

Creators must:
- Own the submitted work
- Possess rights to publish
- Provide proof if requested
- Not violate intellectual property

**Violations may result in:**
- Content removal
- Account restrictions
- Moderator investigation

### ⚖️ Canon Policy

Submission ≠ Canon Status

Canon assignments are made through:
- Moderator review process
- Community approval
- Continuity Team decisions
- Historical significance
        """)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    st.markdown("""
### 🚫 Do Not Submit:

- Harassment or hate content
- Spam or promotional material
- Malicious or harmful content
- Copyright violations
- Explicit adult content
- Off-topic material

### ⚙️ Review Process

```
1. Submission → 2. Initial Review → 3. Quality Check
        ↓
4. Canon Evaluation → 5. Final Approval → 6. Publication
```

**Average review time: 3-7 days**

### 📖 Word Count Guidelines

| Category | Minimum | Recommended |
|----------|---------|-------------|
| Novel | 50,000 | 80,000+ |
| Short Story | 100 | 5,000-10,000 |
| Comic | 500 | 2,000-5,000 |
| Lore Article | 500 | 2,000-5,000 |
| Character Profile | 300 | 1,000-3,000 |
| Worldbuilding | 1,000 | 5,000+ |
    """)

# =====================================================
# QUICK REFERENCE
# =====================================================

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

st.subheader("⚡ Quick Reference")

ref_col1, ref_col2, ref_col3 = st.columns(3)

with ref_col1:
    st.markdown("""
<div class='epic-card' style='text-align: center;'>
<div style='font-size: 2rem;'>📝</div>
<div style='color: var(--gold-primary); font-weight: bold;'>Minimum 100 Words</div>
<small style='color: #A8A8A8;'>For all submissions</small>
</div>
    """, unsafe_allow_html=True)

with ref_col2:
    st.markdown("""
<div class='epic-card' style='text-align: center;'>
<div style='font-size: 2rem;'>⏱️</div>
<div style='color: var(--gold-primary); font-weight: bold;'>3-7 Days Review</div>
<small style='color: #A8A8A8;'>Average processing time</small>
</div>
    """, unsafe_allow_html=True)

with ref_col3:
    st.markdown("""
<div class='epic-card' style='text-align: center;'>
<div style='font-size: 2rem;'>✓</div>
<div style='color: var(--gold-primary); font-weight: bold;'>Separate Review</div>
<small style='color: #A8A8A8;'>For canon status</small>
</div>
    """, unsafe_allow_html=True)

# =====================================================
# FOOTER
# =====================================================

st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

st.caption("⚔️ Empire of Continuum • Publishing System v2.0 • Powered by Epic Fantasy Design")
