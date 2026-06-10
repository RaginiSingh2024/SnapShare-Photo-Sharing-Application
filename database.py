import sqlite3
import os
from datetime import datetime

DATABASE_NAME = "snapshare.db"

def get_db_connection():
    """Establishes a connection to the SQLite database with Foreign Key support enabled."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initializes the database schema and creates indexes for query optimization."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        bio TEXT,
        profile_pic TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Posts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        caption TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)

    # Likes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        post_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
        UNIQUE(user_id, post_id)
    );
    """)

    # Comments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        post_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
    );
    """)

    # Followers Table (follower_id follows following_id)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS followers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        follower_id INTEGER NOT NULL,
        following_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (follower_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (following_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(follower_id, following_id)
    );
    """)

    # Notifications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL, -- The receiver
        sender_id INTEGER NOT NULL, -- The sender/actor
        type TEXT NOT NULL, -- 'like', 'comment', 'follow'
        post_id INTEGER,
        is_read INTEGER DEFAULT 0, -- 0 for false, 1 for true
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
    );
    """)

    # Create Indexes for optimization
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_likes_post_id ON likes(post_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_followers_follower_id ON followers(follower_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_followers_following_id ON followers(following_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);")

    conn.commit()
    conn.close()

# ----------------- USER OPERATIONS -----------------

def create_user(username, email, password_hash, bio="", profile_pic=""):
    """Inserts a new user record into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, bio, profile_pic) VALUES (?, ?, ?, ?, ?);",
            (username.lower().strip(), email.lower().strip(), password_hash, bio, profile_pic)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_username(username):
    """Retrieves a user profile by their unique username."""
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?;",
        (username.lower().strip(),)
    ).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Retrieves a user profile by their user ID."""
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?;",
        (user_id,)
    ).fetchone()
    conn.close()
    return user

def update_user_profile(user_id, bio, profile_pic):
    """Updates the bio and profile picture URL of a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET bio = ?, profile_pic = ? WHERE id = ?;",
        (bio, profile_pic, user_id)
    )
    conn.commit()
    conn.close()

def search_users(query):
    """Searches for users by matching username prefixes or fragments."""
    conn = get_db_connection()
    users = conn.execute(
        "SELECT id, username, bio, profile_pic FROM users WHERE username LIKE ? OR bio LIKE ? LIMIT 20;",
        (f"%{query}%", f"%{query}%")
    ).fetchall()
    conn.close()
    return users

# ----------------- POST OPERATIONS -----------------

def create_post(user_id, image_path, caption):
    """Inserts a new post record into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO posts (user_id, image_path, caption) VALUES (?, ?, ?);",
        (user_id, image_path, caption)
    )
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return post_id

def delete_post(post_id, user_id):
    """Deletes a post if it belongs to the logged-in user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Check ownership
    post = cursor.execute("SELECT image_path FROM posts WHERE id = ? AND user_id = ?;", (post_id, user_id)).fetchone()
    if post:
        image_path = post["image_path"]
        cursor.execute("DELETE FROM posts WHERE id = ? AND user_id = ?;", (post_id, user_id))
        conn.commit()
        conn.close()
        # Attempt to delete file locally
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
        except Exception:
            pass
        return True
    conn.close()
    return False

def get_post_by_id(post_id):
    """Fetches a specific post with creator details."""
    conn = get_db_connection()
    post = conn.execute(
        """
        SELECT p.*, u.username, u.profile_pic 
        FROM posts p 
        JOIN users u ON p.user_id = u.id 
        WHERE p.id = ?;
        """,
        (post_id,)
    ).fetchone()
    conn.close()
    return post

def get_posts_by_user(user_id):
    """Fetches all posts uploaded by a specific user."""
    conn = get_db_connection()
    posts = conn.execute(
        "SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC;",
        (user_id,)
    ).fetchall()
    conn.close()
    return posts

# ----------------- LIKE OPERATIONS -----------------

