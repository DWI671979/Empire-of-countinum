import streamlit as st
from database.database import get_connection

# =====================================================
# ACCESS CONTROL
# =====================================================

if not st.session_state.get("logged_in", False):
    st.warning("Please login first.")
    st.stop()

# Simple admin check
user_role = st.session_state.get("role", "user")

if user_role not in ["admin", "moderator", "continuity_team"]:
    st.error("You do not have permission to access the Admin Panel.")
    st.stop()

# =====================================================
# PAGE CONFIG
# =====================================================

st.title("🏛 Empire of Continuum Administration")

st.markdown("""
Manage the Empire of Continuum platform.

This dashboard allows administrators,
moderators, and continuity staff to review:

- Stories
- Artwork
- Wiki Articles
- Copyright Claims
- Support Tickets
- Community Statistics
""")

st.divider()

# =====================================================
# HELPERS
# =====================================================

def fetch_rows(query, params=()):
    try:
        conn = get_connection()
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return rows
    except Exception as e:
        st.warning(str(e))
        return []


def execute_query(query, params=()):
    try:
        conn = get_connection()
        conn.execute(query, params)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(str(e))
        return False


def fetch_scalar(query):
    try:
        conn = get_connection()
        result = conn.execute(query).fetchone()
        conn.close()

        if result:
            return list(result)[0]

        return 0

    except:
        return 0


# =====================================================
# STATS
# =====================================================

stories_count = fetch_scalar(
    "SELECT COUNT(*) FROM stories"
)

users_count = fetch_scalar(
    "SELECT COUNT(*) FROM users"
)

wiki_count = fetch_scalar(
    "SELECT COUNT(*) FROM wiki_articles"
)

claims_count = fetch_scalar(
    "SELECT COUNT(*) FROM copyright_claims"
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Users", users_count)

with c2:
    st.metric("Stories", stories_count)

with c3:
    st.metric("Wiki Articles", wiki_count)

with c4:
    st.metric("Copyright Claims", claims_count)

st.divider()

# =====================================================
# TABS
# =====================================================

tabs = st.tabs([
    "Moderation Queue",
    "Stories",
    "Wiki",
    "Copyright",
    "Support",
    "Users",
    "Analytics"
])

# =====================================================
# MODERATION QUEUE
# =====================================================

with tabs[0]:

    st.subheader("Moderation Queue")

    queue = fetch_rows("""
    SELECT *
    FROM moderation_queue
    ORDER BY id DESC
    """)

    if not queue:
        st.info("No moderation items.")
    else:

        for item in queue:

            st.markdown(f"""
### Queue Item #{item['id']}

Content Type:
{item['content_type']}

Content ID:
{item['content_id']}

Submitted By:
{item['submitted_by']}
""")

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    f"Approve {item['id']}",
                    key=f"approve_queue_{item['id']}"
                ):

                    execute_query("""
                    UPDATE moderation_queue
                    SET status='approved'
                    WHERE id=?
                    """,
                    (item["id"],))

                    st.success("Approved")
                    st.rerun()

            with col2:

                if st.button(
                    f"Reject {item['id']}",
                    key=f"reject_queue_{item['id']}"
                ):

                    execute_query("""
                    UPDATE moderation_queue
                    SET status='rejected'
                    WHERE id=?
                    """,
                    (item["id"],))

                    st.success("Rejected")
                    st.rerun()

            st.divider()

# =====================================================
# STORIES
# =====================================================

with tabs[1]:

    st.subheader("Story Management")

    stories = fetch_rows("""
    SELECT
        s.*,
        u.username AS author_name
    FROM stories s
    LEFT JOIN users u
        ON s.author_id=u.id
    ORDER BY s.id DESC
    """)

    if not stories:
        st.info("No stories found.")

    for story in stories:

        st.markdown(f"""
### {story['title']}

Author:
{story.get('author_name', 'Unknown')}

Category:
{story['category']}

Status:
{story['status']}
""")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                f"Approve Story {story['id']}",
                key=f"story_approve_{story['id']}"
            ):

                execute_query("""
                UPDATE stories
                SET status='approved'
                WHERE id=?
                """,
                (story["id"],))

                st.success("Story approved.")
                st.rerun()

        with col2:

            if st.button(
                f"Reject Story {story['id']}",
                key=f"story_reject_{story['id']}"
            ):

                execute_query("""
                UPDATE stories
                SET status='rejected'
                WHERE id=?
                """,
                (story["id"],))

                st.success("Story rejected.")
                st.rerun()

        st.divider()

