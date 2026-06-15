import bcrypt # type: ignore

from database.database import get_connection


def register_user(username, email, password):

    conn = get_connection()
    cursor = conn.cursor()

    existing = cursor.execute(
        "SELECT * FROM users WHERE email=? OR username=?",
        (email, username)
    ).fetchone()

    if existing:
        conn.close()
        return False, "User already exists"

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute("""
    INSERT INTO users
    (
        username,
        email,
        password_hash,
        role
    )
    VALUES
    (?, ?, ?, ?)
    """,
    (
        username,
        email,
        hashed_password,
        "creator"
    ))

    conn.commit()
    conn.close()

    return True, "Account created successfully"