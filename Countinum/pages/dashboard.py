import streamlit as st
from database.database import get_connection

# =====================================================
# ACCESS CONTROL
# =====================================================

if not st.session_state.get("logged_in", False):
    st.warning("Please login to access the Dashboard.")
    st.stop()

# =====================================================
# HELPERS
# =====================================================

def get_dashboard_stats():
    conn = get_connection()

    total_users = conn.execute(
        "SELECT COUNT(*) AS t FROM users"
    ).fetchone()["t"]

    total_stories = conn.execute(
        "SELECT COUNT(*) AS t FROM stories"
    ).fetchone()["t"]

    pending_stories = conn.execute(
        "SELECT COUNT(*) AS t FROM stories WHERE status='pending'"
    ).fetchone()["t"]

    total_artworks = conn.execute(
        "SELECT COUNT(*) AS t FROM artworks"
    ).fetchone()["t"]

    total_wiki = conn.execute(
        "SELECT COUNT(*) AS t FROM wiki_articles"
    ).fetchone()["t"]

    total_projects = conn.execute(
        "SELECT COUNT(*) AS t FROM collaboration_projects"
    ).fetchone()["t"]

    open_messages = conn.execute(
        "SELECT COUNT(*) AS t FROM contact_messages WHERE status='open'"
    ).fetchone()["t"]

    pending_moderation = conn.execute(
        "SELECT COUNT(*) AS t FROM moderation_queue WHERE status='pending'"
    ).fetchone()["t"]

    conn.close()

    return {
        "total_users": total_users,
        "total_stories": total_stories,
        "pending_stories": pending_stories,
        "total_artworks": total_artworks,
        "total_wiki": total_wiki,
        "total_projects": total_projects,
        "open_messages": open_messages,
        "pending_moderation": pending_moderation
    }


def get_recent_stories(limit=5):
    conn = get_connection()
    rows = conn.execute("""
        SELECT s.title, s.status, s.created_at, u.username
        FROM stories s
        LEFT JOIN users u ON s.author_id = u.id
        ORDER BY s.id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return rows


def get_recent_artworks(limit=5):
    conn = get_connection()
    rows = conn.execute("""
        SELECT a.title, a.status, a.created_at, u.username
        FROM artworks a
        LEFT JOIN users u ON a.artist_id = u.id
        ORDER BY a.id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return rows


def get_recent_users(limit=5):
    conn = get_connection()
    rows = conn.execute("""
        SELECT username, role, created_at
        FROM users
        ORDER BY id DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return rows


def get_my_stories(user_id, limit=5):
    conn = get_connection()
    rows = conn.execute("""
        SELECT title, status, created_at
        FROM stories
        WHERE author_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit)).fetchall()
    conn.close()
    return rows


