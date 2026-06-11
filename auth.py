import hashlib
import re
import streamlit as st
import database

def hash_password(password, username):
    """
    Hashes a password using SHA-256 with the username as a salt.
    This provides protection against pre-computed rainbow table attacks.
    """
    salt = username.lower().strip()
    salted_pwd = password + salt
    return hashlib.sha256(salted_pwd.encode()).hexdigest()

def validate_username(username):
    """Validates that a username is alphanumeric and between 3-20 characters."""
    username = username.strip()
    if not username:
        return False, "Username cannot be empty."
    if not re.match("^[a-zA-Z0-9_]{3,20}$", username):
        return False, "Username must be 3-20 characters long and contain only letters, numbers, or underscores."
    return True, ""

def validate_email(email):
    """Validates that an email matches standard email formats."""
    email = email.strip()
    if not email:
        return False, "Email cannot be empty."
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return False, "Please enter a valid email address."
    return True, ""

def register_user(username, email, password, bio="", profile_pic=""):
    """
    Registers a new user by validating details, hashing the password,
    and committing to the SQLite database.
    """
    # Validation
    is_valid_uname, uname_err = validate_username(username)
    if not is_valid_uname:
        return False, uname_err

    is_valid_email, email_err = validate_email(email)
    if not is_valid_email:
        return False, email_err

    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    username = username.strip()
    email = email.strip()

    # Check for existing user
    if database.get_user_by_username(username) is not None:
        return False, f"Username '{username}' is already taken."
    if database.get_user_by_email(email) is not None:
        return False, f"Email '{email}' is already registered."

    # Hash password & save
    pwd_hash = hash_password(password, username)
    result = database.create_user(username, email, pwd_hash, bio, profile_pic)

    if isinstance(result, int) and result > 0:
        return True, "Registration successful! Please log in."
    if result == "username_taken":
        return False, f"Username '{username}' is already taken."
    if result == "email_taken":
        return False, f"Email '{email}' is already registered."
    return False, "Could not create account. Please try again."

def login_user(username, password):
    """
    Verifies user credentials. On success, initializes Streamlit session state keys.
    """
    username = username.strip()
    if not username or not password:
        return False, "Username and password cannot be empty."

    user = database.get_user_by_username(username)
    if user is None:
        return False, "Invalid username or password."

    pwd_hash = hash_password(password, username)
    if user["password_hash"] == pwd_hash:
        # Set session state
        st.session_state["logged_in"] = True
        st.session_state["user_id"] = user["id"]
        st.session_state["username"] = user["username"]
        return True, "Login successful."
    
    return False, "Invalid username or password."

def logout_user():
    """Clears all authentication keys from the Streamlit session state."""
    st.session_state["logged_in"] = False
    st.session_state["user_id"] = None
    st.session_state["username"] = None
    st.session_state["nav_target"] = "🔑  Sign In"
    st.rerun()

def get_current_user_id():
    """Returns the logged-in user ID, or None if anonymous."""
    return st.session_state.get("user_id")

def is_logged_in():
    """Returns True if a user is logged in, False otherwise."""
    return st.session_state.get("logged_in", False)
