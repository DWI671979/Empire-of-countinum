import streamlit as st

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
# PAGE CONFIG
# =====================================================

st.title("🖋️ Publish to the Empire")

st.markdown("""
Submit stories, lore articles, comics,
character profiles and worldbuilding documents
for moderation and eventual publication
within the Empire of Continuum.
""")

st.divider()

# =====================================================
# USER INFO
# =====================================================

user_id = st.session_state.get("user_id")
username = st.session_state.get("username")

st.success(
    f"Publishing as: {username}"
)

# =====================================================
# CATEGORY LIST
# =====================================================

categories = get_story_categories()

# =====================================================
# TABS
# =====================================================

tab1, tab2 = st.tabs([
    "Story Submission",
    "Publishing Guidelines"
])

# =====================================================
# SUBMISSION TAB
# =====================================================

with tab1:

    st.subheader(
        "Submit New Content"
    )

    title = st.text_input(
        "Title"
    )

    category = st.selectbox(
        "Category",
        categories
    )

    synopsis = st.text_area(
        "Synopsis",
        height=120,
        help="Brief overview of your work."
    )

    content = st.text_area(
        "Content",
        height=500,
        help="Paste your full work here."
    )

    copyright_confirmation = st.checkbox(
        "I confirm that I own this work "
        "or have permission to publish it."
    )

    canon_confirmation = st.checkbox(
        "I understand that submission "
        "does not automatically make "
        "this work canon."
    )

    # -----------------------------------------
    # WORD COUNT
    # -----------------------------------------

    word_count = len(
        content.split()
    ) if content else 0

    st.info(
        f"Word Count: {word_count}"
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
            errors.append(
                "Title is required."
            )

        if not synopsis.strip():
            errors.append(
                "Synopsis is required."
            )

        if not content.strip():
            errors.append(
                "Content is required."
            )

        if len(content) < 100:
            errors.append(
                "Content is too short."
            )

        if not copyright_confirmation:
            errors.append(
                "Copyright confirmation required."
            )

        if not canon_confirmation:
            errors.append(
                "Canon acknowledgement required."
            )

        # ------------------------------
        # DISPLAY ERRORS
        # ------------------------------

        if errors:

            for error in errors:
                st.error(error)

        else:

            story_id = create_story(
                title=title,
                author_id=user_id,
                category=category,
                content=content
            )

            st.success(
                f"""
                Submission received.

                Story ID: {story_id}

                Your work has entered the
                moderation queue.
                """
            )

            st.balloons()

# =====================================================
# GUIDELINES TAB
# =====================================================

with tab2:

    st.subheader(
        "Empire Publishing Standards"
    )

    st.markdown("""
### Content Quality

All submissions should:

- Be readable
- Use proper grammar
- Have clear formatting
- Remain consistent with chosen themes

---

### Allowed Categories

- Novel
- Short Story
- Comic
- Lore Article
- Character Profile
- Worldbuilding Document

---

### Copyright

Creators must:

- Own the submitted work
- Possess rights to publish
- Provide proof if requested

Copyright disputes may result in:

- Removal of content
- Account restrictions
- Moderator investigation

---

### Canon Policy

Submission does NOT automatically
become canon.

Canon status may be granted through:

- Moderator review
- Community approval processes
- Continuity Team decisions

---

### Community Conduct

Do not submit:

- Harassment
- Hate content
- Spam
- Malicious content
- Copyright violations

---

### Review Process

Submission
↓
Moderation Review
↓
Approved / Rejected
↓
Publication
    """)

# =====================================================
# QUICK REFERENCE
# =====================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Minimum Length",
        "100 Words"
    )

with col2:
    st.metric(
        "Review Status",
        "Moderated"
    )

with col3:
    st.metric(
        "Canon Status",
        "Separate Review"
    )

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Empire of Continuum • Publishing System v1.0"
)