import streamlit as st
import database
import os

def render_profile_view(user_id, current_user_id):
    """
    Renders a comprehensive, styled profile page for a given user_id.
    Includes avatar, stats (posts, followers, following) metric cards,
    follow button (if not own profile), bio, and a 3-column grid of posts.
    """
    user = database.get_user_by_id(user_id)
    if not user:
        st.error("User not found.")
        return

    username = user["username"]
    bio = user["bio"] if user["bio"] else "No bio yet."
    profile_pic = user["profile_pic"]

    # Fetch Stats
    posts = database.get_posts_by_user(user_id)
    posts_count = len(posts)
    followers_count = database.get_followers_count(user_id)
    following_count = database.get_following_count(user_id)
    
    # Check if viewing own profile
    is_own_profile = (user_id == current_user_id)
    
    # Styled Profile Header Grid using Streamlit Columns (Responsive & Native)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    header_col1, header_col2 = st.columns([1, 2.5])
    
    with header_col1:
        # Display Avatar
        if profile_pic and (profile_pic.startswith("http://") or profile_pic.startswith("https://") or os.path.exists(profile_pic)):
            st.image(profile_pic, use_column_width=True)
        else:
            # CSS Class is injected from app.py to style this cleanly
            st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; min-height: 100px; height: 100%;">
                <div class="user-avatar-large">{username[0].upper()}</div>
            </div>
            """, unsafe_allow_html=True)
            
    with header_col2:
        st.subheader(f"@{username}")
        
        # Stats Metrics
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        with stats_col1:
            st.metric(label="Posts", value=posts_count)
        with stats_col2:
            st.metric(label="Followers", value=followers_count)
        with stats_col3:
            st.metric(label="Following", value=following_count)
        
        st.markdown("---")
        st.write(f"**Bio:** {bio}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Follow / Unfollow button if not own profile
    if not is_own_profile:
        col_f, col_spacer = st.columns([1, 4])
        with col_f:
            is_following_user = database.is_following(current_user_id, user_id)
            if is_following_user:
                if st.button("Unfollow", key="unfollow_btn_profile", use_container_width=True):
                    database.unfollow_user(current_user_id, user_id)
                    st.rerun()
            else:
                if st.button("Follow", key="follow_btn_profile", type="primary", use_container_width=True):
                    database.follow_user(current_user_id, user_id)
                    st.rerun()

    st.markdown("### 📷 Posts Grid")

    # 3-Column Posts Grid
    if not posts:
        st.info("No posts uploaded yet.")
    else:
        # Streamlit 3-column layout
        cols = st.columns(3)
        for idx, post in enumerate(posts):
            col_idx = idx % 3
            with cols[col_idx]:
                image_path = post["image_path"]
                if os.path.exists(image_path):
                    st.image(image_path, use_column_width=True)
                    # Expandable details
                    with st.expander("Details", expanded=False):
                        st.write(post["caption"] if post["caption"] else "No caption.")
                        st.caption(post["created_at"])
                        # View comments / likes
                        likes_cnt = database.get_post_likes_count(post["id"])
                        st.write(f"❤️ **{likes_cnt} likes**")
                        
                        # Add a quick delete option from profile if owned
                        if is_own_profile:
                            if st.button("🗑️ Delete", key=f"prof_del_{post['id']}", use_container_width=True):
                                database.delete_post(post["id"], current_user_id)
                                st.rerun()
                else:
                    st.error("Image file missing")

def render_edit_profile(user_id):
    """
    Renders form controls allowing users to modify their bios and avatars.
    """
    user = database.get_user_by_id(user_id)
    if not user:
        st.error("User not found.")
        return

    st.markdown("## ✏️ Edit Profile")
    
    # Form layout
    with st.form("edit_profile_form"):
        bio_val = st.text_area("Bio", value=user["bio"] if user["bio"] else "", max_chars=150, help="Brief bio (max 150 chars)")
        profile_pic_val = st.text_input("Profile Picture URL (Optional)", value=user["profile_pic"] if user["profile_pic"] else "")
        
        submitted = st.form_submit_button("Save Changes", type="primary")
        if submitted:
            database.update_user_profile(user_id, bio_val.strip(), profile_pic_val.strip())
            st.success("Profile updated successfully!")
            st.rerun()
