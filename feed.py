import streamlit as st
import database
import os
from datetime import datetime

def format_timestamp(timestamp_str):
    """Converts a SQLite ISO timestamp to a human-readable format."""
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y  •  %I:%M %p")
    except (ValueError, TypeError):
        return str(timestamp_str)

# ─────────────────────────────────────────────────────────────────
# Post Card
# ─────────────────────────────────────────────────────────────────

def render_post_card(post, current_user_id):
    """Renders a premium glassmorphic post card."""
    post_id     = post["id"]
    author_id   = post["user_id"]
    author_name = post["username"]
    image_path  = post["image_path"]
    caption     = post["caption"] or ""
    created_at  = post["created_at"]

    likes_count = database.get_post_likes_count(post_id)
    user_liked  = database.has_user_liked(current_user_id, post_id)
    comments    = database.get_post_comments(post_id)

    # ── Card wrapper ─────────────────────────────────────────────
    st.markdown('<div class="post-card">', unsafe_allow_html=True)

    # ── Author header row ─────────────────────────────────────────
    avatar_letter = author_name[0].upper()
    st.markdown(
        f'<div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">'
        f'  <div class="user-avatar-small">{avatar_letter}</div>'
        f'  <div>'
        f'    <div style="font-weight:700; font-size:0.95rem; '
        f'         color:var(--ss-text-1);">@{author_name}</div>'
        f'    <div style="font-size:0.75rem; color:var(--ss-text-3); font-weight:600;">'
        f'         {format_timestamp(created_at)}</div>'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Post image ────────────────────────────────────────────────
    if os.path.exists(image_path):
        st.image(image_path, use_column_width=True)
    else:
        st.warning("⚠️ Media file not found.")

    # ── Caption ───────────────────────────────────────────────────
    if caption.strip():
        st.markdown(
            f'<div style="margin:10px 0 4px; font-size:0.9rem; '
            f'line-height:1.5; color:var(--ss-text-2);">'
            f'<strong style="color:var(--ss-text-1);">@{author_name}</strong>'
            f'&nbsp;{caption}</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<div style="font-size:0.75rem; color:var(--ss-text-3); margin-bottom:12px;">'
        f'❤️ {likes_count} like{"s" if likes_count != 1 else ""}  •  '
        f'💬 {len(comments)} comment{"s" if len(comments) != 1 else ""}'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ── Action bar: Like | Delete ─────────────────────────────────
    act_col1, act_col2, act_col3 = st.columns([2.5, 5, 2])
    with act_col1:
        like_label = f"{'❤️' if user_liked else '🤍'}  {'Liked' if user_liked else 'Like'}"
        if st.button(like_label, key=f"btn_like_{post_id}", use_container_width=True):
            if user_liked:
                database.unlike_post(current_user_id, post_id)
            else:
                database.like_post(current_user_id, post_id)
            st.rerun()

    with act_col3:
        if author_id == current_user_id:
            if st.button("🗑️", key=f"btn_del_{post_id}",
                         help="Delete this post", use_container_width=True):
                if database.delete_post(post_id, current_user_id):
                    st.success("Post deleted!")
                    st.rerun()

    # ── Comments ──────────────────────────────────────────────────
    if comments:
        with st.expander(f"💬  View {len(comments)} comment{'s' if len(comments)!=1 else ''}"):
            for c in comments:
                st.markdown(
                    f'<div style="padding:8px 0; border-bottom:1px solid var(--ss-border);">'
                    f'<span style="font-weight:700; color:var(--ss-text-1);">@{c["username"]}</span>'
                    f'&nbsp;<span style="color:var(--ss-text-2); font-size:0.88rem;">{c["content"]}</span>'
                    f'<br><small style="color:var(--ss-text-3); font-weight:600;">{format_timestamp(c["created_at"])}</small>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # ── Add comment ───────────────────────────────────────────────
    c_in, c_btn = st.columns([7, 2])
    with c_in:
        new_comment = st.text_input(
            "comment", key=f"in_comm_{post_id}",
            placeholder="✍️  Write a comment…", label_visibility="collapsed"
        )
    with c_btn:
        if st.button("Post", key=f"btn_comm_{post_id}", use_container_width=True):
            if new_comment.strip():
                database.add_comment(current_user_id, post_id, new_comment)
                st.rerun()
            else:
                st.toast("Comment can't be empty.")

    st.markdown(
        '<div style="margin:20px 0; height:1px; background:var(--ss-border);"></div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────
# Feed View
# ─────────────────────────────────────────────────────────────────

def render_feed_view(feed_type, current_user_id):
    """Renders the selected feed in a premium centred layout."""
    config = {
        "home":         ("🏠", "Home Feed",   "Posts from users you follow and your own uploads."),
        "latest":       ("🔥", "Explore",      "Discover the newest posts on SnapShare."),
        "personalized": ("✨", "Trending",     "Top posts ranked by likes & comments."),
    }
    icon, title, desc = config.get(feed_type, ("📷", "Feed", ""))

    # Header
    st.markdown(
        f'<div class="feed-header" style="display:flex; align-items:center; gap:14px;">'
        f'  <span style="font-size:2rem; line-height:1;">{icon}</span>'
        f'  <div>'
        f'    <div style="font-size:1.25rem; font-weight:800; color:var(--ss-text-1);">{title}</div>'
        f'    <div style="font-size:0.82rem; color:var(--ss-text-3);">{desc}</div>'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    fetch = {
        "home":         database.get_home_feed,
        "latest":       database.get_latest_posts_feed,
        "personalized": database.get_personalized_feed,
    }
    posts = fetch[feed_type](current_user_id)

    if not posts:
        st.markdown(
            '<div class="glass-card" style="text-align:center; padding:52px 24px;">'
            '  <div style="font-size:3rem; margin-bottom:16px;">📭</div>'
            '  <div style="font-size:1.1rem; font-weight:700; '
            '       color:var(--ss-text-1); margin-bottom:8px;">Nothing here yet</div>'
            '  <div style="font-size:0.88rem; color:var(--ss-text-3);">'
            '       Upload a photo or follow some users to get started!'
            '  </div>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    _, col, _ = st.columns([1, 2.5, 1])
    with col:
        for post in posts:
            render_post_card(post, current_user_id)
