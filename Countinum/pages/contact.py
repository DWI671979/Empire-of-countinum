import streamlit as st

from services.contact_service import (
    submit_message,
    get_user_messages,
    get_all_messages,
    update_message_status,
    get_open_message_count
)

# =====================================================
# ACCESS CONTROL
# =====================================================

if not st.session_state.get("logged_in", False):
    st.warning("Please login to contact the Continuity Team.")
    st.stop()

# =====================================================
# PAGE HEADER
# =====================================================

st.title("📬 Contact the Continuity Team")

st.markdown("""
Have a question about canon, lore, or your submitted work?
Send a message directly to the Continuity Management Team.
They will review your message and respond as soon as possible.
""")

st.divider()

# =====================================================
# ADMIN / CONTINUITY MANAGER VIEW
# =====================================================

user_role = st.session_state.get("role", "")

if user_role in ("administrator", "continuity_manager"):

    st.subheader("📋 Incoming Messages")

    open_count = get_open_message_count()

    st.metric("Open Messages", open_count)

    all_messages = get_all_messages()

    if not all_messages:
        st.info("No messages yet.")

    else:

        for msg in all_messages:

            status_color = (
                "🟡" if msg["status"] == "open"
                else "🟢" if msg["status"] == "resolved"
                else "🔴"
            )

            with st.expander(
                f"{status_color} [{msg['status'].upper()}] "
                f"{msg['subject']} — from {msg['sender_name']}"
            ):

                st.markdown(f"**From:** {msg['sender_name']}")
                st.markdown(f"**Subject:** {msg['subject']}")
                st.markdown(f"**Sent:** {msg['created_at']}")
                st.divider()
                st.write(msg["message"])
                st.divider()

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "✅ Mark Resolved",
                        key=f"resolve_{msg['id']}"
                    ):
                        update_message_status(
                            msg["id"],
                            "resolved"
                        )
                        st.success("Marked as resolved.")
                        st.rerun()

                with col2:
                    if st.button(
                        "🔴 Mark Closed",
                        key=f"close_{msg['id']}"
                    ):
                        update_message_status(
                            msg["id"],
                            "closed"
                        )
                        st.success("Marked as closed.")
                        st.rerun()

    st.divider()

# =====================================================
# SEND A MESSAGE
# =====================================================

st.subheader("✉️ Send a Message")

subject = st.selectbox(
    "Subject",
    [
        "Canon / Lore Question",
        "Work Submission Query",
        "Copyright Concern",
        "Collaboration Request",
        "Technical Issue",
        "General Feedback",
        "Other"
    ]
)

message = st.text_area(
    "Your Message",
    height=200,
    placeholder="Describe your question or concern in detail..."
)

if st.button("📨 Send Message"):

    if not message.strip():
        st.error("Please write a message before sending.")

    else:

        success = submit_message(
            sender_id=st.session_state.user_id,
            subject=subject,
            message=message.strip()
        )

        if success:
            st.success(
                "Your message has been sent to the "
                "Continuity Team. They will review it shortly."
            )
            st.balloons()

        else:
            st.error("Something went wrong. Please try again.")

st.divider()

# =====================================================
# USER'S OWN MESSAGE HISTORY
# =====================================================

st.subheader("📁 My Previous Messages")

my_messages = get_user_messages(
    st.session_state.user_id
)

if not my_messages:
    st.info("You have not sent any messages yet.")

else:

    for msg in my_messages:

        status_icon = (
            "🟡" if msg["status"] == "open"
            else "🟢" if msg["status"] == "resolved"
            else "🔴"
        )

        with st.expander(
            f"{status_icon} {msg['subject']} "
            f"— {msg['created_at']}"
        ):
            st.write(msg["message"])
            st.caption(f"Status: {msg['status'].upper()}")

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("📬 Contact")

    st.markdown("""
### Response Times

🟢 **Canon Questions**
Usually within 48 hours.

🟡 **Submission Queries**
Within 3–5 working days.

🔴 **Urgent Issues**
Flag as Copyright Concern
for priority handling.

---

### Tips

- Be as specific as possible
- Reference story or character names
- Include chapter or scene details
if relevant
    """)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Empire of Continuum • Continuity Support Center v1.0"
)