def has_user_liked(user_id, post_id):
    """Checks if a user has already liked a post."""
    conn = get_db_connection()
    like = conn.execute(
        "SELECT 1 FROM likes WHERE user_id = ? AND post_id = ?;",
        (user_id, post_id)
    ).fetchone()
    conn.close()
    return like is not None

def like_post(user_id, post_id):
    """Likes a post and triggers a notification for the author."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO likes (user_id, post_id) VALUES (?, ?);",
            (user_id, post_id)
        )
        conn.commit()
        
        # Trigger notification
        post = cursor.execute("SELECT user_id FROM posts WHERE id = ?;", (post_id,)).fetchone()
        if post and post["user_id"] != user_id:
            create_notification(post["user_id"], user_id, "like", post_id)
            
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def unlike_post(user_id, post_id):
    """Unlikes a post."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM likes WHERE user_id = ? AND post_id = ?;",
        (user_id, post_id)
    )
    conn.commit()
    conn.close()
    return True

def get_post_likes_count(post_id):
    """Fetches total like count for a post."""
    conn = get_db_connection()
    count = conn.execute(
        "SELECT COUNT(*) as count FROM likes WHERE post_id = ?;",
        (post_id,)
    ).fetchone()["count"]
    conn.close()
    return count

# ----------------- COMMENT OPERATIONS -----------------

def add_comment(user_id, post_id, content):
    """Adds a comment to a post and triggers a notification for the author."""
    if not content.strip():
        return None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comments (user_id, post_id, content) VALUES (?, ?, ?);",
        (user_id, post_id, content.strip())
    )
    conn.commit()
    comment_id = cursor.lastrowid
    
    # Trigger notification
    post = cursor.execute("SELECT user_id FROM posts WHERE id = ?;", (post_id,)).fetchone()
    if post and post["user_id"] != user_id:
        create_notification(post["user_id"], user_id, "comment", post_id)
        
    conn.close()
    return comment_id

def get_post_comments(post_id):
    """Fetches all comments on a post along with the commenter's username and profile pic."""
    conn = get_db_connection()
    comments = conn.execute(
        """
        SELECT c.*, u.username, u.profile_pic 
        FROM comments c 
        JOIN users u ON c.user_id = u.id 
        WHERE c.post_id = ? 
        ORDER BY c.created_at ASC;
        """,
        (post_id,)
    ).fetchall()
    conn.close()
    return comments

# ----------------- FOLLOW OPERATIONS -----------------

def follow_user(follower_id, following_id):
    """Enables a user to follow another user."""
    if follower_id == following_id:
        return False
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO followers (follower_id, following_id) VALUES (?, ?);",
            (follower_id, following_id)
        )
        conn.commit()
        
        # Trigger notification
        create_notification(following_id, follower_id, "follow", None)
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def unfollow_user(follower_id, following_id):
    """Enables a user to unfollow another user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM followers WHERE follower_id = ? AND following_id = ?;",
        (follower_id, following_id)
    )
    conn.commit()
    conn.close()
    return True

def is_following(follower_id, following_id):
    """Checks if follower_id is following following_id."""
    conn = get_db_connection()
    follow = conn.execute(
        "SELECT 1 FROM followers WHERE follower_id = ? AND following_id = ?;",
        (follower_id, following_id)
    ).fetchone()
    conn.close()
    return follow is not None

def get_followers_count(user_id):
    """Returns the total number of followers a user has."""
    conn = get_db_connection()
    count = conn.execute(
        "SELECT COUNT(*) as count FROM followers WHERE following_id = ?;",
        (user_id,)
    ).fetchone()["count"]
    conn.close()
    return count

def get_following_count(user_id):
    """Returns the total number of users a user is following."""
    conn = get_db_connection()
    count = conn.execute(
        "SELECT COUNT(*) as count FROM followers WHERE follower_id = ?;",
        (user_id,)
    ).fetchone()["count"]
    conn.close()
    return count

# ----------------- NOTIFICATION OPERATIONS -----------------

def create_notification(user_id, sender_id, type_, post_id=None):
    """Inserts a notification record (helper method)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notifications (user_id, sender_id, type, post_id, is_read) VALUES (?, ?, ?, ?, 0);",
        (user_id, sender_id, type_, post_id)
    )
    conn.commit()
    conn.close()

