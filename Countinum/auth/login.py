import bcrypt  # ✅ FIX 3: Added missing import

from database.database import get_connection


def authenticate_user(email, password):

    conn = get_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    ).fetchone()

    conn.close()

    if not user:
        return None

    if bcrypt.checkpw(
        password.encode(),
        user["password_hash"].encode()
    ):
        return user

    return None
