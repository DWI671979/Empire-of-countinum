import streamlit as st

from services.collaboration_service import (
    create_project,
    get_projects,
    get_open_projects,
    search_projects,
    get_project,
    get_project_members,
    get_project_requests,
    get_user_projects,
    get_project_categories,
    submit_join_request,
    get_collaboration_stats
)

# =====================================================
# ACCESS CONTROL
# =====================================================

if not st.session_state.get("logged_in", False):
    st.warning(
        "Please login to access the Collaboration Hub."
    )
    st.stop()

# =====================================================
# SESSION STATE
# =====================================================

if "selected_project_id" not in st.session_state:
    st.session_state.selected_project_id = None

# =====================================================
# PAGE HEADER
# =====================================================

st.title("🤝 Collaboration Hub")

st.markdown("""
The heart of Empire of Continuum.

Build worlds together, recruit writers and artists,
create shared universes, and collaborate on stories,
comics, lore projects, and timeline expansions.
""")

st.divider()

# =====================================================
# STATISTICS
# =====================================================

stats = get_collaboration_stats()

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric(
        "Projects",
        stats["total_projects"]
    )

with s2:
    st.metric(
        "Open Recruitment",
        stats["open_projects"]
    )

with s3:
    st.metric(
        "Contributors",
        stats["total_members"]
    )

with s4:
    st.metric(
        "Pending Requests",
        stats["pending_requests"]
    )

st.divider()

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Browse Projects",
    "Create Project",
    "My Projects",
    "Open Recruitment"
])

# =====================================================
# BROWSE PROJECTS
# =====================================================

with tab1:

    st.subheader("🌎 Project Directory")

    search_term = st.text_input(
        "Search Projects"
    )

    if search_term:

        projects = search_projects(
            search_term
        )

    else:

        projects = get_projects()

    if not projects:

        st.info(
            "No projects available."
        )

    for project in projects:

        with st.container():

            st.markdown(f"""
            ### {project['title']}

            **Category:** {project['category']}

            **Creator:** {project['creator_name']}
            """)

            description = (
                project["description"][:250]
                + "..."
                if len(project["description"]) > 250
                else project["description"]
            )

            st.write(description)

            recruitment_status = (
                "🟢 Open"
                if project["recruitment_open"]
                else "🔴 Closed"
            )

            st.caption(
                f"Recruitment: {recruitment_status}"
            )

            if st.button(
                f"View Project #{project['id']}",
                key=f"view_{project['id']}"
            ):

                st.session_state.selected_project_id = (
                    project["id"]
                )

                st.rerun()

            st.divider()

# =====================================================
# CREATE PROJECT
# =====================================================

with tab2:

    st.subheader("🚀 Create New Project")

    title = st.text_input(
        "Project Title"
    )

    category = st.selectbox(
        "Category",
        get_project_categories()
    )

    description = st.text_area(
        "Project Description",
        height=250
    )

    recruitment_open = st.checkbox(
        "Open Recruitment",
        value=True
    )

    if st.button(
        "Create Project"
    ):

        if not title.strip():

            st.error(
                "Title required."
            )

        elif not description.strip():

            st.error(
                "Description required."
            )

        else:

            project_id = create_project(
                title=title,
                creator_id=st.session_state.user_id,
                category=category,
                description=description,
                recruitment_open=recruitment_open
            )

            st.success(
                f"""
                Project created successfully.

                Project ID:
                {project_id}
                """
            )

            st.balloons()

# =====================================================
# MY PROJECTS
# =====================================================

with tab3:

    st.subheader("📂 My Projects")

    my_projects = get_user_projects(
        st.session_state.user_id
    )

    if not my_projects:

        st.info(
            "You have not joined any projects."
        )

    for project in my_projects:

        st.markdown(f"""
        ### {project['title']}

        Category:
        {project['category']}
        """)

        st.write(
            project["description"]
        )

        st.divider()

# =====================================================
# OPEN RECRUITMENT
# =====================================================

with tab4:

    st.subheader(
        "🟢 Recruiting Projects"
    )

    open_projects = get_open_projects()

    if not open_projects:

        st.info(
            "No projects recruiting."
        )

    for project in open_projects:

        st.markdown(f"""
        ### {project['title']}

        **Category:** {project['category']}

        **Creator:** {project['creator_name']}
        """)

        st.write(
            project["description"]
        )

        if st.button(
            f"Join Request #{project['id']}",
            key=f"join_{project['id']}"
        ):

            st.session_state.selected_project_id = (
                project["id"]
            )

            st.rerun()

        st.divider()

# =====================================================
# PROJECT DETAIL VIEW
# =====================================================

if st.session_state.selected_project_id:

    st.divider()

    project = get_project(
        st.session_state.selected_project_id
    )

    if project:

        st.header(
            project["title"]
        )

        st.caption(
            f"Created by {project['creator_name']}"
        )

        st.markdown(
            f"""
            **Category:** {project['category']}
            """
        )

        st.write(
            project["description"]
        )

        st.divider()

        # ============================================
        # MEMBERS
        # ============================================

        st.subheader(
            "👥 Team Members"
        )

        members = get_project_members(
            project["id"]
        )

        if members:

            for member in members:

                st.write(
                    f"• {member['username']} "
                    f"({member['role']})"
                )

        else:

            st.info(
                "No members."
            )

        st.divider()

        # ============================================
        # JOIN REQUEST
        # ============================================

        if project["recruitment_open"]:

            st.subheader(
                "📝 Join Project"
            )

            join_message = st.text_area(
                "Introduce yourself"
            )

            if st.button(
                "Submit Join Request"
            ):

                success = submit_join_request(
                    project["id"],
                    st.session_state.user_id,
                    join_message
                )

                if success:

                    st.success(
                        "Request submitted."
                    )

                else:

                    st.warning(
                        "Request already exists."
                    )

        else:

            st.info(
                "Recruitment currently closed."
            )

        st.divider()

        # ============================================
        # OWNER TOOLS
        # ============================================

        if (
            project["creator_id"]
            == st.session_state.user_id
        ):

            st.subheader(
                "⚙ Project Management"
            )

            requests = get_project_requests(
                project["id"]
            )

            if requests:

                st.write(
                    f"{len(requests)} "
                    f"join requests found."
                )

                for request in requests:

                    status = request["status"]

                    st.markdown(f"""
                    **{request['username']}**

                    Status:
                    {status}

                    Message:
                    {request['message']}
                    """)

                    st.divider()

            else:

                st.info(
                    "No requests."
                )

        if st.button(
            "⬅ Close Project View"
        ):

            st.session_state.selected_project_id = None
            st.rerun()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("🤝 Collaboration Hub")

    st.write(
        f"Logged in as "
        f"**{st.session_state.username}**"
    )

    st.divider()

    st.markdown("""
### Project Types

- Shared Universes
- Novels
- Comics
- Lore Projects
- Artwork Projects
- Timeline Expansion
- Character Development
- Wiki Projects

### Workflow

Create Project
↓
Recruit Team
↓
Collaborate
↓
Publish
    """)

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Empire of Continuum • Collaboration Hub v1.0"
)