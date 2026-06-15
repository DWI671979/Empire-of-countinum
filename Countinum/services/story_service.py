
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

    try:
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
    except Exception:
        pass

    conn.commit()
    conn.close()

    return story_id


# =====================================================
# GET STORY
# =====================================================

def get_story(story_id):

    conn = get_connection()

    row = conn.execute("""
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

    if row:
        return dict(row)

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
        title=?,
        category=?,
        content=?
    WHERE id=?
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

    conn.execute(
        "DELETE FROM stories WHERE id=?",
        (story_id,)
    )

    try:
        conn.execute(
            "DELETE FROM story_likes WHERE story_id=?",
            (story_id,)
        )
    except Exception:
        pass

    try:
        conn.execute(
            "DELETE FROM story_comments WHERE story_id=?",
            (story_id,)
        )
    except Exception:
        pass

    conn.commit()
    conn.close()

    return True


# =====================================================
# APPROVAL
# =====================================================

def approve_story(story_id):

    conn = get_connection()

    conn.execute("""
    UPDATE stories
    SET status='approved'
    WHERE id=?
    """,
    (story_id,)
    )

    conn.commit()
    conn.close()

    return True


def reject_story(story_id):

    conn = get_connection()

    conn.execute("""
    UPDATE stories
    SET status='rejected'
    WHERE id=?
    """,
    (story_id,)
    )

    conn.commit()
    conn.close()

    return True


# =====================================================
# STORY LISTS
# =====================================================

def get_approved_stories(limit=100):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        s.*,
        u.username AS author_name
    FROM stories s
    LEFT JOIN users u
        ON s.author_id=u.id
    WHERE s.status='approved'
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
        s.*,
        u.username AS author_name
    FROM stories s
    LEFT JOIN users u
        ON s.author_id=u.id
    WHERE s.status='pending'
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
    WHERE author_id=?
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
            s.*,
            u.username AS author_name
        FROM stories s
        LEFT JOIN users u
            ON s.author_id=u.id
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
            s.*,
            u.username AS author_name
        FROM stories s
        LEFT JOIN users u
            ON s.author_id=u.id
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
# CATEGORY FILTER
# =====================================================

def get_stories_by_category(category):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        s.*,
        u.username AS author_name
    FROM stories s
    LEFT JOIN users u
        ON s.author_id=u.id
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

def increment_story_view(story_id):

    conn = get_connection()

    conn.execute("""
    UPDATE stories
    SET views = COALESCE(views,0) + 1
    WHERE id=?
    """,
    (story_id,)
    )

    conn.commit()
    conn.close()


# =====================================================
# LIKES
# =====================================================

def like_story(
    user_id,
    story_id
):

    conn = get_connection()

    try:

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
        SET likes = COALESCE(likes,0) + 1
        WHERE id=?
        """,
        (story_id,)
        )

        conn.commit()

    except Exception:
        conn.close()
        return False

    conn.close()

    return True


# =====================================================
# COMMENTS
# =====================================================

def add_story_comment(
    story_id,
    user_id,
    comment
):

    conn = get_connection()

    conn.execute("""
    INSERT INTO story_comments(
        story_id,
        user_id,
        comment
    )
    VALUES (?, ?, ?)
    """,
    (
        story_id,
        user_id,
        comment
    )
    )

    conn.commit()
    conn.close()

    return True


def get_story_comments(story_id):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        c.*,
        u.username
    FROM story_comments c
    LEFT JOIN users u
        ON c.user_id=u.id
    WHERE c.story_id=?
    ORDER BY c.id DESC
    """,
    (story_id,)
    ).fetchall()

    conn.close()

    return rows


# =====================================================
# BOOKMARKS
# =====================================================

def bookmark_story(
    user_id,
    story_id
):

    conn = get_connection()

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


# =====================================================
# STATISTICS
# =====================================================

def get_story_statistics():

    conn = get_connection()

    total_stories = conn.execute(
        "SELECT COUNT(*) AS total FROM stories"
    ).fetchone()["total"]

    approved_stories = conn.execute(
        "SELECT COUNT(*) AS total FROM stories WHERE status='approved'"
    ).fetchone()["total"]

    pending_stories = conn.execute(
        "SELECT COUNT(*) AS total FROM stories WHERE status='pending'"
    ).fetchone()["total"]

    total_views = conn.execute("""
    SELECT COALESCE(SUM(views),0) AS total
    FROM stories
    """).fetchone()["total"]

    total_likes = conn.execute("""
    SELECT COALESCE(SUM(likes),0) AS total
    FROM stories
    """).fetchone()["total"]

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

def get_most_liked_stories(limit=10):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        s.*,
        u.username AS author_name
    FROM stories s
    LEFT JOIN users u
        ON s.author_id=u.id
    WHERE s.status='approved'
    ORDER BY likes DESC
    LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return rows


def get_most_viewed_stories(limit=10):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        s.*,
        u.username AS author_name
    FROM stories s
    LEFT JOIN users u
        ON s.author_id=u.id
    WHERE s.status='approved'
    ORDER BY views DESC
    LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return rows

