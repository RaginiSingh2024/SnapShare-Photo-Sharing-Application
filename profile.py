import streamlit as st
import database
import os

def render_profile_view(user_id, current_user_id):
    """Premium Instagram-style profile page."""
    user = database.get_user_by_id(user_id)
    if not user:
        st.error("User not found.")
        return

    username    = user["username"]
    bio         = user["bio"] or "No bio yet. ✨"
    profile_pic = user["profile_pic"]
    is_own      = (user_id == current_user_id)

    posts             = database.get_posts_by_user(user_id)
    posts_count       = len(posts)
    followers_count   = database.get_followers_count(user_id)
    following_count   = database.get_following_count(user_id)
    is_following_user = not is_own and database.is_following(current_user_id, user_id)

    # ── Profile Header ───────────────────────────────────────────
    avatar_letter = username[0].upper()

    st.markdown(
        '<div class="glass-card" style="padding:32px 36px; margin-bottom:20px;">',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 2.8])

    with left:
        if profile_pic and (
            profile_pic.startswith("http") or os.path.exists(profile_pic)
        ):
            st.image(profile_pic, use_column_width=True)
        else:
            st.markdown(
                f'<div style="display:flex; justify-content:center; align-items:center; height:120px;">'
                f'  <div class="user-avatar-large">{avatar_letter}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    with right:
        st.markdown(
            f'<div style="font-size:1.6rem; font-weight:900; letter-spacing:-0.03em; '
            f'color:var(--ss-text-1); margin-bottom:4px;">@{username}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="font-size:0.9rem; color:var(--ss-text-2); '
            f'margin-bottom:20px; line-height:1.5;">{bio}</div>',
            unsafe_allow_html=True,
        )

        # Stats
        st.markdown(
            f'<div style="display:flex; gap:28px; margin-bottom:22px; flex-wrap:wrap;">'
            f'  <div style="text-align:center;">'
            f'    <div style="font-size:1.5rem; font-weight:900; letter-spacing:-0.03em; '
            f'         color:var(--ss-text-1);">{posts_count}</div>'
            f'    <div class="profile-stat-label" style="font-size:0.75rem; text-transform:uppercase;">Posts</div>'
            f'  </div>'
            f'  <div style="text-align:center;">'
            f'    <div style="font-size:1.5rem; font-weight:900; letter-spacing:-0.03em; '
            f'         color:var(--ss-text-1);">{followers_count}</div>'
            f'    <div class="profile-stat-label" style="font-size:0.75rem; text-transform:uppercase;">Followers</div>'
            f'  </div>'
            f'  <div style="text-align:center;">'
            f'    <div style="font-size:1.5rem; font-weight:900; letter-spacing:-0.03em; '
            f'         color:var(--ss-text-1);">{following_count}</div>'
            f'    <div class="profile-stat-label" style="font-size:0.75rem; text-transform:uppercase;">Following</div>'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if not is_own:
            col_btn, _ = st.columns([2, 3])
            with col_btn:
                if is_following_user:
                    if st.button("✓ Following", key="btn_unfollow_profile",
                                 use_container_width=True):
                        database.unfollow_user(current_user_id, user_id)
                        st.rerun()
                else:
                    if st.button("➕ Follow", key="btn_follow_profile",
                                 type="primary", use_container_width=True):
                        database.follow_user(current_user_id, user_id)
                        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # ── Posts Grid ────────────────────────────────────────────────
    st.markdown(
        '<div class="settings-section-label" style="font-size:0.78rem; '
        'text-transform:uppercase; margin-bottom:14px; padding-bottom:10px; '
        'border-bottom:1px solid var(--ss-border);">📷  Posts</div>',
        unsafe_allow_html=True,
    )

    if not posts:
        st.markdown(
            '<div class="glass-card" style="text-align:center; padding:48px 24px;">'
            '  <div style="font-size:3rem; margin-bottom:14px;">🖼️</div>'
            '  <div style="color:var(--ss-text-2); font-size:0.9rem; font-weight:500;">No posts uploaded yet.</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        cols = st.columns(3)
        for idx, post in enumerate(posts):
            with cols[idx % 3]:
                if os.path.exists(post["image_path"]):
                    st.image(post["image_path"], use_column_width=True)
                    with st.expander("", expanded=False):
                        st.markdown(
                            post["caption"] if post["caption"] else "_No caption._"
                        )
                        likes = database.get_post_likes_count(post["id"])
                        st.caption(f"❤️ {likes} likes  •  {post['created_at']}")
                        if is_own:
                            if st.button("🗑️ Delete",
                                         key=f"prof_del_{post['id']}",
                                         use_container_width=True):
                                database.delete_post(post["id"], current_user_id)
                                st.rerun()
                else:
                    st.error("File missing")


def render_edit_profile(user_id):
    """Premium edit profile form."""
    user = database.get_user_by_id(user_id)
    if not user:
        st.error("User not found.")
        return

    st.markdown(
        '<div style="font-size:1.6rem; font-weight:900; letter-spacing:-0.03em; '
        'color:var(--ss-text-1); margin-bottom:24px;">✏️  Edit Profile</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    with st.form("edit_profile_form"):
        bio_val = st.text_area(
            "Bio", value=user["bio"] or "",
            max_chars=150, height=100,
            help="Tell the world a little about yourself (max 150 chars)",
        )
        pic_val = st.text_input(
            "Profile Picture URL",
            value=user["profile_pic"] or "",
            help="Paste an image URL (https://…)",
        )
        if st.form_submit_button("💾  Save Changes", type="primary",
                                  use_container_width=True):
            database.update_user_profile(user_id, bio_val.strip(), pic_val.strip())
            st.success("Profile updated! ✨")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
