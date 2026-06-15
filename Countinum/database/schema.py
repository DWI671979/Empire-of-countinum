from database.database import get_connection


def initialize_database():

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
        role TEXT DEFAULT 'member',
        bio TEXT DEFAULT '',
        avatar TEXT DEFAULT '',
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
        tagline TEXT,
        location TEXT,
        website TEXT,
        portfolio TEXT,
        bio TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
        category TEXT,
        content TEXT,
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
        UNIQUE(user_id, story_id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(story_id) REFERENCES stories(id)
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(story_id) REFERENCES stories(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
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
        image_path TEXT NOT NULL,
        likes INTEGER DEFAULT 0,
        views INTEGER DEFAULT 0,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(artist_id) REFERENCES users(id)
    )
    """)

    # =====================================================
    # ARTWORK LIKES
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artwork_likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        artwork_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, artwork_id),
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(artwork_id) REFERENCES artworks(id)
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(artwork_id) REFERENCES artworks(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # =====================================================
    # FOLLOWERS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        follower_id INTEGER NOT NULL,
        following_id INTEGER NOT NULL,
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, content_type, content_id)
    )
    """)

    # =====================================================
    # NOTIFICATIONS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT,
        message TEXT,
        read_status INTEGER DEFAULT 0,
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
        submitted_by INTEGER,
        status TEXT DEFAULT 'pending',
        moderator_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        reviewed_at TIMESTAMP
    )
    """)

    # =====================================================
    # COPYRIGHT CLAIMS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS copyright_claims (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        claimant_id INTEGER,
        content_type TEXT,
        content_id INTEGER,
        ownership_statement TEXT,
        evidence_path TEXT,
        status TEXT DEFAULT 'pending',
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
        creator_id INTEGER NOT NULL,
        category TEXT,
        description TEXT,
        recruitment_open INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(creator_id) REFERENCES users(id)
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
        role TEXT DEFAULT 'Contributor',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(project_id) REFERENCES collaboration_projects(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # =====================================================
    # PROJECT JOIN REQUESTS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project_join_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        message TEXT,
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(project_id) REFERENCES collaboration_projects(id),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    # =====================================================
    # CONTINUITY WIKI ARTICLES
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wiki_articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        article_type TEXT,
        content TEXT,
        author_id INTEGER,
        canon_status TEXT DEFAULT 'non-canon',
        views INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    # CONTACT MESSAGES
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contact_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER,
        subject TEXT,
        message TEXT,
        status TEXT DEFAULT 'open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =====================================================
    # CONTINUITY TEAM MEMBERS
    # =====================================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS continuity_team (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        position TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()