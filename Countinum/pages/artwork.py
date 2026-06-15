import streamlit as st
from pathlib import Path

from services.artwork_service import (
    save_artwork_file,
    create_artwork,
    get_approved_artworks,
    get_artwork,
    search_artworks,
    increment_artwork_view,
    like_artwork,
    get_most_liked_artworks,
    get_most_viewed_artworks
)

# =====================================================
# ACCESS CONTROL
# =====================================================

if not st.session_state.get("logged_in", False):
    st.warning(
        "Please login to access the Artwork Gallery."
    )
    st.stop()

# =====================================================
# SESSION STATE
# =====================================================

if "selected_artwork_id" not in st.session_state:
    st.session_state.selected_artwork_id = None

# =====================================================
# HEADER
# =====================================================

st.title("🎨 Empire Artwork Gallery")

st.markdown("""
Discover community-created artwork from across the
Empire of Continuum. Upload your creations, explore
featured illustrations, and support fellow artists.
""")

st.divider()

# =====================================================
# TABS
# =====================================================

gallery_tab, upload_tab = st.tabs([
    "Gallery",
    "Upload Artwork"
])

# =====================================================
# GALLERY TAB
# =====================================================

with gallery_tab:

    st.subheader("🌟 Featured Artwork")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### ❤️ Most Liked")

        top_liked = get_most_liked_artworks(5)

        if top_liked:

            for art in top_liked:

                st.markdown(f"""
                **{art['title']}**

                Artist: {art['artist_name']}

                ❤️ {art['likes']} | 👁️ {art['views']}
                """)

                st.divider()

        else:
            st.info("No artwork available.")

    with col2:

        st.markdown("### 👁️ Most Viewed")

        top_viewed = get_most_viewed_artworks(5)

        if top_viewed:

            for art in top_viewed:

                st.markdown(f"""
                **{art['title']}**

                Artist: {art['artist_name']}

                ❤️ {art['likes']} | 👁️ {art['views']}
                """)

                st.divider()

        else:
            st.info("No artwork available.")

    st.divider()

    # =================================================
    # SEARCH
    # =================================================

    search_query = st.text_input(
        "🔎 Search Artwork",
        placeholder="Search artwork titles..."
    )

    if search_query:
        artworks = search_artworks(
            search_query
        )
    else:
        artworks = get_approved_artworks()

    st.subheader("🖼 Community Gallery")

    if not artworks:
        st.info(
            "No artwork available yet."
        )

    # ===============================================
    # GALLERY CARDS
    # ===============================================

    for artwork in artworks:

        with st.container():

            st.markdown(f"""
            ### {artwork['title']}

            Artist: **{artwork['artist_name']}**

            ❤️ {artwork['likes']} |
            👁️ {artwork['views']}
            """)

            if Path(
                artwork["image_path"]
            ).exists():

                st.image(
                    artwork["image_path"],
                    use_container_width=True
                )

            else:

                st.warning(
                    "Artwork file missing."
                )

            if st.button(
                f"View Artwork #{artwork['id']}",
                key=f"art_{artwork['id']}"
            ):

                st.session_state.selected_artwork_id = (
                    artwork["id"]
                )

                st.rerun()

            st.divider()

# =====================================================
# ARTWORK VIEWER
# =====================================================

if st.session_state.selected_artwork_id:

    artwork = get_artwork(
        st.session_state.selected_artwork_id
    )

    if artwork:

        increment_artwork_view(
            artwork["id"]
        )

        st.divider()

        st.header(
            artwork["title"]
        )

        st.caption(
            f"By {artwork['artist_name']}"
        )

        if Path(
            artwork["image_path"]
        ).exists():

            st.image(
                artwork["image_path"],
                use_container_width=True
            )

        else:

            st.error(
                "Artwork file not found."
            )

        st.divider()

        stat1, stat2 = st.columns(2)

        with stat1:
            st.metric(
                "Likes",
                artwork["likes"]
            )

        with stat2:
            st.metric(
                "Views",
                artwork["views"]
            )

        st.divider()

        left, right = st.columns(2)

        with left:

            if st.button(
                "❤️ Like Artwork"
            ):

                result = like_artwork(
                    st.session_state.user_id,
                    artwork["id"]
                )

                if result:

                    st.success(
                        "Artwork liked."
                    )

                else:

                    st.warning(
                        "Already liked."
                    )

                st.rerun()

        with right:

            if st.button(
                "⬅ Return to Gallery"
            ):

                st.session_state.selected_artwork_id = None
                st.rerun()

# =====================================================
# UPLOAD TAB
# =====================================================

with upload_tab:

    st.subheader(
        "📤 Upload Artwork"
    )

    st.info(
        "Only JPG/JPEG artwork files "
        "are accepted."
    )

    title = st.text_input(
        "Artwork Title"
    )

    uploaded_file = st.file_uploader(
        "Select JPG Artwork",
        type=["jpg", "jpeg"]
    )

    copyright_confirm = st.checkbox(
        "I confirm that I own the rights "
        "to this artwork."
    )

    if st.button(
        "Submit Artwork"
    ):

        if not title.strip():

            st.error(
                "Artwork title required."
            )

        elif uploaded_file is None:

            st.error(
                "Please upload an image."
            )

        elif not copyright_confirm:

            st.error(
                "Copyright confirmation required."
            )

        else:

            image_path = save_artwork_file(
                uploaded_file
            )

            if image_path is None:

                st.error(
                    "Invalid file type."
                )

            else:

                artwork_id = create_artwork(
                    title=title,
                    artist_id=st.session_state.user_id,
                    image_path=image_path
                )

                st.success(
                    f"""
                    Artwork submitted.

                    Artwork ID:
                    {artwork_id}

                    Awaiting moderation review.
                    """
                )

                st.balloons()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("🎨 Artist Hub")

    st.write(
        f"Logged in as "
        f"**{st.session_state.username}**"
    )

    st.divider()

    st.markdown("""
    **Accepted Formats**

    - JPG
    - JPEG

    **Submission Flow**

    Upload
    ↓
    Moderation
    ↓
    Publication
    """)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Empire of Continuum • Artwork Gallery v1.0"
)