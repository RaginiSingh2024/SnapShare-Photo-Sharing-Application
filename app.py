import streamlit as st
import os

# ── Page config MUST be first Streamlit call ──────────────────────
st.set_page_config(
    page_title="SnapShare — Premium Photo Sharing",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded",
)

import database
import auth
import feed
import profile
import posts
import themes

database.init_db()

# ── Theme (initialise before first render) ────────────────────────
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

st.markdown(themes.get_theme_css(st.session_state["theme"]), unsafe_allow_html=True)

# ── Session state defaults ─────────────────────────────────────────
for key, val in [
    ("logged_in", False),
    ("user_id", None),
    ("username", None),
    ("view_profile_id", None),
    ("nav_target", None),
]:
    if key not in st.session_state:
        st.session_state[key] = val


def view_profile(uid):
    st.session_state["view_profile_id"] = uid
    st.rerun()

def clear_profile_view():
    st.session_state["view_profile_id"] = None


def _render_user_card(user_id, username, bio, current_uid, suffix=""):
    is_foll = database.is_following(current_uid, user_id)
    bio_txt = bio if bio else "No bio yet."

    try:
        followers_count = database.get_followers_count(user_id)
        posts_count = len(database.get_posts_by_user(user_id))
    except Exception:
        followers_count = 0
        posts_count = 0

    with st.container(border=True):
        st.markdown(
            f'<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">'
            f'  <div class="user-avatar-small">{username[0].upper()}</div>'
            f'  <div style="flex: 1; min-width: 0;">'
            f'    <div style="font-weight: 700; font-size: 0.95rem; color: var(--ss-text-1); overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">@{username}</div>'
            f'    <div style="font-size: 0.76rem; color: var(--ss-text-2); font-weight: 600; display: flex; gap: 8px;">'
            f'      <span>👥 {followers_count} followers</span>'
            f'      <span>•</span>'
            f'      <span>📷 {posts_count} posts</span>'
            f'    </div>'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div style="font-size: 0.8rem; color: var(--ss-text-2); margin-bottom: 12px; '
            f'height: 38px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">'
            f'{bio_txt}</div>',
            unsafe_allow_html=True,
        )

        btn_col1, btn_col2 = st.columns([1, 1.8])
        with btn_col1:
            if st.button("👤 View", key=f"view_{user_id}_{suffix}", use_container_width=True):
                view_profile(user_id)
        with btn_col2:
            if user_id == current_uid:
                st.button("You", key=f"self_{user_id}_{suffix}", disabled=True, use_container_width=True)
            elif is_foll:
                if st.button("Unfollow", key=f"unf_{user_id}_{suffix}", use_container_width=True):
                    database.unfollow_user(current_uid, user_id)
                    st.rerun()
            else:
                if st.button("Follow", key=f"fol_{user_id}_{suffix}", type="primary", use_container_width=True):
                    database.follow_user(current_uid, user_id)
                    st.rerun()


# ──────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown(
        '<div class="sidebar-brand-wrap">'
        '  <div style="font-size:2rem;" class="gradient-text">SnapShare</div>'
        '  <div class="sidebar-tagline">Photo sharing · Create, connect, discover</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Theme toggle
    _theme = st.session_state["theme"]
    _icon  = "☀️" if _theme == "dark" else "🌙"
    _label = f"{_icon}  {'Light Mode' if _theme == 'dark' else 'Dark Mode'}"
    if st.button(_label, key="theme_toggle", use_container_width=True):
        st.session_state["theme"] = "light" if _theme == "dark" else "dark"
        st.rerun()

    st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)

    # Logged-in user pill
    if st.session_state["logged_in"]:
        _uname = st.session_state["username"] or "User"
        _uid   = st.session_state["user_id"]
        try:
            _notifs = database.get_unread_notifications_count(_uid)
        except Exception:
            _notifs = 0

        st.markdown(
            f'<div class="sidebar-user-card">'
            f'  <div class="user-avatar-small" style="width:34px;height:34px;font-size:0.9rem;">'
            f'    {_uname[0].upper()}</div>'
            f'  <div>'
            f'    <div class="sidebar-user-name">@{_uname}</div>'
            f'    <div class="sidebar-user-handle">Logged in</div>'
            f'  </div>'
            f'  {"🔴" if _notifs > 0 else ""}'
            f'</div>',
            unsafe_allow_html=True,
        )

    # Navigation
    if not st.session_state["logged_in"]:
        menu = ["🌟  Discover", "🔑  Sign In", "✨  Create Account"]
        if "sidebar_nav" not in st.session_state:
            st.session_state["sidebar_nav"] = menu[0]
        pending_choice = st.session_state.pop("nav_target", None)
        if pending_choice in menu:
            st.session_state["sidebar_nav"] = pending_choice
        choice = st.radio("nav", menu, label_visibility="collapsed", key="sidebar_nav")
    else:
        _uid    = st.session_state["user_id"]
        try:
            _notifs = database.get_unread_notifications_count(_uid)
        except Exception:
            _notifs = 0

        notif_lbl = f"🔔  Notifications{'  ●' if _notifs > 0 else ''}"
        menu = [
            "🏠  Home Feed",
            "🔥  Explore",
            "✨  Trending",
            "📷  Upload",
            "🔍  Search",
            notif_lbl,
            "👤  My Profile",
            "✏️  Edit Profile",
            "⚙️  Settings",
            "🚪  Sign Out",
        ]
        choice = st.radio("nav", menu, label_visibility="collapsed")


