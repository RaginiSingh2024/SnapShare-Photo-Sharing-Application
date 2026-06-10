import streamlit as st
import os

# Set page config FIRST to prevent Streamlit error
st.set_page_config(
    page_title="SnapShare - Instagram for Academics",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded"
)

import database
import auth
import feed
import profile
import posts

# Initialize Database on startup
database.init_db()

# Custom CSS for Premium Glassmorphism Dark Mode Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* Apply font globally */
html, body, [class*="css"], .stApp {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background-color: #080c14;
    color: #f3f4f6;
}

/* Glassmorphism Card Style */
.glass-card {
    background: rgba(17, 24, 39, 0.7);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.45);
    margin-bottom: 24px;
}

/* Post Container Card */
.post-card {
    background: rgba(17, 24, 39, 0.85);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 24px;
    padding: 20px;
    margin-bottom: 30px;
    box-shadow: 0 6px 24px rgba(0,0,0,0.3);
}

/* Interactive elements styles */
.stButton>button {
    background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
    color: white !important;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.25);
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(236, 72, 153, 0.45);
    border: none;
}

/* Inputs styling */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background-color: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f3f4f6 !important;
    border-radius: 10px !important;
}

/* Custom rounded small avatar */
.user-avatar-small {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
    color: white;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.15rem;
    border: 2px solid rgba(255, 255, 255, 0.15);
}

/* Custom rounded large avatar */
.user-avatar-large {
    width: 96px;
    height: 96px;
    border-radius: 50%;
    background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);
    color: white;
    font-weight: 800;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.6rem;
    border: 4px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
}

