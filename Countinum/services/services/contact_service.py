from database.database import get_connection


# =====================================================
# CREATE MESSAGE
# =====================================================

def create_contact_message(
    sender_id,
    subject,
    message
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO contact_messages (
        sender_id,
        subject,
        message,
        status
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        sender_id,
        subject,
        message,
        "open"
    ))

    message_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return message_id


# =====================================================
# GET MESSAGE
# =====================================================

def get_contact_message(message_id):

    conn = get_connection()

    row = conn.execute("""
    SELECT
        c.*,
        u.username
    FROM contact_messages c
    LEFT JOIN users u
        ON c.sender_id=u.id
    WHERE c.id=?
    """,
    (message_id,)
    ).fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


# =====================================================
# USER MESSAGES
# =====================================================

def get_user_messages(user_id):

    conn = get_connection()

    rows = conn.execute("""
    SELECT *
    FROM contact_messages
    WHERE sender_id=?
    ORDER BY id DESC
    """,
    (user_id,)
    ).fetchall()

    conn.close()

    return rows


# =====================================================
# ALL MESSAGES
# =====================================================

def get_all_messages():

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        c.*,
        u.username
    FROM contact_messages c
    LEFT JOIN users u
        ON c.sender_id=u.id
    ORDER BY c.id DESC
    """).fetchall()

    conn.close()

    return rows


# =====================================================
# UPDATE STATUS
# =====================================================

def update_message_status(
    message_id,
    status
):

    conn = get_connection()

    conn.execute("""
    UPDATE contact_messages
    SET status=?
    WHERE id=?
    """,
    (
        status,
        message_id
    ))

    conn.commit()
    conn.close()

    return True


# =====================================================
# SEARCH
# =====================================================

def search_messages(search_term):

    conn = get_connection()

    rows = conn.execute("""
    SELECT *
    FROM contact_messages
    WHERE
        subject LIKE ?
        OR message LIKE ?
    ORDER BY id DESC
    """,
    (
        f"%{search_term}%",
        f"%{search_term}%"
    )
    ).fetchall()

    conn.close()

    return rows


# =====================================================
# STATISTICS
# =====================================================

def get_contact_statistics():

    conn = get_connection()

    total = conn.execute("""
    SELECT COUNT(*) AS total
    FROM contact_messages
    """).fetchone()["total"]

    open_count = conn.execute("""
    SELECT COUNT(*) AS total
    FROM contact_messages
    WHERE status='open'
    """).fetchone()["total"]

    in_progress = conn.execute("""
    SELECT COUNT(*) AS total
    FROM contact_messages
    WHERE status='in_progress'
    """).fetchone()["total"]

    closed = conn.execute("""
    SELECT COUNT(*) AS total
    FROM contact_messages
    WHERE status='closed'
    """).fetchone()["total"]

    conn.close()

    return {
        "total": total,
        "open": open_count,
        "in_progress": in_progress,
        "closed": closed
    }


# =====================================================
# CONTACT CATEGORIES
# =====================================================

def get_contact_categories():

    return [
        "General Support",
        "Moderation Appeal",
        "Copyright Issue",
        "Canon Review Request",
        "Continuity Question",
        "Bug Report",
        "Technical Support",
        "Account Problem",
        "Content Report",
        "Other"
    ]