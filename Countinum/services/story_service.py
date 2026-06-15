from sqlite3 import Cursor
from tkinter import _Cursor

from database.database import get_connection


# =====================================================
# STORY CATEGORIES
# =====================================================

STORY_CATEGORIES = [
    "Novel",
    "Short Story",
    "Comic",
    "Lore Article",
    "Character Profile",
    "Worldbuilding Document"
]


def get_story_categories():
    return STORY_CATEGORIES


# =====================================================
# CREATE STORY
# =====================================================

def create_story(
    title,
    author_id,
    category,
    content
):
    """
    Submit a story for moderation.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO stories (
            title,
            author_id,
            category,
            content,
            status
        )
        VALUES (?, ?, ?, ?, ?)
    """,
    (
        title,
        author_id,
        category,
        content,
        "pending"
    ))

    story_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return story_id


# =====================================================
# GET STORY
# =====================================================

def get_story(story_id):

    conn = get_connection()

    story = conn.execute("""
        SELECT
            s.*,
            u.username AS author_name
        FROM stories s
        LEFT JOIN users u
            ON s.author_id = u.id
        WHERE s.id = ?
    """,
    (story_id,)
    ).fetchone()

    conn.close()

    if story:
        return dict(story)

    return None


# =====================================================
# UPDATE STORY
# =====================================================

def update_story(
    story_id,
    title,
    category,
    content
):

    conn = get_connection()

    conn.execute("""
        UPDATE stories
        SET
            title = ?,
            category = ?,
            content = ?
        WHERE id = ?
    """,
    (
        title,
        category,
        content,
        story_id
    ))

    conn.commit()
    conn.close()

    return True


# =====================================================
# DELETE STORY
# =====================================================

def delete_story(story_id):

    conn = get_connection()

    conn.execute("""
        DELETE FROM stories
        WHERE id = ?
    """,
    (story_id,)
    )

    conn.commit()
    conn.close()

    return True


# =====================================================
# PUBLISH / MODERATION
# =====================================================

def approve_story(story_id):

    conn = get_connection()

    conn.execute("""
        UPDATE stories
        SET status = 'approved'
        WHERE id = ?
    """,
    (story_id,)
    )

    conn.commit()
    conn.close()


def reject_story(story_id):

    conn = get_connection()

    conn.execute("""
        UPDATE stories
        SET status = 'rejected'
        WHERE id = ?
    """,
    (story_id,)
    )

    conn.commit()
    conn.close()


# =====================================================
# LIST STORIES
# =====================================================

def get_approved_stories(limit=100):

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            s.id,
            s.title,
            s.category,
            s.views,
            s.likes,
            s.created_at,
            u.username AS author_name
        FROM stories s
        LEFT JOIN users u
            ON s.author_id = u.id
        WHERE s.status = 'approved'
        ORDER BY s.id DESC
        LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return rows



def get_pending_stories(limit=100):

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            s.id,
            s.title,
            s.category,
            s.created_at,
            u.username AS author_name
        FROM stories s
        LEFT JOIN users u
            ON s.author_id = u.id
        WHERE s.status = 'pending'
        ORDER BY s.id DESC
        LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return rows


def get_user_stories(
    user_id,
    limit=100
):

    conn = get_connection()

    rows = conn.execute("""
        SELECT *
        FROM stories
        WHERE author_id = ?
        ORDER BY id DESC
        LIMIT ?
    """,
    (
        user_id,
        limit
    )
    ).fetchall()

    conn.close()

    return rows


# =====================================================
# SEARCH
# =====================================================

def search_stories(
    search_term,
    category=None
):

    conn = get_connection()

    if category and category != "All":

        rows = conn.execute("""
            SELECT
                s.id,
                s.title,
                s.category,
                s.likes,
                s.views,
                u.username AS author_name
            FROM stories s
            LEFT JOIN users u
                ON s.author_id = u.id
            WHERE
                s.status='approved'
                AND s.category=?
                AND (
                    s.title LIKE ?
                    OR s.content LIKE ?
                )
            ORDER BY s.id DESC
        """,
        (
            category,
            f"%{search_term}%",
            f"%{search_term}%"
        )
        ).fetchall()

    else:

        rows = conn.execute("""
            SELECT
                s.id,
                s.title,
                s.category,
                s.likes,
                s.views,
                u.username AS author_name
            FROM stories s
            LEFT JOIN users u
                ON s.author_id = u.id
            WHERE
                s.status='approved'
                AND (
                    s.title LIKE ?
                    OR s.content LIKE ?
                )
            ORDER BY s.id DESC
        """,
        (
            f"%{search_term}%",
            f"%{search_term}%"
        )
        ).fetchall()

    conn.close()

    return rows


# =====================================================
# FILTERS
# =====================================================

