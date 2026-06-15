import streamlit as st

from services.copyright_service import (
    create_copyright_claim,
    get_user_claims,
    get_copyright_statistics
)

# =====================================================
# LOGIN CHECK
# =====================================================

if not st.session_state.get("logged_in", False):
    st.warning(
        "Please login first."
    )
    st.stop()

# =====================================================
# HEADER
# =====================================================

st.title("© Copyright Management")

st.markdown("""
Protect your creative works within the
Empire of Continuum ecosystem.

Creators can register ownership claims,
report disputes, and submit evidence for
review by the Continuity Management Team.
""")

st.divider()

# =====================================================
# STATS
# =====================================================

stats = get_copyright_statistics()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Claims", stats["total"])

with c2:
    st.metric("Pending", stats["pending"])

with c3:
    st.metric("Approved", stats["approved"])

with c4:
    st.metric("Rejected", stats["rejected"])

st.divider()

# =====================================================
# TABS
# =====================================================

tab1, tab2 = st.tabs([
    "Submit Claim",
    "My Claims"
])

# =====================================================
# SUBMIT
# =====================================================

with tab1:

    st.subheader(
        "Submit Copyright Claim"
    )

    content_type = st.selectbox(
        "Content Type",
        [
            "Story",
            "Artwork",
            "Wiki Article",
            "Character",
            "Other"
        ]
    )

    content_id = st.number_input(
        "Content ID",
        min_value=1,
        step=1
    )

    ownership_statement = st.text_area(
        "Ownership Statement",
        height=200
    )

    evidence_path = st.text_input(
        "Evidence File Reference (optional)"
    )

    if st.button(
        "Submit Claim"
    ):

        if not ownership_statement.strip():

            st.error(
                "Ownership statement required."
            )

        else:

            claim_id = create_copyright_claim(
                claimant_id=st.session_state.user_id,
                content_type=content_type,
                content_id=content_id,
                ownership_statement=ownership_statement,
                evidence_path=evidence_path
            )

            st.success(
                f"""
Claim submitted successfully.

Claim ID:
{claim_id}
"""
            )

# =====================================================
# USER CLAIMS
# =====================================================

with tab2:

    st.subheader(
        "My Claims"
    )

    claims = get_user_claims(
        st.session_state.user_id
    )

    if not claims:

        st.info(
            "No claims submitted."
        )

    for claim in claims:

        status = claim["status"]

        if status == "approved":
            badge = "🟢 Approved"
        elif status == "rejected":
            badge = "🔴 Rejected"
        else:
            badge = "🟡 Pending"

        st.markdown(f"""
### Claim #{claim['id']}

Content Type:
{claim['content_type']}

Content ID:
{claim['content_id']}

Status:
{badge}
""")

        st.write(
            claim["ownership_statement"]
        )

        st.divider()

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Empire of Continuum • Copyright Management"
)