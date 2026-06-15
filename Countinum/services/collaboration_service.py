from database.database import get_connection

# =====================================================
# PROJECT CATEGORIES
# =====================================================

PROJECT_CATEGORIES = [
    "Novel Project",
    "Comic Project",
    "Shared Universe",
    "Worldbuilding Initiative",
    "Lore Development",
    "Character Development",
    "Artwork Collaboration",
    "Timeline Expansion",
    "Wiki Development",
    "Community Event"
]


def get_project_categories():
    return PROJECT_CATEGORIES


# =====================================================
# PROJECT CREATION
# =====================================================

def create_project(
    title,
    creator_id,
    category,
    description,
    recruitment_open=True
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO collaboration_projects (
        title,
        creator_id,
        category,
        description,
        recruitment_open
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        title,
        creator_id,
        category,
        description,
        1 if recruitment_open else 0
    ))

    project_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO project_members (
        project_id,
        user_id,
        role
    )
    VALUES (?, ?, ?)
    """,
    (
        project_id,
        creator_id,
        "Project Owner"
    ))

    conn.commit()
    conn.close()

    return project_id


# =====================================================
# PROJECT LOOKUP
# =====================================================

def get_project(project_id):

    conn = get_connection()

    project = conn.execute("""
    SELECT
        p.*,
        u.username AS creator_name
    FROM collaboration_projects p
    LEFT JOIN users u
        ON p.creator_id = u.id
    WHERE p.id = ?
    """,
    (project_id,)
    ).fetchone()

    conn.close()

    if project:
        return dict(project)

    return None


# =====================================================
# PROJECT LISTS
# =====================================================

def get_projects(limit=100):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        p.*,
        u.username AS creator_name
    FROM collaboration_projects p
    LEFT JOIN users u
        ON p.creator_id=u.id
    ORDER BY p.id DESC
    LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return rows


def get_open_projects(limit=100):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        p.*,
        u.username AS creator_name
    FROM collaboration_projects p
    LEFT JOIN users u
        ON p.creator_id=u.id
    WHERE recruitment_open = 1
    ORDER BY p.id DESC
    LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return rows


# =====================================================
# SEARCH
# =====================================================

def search_projects(search_term):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        p.*,
        u.username AS creator_name
    FROM collaboration_projects p
    LEFT JOIN users u
        ON p.creator_id=u.id
    WHERE
        p.title LIKE ?
        OR p.description LIKE ?
    ORDER BY p.id DESC
    """,
    (
        f"%{search_term}%",
        f"%{search_term}%"
    )
    ).fetchall()

    conn.close()

    return rows


# =====================================================
# JOIN REQUESTS
# =====================================================

def submit_join_request(
    project_id,
    user_id,
    message
):

    conn = get_connection()

    existing = conn.execute("""
    SELECT id
    FROM project_join_requests
    WHERE
        project_id = ?
        AND user_id = ?
        AND status = 'pending'
    """,
    (
        project_id,
        user_id
    )
    ).fetchone()

    if existing:
        conn.close()
        return False

    conn.execute("""
    INSERT INTO project_join_requests (
        project_id,
        user_id,
        message,
        status
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        project_id,
        user_id,
        message,
        "pending"
    ))

    conn.commit()
    conn.close()

    return True


# =====================================================
# APPROVE REQUEST
# =====================================================

def approve_join_request(request_id):

    conn = get_connection()

    request = conn.execute("""
    SELECT *
    FROM project_join_requests
    WHERE id = ?
    """,
    (request_id,)
    ).fetchone()

    if not request:
        conn.close()
        return False

    conn.execute("""
    UPDATE project_join_requests
    SET status='approved'
    WHERE id=?
    """,
    (request_id,)
    )

    conn.execute("""
    INSERT INTO project_members(
        project_id,
        user_id,
        role
    )
    VALUES (?, ?, ?)
    """,
    (
        request["project_id"],
        request["user_id"],
        "Contributor"
    ))

    conn.commit()
    conn.close()

    return True


# =====================================================
# REJECT REQUEST
# =====================================================

def reject_join_request(request_id):

    conn = get_connection()

    conn.execute("""
    UPDATE project_join_requests
    SET status='rejected'
    WHERE id=?
    """,
    (request_id,)
    )

    conn.commit()
    conn.close()

    return True


# =====================================================
# MEMBERS
# =====================================================

def get_project_members(project_id):

    conn = get_connection()

    members = conn.execute("""
    SELECT
        pm.*,
        u.username
    FROM project_members pm
    LEFT JOIN users u
        ON pm.user_id=u.id
    WHERE pm.project_id=?
    ORDER BY pm.id ASC
    """,
    (project_id,)
    ).fetchall()

    conn.close()

    return members


# =====================================================
# JOIN REQUESTS
# =====================================================

def get_project_requests(project_id):

    conn = get_connection()

    requests = conn.execute("""
    SELECT
        r.*,
        u.username
    FROM project_join_requests r
    LEFT JOIN users u
        ON r.user_id=u.id
    WHERE r.project_id=?
    ORDER BY r.id DESC
    """,
    (project_id,)
    ).fetchall()

    conn.close()

    return requests


# =====================================================
# USER PROJECTS
# =====================================================

def get_user_projects(user_id):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        p.*
    FROM collaboration_projects p
    INNER JOIN project_members pm
        ON p.id = pm.project_id
    WHERE pm.user_id = ?
    ORDER BY p.id DESC
    """,
    (user_id,)
    ).fetchall()

    conn.close()

    return rows


# =====================================================
# PROJECT UPDATE
# =====================================================

def update_project(
    project_id,
    title,
    category,
    description,
    recruitment_open
):

    conn = get_connection()

    conn.execute("""
    UPDATE collaboration_projects
    SET
        title=?,
        category=?,
        description=?,
        recruitment_open=?
    WHERE id=?
    """,
    (
        title,
        category,
        description,
        1 if recruitment_open else 0,
        project_id
    ))

    conn.commit()
    conn.close()

    return True


# =====================================================
# DELETE PROJECT
# =====================================================

def delete_project(project_id):

    conn = get_connection()

    conn.execute("""
    DELETE FROM collaboration_projects
    WHERE id=?
    """,
    (project_id,)
    )

    conn.execute("""
    DELETE FROM project_members
    WHERE project_id=?
    """,
    (project_id,)
    )

    conn.execute("""
    DELETE FROM project_join_requests
    WHERE project_id=?
    """,
    (project_id,)
    )

    conn.commit()
    conn.close()

    return True


# =====================================================
# STATS
# =====================================================

def get_collaboration_stats():

    conn = get_connection()

    total_projects = conn.execute("""
    SELECT COUNT(*) AS total
    FROM collaboration_projects
    """).fetchone()["total"]

    open_projects = conn.execute("""
    SELECT COUNT(*) AS total
    FROM collaboration_projects
    WHERE recruitment_open=1
    """).fetchone()["total"]

    total_members = conn.execute("""
    SELECT COUNT(*) AS total
    FROM project_members
    """).fetchone()["total"]

    pending_requests = conn.execute("""
    SELECT COUNT(*) AS total
    FROM project_join_requests
    WHERE status='pending'
    """).fetchone()["total"]

    conn.close()

    return {
        "total_projects": total_projects,
        "open_projects": open_projects,
        "total_members": total_members,
        "pending_requests": pending_requests
    }