/* Title text */
.gradient-text {
    background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* Feed Headers */
.feed-header {
    background: rgba(255, 255, 255, 0.02);
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    padding: 16px 24px;
    border-radius: 16px;
    margin-bottom: 24px;
}

/* Notification Card */
.notification-item {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 14px 20px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: background 0.2s ease;
}

.notification-item:hover {
    background: rgba(255, 255, 255, 0.06);
}
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE STABILIZATION -----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "username" not in st.session_state:
    st.session_state["username"] = None
if "view_profile_id" not in st.session_state:
    st.session_state["view_profile_id"] = None

# Helper to redirect to profile page
def view_profile(user_id):
    st.session_state["view_profile_id"] = user_id
    st.rerun()

# Clear dynamic profile viewing
def clear_profile_view():
    st.session_state["view_profile_id"] = None

# Sidebar Branding
st.sidebar.markdown("""
<div style="text-align: center; padding: 15px 0;">
    <h1 style="margin: 0; font-size: 2rem;" class="gradient-text">SnapShare</h1>
    <p style="color: #64748b; font-size: 0.85rem; margin-top: 5px;">Instagram-like System Design Project</p>
</div>
<hr style="border: 0.5px solid rgba(255,255,255,0.1); margin-bottom: 20px;">
""", unsafe_allow_html=True)

# ----------------- NAVIGATION ROUTING -----------------
if not st.session_state["logged_in"]:
    # Anonymous Navigation
    menu = ["👋 Splash Screen", "🔑 Log In", "📝 Sign Up"]
    choice = st.sidebar.radio("Navigation", menu)

    # 1. SPLASH SCREEN
    if choice == "👋 Splash Screen":
        st.markdown("""
        <div style="text-align: center; margin-top: 40px; margin-bottom: 40px;">
            <h1 style="font-size: 4rem; margin: 0;" class="gradient-text">SnapShare</h1>
            <p style="font-size: 1.3rem; color: #a1a1aa; margin-top: 10px;">
                Designing a Highly Scalable, Beautiful, and Premium Photo Sharing Platform
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1.5, 1])
        with col1:
            st.markdown("""
            <div class="glass-card">
                <h3 style="color: #ffffff; margin-top: 0;">🎓 Academic Project Overview</h3>
                <p style="line-height: 1.6; color: #d1d5db; font-size: 0.95rem;">
                    SnapShare is an end-to-end photo sharing application modeled after industry giants like Instagram. 
                    This project satisfies final-year System Design academic requirements by implementing functional application layers 
                    integrated with a database layer, alongside detailed architectural designs for scalable production environments.
                </p>
                <h4 style="color: #a78bfa; margin-bottom: 8px;">Key Capabilities Handled:</h4>
                <ul style="color: #d1d5db; padding-left: 20px; line-height: 1.7; font-size: 0.9rem;">
                    <li><strong>Authentication:</strong> Secure hashing & session management</li>
                    <li><strong>Media Engine:</strong> Image upload, automatic resizing & lossy/lossless compression</li>
                    <li><strong>Interactions:</strong> Real-time likes, comment thread structures, and follower graphs</li>
                    <li><strong>Activity System:</strong> Custom notifications triggered on follower & post engagements</li>
                    <li><strong>Feed System:</strong> Chronological feeds & engagement-based personalization sorting</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h3 style="color: #ffffff; margin-top:0;">🚀 Experience the Platform</h3>
                <p style="color: #a1a1aa; font-size: 0.9rem; margin-bottom: 24px;">
                    Register an account or log in to interact with feeds, upload files, comment, like, and follow users.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Sign Up Now", use_container_width=True):
                    # In Streamlit, navigating directly changes radio selection if we trigger state changes,
                    # but since choice is read directly, a simple toast asking them to use sidebar works best.
                    st.info("Please select 'Sign Up' in the sidebar.")
            with c2:
                if st.button("Log In Now", use_container_width=True):
                    st.info("Please select 'Log In' in the sidebar.")

            st.markdown("""
            <div class="glass-card" style="margin-top: 20px; text-align: left; padding: 20px;">
                <h4 style="color: #ffffff; margin-top: 0; margin-bottom: 8px;">📊 Database Metadata</h4>
                <p style="color: #a1a1aa; font-size: 0.85rem; margin: 0; line-height: 1.5;">
                    Built on <strong>SQLite DB</strong><br>
                    Includes 6 tables, relational Foreign Keys, and optimized Indexes on post listings and follower lookups.
                </p>
            </div>
            """, unsafe_allow_html=True)

    # 2. LOGIN SCREEN
    elif choice == "🔑 Log In":
        st.markdown("<h2 style='text-align: center; color: #ffffff;'>Log In to SnapShare</h2>", unsafe_allow_html=True)
        col_space1, col_login, col_space2 = st.columns([1, 1.5, 1])
        with col_login:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            l_username = st.text_input("Username").strip()
            l_password = st.text_input("Password", type="password")
            
            if st.button("Log In", use_container_width=True):
                success, msg = auth.login_user(l_username, l_password)
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            st.markdown('</div>', unsafe_allow_html=True)

    # 3. SIGNUP SCREEN
    elif choice == "📝 Sign Up":
        st.markdown("<h2 style='text-align: center; color: #ffffff;'>Create an Account</h2>", unsafe_allow_html=True)
        col_space1, col_signup, col_space2 = st.columns([1, 1.5, 1])
        with col_signup:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            s_username = st.text_input("Username", help="Alphanumeric, 3-20 characters").strip()
            s_email = st.text_input("Email").strip()
            s_bio = st.text_area("Bio (Optional)", max_chars=150)
            s_password = st.text_input("Password", type="password", help="Minimum 6 characters")
            s_confirm = st.text_input("Confirm Password", type="password")
            
            if st.button("Register", use_container_width=True):
                if s_password != s_confirm:
                    st.error("Passwords do not match.")
                else:
                    success, msg = auth.register_user(s_username, s_email, s_password, s_bio)
                    if success:
                        st.success(msg)
                        st.info("Switch to 'Log In' in the sidebar to enter.")
                    else:
                        st.error(msg)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # Logged In Navigation
    current_uid = st.session_state["user_id"]
    current_uname = st.session_state["username"]
    
    # Check notifications count for the sidebar badge
    unread_notifs = database.get_unread_notifications_count(current_uid)
    notif_label = f"🔔 Notifications ({unread_notifs})" if unread_notifs > 0 else "🔔 Notifications"

    # Define menu
    menu = [
        "👋 Welcome / Architecture",
        "🏠 Home Feed",
        "🔥 Explore Latest",
        "✨ Personalized Feed",
        "📷 Upload Photo",
        "🔍 Search Users",
        notif_label,
        "👤 My Profile",
        "✏️ Edit Profile",
        "⚙️ Settings",
        "🚪 Log Out"
    ]
    
    choice = st.sidebar.radio("Navigation", menu)

    # Clear dynamic profile viewing when clicking other options
    if choice not in ["🔍 Search Users", "🏠 Home Feed", "🔥 Explore Latest", "✨ Personalized Feed"] and notif_label not in choice:
        clear_profile_view()

    # Dynamic Routing Override if viewing someone else's profile
    if st.session_state["view_profile_id"] is not None:
        if st.button("⬅️ Back to Main Screen", key="back_from_profile_view"):
            clear_profile_view()
            st.rerun()
        else:
            profile.render_profile_view(st.session_state["view_profile_id"], current_uid)
    else:
        # Standard Screens

        # Welcome/Splash Screen
        if choice == "👋 Welcome / Architecture":
            st.markdown(f"""
            <div style="margin-top: 20px; margin-bottom: 20px;">
                <h1 style="font-size: 3rem;" class="gradient-text">Welcome, @{current_uname}!</h1>
                <p style="font-size: 1.15rem; color: #a1a1aa;">Explore SnapShare and examine its underlying System Architecture design.</p>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns([1.2, 1])
            with col1:
                st.markdown("""
                <div class="glass-card">
                    <h3 style="color:#ffffff; margin-top:0;">📂 Project Navigation Hints</h3>
                    <p style="line-height:1.6; color:#d1d5db; font-size:0.95rem;">
                        Use the sidebar to explore the platform:
                    </p>
                    <ul style="color:#d1d5db; padding-left:20px; line-height:1.7; font-size:0.9rem;">
                        <li><strong>Home Feed:</strong> View posts from users you follow.</li>
                        <li><strong>Explore Latest:</strong> View all global posts in real-time.</li>
                        <li><strong>Personalized Feed:</strong> View trending items calculated by engagement scores.</li>
                        <li><strong>Upload Photo:</strong> Share photos with compression automatically optimized.</li>
                        <li><strong>Search Users:</strong> Look up, inspect profiles, and follow accounts.</li>
                        <li><strong>Notifications:</strong> Track new follows, likes, and comments left on your uploads.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="glass-card">
                    <h3 style="color:#ffffff; margin-top:0;">🛡️ Scalable Production Architecture Description</h3>
                    <p style="line-height:1.6; color:#d1d5db; font-size:0.9rem;">
                        In a production system, SnapShare shifts from monolithic SQLite to a decoupled, microservices-oriented architecture:
                    </p>
                    <ul style="color:#d1d5db; padding-left:20px; line-height:1.6; font-size:0.85rem;">
                        <li><strong>Load Balancer:</strong> Distributes client requests across API Gateways.</li>
                        <li><strong>Feed Generation Service:</strong> Generates user feeds asynchronously and stores them in Redis cache for sub-millisecond retrieval.</li>
                        <li><strong>Media Processing Service:</strong> Compresses images, publishes them to AWS S3 buckets, and delivers them via CloudFront CDN.</li>
                        <li><strong>Database Replica Clustering:</strong> Masters handle writes, while read replicas scale read-heavy feed fetches.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div class="glass-card">
                    <h3 style="color:#ffffff; margin-top:0;">⚙️ Media Pipeline Flow</h3>
                    <div style="font-size:0.9rem; color:#d1d5db; border-left:3px solid #8b5cf6; padding-left:14px; line-height:1.7;">
                        <strong>Step 1: Upload</strong> - Streamlit file handler accepts image format (PNG, JPEG, etc.).<br>
                        <strong>Step 2: Validation</strong> - System verifies file formats, size, and corrupt files.<br>
                        <strong>Step 3: Compression</strong> - Pillow (PIL) scales quality settings down to 75% for file transmission size savings.<br>
                        <strong>Step 4: Resizing</strong> - Images exceeding 1080px width are automatically scaled down while locking aspect ratio.<br>
                        <strong>Step 5: Database Commit</strong> - Image reference is stored in SQLite DB and file written to local disk.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div class="glass-card" style="text-align: center; padding: 25px;">
                    <h4 style="color:#ffffff; margin-top:0;">👨‍🎓 Examiner Dashboard Info</h4>
                    <p style="font-size:0.85rem; color:#a1a1aa; line-height:1.5;">
                        This Streamlit build acts as the full operational frontend & backend prototype. 
                        Detailed PDF Documentation content and Viva prep are located in the project root to support oral evaluations.
                    </p>
                </div>
                """, unsafe_allow_html=True)

        # Home Feed View
        elif choice == "🏠 Home Feed":
            feed.render_feed_view("home", current_uid)

        # Explore Latest Posts
        elif choice == "🔥 Explore Latest":
            feed.render_feed_view("latest", current_uid)

        # Personalized Trending Feed
        elif choice == "✨ Personalized Feed":
            feed.render_feed_view("personalized", current_uid)

        # Upload Photo Screen
        elif choice == "📷 Upload Photo":
            st.markdown("<h2 style='color:#ffffff;'>📷 Upload New Post</h2>", unsafe_allow_html=True)
            col1, col2 = st.columns([1.5, 1])
            with col1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                uploaded_img = st.file_uploader("Choose a Photo", type=["jpg", "jpeg", "png"])
                caption_text = st.text_area("Caption", max_chars=2200, placeholder="Write a caption...")
                
                if st.button("Share Post", use_container_width=True):
                    if not uploaded_img:
                        st.error("Please upload an image first.")
                    else:
                        with st.spinner("Processing image and resizing..."):
                            success, msg = posts.upload_post(current_uid, uploaded_img, caption_text)
                            if success:
                                st.success(msg)
                                st.balloons()
                            else:
                                st.error(msg)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown("""
                <div class="glass-card">
                    <h4 style="color:#ffffff; margin-top:0;">📝 Media Processing Rules:</h4>
                    <ul style="color:#a1a1aa; font-size:0.85rem; padding-left:18px; line-height:1.6;">
                        <li>Files are converted automatically to standard JPEG format.</li>
                        <li>High-resolution photos are scaled to a maximum width of 1080px.</li>
                        <li>Active quality compression reduces file sizes by up to 70% with negligible visual impact.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

        # Search Users Screen
        elif choice == "🔍 Search Users":
            st.markdown("<h2 style='color:#ffffff;'>🔍 Search Profiles</h2>", unsafe_allow_html=True)
            search_query = st.text_input("Search username or bio...", placeholder="Type name...").strip()
            
            if search_query:
                results = database.search_users(search_query)
                if not results:
                    st.info("No matching users found.")
                else:
                    for row in results:
                        pic_url = row["profile_pic"]
                        uname = row["username"]
                        bio_text = row["bio"] if row["bio"] else "No bio."
                        
                        col_avatar, col_details, col_action = st.columns([1, 6, 2])
                        with col_avatar:
                            st.markdown(f"""
                            <div class="user-avatar-small" style="margin-top: 6px;">
                                {uname[0].upper() if not pic_url else ""}
                            </div>
                            """, unsafe_allow_html=True)
                        with col_details:
                            st.markdown(f"**@{uname}**")
                            st.markdown(f"<span style='color:#a1a1aa; font-size:0.85rem;'>{bio_text}</span>", unsafe_allow_html=True)
                        with col_action:
                            if st.button("View Profile", key=f"src_usr_{row['id']}"):
                                view_profile(row["id"])
                        st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.05); margin: 10px 0;'>", unsafe_allow_html=True)
            else:
                # Show suggestions of other active users to follow
                st.subheader("💡 Suggested Users to Follow")
                conn = database.get_db_connection()
                suggested = conn.execute(
                    "SELECT id, username, bio, profile_pic FROM users WHERE id != ? LIMIT 10;",
                    (current_uid,)
                ).fetchall()
                conn.close()
                
                if not suggested:
                    st.caption("No other users registered on this node yet.")
                else:
                    for row in suggested:
                        pic_url = row["profile_pic"]
                        uname = row["username"]
                        bio_text = row["bio"] if row["bio"] else "No bio."
                        is_following_suggested = database.is_following(current_uid, row["id"])
                        
                        col_avatar, col_details, col_action = st.columns([1, 6, 2])
                        with col_avatar:
                            st.markdown(f"""
                            <div class="user-avatar-small" style="margin-top: 6px;">
                                {uname[0].upper() if not pic_url else ""}
                            </div>
                            """, unsafe_allow_html=True)
                        with col_details:
                            st.markdown(f"**@{uname}**")
                            st.markdown(f"<span style='color:#a1a1aa; font-size:0.85rem;'>{bio_text}</span>", unsafe_allow_html=True)
                        with col_action:
                            # Direct follow/unfollow toggle or view profile
                            c_btn1, c_btn2 = st.columns(2)
                            with c_btn1:
                                if st.button("Profile", key=f"sug_prof_{row['id']}"):
                                    view_profile(row["id"])
                            with c_btn2:
                                if is_following_suggested:
                                    if st.button("Unfollow", key=f"sug_unfol_{row['id']}", use_container_width=True):
                                        database.unfollow_user(current_uid, row["id"])
                                        st.rerun()
                                else:
                                    if st.button("Follow", key=f"sug_fol_{row['id']}", type="primary", use_container_width=True):
                                        database.follow_user(current_uid, row["id"])
                                        st.rerun()
                        st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.05); margin: 10px 0;'>", unsafe_allow_html=True)

        # Notifications Screen
        elif choice == notif_label:
            st.markdown("<h2 style='color:#ffffff;'>🔔 Notification Center</h2>", unsafe_allow_html=True)
            
            # Action: mark all read
            if unread_notifs > 0:
                if st.button("Mark All as Read"):
                    database.mark_notifications_as_read(current_uid)
                    st.rerun()
            
            notifs = database.get_notifications(current_uid)
            if not notifs:
                st.info("No notifications to display.")
            else:
                for notif in notifs:
                    sender = notif["sender_name"]
                    ntype = notif["type"]
                    created = notif["created_at"]
                    is_unread = notif["is_read"] == 0
                    post_id = notif["post_id"]
                    
                    bg_color = "rgba(139, 92, 246, 0.08)" if is_unread else "rgba(255,255,255,0.02)"
                    border_color = "1px solid rgba(139, 92, 246, 0.25)" if is_unread else "1px solid rgba(255, 255, 255, 0.05)"
                    
                    # Construct message
                    if ntype == "like":
                        message_txt = "liked your post."
                    elif ntype == "comment":
                        message_txt = "commented on your post."
                    elif ntype == "follow":
                        message_txt = "started following you."
                    else:
                        message_txt = "interacted with your profile."
                        
                    st.markdown(f"""
                    <div class="notification-item" style="background: {bg_color}; border: {border_color};">
                        <div class="user-avatar-small">
                            {sender[0].upper()}
                        </div>
                        <div style="flex:1;">
                            <span style="font-weight: 700; color: #ffffff;">@{sender}</span> {message_txt} <br>
                            <span style="font-size:0.75rem; color:#8b8e95;">{format_timestamp(created)}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # If comment/like, let user view post
                    if post_id:
                        with st.expander("View Post Link"):
                            post_row = database.get_post_by_id(post_id)
                            if post_row:
                                if os.path.exists(post_row["image_path"]):
                                    st.image(post_row["image_path"], width=300)
                                    st.caption(post_row["caption"])
                            else:
                                st.caption("Post has been deleted.")
                                
                    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

        # Profile Screen
        elif choice == "👤 My Profile":
            profile.render_profile_view(current_uid, current_uid)

        # Edit Profile Screen
        elif choice == "✏️ Edit Profile":
            profile.render_edit_profile(current_uid)

        # Settings Screen
        elif choice == "⚙️ Settings":
            st.markdown("<h2 style='color:#ffffff;'>⚙️ App Settings</h2>", unsafe_allow_html=True)
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.write("### 🛠️ Developer & Academic Info")
            st.markdown(f"""
            - **Current Account ID:** {current_uid}
            - **Logged In Username:** @{current_uname}
            - **Database Target:** `sqlite:///{DATABASE_NAME}`
            - **Status:** Execution Layer Active
            """)
            st.write("---")
            st.write("### 🧹 Database Operations")
            if st.button("Reset Session and Log Out"):
                auth.logout_user()
            st.markdown('</div>', unsafe_allow_html=True)

        # Logout Screen
        elif choice == "🚪 Log Out":
            auth.logout_user()
