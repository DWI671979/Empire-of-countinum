from database.database import get_connection

# =====================================================
# CREATE CLAIM
# =====================================================

def create_copyright_claim(
    claimant_id,
    content_type,
    content_id,
    ownership_statement,
    evidence_path=""
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO copyright_claims (
        claimant_id,
        content_type,
        content_id,
        ownership_statement,
        evidence_path,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        claimant_id,
        content_type,
        content_id,
        ownership_statement,
        evidence_path,
        "pending"
    ))

    claim_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return claim_id


# =====================================================
# GET CLAIM
# =====================================================

def get_claim(claim_id):

    conn = get_connection()

    claim = conn.execute("""
    SELECT
        c.*,
        u.username
    FROM copyright_claims c
    LEFT JOIN users u
        ON c.claimant_id=u.id
    WHERE c.id=?
    """,
    (claim_id,)
    ).fetchone()

    conn.close()

    if claim:
        return dict(claim)

    return None


# =====================================================
# USER CLAIMS
# =====================================================

def get_user_claims(user_id):

    conn = get_connection()

    rows = conn.execute("""
    SELECT *
    FROM copyright_claims
    WHERE claimant_id=?
    ORDER BY id DESC
    """,
    (user_id,)
    ).fetchall()

    conn.close()

    return rows


# =====================================================
# ALL CLAIMS
# =====================================================

def get_all_claims():

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        c.*,
        u.username
    FROM copyright_claims c
    LEFT JOIN users u
        ON c.claimant_id=u.id
    ORDER BY c.id DESC
    """).fetchall()

    conn.close()

    return rows


# =====================================================
# STATUS UPDATE
# =====================================================

def update_claim_status(
    claim_id,
    status
):

    conn = get_connection()

    conn.execute("""
    UPDATE copyright_claims
    SET status=?
    WHERE id=?
    """,
    (
        status,
        claim_id
    ))

    conn.commit()
    conn.close()

    return True


# =====================================================
# SEARCH
# =====================================================

def search_claims(search_term):

    conn = get_connection()

    rows = conn.execute("""
    SELECT *
    FROM copyright_claims
    WHERE
        ownership_statement LIKE ?
        OR content_type LIKE ?
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

def get_copyright_statistics():

    conn = get_connection()

    total = conn.execute("""
    SELECT COUNT(*) AS total
    FROM copyright_claims
    """).fetchone()["total"]

    pending = conn.execute("""
    SELECT COUNT(*) AS total
    FROM copyright_claims
    WHERE status='pending'
    """).fetchone()["total"]

    approved = conn.execute("""
    SELECT COUNT(*) AS total
    FROM copyright_claims
    WHERE status='approved'
    """).fetchone()["total"]

    rejected = conn.execute("""
    SELECT COUNT(*) AS total
    FROM copyright_claims
    WHERE status='rejected'
    """).fetchone()["total"]

    conn.close()

    return {
        "total": total,
        "pending": pending,
        "approved": approved,
        "rejected": rejected
    }