def get_my_artworks(user_id, limit=5):
    conn = get_connection()
    rows = conn.execute("""
        SELECT title, status, created_at
        FROM artworks
        WHERE artist_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit)).fetchall()
    conn.close()
    return rows


def get_pending_moderation():
    conn = get_connection()
    rows = conn.execute("""
        SELECT mq.*, u.username AS submitter
        FROM moderation_queue mq
        LEFT JOIN users u ON mq.submitted_by = u.id
        WHERE mq.status = 'pending'
        ORDER BY mq.id DESC
    """).fetchall()
    conn.close()
    return rows


def approve_moderation(item_id, content_type, content_id):
    conn = get_connection()
    conn.execute(
        "UPDATE moderation_queue SET status='approved' WHERE id=?",
        (item_id,)
    )
    if content_type == "story":
        conn.execute(
            "UPDATE stories SET status='published' WHERE id=?",
            (content_id,)
        )
    elif content_type == "artwork":
        conn.execute(
            "UPDATE artworks SET status='published' WHERE id=?",
            (content_id,)
        )
    conn.commit()
    conn.close()


def reject_moderation(item_id, content_type, content_id):
    conn = get_connection()
    conn.execute(
        "UPDATE moderation_queue SET status='rejected' WHERE id=?",
        (item_id,)
    )
    if content_type == "story":
        conn.execute(
            "UPDATE stories SET status='rejected' WHERE id=?",
            (content_id,)
        )
    elif content_type == "artwork":
        conn.execute(
            "UPDATE artworks SET status='rejected' WHERE id=?",
            (content_id,)
        )
    conn.commit()
    conn.close()


# =====================================================
# PAGE HEADER
# =====================================================

username = st.session_state.get("username", "Creator")
role = st.session_state.get("role", "user")
user_id = st.session_state.get("user_id")

st.title("⚔️ Dashboard")
st.markdown(f"Welcome back, **{username}** — *{role}*")
st.divider()

stats = get_dashboard_stats()

# =====================================================
# ADMIN / CONTINUITY MANAGER VIEW
# =====================================================

if role in ("administrator", "continuity_manager"):

    st.subheader("🌐 Universe Overview")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Total Users",    stats["total_users"])
    c2.metric("📖 Stories",        stats["total_stories"])
    c3.metric("🎨 Artworks",       stats["total_artworks"])
    c4.metric("📚 Wiki Articles",  stats["total_wiki"])

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("🤝 Projects",         stats["total_projects"])
    c6.metric("⏳ Pending Stories",   stats["pending_stories"])
    c7.metric("📬 Open Messages",     stats["open_messages"])
    c8.metric("🔎 Pending Reviews",   stats["pending_moderation"])

    st.divider()

    # --------------------------------------------------
    # MODERATION QUEUE
    # --------------------------------------------------

    st.subheader("🔎 Continuity Approval Queue")

    queue = get_pending_moderation()

    if not queue:
        st.success("All clear — no pending submissions.")
    else:
        for item in queue:
            with st.expander(
                f"📄 {item['content_type'].upper()} #{item['content_id']}"
                f" — submitted by {item['submitter']}"
            ):
                st.markdown(f"**Type:** {item['content_type']}")
                st.markdown(f"**Submitted:** {item['created_at']}")

                col_a, col_b = st.columns(2)

                with col_a:
                    if st.button(
                        "✅ Approve & Publish",
                        key=f"approve_{item['id']}"
                    ):
                        approve_moderation(
                            item["id"],
                            item["content_type"],
                            item["content_id"]
                        )
                        st.success("Approved and published!")
                        st.rerun()

                with col_b:
                    if st.button(
                        "❌ Reject",
                        key=f"reject_{item['id']}"
                    ):
                        reject_moderation(
                            item["id"],
                            item["content_type"],
                            item["content_id"]
                        )
                        st.error("Submission rejected.")
                        st.rerun()

    st.divider()

    # --------------------------------------------------
    # RECENT ACTIVITY
    # --------------------------------------------------

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📖 Recent Stories")
        recent_stories = get_recent_stories()
        if not recent_stories:
            st.info("No stories yet.")
        for s in recent_stories:
            status_icon = (
                "🟢" if s["status"] == "published"
                else "🟡" if s["status"] == "pending"
                else "🔴"
            )
            st.markdown(
                f"{status_icon} **{s['title']}** "
                f"by *{s['username']}* — {s['created_at'][:10]}"
            )

    with col_right:
        st.subheader("🎨 Recent Artworks")
        recent_art = get_recent_artworks()
        if not recent_art:
            st.info("No artworks yet.")
        for a in recent_art:
            status_icon = (
                "🟢" if a["status"] == "published"
                else "🟡" if a["status"] == "pending"
                else "🔴"
            )
            st.markdown(
                f"{status_icon} **{a['title']}** "
                f"by *{a['username']}* — {a['created_at'][:10]}"
            )

    st.divider()

    st.subheader("👥 Newest Members")
    new_users = get_recent_users()
    if not new_users:
        st.info("No users yet.")
    for u in new_users:
        st.markdown(
            f"• **{u['username']}** — *{u['role']}* "
            f"— joined {u['created_at'][:10]}"
        )

# =====================================================
# REGULAR USER / CREATOR VIEW
# =====================================================

else:

    st.subheader("📊 My Activity")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📖 Universe Stories",   stats["total_stories"])
    c2.metric("🎨 Universe Artworks",  stats["total_artworks"])
    c3.metric("📚 Wiki Articles",      stats["total_wiki"])
    c4.metric("🤝 Active Projects",    stats["total_projects"])

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📖 My Stories")
        my_stories = get_my_stories(user_id)
        if not my_stories:
            st.info("You haven't submitted any stories yet.")
        for s in my_stories:
            status_icon = (
                "🟢" if s["status"] == "published"
                else "🟡" if s["status"] == "pending"
                else "🔴"
            )
            st.markdown(
                f"{status_icon} **{s['title']}** "
                f"— {s['status']} — {s['created_at'][:10]}"
            )

    with col_right:
        st.subheader("🎨 My Artworks")
        my_artworks = get_my_artworks(user_id)
        if not my_artworks:
            st.info("You haven't submitted any artworks yet.")
        for a in my_artworks:
            status_icon = (
                "🟢" if a["status"] == "published"
                else "🟡" if a["status"] == "pending"
                else "🔴"
            )
            st.markdown(
                f"{status_icon} **{a['title']}** "
                f"— {a['status']} — {a['created_at'][:10]}"
            )

    st.divider()

    # Quick nav buttons
    st.subheader("🚀 Quick Actions")

    b1, b2, b3, b4 = st.columns(4)

    with b1:
        if st.button("📖 Browse Stories", use_container_width=True):
            st.switch_page("pages/stories.py")

    with b2:
        if st.button("🎨 View Artwork", use_container_width=True):
            st.switch_page("pages/artwork.py")

    with b3:
        if st.button("🤝 Collaborate", use_container_width=True):
            st.switch_page("pages/collaboration.py")

    with b4:
        if st.button("📚 Read the Wiki", use_container_width=True):
            st.switch_page("pages/wiki.py")

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("⚔️ Dashboard")
    st.write(f"Logged in as **{username}**")
    st.caption(f"Role: {role}")
    st.divider()

    st.markdown("""
### Navigation

- 📖 Stories
- 🎨 Artwork
- 📚 Wiki
- 🤝 Collaboration
- 📬 Contact
- ⚙️ Profile
    """)

# =====================================================
# FOOTER
# =====================================================

st.divider()
st.caption("Empire of Continuum • Dashboard v1.0")
