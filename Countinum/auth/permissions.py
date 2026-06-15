def is_logged_in(session_state):
    return session_state.get("logged_in", False)


def is_admin(session_state):
    return session_state.get("role") == "admin"


def is_moderator(session_state):
    return session_state.get("role") in ["admin", "moderator"]