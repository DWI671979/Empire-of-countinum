import streamlit as st

from services.contact_service import (
    create_contact_message,
    get_user_messages,
    get_contact_statistics,
    get_contact_categories
)

# =====================================================
# ACCESS CONTROL
# =====================================================

if not st.session_state.get("logged_in", False):
    st.warning(
        "Please login to contact the Continuity Team."
    )
    st.stop()

# =====================================================
# PAGE HEADER
# =====================================================

st.title("📨 Contact Continuity Management")

st.markdown("""
Need assistance?

Contact the Empire of Continuum Continuity
Management Team regarding moderation,
copyright issues, canon reviews,
technical support, account concerns,
or general questions.
""")

st.divider()

# =====================================================
# STATISTICS
# =====================================================

stats = get_contact_statistics()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Tickets",
        stats["total"]
    )

with c2:
    st.metric(
        "Open",
        stats["open"]
    )

with c3:
    st.metric(
        "In Progress",
        stats["in_progress"]
    )

with c4:
    st.metric(
        "Closed",
        stats["closed"]
    )

st.divider()

# =====================================================
# TABS
# =====================================================

tab1, tab2 = st.tabs([
    "Create Ticket",
    "My Tickets"
])

# =====================================================
# CREATE TICKET
# =====================================================

with tab1:

    st.subheader(
        "Open Support Ticket"
    )

    category = st.selectbox(
        "Category",
        get_contact_categories()
    )

    subject = st.text_input(
        "Subject"
    )

    message = st.text_area(
        "Describe your issue",
        height=250
    )

    priority = st.selectbox(
        "Priority",
        [
            "Low",
            "Medium",
            "High",
            "Urgent"
        ]
    )

    if st.button(
        "Submit Ticket"
    ):

        if not subject.strip():

            st.error(
                "Subject required."
            )

        elif not message.strip():

            st.error(
                "Message required."
            )

        else:

            full_message = f"""
Category: {category}

Priority: {priority}

Message:

{message}
"""

            ticket_id = create_contact_message(
                sender_id=st.session_state.user_id,
                subject=subject,
                message=full_message
            )

            st.success(
                f"""
Support ticket submitted.

Ticket ID:
{ticket_id}

The Continuity Team will review
your request.
"""
            )

            st.balloons()

# =====================================================
# MY TICKETS
# =====================================================

with tab2:

    st.subheader(
        "My Support Tickets"
    )

    tickets = get_user_messages(
        st.session_state.user_id
    )

    if not tickets:

        st.info(
            "No tickets submitted."
        )

    for ticket in tickets:

        status = ticket["status"]

        if status == "open":
            badge = "🟡 Open"

        elif status == "in_progress":
            badge = "🔵 In Progress"

        else:
            badge = "🟢 Closed"

        st.markdown(f"""
### Ticket #{ticket['id']}

Subject:
{ticket['subject']}

Status:
{badge}
""")

        st.text_area(
            "Ticket Content",
            ticket["message"],
            disabled=True,
            key=f"ticket_{ticket['id']}"
        )

        st.divider()

# =====================================================
# CONTINUITY TEAM INFORMATION
# =====================================================

st.divider()

st.subheader(
    "🏛 Continuity Management Team"
)

st.markdown("""
The Continuity Management Team oversees:

- Canon continuity
- Moderation reviews
- Copyright disputes
- User support
- Community governance
- Wiki maintenance
- Timeline consistency
- Shared universe integrity

Response times vary depending on
ticket volume and complexity.
""")

# =====================================================
# QUICK HELP
# =====================================================

with st.expander(
    "Frequently Asked Questions"
):

    st.markdown("""
### How do I appeal moderation?

Create a ticket using:

**Moderation Appeal**

---

### How do I report stolen content?

Create a ticket using:

**Copyright Issue**

and submit a copyright claim.

---

### How do I request canon status?

Create a ticket using:

**Canon Review Request**

---

### How do I report bugs?

Use:

**Bug Report**

and provide steps to reproduce.
""")

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header(
        "📨 Support Center"
    )

    st.write(
        f"User: "
        f"**{st.session_state.username}**"
    )

    st.divider()

    st.markdown("""
### Available Services

- Technical Support
- Copyright Support
- Canon Reviews
- Moderation Appeals
- Account Recovery
- Content Reports
- Continuity Questions

### Support Workflow

Submit Ticket
↓
Team Review
↓
Investigation
↓
Resolution
""")

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Empire of Continuum • Continuity Support Center v1.0"
)