def get_notifications(user_id):
    """Retrieves all notifications for a user, sorted chronologically."""
    conn = get_db_connection()
    notifications = conn.execute(
        """
        SELECT n.*, u.username as sender_name, u.profile_pic as sender_pic 
        FROM notifications n
        JOIN users u ON n.sender_id = u.id
        WHERE n.user_id = ? 
        ORDER BY n.created_at DESC LIMIT 50;
        """,
        (user_id,)
    ).fetchall()
    conn.close()
    return notifications

def get_unread_notifications_count(user_id):
    """Retrieves unread notifications count."""
    conn = get_db_connection()
    count = conn.execute(
        "SELECT COUNT(*) as count FROM notifications WHERE user_id = ? AND is_read = 0;",
        (user_id,)
    ).fetchone()["count"]
    conn.close()
    return count

def mark_notifications_as_read(user_id):
    """Marks all notifications for a user as read."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE notifications SET is_read = 1 WHERE user_id = ?;",
        (user_id,)
    )
    conn.commit()
    conn.close()

# ----------------- FEED GENERATION -----------------

def get_home_feed(user_id):
    """
    Chronological feed: displays posts from users that user_id follows + own posts,
    annotated with author details, likes count, and comment count.
    """
    conn = get_db_connection()
    posts = conn.execute(
        """
        SELECT p.*, u.username, u.profile_pic,
               (SELECT COUNT(*) FROM likes WHERE post_id = p.id) as likes_count,
               (SELECT COUNT(*) FROM comments WHERE post_id = p.id) as comments_count,
               EXISTS(SELECT 1 FROM likes WHERE user_id = ? AND post_id = p.id) as user_liked
        FROM posts p
        JOIN users u ON p.user_id = u.id
        WHERE p.user_id = ? OR p.user_id IN (
            SELECT following_id FROM followers WHERE follower_id = ?
        )
        ORDER BY p.created_at DESC;
        """,
        (user_id, user_id, user_id)
    ).fetchall()
    conn.close()
    return posts

def get_latest_posts_feed(user_id):
    """Gets all latest posts in the platform chronologically."""
    conn = get_db_connection()
    posts = conn.execute(
        """
        SELECT p.*, u.username, u.profile_pic,
               (SELECT COUNT(*) FROM likes WHERE post_id = p.id) as likes_count,
               (SELECT COUNT(*) FROM comments WHERE post_id = p.id) as comments_count,
               EXISTS(SELECT 1 FROM likes WHERE user_id = ? AND post_id = p.id) as user_liked
        FROM posts p
        JOIN users u ON p.user_id = u.id
        ORDER BY p.created_at DESC LIMIT 50;
        """,
        (user_id,)
    ).fetchall()
    conn.close()
    return posts

def get_personalized_feed(user_id):
    """
    Engagement-based personalized feed. Calculates post rank score:
    Score = (likes_count + comments_count * 2) 
    Sorted DESC.
    """
    conn = get_db_connection()
    posts = conn.execute(
        """
        SELECT p.*, u.username, u.profile_pic,
               (SELECT COUNT(*) FROM likes WHERE post_id = p.id) as likes_count,
               (SELECT COUNT(*) FROM comments WHERE post_id = p.id) as comments_count,
               EXISTS(SELECT 1 FROM likes WHERE user_id = ? AND post_id = p.id) as user_liked,
               ((SELECT COUNT(*) FROM likes WHERE post_id = p.id) + (SELECT COUNT(*) FROM comments WHERE post_id = p.id) * 2.0) as engagement_score
        FROM posts p
        JOIN users u ON p.user_id = u.id
        ORDER BY engagement_score DESC, p.created_at DESC LIMIT 50;
        """,
        (user_id,)
    ).fetchall()
    conn.close()
    return posts
