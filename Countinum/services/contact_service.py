from database.database import get_connection


# =====================================================
# SUBMIT CONTACT MESSAGE
# =====================================================

def submit_message(sender_id, subject, message):

    conn = get_connection()

    conn.execute("""
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

    conn.commit()
    conn.close()

    return True


# =====================================================
# GET ALL MESSAGES (for continuity managers / admins)
# =====================================================

def get_all_messages():

    conn = get_connection()

    messages = conn.execute("""
    SELECT
        cm.*,
        u.username AS sender_name
    FROM contact_messages cm
    LEFT JOIN users u
        ON cm.sender_id = u.id
    ORDER BY cm.id DESC
    """).fetchall()

    conn.close()

    return messages


# =====================================================
# GET MESSAGES BY USER
# =====================================================

def get_user_messages(user_id):

    conn = get_connection()

    messages = conn.execute("""
    SELECT *
    FROM contact_messages
    WHERE sender_id = ?
    ORDER BY id DESC
    """,
    (user_id,)
    ).fetchall()

    conn.close()

    return messages


# =====================================================
# UPDATE MESSAGE STATUS
# =====================================================

def update_message_status(message_id, status):

    conn = get_connection()

    conn.execute("""
    UPDATE contact_messages
    SET status = ?
    WHERE id = ?
    """,
    (
        status,
        message_id
    ))

    conn.commit()
    conn.close()

    return True


# =====================================================
# GET OPEN MESSAGE COUNT
# =====================================================

def get_open_message_count():

    conn = get_connection()

    count = conn.execute("""
    SELECT COUNT(*) AS total
    FROM contact_messages
    WHERE status = 'open'
    """).fetchone()["total"]

    conn.close()

    return count