def get_stories_by_category(
    category
):

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            s.id,
            s.title,
            s.category,
            s.views,
            s.likes,
            u.username AS author_name
        FROM stories s
        LEFT JOIN users u
            ON s.author_id = u.id
        WHERE
            s.status='approved'
            AND s.category=?
        ORDER BY s.id DESC
    """,
    (category,)
    ).fetchall()

    conn.close()

    return rows


# =====================================================
# VIEWS
# =====================================================

def increment_story_view(
    story_id
):

    conn = get_connection()

    conn.execute("""
        UPDATE stories
        SET views = views + 1
        WHERE id = ?
    """,
    (story_id,)
    )

    conn.commit()
    conn.close()


# =====================================================
# BOOKMARKS
# =====================================================

def bookmark_story(
    user_id,
    story_id
):

    conn = get_connection()

    existing = conn.execute("""
        SELECT id
        FROM bookmarks
        WHERE
            user_id=?
            AND content_type='story'
            AND content_id=?
    """,
    (
        user_id,
        story_id
    )
    ).fetchone()

    if existing:
        conn.close()
        return False

    conn.execute("""
        INSERT INTO bookmarks(
            user_id,
            content_type,
            content_id
        )
        VALUES (?, ?, ?)
    """,
    (
        user_id,
        "story",
        story_id
    )
    )

    conn.commit()
    conn.close()

    return True


def remove_bookmark(
    user_id,
    story_id
):

    conn = get_connection()

    conn.execute("""
        DELETE FROM bookmarks
        WHERE
            user_id=?
            AND content_type='story'
            AND content_id=?
    """,
    (
        user_id,
        story_id
    )
    )

    conn.commit()
    conn.close()

    return True


# =====================================================
# LIKES
# =====================================================

def like_story(
    user_id,
    story_id
):
    """
    Simple implementation.
    Prevents duplicate likes.
    """

    conn = get_connection()

    existing = conn.execute("""
        SELECT id
        FROM story_likes
        WHERE user_id=?
        AND story_id=?
    """,
    (
        user_id,
        story_id
    )
    ).fetchone()

    if existing:
        conn.close()
        return False

    conn.execute("""
        INSERT INTO story_likes(
            user_id,
            story_id
        )
        VALUES (?, ?)
    """,
    (
        user_id,
        story_id
    )
    )

    conn.execute("""
        UPDATE stories
        SET likes = likes + 1
        WHERE id = ?
    """,
    (story_id,)
    )
_Cursor.execute("""
INSERT INTO moderation_queue (
    content_type,
    content_id,
    submitted_by
)
VALUES (?, ?, ?)
""",
(
    "story",
    story_id,
    author_id
))
Cursor.execute("""
INSERT INTO moderation_queue (
    content_type,
    content_id,
    submitted_by
)
VALUES (?, ?, ?)
""",
(
    "story",
    story_id,
    author_id
)
cursor.execute("""
INSERT INTO moderation_queue (
    content_type,
    content_id,
    submitted_by
)
VALUES (?, ?, ?)
""",
(
    "story",
    story_id,
    author_id
)
cursor.execute("""
INSERT INTO moderation_queue (
    content_type,
    content_id,
    submitted_by
)
VALUES (?, ?, ?)
""",
(
    "story",
    story_id,
    author_id
)
    conn.commit()
    conn.close()

    return True


# =====================================================
# STATISTICS
# =====================================================

def get_story_statistics():

    conn = get_connection()

    total_stories = conn.execute("""
        SELECT COUNT(*) AS total
        FROM stories
    """).fetchone()["total"]

    approved_stories = conn.execute("""
        SELECT COUNT(*) AS total
        FROM stories
        WHERE status='approved'
    """).fetchone()["total"]

    pending_stories = conn.execute("""
        SELECT COUNT(*) AS total
        FROM stories
        WHERE status='pending'
    """).fetchone()["total"]

    total_views = conn.execute("""
        SELECT COALESCE(SUM(views),0)
        AS total
        FROM stories
    """).fetchone()["total"]

    total_likes = conn.execute("""
        SELECT COALESCE(SUM(likes),0)
        AS total
        FROM stories
    """).fetchone()["total"]
cursor.execute("""
INSERT INTO moderation_queue (
    content_type,
    content_id,
    submitted_by
)
VALUES (?, ?, ?)
""",
(
    "story",
    story_id,
    author_id
))

    conn.close()

    return {
        "total_stories": total_stories,
        "approved_stories": approved_stories,
        "pending_stories": pending_stories,
        "total_views": total_views,
        "total_likes": total_likes
    }


# =====================================================
# FEATURED STORIES
# =====================================================

def get_most_liked_stories(
    limit=10
):

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            s.id,
            s.title,
            s.likes,
            s.views,
            u.username AS author_name
        FROM stories s
        LEFT JOIN users u
            ON s.author_id=u.id
        WHERE s.status='approved'
        ORDER BY s.likes DESC
        LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return rows


def get_most_viewed_stories(
    limit=10
):

    conn = get_connection()

    rows = conn.execute("""
        SELECT
            s.id,
            s.title,
            s.likes,
            s.views,
            u.username AS author_name
        FROM stories s
        LEFT JOIN users u
            ON s.author_id=u.id
        WHERE s.status='approved'
        ORDER BY s.views DESC
        LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return rows