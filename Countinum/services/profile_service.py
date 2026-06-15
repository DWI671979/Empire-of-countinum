from database.database import get_connection


# =====================================================
# PROFILE MANAGEMENT
# =====================================================

def get_profile(user_id):
    """
    Returns a user's profile.
    Creates a default profile if one does not exist.
    """

    conn = get_connection()

    profile = conn.execute("""
        SELECT *
        FROM profiles
        WHERE user_id = ?
    """, (user_id,)).fetchone()

    if profile:

        conn.close()
        return dict(profile)

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    if not user:
        conn.close()
        return None

    conn.execute("""
        INSERT INTO profiles (
            user_id,
            display_name,
            tagline,
            location,
            website,
            portfolio,
            bio
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
        user_id,
        user["username"],
        "",
        "",
        "",
        "",
        user["bio"] if "bio" in user.keys() else ""
    ))

    conn.commit()

    profile = conn.execute("""
        SELECT *
        FROM profiles
        WHERE user_id = ?
    """, (user_id,)).fetchone()

    conn.close()

    return dict(profile)


# =====================================================
# UPDATE PROFILE
# =====================================================

def update_profile(
    user_id,
    display_name,
    tagline,
    location,
    website,
    portfolio,
    bio
):
    """
    Updates profile details.
    """

    conn = get_connection()

    existing = conn.execute("""
        SELECT id
        FROM profiles
        WHERE user_id = ?
    """, (user_id,)).fetchone()

    if existing:

        conn.execute("""
            UPDATE profiles
            SET
                display_name = ?,
                tagline = ?,
                location = ?,
                website = ?,
                portfolio = ?,
                bio = ?
            WHERE user_id = ?
        """,
        (
            display_name,
            tagline,
            location,
            website,
            portfolio,
            bio,
            user_id
        ))

    else:

        conn.execute("""
            INSERT INTO profiles (
                user_id,
                display_name,
                tagline,
                location,
                website,
                portfolio,
                bio
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            display_name,
            tagline,
            location,
            website,
            portfolio,
            bio
        ))

    conn.commit()
    conn.close()

    return True


# =====================================================
# FOLLOWERS
# =====================================================

def follow_user(
    follower_id,
    following_id
):
    """
    Follow another creator.
    """

    if follower_id == following_id:
        return False

    conn = get_connection()

    exists = conn.execute("""
        SELECT id
        FROM followers
        WHERE follower_id = ?
        AND following_id = ?
    """,
    (
        follower_id,
        following_id
    )).fetchone()

    if exists:
        conn.close()
        return False

    conn.execute("""
        INSERT INTO followers (
            follower_id,
            following_id
        )
        VALUES (?, ?)
    """,
    (
        follower_id,
        following_id
    ))

    conn.commit()
    conn.close()

    return True


def unfollow_user(
    follower_id,
    following_id
):
    """
    Remove a follow relationship.
    """

    conn = get_connection()

    conn.execute("""
        DELETE FROM followers
        WHERE follower_id = ?
        AND following_id = ?
    """,
    (
        follower_id,
        following_id
    ))

    conn.commit()
    conn.close()

    return True


def get_follower_count(user_id):

    conn = get_connection()

    count = conn.execute("""
        SELECT COUNT(*) AS total
        FROM followers
        WHERE following_id = ?
    """, (user_id,)).fetchone()["total"]

    conn.close()

    return count


def get_following_count(user_id):

    conn = get_connection()

    count = conn.execute("""
        SELECT COUNT(*) AS total
        FROM followers
        WHERE follower_id = ?
    """, (user_id,)).fetchone()["total"]

    conn.close()

    return count


# =====================================================
# USER STATISTICS
# =====================================================

def get_user_statistics(user_id):
    """
    Returns creator statistics.
    """

    conn = get_connection()

    story_count = conn.execute("""
        SELECT COUNT(*) AS total
        FROM stories
        WHERE author_id = ?
    """, (user_id,)).fetchone()["total"]

    artwork_count = conn.execute("""
        SELECT COUNT(*) AS total
        FROM artworks
        WHERE artist_id = ?
    """, (user_id,)).fetchone()["total"]

    bookmark_count = conn.execute("""
        SELECT COUNT(*) AS total
        FROM bookmarks
        WHERE user_id = ?
    """, (user_id,)).fetchone()["total"]

    follower_count = conn.execute("""
        SELECT COUNT(*) AS total
        FROM followers
        WHERE following_id = ?
    """, (user_id,)).fetchone()["total"]

    conn.close()

    return {
        "stories": story_count,
        "artworks": artwork_count,
        "bookmarks": bookmark_count,
        "followers": follower_count
    }


# =====================================================
# USER CONTENT
# =====================================================

def get_user_stories(
    user_id,
    limit=25
):

    conn = get_connection()

    stories = conn.execute("""
        SELECT
            id,
            title,
            category,
            status,
            created_at
        FROM stories
        WHERE author_id = ?
        ORDER BY id DESC
        LIMIT ?
    """,
    (
        user_id,
        limit
    )).fetchall()

    conn.close()

    return stories


def get_user_artworks(
    user_id,
    limit=25
):

    conn = get_connection()

    artworks = conn.execute("""
        SELECT
            id,
            title,
            image_path,
            status,
            created_at
        FROM artworks
        WHERE artist_id = ?
        ORDER BY id DESC
        LIMIT ?
    """,
    (
        user_id,
        limit
    )).fetchall()

    conn.close()

    return artworks


# =====================================================
# CREATOR DIRECTORY
# =====================================================

def get_all_creators(limit=100):

    conn = get_connection()

    creators = conn.execute("""
        SELECT
            id,
            username,
            role,
            created_at
        FROM users
        ORDER BY username ASC
        LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    return creators


def search_creators(search_term):

    conn = get_connection()

    creators = conn.execute("""
        SELECT
            id,
            username,
            role
        FROM users
        WHERE username LIKE ?
        ORDER BY username ASC
    """,
    (
        f"%{search_term}%",
    )).fetchall()

    conn.close()

    return creators


# =====================================================
# NOTIFICATIONS
# =====================================================

def create_notification(
    user_id,
    title,
    message
):

    conn = get_connection()

    conn.execute("""
        INSERT INTO notifications (
            user_id,
            title,
            message
        )
        VALUES (?, ?, ?)
    """,
    (
        user_id,
        title,
        message
    ))

    conn.commit()
    conn.close()


def get_notifications(
    user_id,
    limit=20
):

    conn = get_connection()

    notifications = conn.execute("""
        SELECT *
        FROM notifications
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """,
    (
        user_id,
        limit
    )).fetchall()

    conn.close()

    return notifications


def mark_notification_read(notification_id):

    conn = get_connection()

    conn.execute("""
        UPDATE notifications
        SET read_status = 1
        WHERE id = ?
    """, (notification_id,))

    conn.commit()
    conn.close()


# =====================================================
# PUBLIC PROFILE LOOKUP
# =====================================================

def get_creator_by_id(user_id):

    conn = get_connection()

    creator = conn.execute("""
        SELECT
            id,
            username,
            email,
            role,
            created_at
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    conn.close()

    if creator:
        return dict(creator)

    return None