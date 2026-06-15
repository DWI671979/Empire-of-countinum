
from database.database import get_connection


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================================
    # USERS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================================================
    # USER PROFILES
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        display_name TEXT,
        bio TEXT,
        avatar_path TEXT,
        website TEXT,
        social_links TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # =====================================================
    # STORIES
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        content TEXT NOT NULL,
        status TEXT DEFAULT 'pending',
        views INTEGER DEFAULT 0,
        likes INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(author_id) REFERENCES users(id)
    )
    """)

    # =====================================================
    # STORY LIKES
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS story_likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        story_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, story_id)
    )
    """)

    # =====================================================
    # STORY COMMENTS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS story_comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        comment TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================================================
    # ARTWORKS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artworks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist_id INTEGER NOT NULL,
        description TEXT,
        image_path TEXT,
        status TEXT DEFAULT 'pending',
        views INTEGER DEFAULT 0,
        likes INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(artist_id) REFERENCES users(id)
    )
    """)

    # =====================================================
    # ARTWORK COMMENTS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artwork_comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        artwork_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        comment TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================================================
    # WIKI ARTICLES
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wiki_articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        article_type TEXT NOT NULL,
        content TEXT NOT NULL,
        author_id INTEGER NOT NULL,
        canon_status TEXT DEFAULT 'non-canon',
        views INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(author_id) REFERENCES users(id)
    )
    """)

    # =====================================================
    # TIMELINE EVENTS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timeline_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_title TEXT NOT NULL,
        event_date TEXT,
        era TEXT,
        description TEXT,
        canon_status TEXT DEFAULT 'canon',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================================================
    # BOOKMARKS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        content_type TEXT NOT NULL,
        content_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================================================
    # COLLABORATION PROJECTS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS collaboration_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        owner_id INTEGER NOT NULL,
        status TEXT DEFAULT 'open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================================================
    # PROJECT MEMBERS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        role TEXT DEFAULT 'member'
    )
    """)

    # =====================================================
    # COPYRIGHT CLAIMS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS copyright_claims (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        claimant_id INTEGER NOT NULL,
        content_type TEXT NOT NULL,
        content_id INTEGER NOT NULL,
        ownership_statement TEXT NOT NULL,
        evidence_path TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================================================
    # CONTACT / SUPPORT
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        message TEXT NOT NULL,
        status TEXT DEFAULT 'open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================================================
    # MODERATION QUEUE
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS moderation_queue (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content_type TEXT NOT NULL,
        content_id INTEGER NOT NULL,
        submitted_by INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================================================
    # SITE ANNOUNCEMENTS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS announcements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        created_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Empire of Continuum database schema created successfully.")

