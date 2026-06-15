from errno import EEXIST
from http.client import CREATED
import os
import uuid
from pathlib import Path

from streamlit import table

from database.database import get_connection

# =====================================================
# CONFIGURATION
# =====================================================

UPLOAD_DIR = Path("uploads/artworks")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = [
    ".jpg",
    ".jpeg"
]

# =====================================================
# VALIDATION
# =====================================================

def is_valid_artwork(filename):

    if not filename:
        return False

    extension = Path(filename).suffix.lower()

    return extension in ALLOWED_EXTENSIONS


# =====================================================
# ARTWORK UPLOAD
# =====================================================

def save_artwork_file(uploaded_file):

    if uploaded_file is None:
        return None

    if not is_valid_artwork(uploaded_file.name):
        return None

    extension = Path(uploaded_file.name).suffix.lower()

    unique_name = (
        f"{uuid.uuid4().hex}{extension}"
    )

    save_path = UPLOAD_DIR / unique_name

    with open(save_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return str(save_path)


# =====================================================
# CREATE ARTWORK
# =====================================================

def create_artwork(
    title,
    artist_id,
    image_path
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO artworks (
        title,
        artist_id,
        image_path,
        status
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        title,
        artist_id,
        image_path,
        "pending"
    ))

    artwork_id = cursor.lastrowid

    # Add moderation entry

    cursor.execute("""
    INSERT INTO moderation_queue (
        content_type,
        content_id,
        submitted_by
    )
    VALUES (?, ?, ?)
    """,
    (
        "artwork",
        artwork_id,
        artist_id
    ))

    conn.commit()
    conn.close()

    return artwork_id


# =====================================================
# GET ARTWORK
# =====================================================

def get_artwork(artwork_id):

    conn = get_connection()

    artwork = conn.execute("""
    SELECT
        a.*,
        u.username AS artist_name
    FROM artworks a
    LEFT JOIN users u
        ON a.artist_id = u.id
    WHERE a.id = ?
    """,
    (artwork_id,)
    ).fetchone()

    conn.close()

    if artwork:
        return dict(artwork)

    return None


# =====================================================
# LIST APPROVED ARTWORK
# =====================================================

def get_approved_artworks(limit=100):

    conn = get_connection()

    artworks = conn.execute("""
    SELECT
        a.id,
        a.title,
        a.image_path,
        a.likes,
        a.views,
        a.created_at,
        u.username AS artist_name
    FROM artworks a
    LEFT JOIN users u
        ON a.artist_id = u.id
    WHERE a.status='approved'
    ORDER BY a.id DESC
    LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return artworks


# =====================================================
# USER ARTWORKS
# =====================================================

def get_user_artworks(
    artist_id,
    limit=100
):

    conn = get_connection()

    artworks = conn.execute("""
    SELECT *
    FROM artworks
    WHERE artist_id = ?
    ORDER BY id DESC
    LIMIT ?
    """,
    (
        artist_id,
        limit
    )
    ).fetchall()

    conn.close()

    return artworks


# =====================================================
# CATEGORY SEARCH
# =====================================================

def search_artworks(search_term):

    conn = get_connection()

    artworks = conn.execute("""
    SELECT
        a.id,
        a.title,
        a.image_path,
        a.likes,
        a.views,
        u.username AS artist_name
    FROM artworks a
    LEFT JOIN users u
        ON a.artist_id=u.id
    WHERE
        a.status='approved'
        AND a.title LIKE ?
    ORDER BY a.id DESC
    """,
    (
        f"%{search_term}%",
    )
    ).fetchall()

    conn.close()

    return artworks


# =====================================================
# APPROVAL
# =====================================================

def approve_artwork(artwork_id):

    conn = get_connection()

    conn.execute("""
    UPDATE artworks
    SET status='approved'
    WHERE id=?
    """,
    (artwork_id,)
    )

    conn.commit()
    conn.close()


def reject_artwork(artwork_id):

    conn = get_connection()

    conn.execute("""
    UPDATE artworks
    SET status='rejected'
    WHERE id=?
    """,
    (artwork_id,)
    )

    conn.commit()
    conn.close()


# =====================================================
# VIEWS
# =====================================================

def increment_artwork_view(
    artwork_id
):

    conn = get_connection()

    conn.execute("""
    UPDATE artworks
    SET views = views + 1
    WHERE id = ?
    """,
    (artwork_id,)
    )

    conn.commit()
    conn.close()


# =====================================================
# LIKES
# =====================================================

def like_artwork(
    user_id,
    artwork_id
):

    conn = get_connection()

    existing = conn.execute("""
    SELECT id
    FROM artwork_likes
    WHERE
        user_id=?
        AND artwork_id=?
    """,
    (
        user_id,
        artwork_id
    )
    ).fetchone()

    if existing:
        conn.close()
        return False

    conn.execute("""
    INSERT INTO artwork_likes(
        user_id,
        artwork_id
    )
    VALUES (?, ?)
    """,
    (
        user_id,
        artwork_id
    )
    )

    conn.execute("""
    UPDATE artworks
    SET likes = likes + 1
    WHERE id = ?
    """,
    (artwork_id,)
    )

    conn.commit()
    conn.close()

    return True


# =====================================================
# FEATURED ARTWORK
# =====================================================

def get_most_liked_artworks(
    limit=10
):

    conn = get_connection()

    artworks = conn.execute("""
    SELECT
        a.id,
        a.title,
        a.likes,
        a.views,
        u.username AS artist_name
    FROM artworks a
    LEFT JOIN users u
        ON a.artist_id=u.id
    WHERE a.status='approved'
    ORDER BY a.likes DESC
    LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return artworks


def get_most_viewed_artworks(
    limit=10
):

    conn = get_connection()

    artworks = conn.execute("""
    SELECT
        a.id,
        a.title,
        a.likes,
        a.views,
        u.username AS artist_name
    FROM artworks a
    LEFT JOIN users u
        ON a.artist_id=u.id
    WHERE a.status='approved'
    ORDER BY a.views DESC
    LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return artworks


# =====================================================
# DELETE
# =====================================================

def delete_artwork(artwork_id):

    artwork = get_artwork(artwork_id)

    if artwork:

        image_path = artwork["image_path"]

        if image_path and os.path.exists(image_path):
            os.remove(image_path)

    conn = get_connection()

    conn.execute("""
    DELETE FROM artworks
    WHERE id=?
    """,
    (artwork_id,)
    )

    conn.commit()
    conn.close()

    return True


# =====================================================
# STATISTICS
# =====================================================

def get_artwork_statistics():

    conn = get_connection()

    total_artworks = conn.execute("""
    SELECT COUNT(*)
    AS total
    FROM artworks
    """).fetchone()["total"]

    approved_artworks = conn.execute("""
    SELECT COUNT(*)
    AS total
    FROM artworks
    WHERE status='approved'
    """).fetchone()["total"]

    pending_artworks = conn.execute("""
    SELECT COUNT(*)
    AS total
    FROM artworks
    WHERE status='pending'
    """).fetchone()["total"]

    total_views = conn.execute("""
    SELECT COALESCE(
        SUM(views),0
    ) AS total
    FROM artworks
    """).fetchone()["total"]

    total_likes = conn.execute("""
    SELECT COALESCE(
        SUM(likes),0
    ) AS total
    FROM artworks
    """).fetchone()["total"]

    conn.close()

    return {
        "total_artworks": total_artworks,
        "approved_artworks": approved_artworks,
        "pending_artworks": pending_artworks,
        "total_views": total_views,
        "total_likes": total_likes
    }