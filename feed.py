import streamlit as st
import database
import os
from datetime import datetime

def format_timestamp(timestamp_str):
    """Converts a SQLite ISO timestamp string to a readable format."""
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y - %I:%M %p")
    except ValueError:
        return timestamp_str

def render_post_card(post, current_user_id):
    """
    Renders a single post card with Glassmorphic design styling.
    Includes profile picture, username, post image, caption, action buttons (like, comment), and comments list.
    """
    post_id = post["id"]
    author_id = post["user_id"]
    author_name = post["username"]
    author_pic = post["profile_pic"]
    image_path = post["image_path"]
    caption = post["caption"]
    created_at = post["created_at"]
    likes_count = post["likes_count"]
    comments_count = post["comments_count"]
    user_liked = post["user_liked"]

    # Retrieve current like state from database dynamically
    likes_count = database.get_post_likes_count(post_id)
    user_liked = database.has_user_liked(current_user_id, post_id)

    # Post Card Container
    st.markdown(f"""
    <div class="post-card">
        <!-- Post Header -->
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div class="user-avatar-small">
                    {author_name[0].upper() if not author_pic else ""}
                </div>
                <div>
                    <span style="font-weight: 700; color: #f5f6f7; font-size: 0.95rem;">@{author_name}</span><br>
                    <span style="font-size: 0.75rem; color: #9a9da3;">{format_timestamp(created_at)}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Post Image (Streamlit native image handles layout and responsiveness beautifully)
    if os.path.exists(image_path):
        st.image(image_path, use_column_width=True)
    else:
        st.warning("Media file not found.")

    # Post Actions (Like, Comment, Delete)
    col1, col2, col3 = st.columns([1.5, 6, 2])
    
    # Like Action
    with col1:
        like_btn_label = "❤️ Liked" if user_liked else "🖤 Like"
        if st.button(f"{like_btn_label} ({likes_count})", key=f"btn_like_{post_id}"):
            if user_liked:
                database.unlike_post(current_user_id, post_id)
            else:
                database.like_post(current_user_id, post_id)
            st.rerun()

    # Delete Action (if owner)
    with col3:
        if author_id == current_user_id:
            if st.button("🗑️ Delete", key=f"btn_del_{post_id}", help="Delete this post permanently"):
                success = database.delete_post(post_id, current_user_id)
                if success:
                    st.success("Post deleted!")
                    st.rerun()
                else:
                    st.error("Failed to delete.")

    # Caption Section
    if caption:
        st.markdown(f"""
        <div style="margin: 8px 0; font-size: 0.9rem; color: #e1e3e6; line-height: 1.4;">
            <strong style="color: #ffffff; margin-right: 6px;">@{author_name}</strong> {caption}
        </div>
        """, unsafe_allow_html=True)

    # Comments Section
    comments = database.get_post_comments(post_id)
    
    # Render comments if any
    if comments:
        with st.expander(f"💬 View Comments ({len(comments)})"):
            for comment in comments:
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.03); padding: 6px 10px; border-radius: 6px; margin-bottom: 6px; font-size: 0.85rem; border-left: 2px solid #a855f7;">
                    <strong style="color: #c084fc;">@{comment['username']}</strong>: 
                    <span style="color: #d1d5db;">{comment['content']}</span>
                </div>
                """, unsafe_allow_html=True)

    # Add Comment
    comment_input_col, comment_btn_col = st.columns([7, 2])
    with comment_input_col:
        new_comment = st.text_input("Add a comment...", key=f"in_comm_{post_id}", label_visibility="collapsed")
    with comment_btn_col:
        if st.button("Post", key=f"btn_comm_{post_id}", use_container_width=True):
            if new_comment.strip():
                database.add_comment(current_user_id, post_id, new_comment)
                st.rerun()

    st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.1); margin: 30px 0;'>", unsafe_allow_html=True)

def render_feed_view(feed_type, current_user_id):
    """
    Fetches the respective feed data and renders the list of post cards.
    Options: 'home', 'latest', 'personalized'
    """
    if feed_type == "home":
        posts = database.get_home_feed(current_user_id)
        feed_title = "🏠 Home Feed"
        feed_desc = "Posts from users you follow and your own updates."
    elif feed_type == "latest":
        posts = database.get_latest_posts_feed(current_user_id)
        feed_title = "🔥 Explore Latest"
        feed_desc = "All recently uploaded posts on SnapShare."
    else:  # personalized
        posts = database.get_personalized_feed(current_user_id)
        feed_title = "✨ Trending / Personalized"
        feed_desc = "Top engaging posts ranked by likes and comments."

    st.markdown(f"""
    <div class="feed-header">
        <h2 style="margin: 0; color: #ffffff;">{feed_title}</h2>
        <p style="margin: 4px 0 0 0; font-size: 0.9rem; color: #a1a1aa;">{feed_desc}</p>
    </div>
    """, unsafe_allow_html=True)

    if not posts:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 40px; margin-top: 20px;">
            <h3 style="color: #9a9da3; margin-bottom: 10px;">No Posts to Show</h3>
            <p style="color: #64748b; font-size: 0.9rem;">
                Try uploading a photo or following other users to populate your feed!
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Create a centered column for the feed to make it look like a mobile app layout
        feed_col_left, feed_col_main, feed_col_right = st.columns([1, 2.5, 1])
        with feed_col_main:
            for post in posts:
                render_post_card(post, current_user_id)
