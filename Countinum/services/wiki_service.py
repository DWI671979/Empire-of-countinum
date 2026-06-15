from database.database import get_connection

# =====================================================
# ARTICLE TYPES
# =====================================================

ARTICLE_TYPES = [
    "Character",
    "Location",
    "Faction",
    "Organization",
    "Technology",
    "Species",
    "Historical Event",
    "Lore Article",
    "Timeline Entry",
    "Continuity Document"
]


def get_article_types():
    return ARTICLE_TYPES


# =====================================================
# CREATE ARTICLE
# =====================================================

def create_article(
    title,
    article_type,
    content,
    author_id,
    canon_status="non-canon"
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO wiki_articles (
        title,
        article_type,
        content,
        author_id,
        canon_status
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        title,
        article_type,
        content,
        author_id,
        canon_status
    ))

    article_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO moderation_queue(
        content_type,
        content_id,
        submitted_by
    )
    VALUES (?, ?, ?)
    """,
    (
        "wiki",
        article_id,
        author_id
    ))

    conn.commit()
    conn.close()

    return article_id


# =====================================================
# GET ARTICLE
# =====================================================

def get_article(article_id):

    conn = get_connection()

    article = conn.execute("""
    SELECT
        w.*,
        u.username AS author_name
    FROM wiki_articles w
    LEFT JOIN users u
        ON w.author_id=u.id
    WHERE w.id=?
    """,
    (article_id,)
    ).fetchone()

    conn.close()

    if article:
        return dict(article)

    return None


# =====================================================
# LIST ARTICLES
# =====================================================

def get_articles(limit=500):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        w.id,
        w.title,
        w.article_type,
        w.canon_status,
        w.views,
        u.username AS author_name
    FROM wiki_articles w
    LEFT JOIN users u
        ON w.author_id=u.id
    ORDER BY w.title ASC
    LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return rows


# =====================================================
# ARTICLE BY TYPE
# =====================================================

def get_articles_by_type(article_type):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        w.id,
        w.title,
        w.article_type,
        w.canon_status,
        u.username AS author_name
    FROM wiki_articles w
    LEFT JOIN users u
        ON w.author_id=u.id
    WHERE article_type=?
    ORDER BY title ASC
    """,
    (article_type,)
    ).fetchall()

    conn.close()

    return rows


# =====================================================
# SEARCH
# =====================================================

def search_articles(search_term):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        w.id,
        w.title,
        w.article_type,
        w.canon_status,
        u.username AS author_name
    FROM wiki_articles w
    LEFT JOIN users u
        ON w.author_id=u.id
    WHERE
        w.title LIKE ?
        OR w.content LIKE ?
    ORDER BY w.title ASC
    """,
    (
        f"%{search_term}%",
        f"%{search_term}%"
    )
    ).fetchall()

    conn.close()

    return rows


# =====================================================
# ARTICLE UPDATE
# =====================================================

def update_article(
    article_id,
    title,
    article_type,
    content,
    canon_status
):

    conn = get_connection()

    conn.execute("""
    UPDATE wiki_articles
    SET
        title=?,
        article_type=?,
        content=?,
        canon_status=?
    WHERE id=?
    """,
    (
        title,
        article_type,
        content,
        canon_status,
        article_id
    ))

    conn.commit()
    conn.close()

    return True


# =====================================================
# ARTICLE DELETE
# =====================================================

def delete_article(article_id):

    conn = get_connection()

    conn.execute("""
    DELETE FROM wiki_articles
    WHERE id=?
    """,
    (article_id,)
    )

    conn.commit()
    conn.close()

    return True


# =====================================================
# VIEWS
# =====================================================

def increment_article_view(article_id):

    conn = get_connection()

    conn.execute("""
    UPDATE wiki_articles
    SET views = views + 1
    WHERE id=?
    """,
    (article_id,)
    )

    conn.commit()
    conn.close()


# =====================================================
# CANON MANAGEMENT
# =====================================================

def set_canon_status(
    article_id,
    status
):

    conn = get_connection()

    conn.execute("""
    UPDATE wiki_articles
    SET canon_status=?
    WHERE id=?
    """,
    (
        status,
        article_id
    ))

    conn.commit()
    conn.close()


# =====================================================
# ARTICLE COUNTS
# =====================================================

def get_wiki_statistics():

    conn = get_connection()

    total_articles = conn.execute("""
    SELECT COUNT(*) AS total
    FROM wiki_articles
    """).fetchone()["total"]

    canon_articles = conn.execute("""
    SELECT COUNT(*) AS total
    FROM wiki_articles
    WHERE canon_status='canon'
    """).fetchone()["total"]

    noncanon_articles = conn.execute("""
    SELECT COUNT(*) AS total
    FROM wiki_articles
    WHERE canon_status='non-canon'
    """).fetchone()["total"]

    total_views = conn.execute("""
    SELECT COALESCE(SUM(views),0)
    AS total
    FROM wiki_articles
    """).fetchone()["total"]

    conn.close()

    return {
        "total_articles": total_articles,
        "canon_articles": canon_articles,
        "noncanon_articles": noncanon_articles,
        "total_views": total_views
    }


# =====================================================
# TIMELINE EVENTS
# =====================================================

def create_timeline_event(
    event_title,
    event_date,
    era,
    description,
    canon_status="canon"
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO timeline_events (
        event_title,
        event_date,
        era,
        description,
        canon_status
    )
    VALUES (?, ?, ?, ?, ?)
    """,
    (
        event_title,
        event_date,
        era,
        description,
        canon_status
    ))

    event_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return event_id


def get_timeline_events():

    conn = get_connection()

    rows = conn.execute("""
    SELECT *
    FROM timeline_events
    ORDER BY event_date ASC
    """).fetchall()

    conn.close()

    return rows


# =====================================================
# FEATURED ARTICLES
# =====================================================

def get_popular_articles(limit=10):

    conn = get_connection()

    rows = conn.execute("""
    SELECT
        id,
        title,
        article_type,
        canon_status,
        views
    FROM wiki_articles
    ORDER BY views DESC
    LIMIT ?
    """,
    (limit,)
    ).fetchall()

    conn.close()

    return rows