# =====================================================
# WIKI
# =====================================================

with tabs[2]:

    st.subheader("Wiki Management")

    articles = fetch_rows("""
    SELECT *
    FROM wiki_articles
    ORDER BY id DESC
    """)

    if not articles:
        st.info("No wiki articles found.")

    for article in articles:

        st.markdown(f"""
### {article['title']}

Type:
{article['article_type']}

Canon Status:
{article['canon_status']}
""")

        if st.button(
            f"Toggle Canon {article['id']}",
            key=f"canon_{article['id']}"
        ):

            new_status = (
                "non-canon"
                if article["canon_status"] == "canon"
                else "canon"
            )

            execute_query("""
            UPDATE wiki_articles
            SET canon_status=?
            WHERE id=?
            """,
            (
                new_status,
                article["id"]
            ))

            st.success("Updated")
            st.rerun()

        st.divider()

# =====================================================
# COPYRIGHT
# =====================================================

with tabs[3]:

    st.subheader("Copyright Claims")

    claims = fetch_rows("""
    SELECT *
    FROM copyright_claims
    ORDER BY id DESC
    """)

    if not claims:
        st.info("No claims submitted.")

    for claim in claims:

        st.markdown(f"""
### Claim #{claim['id']}

Type:
{claim['content_type']}

Status:
{claim['status']}
""")

        st.write(
            claim["ownership_statement"]
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                f"Approve Claim {claim['id']}",
                key=f"claim_a_{claim['id']}"
            ):

                execute_query("""
                UPDATE copyright_claims
                SET status='approved'
                WHERE id=?
                """,
                (claim["id"],))

                st.rerun()

        with col2:

            if st.button(
                f"Reject Claim {claim['id']}",
                key=f"claim_r_{claim['id']}"
            ):

                execute_query("""
                UPDATE copyright_claims
                SET status='rejected'
                WHERE id=?
                """,
                (claim["id"],))

                st.rerun()

        st.divider()

# =====================================================
# SUPPORT
# =====================================================

with tabs[4]:

    st.subheader("Support Tickets")

    tickets = fetch_rows("""
    SELECT *
    FROM contact_messages
    ORDER BY id DESC
    """)

    if not tickets:
        st.info("No support tickets.")

    for ticket in tickets:

        st.markdown(f"""
### Ticket #{ticket['id']}

Subject:
{ticket['subject']}

Status:
{ticket['status']}
""")

        st.text_area(
            "Message",
            ticket["message"],
            disabled=True,
            key=f"ticket_{ticket['id']}"
        )

        if st.button(
            f"Close Ticket {ticket['id']}",
            key=f"close_{ticket['id']}"
        ):

            execute_query("""
            UPDATE contact_messages
            SET status='closed'
            WHERE id=?
            """,
            (ticket["id"],))

            st.rerun()

        st.divider()

# =====================================================
# USERS
# =====================================================

with tabs[5]:

    st.subheader("User Management")

    users = fetch_rows("""
    SELECT *
    FROM users
    ORDER BY id DESC
    """)

    if not users:
        st.info("No users found.")

    for user in users:

        st.markdown(f"""
### {user['username']}

User ID:
{user['id']}
""")

        role = st.selectbox(
            f"Role {user['id']}",
            [
                "user",
                "moderator",
                "continuity_team",
                "admin"
            ],
            key=f"role_{user['id']}"
        )

        if st.button(
            f"Update Role {user['id']}",
            key=f"update_role_{user['id']}"
        ):

            try:

                execute_query("""
                UPDATE users
                SET role=?
                WHERE id=?
                """,
                (
                    role,
                    user["id"]
                ))

                st.success("Role updated.")

            except:

                st.warning(
                    "Role column not found in users table."
                )

        st.divider()

# =====================================================
# ANALYTICS
# =====================================================

with tabs[6]:

    st.subheader("Platform Analytics")

    st.metric(
        "Total Users",
        users_count
    )

    st.metric(
        "Total Stories",
        stories_count
    )

    st.metric(
        "Wiki Articles",
        wiki_count
    )

    st.metric(
        "Copyright Claims",
        claims_count
    )

    st.info("""
Future analytics can include:

• Active users
• Story engagement
• Artwork engagement
• Canon approvals
• Traffic analytics
• Community growth
""")

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Empire of Continuum • Administration Console v1.0"
)