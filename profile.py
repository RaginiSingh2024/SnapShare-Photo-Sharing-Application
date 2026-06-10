import streamlit as st
import database
import os

def render_profile_view(user_id, current_user_id):
    """
    Renders a comprehensive, styled profile page for a given user_id.
    Includes avatar, stats (posts, followers, following), follow button (if not own profile),
    bio, and a 3-column grid of posts.
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
    
    # Styled Profile Header Grid
    st.markdown(f"""
    <div class="glass-card" style="margin-bottom: 24px; padding: 24px;">
        <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 24px;">
            <!-- Profile Avatar -->
            <div class="user-avatar-large">
                {username[0].upper() if not profile_pic else ""}
            </div>
            
            <!-- Profile Details and Stats -->
            <div style="flex: 1; min-width: 250px;">
                <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap; margin-bottom: 12px;">
                    <h2 style="margin: 0; color: #ffffff;">@{username}</h2>
                </div>
                
                <!-- Stats row -->
                <div style="display: flex; gap: 24px; margin-bottom: 16px;">
                    <div><strong style="color: #ffffff; font-size: 1.1rem;">{posts_count}</strong> <span style="color: #9a9da3; font-size: 0.85rem;">posts</span></div>
                    <div><strong style="color: #ffffff; font-size: 1.1rem;">{followers_count}</strong> <span style="color: #9a9da3; font-size: 0.85rem;">followers</span></div>
                    <div><strong style="color: #ffffff; font-size: 1.1rem;">{following_count}</strong> <span style="color: #9a9da3; font-size: 0.85rem;">following</span></div>
                </div>
                
                <!-- Bio -->
                <div style="color: #d1d5db; font-size: 0.9rem; line-height: 1.5; margin-bottom: 8px;">
                    {bio}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("<h4 style='color:#ffffff; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:8px; margin-bottom:16px;'>📷 Posts Grid</h4>", unsafe_allow_html=True)

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
                        st.markdown(f"❤️ **{likes_cnt} likes**", unsafe_allow_html=True)
                        
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

    st.markdown("<h2 style='color:#ffffff; margin-bottom:20px;'>✏️ Edit Profile</h2>", unsafe_allow_html=True)
    
    # Form layout
    with st.form("edit_profile_form"):
        bio_val = st.text_area("Bio", value=user["bio"] if user["bio"] else "", max_chars=150, help="Brief bio (max 150 chars)")
        
        # In a real app we'd let them upload a pic, but here we can support a URL or placeholder setting
        profile_pic_val = st.text_input("Profile Picture URL (Optional)", value=user["profile_pic"] if user["profile_pic"] else "")
        
        submitted = st.form_submit_button("Save Changes", type="primary")
        if submitted:
            database.update_user_profile(user_id, bio_val.strip(), profile_pic_val.strip())
            st.success("Profile updated successfully!")
            st.rerun()