# ──────────────────────────────────────────────────────────────────
# LOGGED-OUT SCREENS
# ──────────────────────────────────────────────────────────────────
if not st.session_state["logged_in"]:

    # ── 1. DISCOVER / SPLASH ───────────────────────────────────────
    if choice == "🌟  Discover":
        # Hero
        st.markdown(
            '<div class="hero-section" style="padding-top:40px;">'
            '  <div class="hero-badge">Photo sharing made simple</div>'
            '  <div class="hero-title gradient-text">SnapShare</div>'
            '  <div class="hero-sub">Share moments with the world.</div>'
            '  <div style="font-size:1.02rem; color:var(--ss-text-2); max-width:680px; margin:0 auto 26px; line-height:1.7;">'
            '    Upload photos, connect with friends, discover creators, and share your story.'
            '  </div>'
            '</div>',
            unsafe_allow_html=True,
        )

        c_create, c_signin = st.columns(2)
        with c_create:
            if st.button("✨ Create Account", use_container_width=True, type="primary", key="hero_create_account"):
                st.session_state["nav_target"] = "✨  Create Account"
                st.rerun()
        with c_signin:
            if st.button("🔑 Sign In", use_container_width=True, key="hero_sign_in"):
                st.session_state["nav_target"] = "🔑  Sign In"
                st.rerun()

        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="glass-card">'
            '  <div style="display:flex; justify-content:space-between; align-items:end; gap:12px; margin-bottom:16px;">'
            '    <div>'
            '      <div style="font-size:1.05rem; font-weight:800; color:var(--ss-text-1);">Featured Photos</div>'
            '      <div style="font-size:0.84rem; color:var(--ss-text-3);">A preview of the kind of moments SnapShare is built for.</div>'
            '    </div>'
            '    <div style="font-size:0.75rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:var(--ss-text-3);">Preview</div>'
            '  </div>'
            '</div>',
            unsafe_allow_html=True,
        )
        photo_cols = st.columns(3)
        featured_photos = [
            ("🌅", "Golden hour city walk", "@maya", "2.4k likes"),
            ("☕", "Coffee shop candid", "@eli", "1.8k likes"),
            ("🏖️", "Weekend escape", "@noah", "3.1k likes"),
        ]
        for col, (icon, title, creator, stat) in zip(photo_cols, featured_photos):
            likes_count, likes_label = stat.split(maxsplit=1)
            with col:
                st.markdown(
                    f'<div class="feature-card" style="text-align:left;">'
                    f'  <div style="font-size:3rem; line-height:1; margin-bottom:14px;">{icon}</div>'
                    f'  <div style="font-size:0.98rem; font-weight:800; color:var(--ss-text-1); margin-bottom:6px;">{title}</div>'
                    f'  <div style="font-size:0.8rem; color:var(--ss-text-3); margin-bottom:10px;">Shared by {creator}</div>'
                    f'  <div class="stat-chip">❤️ <span class="stat-num">{likes_count}</span> {likes_label}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="glass-card">'
            '  <div style="display:flex; justify-content:space-between; align-items:end; gap:12px; margin-bottom:16px;">'
            '    <div>'
            '      <div style="font-size:1.05rem; font-weight:800; color:var(--ss-text-1);">Trending Creators</div>'
            '      <div style="font-size:0.84rem; color:var(--ss-text-3);">People worth following right now.</div>'
            '    </div>'
            '  </div>'
            '</div>',
            unsafe_allow_html=True,
        )
        creator_cols = st.columns(3)
        trending_creators = [
            ("A", "@ava", "Lifestyle & travel"),
            ("J", "@jordan", "Street photography"),
            ("S", "@sophia", "Fashion moments"),
        ]
        for col, (initial, handle, bio) in zip(creator_cols, trending_creators):
            with col:
                st.markdown(
                    f'<div class="glass-card" style="text-align:center; padding:24px 18px;">'
                    f'  <div style="display:flex; justify-content:center; margin-bottom:12px;">'
                    f'    <div class="user-avatar-large" style="width:76px; height:76px; font-size:1.6rem;">{initial}</div>'
                    f'  </div>'
                    f'  <div style="font-size:0.98rem; font-weight:800; color:var(--ss-text-1); margin-bottom:4px;">{handle}</div>'
                    f'  <div style="font-size:0.8rem; color:var(--ss-text-3); margin-bottom:12px;">{bio}</div>'
                    f'  <div class="tech-badge">Trending creator</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="glass-card">'
            '  <div style="display:flex; justify-content:space-between; align-items:end; gap:12px; margin-bottom:16px;">'
            '    <div>'
            '      <div style="font-size:1.05rem; font-weight:800; color:var(--ss-text-1);">Recent Posts</div>'
            '      <div style="font-size:0.84rem; color:var(--ss-text-3);">Fresh moments from the community.</div>'
            '    </div>'
            '  </div>'
            '</div>',
            unsafe_allow_html=True,
        )
        recent_cols = st.columns(2)
        recent_posts = [
            ("📷", "Morning light, fresh start", "@zoe · 12 min ago"),
            ("🌿", "Quiet corner of the city", "@liam · 1 hr ago"),
        ]
        for col, (icon, caption, meta) in zip(recent_cols, recent_posts):
            with col:
                st.markdown(
                    f'<div class="post-card" style="margin-bottom:0;">'
                    f'  <div style="font-size:4rem; text-align:center; line-height:1; margin-bottom:16px;">{icon}</div>'
                    f'  <div style="font-size:0.95rem; font-weight:800; color:var(--ss-text-1); margin-bottom:6px;">{caption}</div>'
                    f'  <div style="font-size:0.8rem; color:var(--ss-text-3);">{meta}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div class="glass-card" style="text-align:center; padding:28px 24px;">'
            '  <div style="font-size:1.2rem; font-weight:800; color:var(--ss-text-1); margin-bottom:8px;">Ready to start sharing?</div>'
            '  <div style="font-size:0.9rem; color:var(--ss-text-3);">Create your account or sign in to explore the full feed.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    # ── 2. SIGN IN ─────────────────────────────────────────────────
    elif choice == "🔑  Sign In":
        st.markdown("<br>", unsafe_allow_html=True)
        _, col_card, _ = st.columns([1, 1.3, 1])
        with col_card:
            st.markdown(
                '<div class="auth-card">'
                '  <div class="auth-logo">'
                '    <span class="gradient-text">SnapShare</span>'
                '  </div>'
                '  <div class="auth-title" style="font-size:1.35rem; font-weight:800; '
                '       color:var(--ss-auth-title); text-align:center; margin-bottom:4px;">'
                '    Welcome back 👋</div>'
                '  <div class="auth-subtitle" style="font-size:0.85rem; color:var(--ss-auth-subtitle); '
                '       text-align:center; margin-bottom:24px;">'
                '    Sign in to your account</div>',
                unsafe_allow_html=True,
            )

            with st.form("login_form"):
                l_username = st.text_input("Username", placeholder="e.g. johndoe")
                l_password = st.text_input("Password", type="password", placeholder="••••••••")
                submitted  = st.form_submit_button("🚀  Sign In", use_container_width=True,
                                                    type="primary")
                if submitted:
                    l_username = (l_username or "").strip()
                    if not l_username or not l_password:
                        st.error("Please fill in all fields.")
                    else:
                        ok, msg = auth.login_user(l_username, l_password)
                        if ok:
                            st.success("Welcome back! ✨")
                            st.rerun()
                        else:
                            st.error(msg)

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(
            '<div style="text-align:center; margin-top:16px; font-size:0.82rem; '
            'color:var(--ss-text-3);">'
            "Don't have an account? Use <strong>Create Account</strong> or the sidebar on desktop."
            '</div>',
            unsafe_allow_html=True,
        )

    # ── 3. CREATE ACCOUNT ──────────────────────────────────────────
    elif choice == "✨  Create Account":
        st.markdown("<br>", unsafe_allow_html=True)
        _, col_card, _ = st.columns([1, 1.3, 1])
        with col_card:
            st.markdown(
                '<div class="auth-card">'
                '  <div class="auth-logo">'
                '    <span class="gradient-text">SnapShare</span>'
                '  </div>'
                '  <div class="auth-title" style="font-size:1.35rem; font-weight:800; '
                '       color:var(--ss-auth-title); text-align:center; margin-bottom:4px;">'
                '    Join SnapShare ✨</div>'
                '  <div class="auth-subtitle" style="font-size:0.85rem; color:var(--ss-auth-subtitle); '
                '       text-align:center; margin-bottom:24px;">'
                '    Create your free account</div>',
                unsafe_allow_html=True,
            )

            with st.form("signup_form"):
                s_username = st.text_input("Username", placeholder="3–20 chars, letters & numbers")
                s_email    = st.text_input("Email", placeholder="you@example.com")
                s_bio      = st.text_area("Bio (optional)", max_chars=150,
                                          placeholder="Tell the world about yourself…", height=80)
                s_password = st.text_input("Password", type="password",
                                            placeholder="Min 6 characters")
                s_confirm  = st.text_input("Confirm Password", type="password",
                                            placeholder="Repeat password")
                submitted  = st.form_submit_button("✨  Create Account",
                                                    use_container_width=True, type="primary")
                if submitted:
                    s_username = (s_username or "").strip()
                    s_email = (s_email or "").strip()
                    if s_password != s_confirm:
                        st.error("Passwords don't match.")
                    else:
                        ok, msg = auth.register_user(s_username, s_email, s_password, s_bio)
                        if ok:
                            st.session_state["nav_target"] = "🔑  Sign In"
                            st.success("Account created! Sign in to get started. ✨")
                            st.rerun()
                        else:
                            st.error(msg)

            st.markdown('</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────────────────────────
# LOGGED-IN SCREENS
# ──────────────────────────────────────────────────────────────────
else:
    current_uid   = st.session_state["user_id"]
    current_uname = st.session_state["username"]

    try:
        unread_notifs = database.get_unread_notifications_count(current_uid)
    except Exception:
        unread_notifs = 0

    # Dynamic profile override
    if st.session_state["view_profile_id"] is not None:
        if st.button("⬅️  Back", key="back_from_profile"):
            clear_profile_view()
            st.rerun()
        else:
            profile.render_profile_view(st.session_state["view_profile_id"], current_uid)
        st.stop()

    # ── Clear profile context on non-search pages ─────────────────
    if choice not in ["🔍  Search", "🏠  Home Feed", "🔥  Explore", "✨  Trending"]:
        clear_profile_view()

    # ── HOME FEED ──────────────────────────────────────────────────
    if choice == "🏠  Home Feed":
        feed.render_feed_view("home", current_uid)

    # ── EXPLORE ────────────────────────────────────────────────────
    elif choice == "🔥  Explore":
        feed.render_feed_view("latest", current_uid)

    # ── TRENDING ───────────────────────────────────────────────────
    elif choice == "✨  Trending":
        feed.render_feed_view("personalized", current_uid)

    # ── UPLOAD ─────────────────────────────────────────────────────
    elif choice == "📷  Upload":
        # ── Upload page custom styles ───────────────────────────────
        st.markdown("""
        <style>
        .upload-hero {
            background: linear-gradient(135deg, rgba(139,92,246,0.08) 0%, rgba(236,72,153,0.05) 100%);
            border: 1px solid var(--ss-border);
            border-radius: 24px;
            padding: 32px 36px 24px;
            margin-bottom: 28px;
            animation: fadeIn 0.4s ease both;
            position: relative;
            overflow: hidden;
        }
        .upload-hero::before {
            content: '';
            position: absolute;
            top: -40px; right: -40px;
            width: 180px; height: 180px;
            background: radial-gradient(circle, rgba(139,92,246,0.15), transparent 70%);
            pointer-events: none;
        }
        .upload-hero-badge {
            display: inline-block;
            background: rgba(139,92,246,0.12);
            color: #a78bfa;
            border: 1px solid rgba(139,92,246,0.3);
            border-radius: 100px;
            padding: 4px 14px;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }
        .upload-hero-title {
            font-size: 2rem;
            font-weight: 900;
            letter-spacing: -0.03em;
            color: var(--ss-text-1);
            margin-bottom: 6px;
        }
        .upload-hero-sub {
            font-size: 0.88rem;
            color: var(--ss-text-3);
        }
        /* Preview zone */
        .preview-zone {
            background: var(--ss-card);
            border: 2px dashed var(--ss-border-strong);
            border-radius: 20px;
            text-align: center;
            padding: 40px 24px;
            transition: all 0.25s ease;
            cursor: pointer;
        }
        .preview-zone:hover {
            border-color: rgba(139,92,246,0.6);
            background: rgba(139,92,246,0.04);
        }
        .preview-zone-icon { font-size: 3.5rem; margin-bottom: 12px; animation: float 3s ease-in-out infinite; }
        .preview-zone-title { font-size: 1.05rem; font-weight: 700; color: var(--ss-text-1); margin-bottom: 6px; }
        .preview-zone-sub { font-size: 0.82rem; color: var(--ss-text-3); }
        /* Metadata card */
        .meta-card {
            background: var(--ss-card);
            border: 1px solid var(--ss-border);
            border-radius: 16px;
            padding: 16px 20px;
            margin-top: 16px;
            animation: fadeInUp 0.3s ease both;
        }
        .meta-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 5px 0;
            border-bottom: 1px solid var(--ss-border);
            font-size: 0.82rem;
        }
        .meta-row:last-child { border-bottom: none; }
        .meta-label { color: var(--ss-text-3); font-weight: 600; }
        .meta-value { color: var(--ss-text-1); font-weight: 700; }
        /* Compression stats */
        .compression-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            margin-top: 14px;
        }
        .compression-stat {
            background: rgba(139,92,246,0.07);
            border: 1px solid rgba(139,92,246,0.18);
            border-radius: 14px;
            padding: 14px 12px;
            text-align: center;
        }
        .compression-stat-val {
            font-size: 1.3rem;
            font-weight: 900;
            background: linear-gradient(135deg, #a78bfa, #f472b6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .compression-stat-lbl {
            font-size: 0.72rem;
            color: var(--ss-text-3);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 2px;
        }
        /* Success panel */
        .success-panel {
            background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(139,92,246,0.06));
            border: 1px solid rgba(16,185,129,0.25);
            border-radius: 20px;
            padding: 32px 24px;
            text-align: center;
            animation: fadeInUp 0.4s ease both;
        }
        .success-panel-icon { font-size: 3.5rem; margin-bottom: 12px; }
        .success-panel-title { font-size: 1.3rem; font-weight: 800; color: #34d399; margin-bottom: 6px; }
        .success-panel-sub { font-size: 0.87rem; color: var(--ss-text-2); }
        /* Validation pill */
        .val-ok   { color: #34d399; font-weight: 700; }
        .val-warn { color: #fbbf24; font-weight: 700; }
        .val-err  { color: #f87171; font-weight: 700; }
        /* Pipeline step states */
        .pipe-step-done { opacity: 1; border-color: rgba(16,185,129,0.4) !important; }
        .pipe-step-active { border-color: rgba(139,92,246,0.5) !important; }
        </style>
        """, unsafe_allow_html=True)

        # Hero header
        st.markdown(
            '<div class="upload-hero">'
            '  <div class="upload-hero-badge">📷 New Post</div>'
            '  <div class="upload-hero-title">Share a Moment</div>'
            '  <div class="upload-hero-sub">Your photo will be auto-optimised and published instantly to your followers.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        col_upload, col_info = st.columns([1.55, 1])

        with col_upload:
            # ── File uploader (drag-and-drop zone) ─────────────────
            uploaded_img = st.file_uploader(
                "Drop your photo here, or click to browse",
                type=["jpg", "jpeg", "png"],
                help="Supported formats: JPG, JPEG, PNG. Max recommended size: 20 MB.",
            )

            # ── Image Preview & Metadata ────────────────────────────
            if uploaded_img is not None:
                from PIL import Image as PilImage
                import io

                # Read for preview
                img_bytes = uploaded_img.read()
                uploaded_img.seek(0)  # Reset for later upload use

                pil_img = PilImage.open(io.BytesIO(img_bytes))
                orig_w, orig_h = pil_img.size
                orig_mode = pil_img.mode
                orig_size_kb = round(len(img_bytes) / 1024, 1)
                file_ext = uploaded_img.name.split(".")[-1].upper()
                needs_convert = orig_mode in ("RGBA", "P")
                needs_resize  = orig_w > 1080

                # Live preview
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                st.image(
                    img_bytes,
                    caption=f"Preview — {uploaded_img.name}",
                    use_container_width=True,
                )

                # Metadata card
                st.markdown(
                    '<div class="meta-card">'
                    '  <div style="font-size:0.82rem; font-weight:800; color:var(--ss-text-1); margin-bottom:10px;">📋 Image Metadata</div>'
                    f'  <div class="meta-row"><span class="meta-label">Filename</span><span class="meta-value">{uploaded_img.name}</span></div>'
                    f'  <div class="meta-row"><span class="meta-label">Format</span><span class="meta-value">{file_ext} · {orig_mode}</span></div>'
                    f'  <div class="meta-row"><span class="meta-label">Dimensions</span><span class="meta-value">{orig_w} × {orig_h} px</span></div>'
                    f'  <div class="meta-row"><span class="meta-label">File size</span><span class="meta-value">{orig_size_kb} KB</span></div>'
                    f'  <div class="meta-row"><span class="meta-label">Resize needed</span>'
                    f'    <span class="{"val-warn" if needs_resize else "val-ok"}">{"⚠️ Will resize to 1080px" if needs_resize else "✅ No resize needed"}</span>'
                    f'  </div>'
                    f'  <div class="meta-row"><span class="meta-label">Color conversion</span>'
                    f'    <span class="{"val-warn" if needs_convert else "val-ok"}">{"⚠️ Will convert to RGB" if needs_convert else "✅ Already RGB"}</span>'
                    f'  </div>'
                    '</div>',
                    unsafe_allow_html=True,
                )

            else:
                # Empty drop zone placeholder
                st.markdown(
                    '<div class="preview-zone">'
                    '  <div class="preview-zone-icon">🖼️</div>'
                    '  <div class="preview-zone-title">No photo selected yet</div>'
                    '  <div class="preview-zone-sub">Use the uploader above to choose or drag a JPG / PNG file.</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

            # Caption input
            caption_text = st.text_area(
                "Caption",
                max_chars=2200,
                placeholder="Write something about this moment… (optional, max 2200 chars)",
                height=90,
            )
            char_count = len(caption_text) if caption_text else 0
            cap_pct = round(char_count / 2200 * 100)
            cap_color = "#34d399" if cap_pct < 70 else ("#fbbf24" if cap_pct < 90 else "#f87171")
            st.markdown(
                f'<div style="font-size:0.75rem; color:{cap_color}; text-align:right; margin-top:-6px; margin-bottom:12px;">'
                f'{char_count} / 2200 characters</div>',
                unsafe_allow_html=True,
            )

            # Share button
            share_btn = st.button("🚀  Share Post", use_container_width=True, type="primary", key="share_post_btn")

            if share_btn:
                # ── Validation ──────────────────────────────────────
                if not uploaded_img:
                    st.markdown(
                        '<div style="background:rgba(248,113,113,0.08); border:1px solid rgba(248,113,113,0.3); '
                        'border-radius:14px; padding:14px 18px; margin-top:12px; font-size:0.88rem; color:#fca5a5;">'
                        '  <strong>⚠️ No photo selected.</strong> Please choose a JPG or PNG file before sharing.'
                        '</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    # ── Upload progress simulation ───────────────────
                    prog_bar = st.progress(0, text="⏳ Starting upload...")
                    prog_bar.progress(15, text="🔍 Validating image format...")
                    import time as _time; _time.sleep(0.2)
                    prog_bar.progress(35, text="🎨 Converting color space...")
                    _time.sleep(0.2)
                    prog_bar.progress(55, text="📐 Resizing to 1080px (if needed)...")
                    _time.sleep(0.2)
                    prog_bar.progress(72, text="🗜️ Compressing with Pillow quality=75...")
                    _time.sleep(0.2)
                    prog_bar.progress(88, text="💾 Saving to /uploads & registering in DB...")
                    _time.sleep(0.1)

                    try:
                        uploaded_img.seek(0)
                        ok, msg, meta = posts.upload_post_with_metadata(current_uid, uploaded_img, caption_text)
                        prog_bar.progress(100, text="✅ Complete!")
                        _time.sleep(0.3)
                        prog_bar.empty()

                        if ok and meta:
                            st.balloons()
                            # Success panel
                            st.markdown(
                                '<div class="success-panel">'
                                '  <div class="success-panel-icon">🎉</div>'
                                '  <div class="success-panel-title">Post Published!</div>'
                                '  <div class="success-panel-sub">Your photo is live and visible to your followers.</div>'
                                '</div>',
                                unsafe_allow_html=True,
                            )
                            # Compression results
                            savings_label = f"{meta['savings_pct']}% saved" if meta['savings_pct'] > 0 else "Optimised"
                            fd_w, fd_h = meta["final_dims"]
                            st.markdown(
                                '<div style="margin-top:16px;">'
                                '<div style="font-size:0.82rem; font-weight:800; color:var(--ss-text-1); margin-bottom:10px;">⚡ Compression Results</div>'
                                '<div class="compression-grid">'
                                f'  <div class="compression-stat">'
                                f'    <div class="compression-stat-val">{meta["original_size_kb"]} KB</div>'
                                f'    <div class="compression-stat-lbl">Original</div>'
                                f'  </div>'
                                f'  <div class="compression-stat">'
                                f'    <div class="compression-stat-val">{meta["compressed_size_kb"]} KB</div>'
                                f'    <div class="compression-stat-lbl">Compressed</div>'
                                f'  </div>'
                                f'  <div class="compression-stat">'
                                f'    <div class="compression-stat-val">{savings_label}</div>'
                                f'    <div class="compression-stat-lbl">Space saved</div>'
                                f'  </div>'
                                '</div>'
                                f'<div style="font-size:0.78rem; color:var(--ss-text-3); margin-top:10px; text-align:center;">'
                                f'  Final output: {fd_w} × {fd_h} px · JPEG quality 75'
                                f'  {"· Resized ✂️" if meta["was_resized"] else "· No resize needed ✅"}'
                                f'</div>'
                                '</div>',
                                unsafe_allow_html=True,
                            )
                        elif ok:
                            st.success(msg)
                            st.balloons()
                        else:
                            prog_bar.empty()
                            st.markdown(
                                f'<div style="background:rgba(248,113,113,0.08); border:1px solid rgba(248,113,113,0.3); '
                                f'border-radius:14px; padding:14px 18px; margin-top:12px; font-size:0.88rem; color:#fca5a5;">'
                                f'  <strong>❌ Upload failed.</strong> {msg}'
                                f'</div>',
                                unsafe_allow_html=True,
                            )
                    except Exception as exc:
                        prog_bar.empty()
                        st.markdown(
                            f'<div style="background:rgba(248,113,113,0.08); border:1px solid rgba(248,113,113,0.3); '
                            f'border-radius:14px; padding:14px 18px; margin-top:12px; font-size:0.88rem; color:#fca5a5;">'
                            f'  <strong>❌ Unexpected error:</strong> {exc}'
                            f'</div>',
                            unsafe_allow_html=True,
                        )

        with col_info:
            # ── Processing Pipeline Panel ───────────────────────────
            st.markdown(
                '<div class="glass-card" style="padding:22px 24px;">'
                '  <div style="font-size:0.95rem; font-weight:800; color:var(--ss-text-1); margin-bottom:18px;">🔧 Processing Pipeline</div>',
                unsafe_allow_html=True,
            )
            pipeline_steps = [
                ("✅", "Format Check", "JPG, JPEG, PNG accepted", "#34d399"),
                ("📐", "Resize",       "Max 1080px width — aspect ratio locked", "#a78bfa"),
                ("🗜️", "Compress",    "Pillow quality=75 → up to 70% reduction", "#f472b6"),
                ("💾", "Persist",      "Saved to /uploads + SQLite record created", "#60a5fa"),
            ]
            for icon, title, desc, color in pipeline_steps:
                st.markdown(
                    f'<div style="display:flex; align-items:flex-start; gap:12px; padding:10px 0; border-bottom:1px solid var(--ss-border);">'
                    f'  <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,{color}22,{color}11);'
                    f'       border:1px solid {color}44; display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:1rem;">{icon}</div>'
                    f'  <div>'
                    f'    <div style="font-size:0.85rem; font-weight:700; color:var(--ss-text-1);">{title}</div>'
                    f'    <div style="font-size:0.77rem; color:var(--ss-text-3); line-height:1.4;">{desc}</div>'
                    f'  </div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

            # ── Upload guidelines ───────────────────────────────────
            st.markdown(
                '<div class="glass-card" style="padding:22px 24px;">'
                '  <div style="font-size:0.95rem; font-weight:800; color:var(--ss-text-1); margin-bottom:14px;">📋 Upload Guidelines</div>',
                unsafe_allow_html=True,
            )
            guidelines = [
                ("✅", "JPG, JPEG, or PNG format"),
                ("✅", "Any resolution — we auto-resize"),
                ("✅", "RGBA / transparent PNGs supported"),
                ("⚡", "Files over 1080px are downscaled"),
                ("🗜️", "All images compressed at quality 75"),
                ("🔒", "Posts are tied to your account"),
            ]
            for gicon, gtxt in guidelines:
                st.markdown(
                    f'<div style="display:flex; align-items:center; gap:10px; padding:7px 0; '
                    f'border-bottom:1px solid var(--ss-border); font-size:0.82rem; color:var(--ss-text-2);">'
                    f'  <span style="flex-shrink:0;">{gicon}</span>{gtxt}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
            st.markdown('</div>', unsafe_allow_html=True)



    # ── SEARCH ─────────────────────────────────────────────────────
    elif choice == "🔍  Search":
        # Custom visual styling for the Search screen
        st.markdown(
            """
            <style>
            .search-header-wrap {
                background: linear-gradient(135deg, var(--ss-card) 0%, rgba(139,92,246,0.05) 100%);
                border: 1px solid var(--ss-border);
                border-radius: 20px;
                padding: 24px;
                margin-bottom: 24px;
                text-align: center;
                animation: fadeIn 0.4s ease both;
            }
            .search-tagline {
                font-size: 0.82rem;
                color: var(--ss-text-3);
                letter-spacing: 0.05em;
                text-transform: uppercase;
                margin-bottom: 8px;
            }
            .search-title {
                font-size: 1.8rem;
                font-weight: 900;
                color: var(--ss-text-1);
                margin-bottom: 6px;
                letter-spacing: -0.03em;
            }
            .search-desc {
                font-size: 0.88rem;
                color: var(--ss-text-2);
                max-width: 520px;
                margin: 0 auto;
                line-height: 1.5;
            }
            .search-bar-container {
                margin-bottom: 28px;
            }
            .section-title {
                font-size: 1.1rem;
                font-weight: 800;
                color: var(--ss-text-1);
                margin-bottom: 16px;
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .empty-state {
                text-align: center;
                padding: 50px 24px;
                background: var(--ss-card);
                border: 1px solid var(--ss-border);
                border-radius: 24px;
                animation: fadeInUp 0.4s ease both;
            }
            .empty-icon {
                font-size: 3.5rem;
                margin-bottom: 16px;
                animation: float 3s ease-in-out infinite;
            }
            </style>
            <div class="search-header-wrap">
              <div class="search-tagline">Network & Explore</div>
              <div class="search-title">Discover Creators</div>
              <div class="search-desc">
                Search the community, follow trending designers, or connect with recommended profiles.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Search Bar Input
        search_q = st.text_input(
            "search_users_input",
            placeholder="🔍 Search by username or bio snippet...",
            label_visibility="collapsed"
        ).strip()

        st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)

        if search_q:
            # SEARCH RESULTS MODE
            results = database.search_users(search_q)
            st.markdown(
                f'<div class="section-title">🔍 Search Results ({len(results)})</div>',
                unsafe_allow_html=True
            )

            if not results:
                # Better Empty Search State
                st.markdown(
                    '<div class="empty-state">'
                    '  <div class="empty-icon">🔍</div>'
                    '  <div style="font-size: 1.3rem; font-weight: 800; color: var(--ss-text-1); margin-bottom: 8px;">'
                    '    No Creators Found'
                    '  </div>'
                    '  <div style="font-size: 0.88rem; color: var(--ss-text-2); max-width: 440px; margin: 0 auto 24px; line-height: 1.6;">'
                    f'    We couldn\'t find any profiles matching "<strong>{search_q}</strong>". Check spelling or try a different term.'
                    '  </div>'
                    '</div>',
                    unsafe_allow_html=True
                )
                
                # Show suggestions below empty search as fallback
                st.markdown('<div style="height: 24px;"></div>', unsafe_allow_html=True)
                st.markdown(
                    '<div class="section-title">💡 Suggested Profiles</div>',
                    unsafe_allow_html=True
                )
                suggested = database.get_suggested_users(current_uid, limit=3)
                if suggested:
                    cols = st.columns(3)
                    for idx, user in enumerate(suggested):
                        with cols[idx % 3]:
                            _render_user_card(user["id"], user["username"], user["bio"], current_uid, suffix="empty_search")
            else:
                # Results Grid (3 Columns)
                cols = st.columns(3)
                for idx, row in enumerate(results):
                    with cols[idx % 3]:
                        _render_user_card(row["id"], row["username"], row["bio"], current_uid, suffix="search_results")
        else:
            # DISCOVERY MODE (Default)
            try:
                conn = database.get_db_connection()
                other_users_count = conn.execute("SELECT COUNT(*) FROM users WHERE id != ?;", (current_uid,)).fetchone()[0]
                conn.close()
            except Exception:
                other_users_count = 0

            if other_users_count == 0:
                # Better Empty DB State UI
                st.markdown(
                    '<div class="empty-state" style="max-width: 680px; margin: 0 auto;">'
                    '  <div class="empty-icon">🪐</div>'
                    '  <div style="font-size: 1.4rem; font-weight: 800; color: var(--ss-text-1); margin-bottom: 8px;">'
                    '    A Quiet Universe'
                    '  </div>'
                    '  <div style="font-size: 0.9rem; color: var(--ss-text-2); max-width: 500px; margin: 0 auto 28px; line-height: 1.65;">'
                    '    It looks like you are the first pioneer here! To make exploration exciting, you can generate simulated creator accounts complete with bios and follow connections instantly.'
                    '  </div>'
                    '</div>',
                    unsafe_allow_html=True
                )
                
                # Centered generate demo button
                c_left, c_mid, c_right = st.columns([1, 1.8, 1])
                with c_mid:
                    if st.button("⚡ Generate Demo Creators", key="gen_demo_empty", use_container_width=True, type="primary"):
                        with st.spinner("Generating beautiful profiles..."):
                            num_created = database.generate_demo_users()
                            st.success(f"Generated {num_created} demo creators! Page reloading...")
                            st.rerun()
            else:
                col_trend, col_suggest = st.columns([1.1, 1.0])

                with col_trend:
                    st.markdown(
                        '<div class="section-title">🔥 Trending Creators</div>',
                        unsafe_allow_html=True
                    )
                    trending = database.get_trending_creators(limit=4)
                    if not trending:
                        st.caption("No trending creators yet.")
                    else:
                        for creator in trending:
                            _render_user_card(
                                creator["id"],
                                creator["username"],
                                creator["bio"],
                                current_uid,
                                suffix="trending"
                            )

                with col_suggest:
                    st.markdown(
                        '<div class="section-title">💡 Suggested for You</div>',
                        unsafe_allow_html=True
                    )
                    suggested = database.get_suggested_users(current_uid, limit=4)
                    
                    # Fallback if no suggested (e.g. they already follow all users)
                    if not suggested:
                        try:
                            # Show any users they already follow or just other users
                            conn = database.get_db_connection()
                            suggested = conn.execute(
                                "SELECT id, username, bio, profile_pic FROM users WHERE id != ? LIMIT 4;",
                                (current_uid,)
                            ).fetchall()
                            conn.close()
                        except Exception:
                            suggested = []
                            
                    if not suggested:
                        st.caption("No other profiles available yet.")
                    else:
                        for user in suggested:
                            _render_user_card(
                                user["id"],
                                user["username"],
                                user["bio"],
                                current_uid,
                                suffix="suggested"
                            )


    # ── NOTIFICATIONS ──────────────────────────────────────────────
    elif "Notifications" in choice:
        st.markdown(
            f'<div style="font-size:1.6rem; font-weight:900; letter-spacing:-0.03em; '
            f'color:var(--ss-text-1); margin-bottom:20px;">🔔  Activity'
            f'{"  <span style=\'background:linear-gradient(135deg,#8b5cf6,#ec4899);"
               "-webkit-background-clip:text;-webkit-text-fill-color:transparent;"
               "font-size:1rem;font-weight:800;\'>" + str(unread_notifs) + " new</span>" if unread_notifs > 0 else ""}'
            f'</div>',
            unsafe_allow_html=True,
        )

        if unread_notifs > 0:
            if st.button("✓  Mark all as read", key="mark_all_read"):
                database.mark_notifications_as_read(current_uid)
                st.rerun()

        notifs = database.get_notifications(current_uid)
        if not notifs:
            st.markdown(
                '<div class="glass-card" style="text-align:center; padding:48px 24px;">'
                '  <div style="font-size:3rem; margin-bottom:14px;">🔕</div>'
                '  <div style="color:var(--ss-text-3); font-size:0.9rem;">'
                '       No notifications yet. Start following people!'
                '  </div>'
                '</div>',
                unsafe_allow_html=True,
            )
        else:
            for notif in notifs:
                sender   = notif["sender_name"] or "Deleted User"
                ntype    = notif["type"] or "unknown"
                created  = notif["created_at"]
                is_unread = notif["is_read"] == 0
                post_id  = notif["post_id"]

                icons = {"like": "❤️", "comment": "💬", "follow": "👤"}
                msgs  = {
                    "like":    "liked your post",
                    "comment": "commented on your post",
                    "follow":  "started following you",
                }
                icon = icons.get(ntype, "🔔")
                msg  = msgs.get(ntype, "interacted with you")

                bg = "var(--ss-nav-hover)" if is_unread else "transparent"
                bd = "var(--ss-border-strong)" if is_unread else "var(--ss-border)"

                st.markdown(
                    f'<div class="notification-item" '
                    f'style="background:{bg}; border:1px solid {bd};">'
                    f'  <div class="user-avatar-small" style="width:36px;height:36px;font-size:0.85rem;">'
                    f'    {sender[0].upper()}</div>'
                    f'  <div style="flex:1;">'
                    f'    <div style="font-size:0.88rem; color:var(--ss-text-1);">'
                    f'      {icon} <strong>@{sender}</strong> {msg}'
                    f'      {"<span style=\'display:inline-block;width:7px;height:7px;"
                               "background:#8b5cf6;border-radius:50%;margin-left:6px;\'></span>" if is_unread else ""}'
                    f'    </div>'
                    f'    <div style="font-size:0.74rem; color:var(--ss-text-3); margin-top:2px;">'
                    f'      {feed.format_timestamp(created)}</div>'
                    f'  </div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                if post_id:
                    try:
                        with st.expander("View post"):
                            post_row = database.get_post_by_id(post_id)
                            if post_row and os.path.exists(post_row["image_path"]):
                                st.image(post_row["image_path"], width=280)
                                if post_row["caption"]:
                                    st.caption(post_row["caption"])
                            else:
                                st.caption("Post has been deleted.")
                    except Exception as exc:
                        st.caption(f"Could not load post: {exc}")

    # ── MY PROFILE ─────────────────────────────────────────────────
    elif choice == "👤  My Profile":
        profile.render_profile_view(current_uid, current_uid)

    # ── EDIT PROFILE ───────────────────────────────────────────────
    elif choice == "✏️  Edit Profile":
        profile.render_edit_profile(current_uid)

    # ── SETTINGS ───────────────────────────────────────────────────
    elif choice == "⚙️  Settings":
        st.markdown(
            '<div style="font-size:1.6rem; font-weight:900; letter-spacing:-0.03em; '
            'color:var(--ss-text-1); margin-bottom:24px;">⚙️  Settings</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.markdown(
                '<div class="settings-section-label" style="font-size:0.78rem; '
                'text-transform:uppercase; margin-bottom:14px;">'
                '👤 Account</div>',
                unsafe_allow_html=True,
            )
            st.markdown(f"Signed in as **@{current_uname}**")
            st.caption("Use the sidebar to switch between light and dark mode.")

        with st.container(border=True):
            st.markdown(
                '<div class="settings-section-label" style="font-size:0.78rem; '
                'text-transform:uppercase; margin-bottom:14px;">'
                '🔐 Session</div>',
                unsafe_allow_html=True,
            )
            st.caption("Logging out clears your session and returns you to the sign-in screen.")
            if st.button("🚪  Sign Out", use_container_width=True, type="primary"):
                auth.logout_user()

    # ── SIGN OUT ───────────────────────────────────────────────────
    elif choice == "🚪  Sign Out":
        auth.logout_user()

    # ── WELCOME DASHBOARD (default / architecture) ─────────────────
    else:
        try:
            _user_data    = database.get_user_by_id(current_uid)
            _posts_count  = len(database.get_posts_by_user(current_uid))
            _followers    = database.get_followers_count(current_uid)
            _following    = database.get_following_count(current_uid)
        except Exception:
            _user_data = None; _posts_count = _followers = _following = 0

        st.markdown(
            f'<div class="hero-section" style="padding:28px 0 20px; text-align:left;">'
            f'  <div class="hero-badge">Dashboard</div>'
            f'  <div style="font-size:2.2rem; font-weight:900; letter-spacing:-0.04em; '
            f'       color:var(--ss-text-1); margin-bottom:6px;">'
            f'    Welcome back, <span class="gradient-text">@{current_uname}</span> 👋</div>'
            f'  <div style="font-size:0.9rem; color:var(--ss-text-3);">'
            f'    Here\'s your SnapShare overview.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Posts",     _posts_count)
        m2.metric("Followers", _followers)
        m3.metric("Following", _following)
        m4.metric("Unread 🔔", unread_notifs)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="glass-card">'
            '  <div style="font-size:0.95rem; font-weight:800; '
            '       color:var(--ss-text-1); margin-bottom:16px;">🗺️ Quick Navigation</div>',
            unsafe_allow_html=True,
        )
        nav_items = [
            ("🏠", "Home Feed",   "Posts from followed users"),
            ("🔥", "Explore",     "Browse all latest posts"),
            ("✨", "Trending",    "Highest-engagement posts"),
            ("📷", "Upload",      "Share a new moment"),
            ("🔍", "Search",      "Discover people"),
        ]
        nav_cols = st.columns(2)
        for idx, (ico, lbl, desc) in enumerate(nav_items):
            with nav_cols[idx % 2]:
                st.markdown(
                    f'<div class="pipeline-step">'
                    f'  <span style="font-size:1.2rem;">{ico}</span>'
                    f'  <div><div style="font-size:0.88rem; font-weight:700; '
                    f'       color:var(--ss-text-1);">{lbl}</div>'
                    f'  <div style="font-size:0.77rem; color:var(--ss-text-3);">{desc}</div></div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        st.markdown('</div>', unsafe_allow_html=True)
