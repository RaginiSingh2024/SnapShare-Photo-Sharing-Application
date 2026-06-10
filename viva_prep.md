# Viva Preparation Guide: SnapShare System Design

This guide provides 50 academic Viva Voce examination questions and answers, alongside deep-dive explanations of the system's architecture, database design, feed generation algorithm, and storage capabilities.

---

## 50 Academic Viva Questions & Answers

### 1. General System Architecture

#### Q1: What is the primary architecture pattern of the local SnapShare application?
**A:** The local application follows a **Three-Tier Monolithic Architecture**:
1. **Presentation Tier:** The Streamlit web framework (UI and routing).
2. **Logic Tier:** Python modules (`auth.py`, `posts.py`, `feed.py`, `profile.py`) coordinating business rules.
3. **Data Tier:** SQLite file-based database for relational records and local directory storage for compressed media.

#### Q2: How does this local monolith differ from a production-scale Instagram system?
**A:** A production system uses **Microservices Architecture**. It decouples services (Auth Service, Feed Service, Media Processing Service, Notification Service) which scale independently, communicate via API Gateways/Message Brokers (e.g., Kafka), and replace SQLite with clustered PostgreSQL and Redis.

#### Q3: Why is Nginx commonly used as a Load Balancer in system design?
**A:** Nginx acts as a reverse proxy that sits in front of backend servers. It routes client requests evenly (using algorithms like Round Robin or Least Connections) to prevent any single server from becoming a bottleneck, terminating SSL, and caching static resources.

#### Q4: What is an API Gateway, and what is its role?
**A:** An API Gateway is the single entry point for all client requests. It handles cross-cutting concerns like authentication, rate limiting, request routing, CORS policies, logging, and protocol translation (e.g., HTTP to gRPC).

#### Q5: What is the role of a Content Delivery Network (CDN) in a photo sharing app?
**A:** CDNs (like CloudFront or Cloudflare) cache static media assets (images, videos) at edge servers located closer to users geographically. This decreases latency (Page Load Time), reduces source bandwidth costs, and decreases load on internal media servers.

---

### 2. Database Design & Optimization

#### Q6: Why did you choose a Relational Database (SQLite) instead of a NoSQL Database (MongoDB) for core metadata?
**A:** The metadata of a photo-sharing platform is highly relational (users follow users, write comments on posts, like posts). Relational databases ensure strict **ACID transactions** (Atomicity, Consistency, Isolation, Durability) and maintain referential integrity through Foreign Key constraints, preventing orphaned comments or dangling likes.

#### Q7: Describe your SQLite schema tables and relationships.
**A:**
- `users`: Stores account information (PK `id`).
- `posts`: Has a Foreign Key referencing `users(id)` (1-to-many: one user can post many images).
- `likes`: Composite unique constraint on `(user_id, post_id)` mapping user reactions.
- `comments`: FKs to `users(id)` and `posts(id)`.
- `followers`: Self-referencing join table with composite unique constraint `(follower_id, following_id)`.
- `notifications`: Tracks alerts, referencing receiver (`user_id`), sender (`sender_id`), and source (`post_id`).

#### Q8: What are database indexes, and why did you add them?
**A:** Indexes are auxiliary data structures (typically B-Trees) created on specific columns to speed up row retrieval without scanning the entire table. We added indexes on foreign keys (`posts(user_id)`, `likes(post_id)`, `comments(post_id)`, `followers(follower_id, following_id)`, `notifications(user_id)`) to keep query times O(log N) rather than O(N) during feed loads.

#### Q9: What is the trade-off of having too many indexes?
**A:** While indexes speed up read queries (`SELECT`), they slow down write queries (`INSERT`, `UPDATE`, `DELETE`) because the database engine must rebuild the B-Tree index structure on every change. They also consume additional storage disk space.

#### Q10: How do you handle database locking in SQLite when concurrent writes occur?
**A:** SQLite uses file-level locking. Under heavy write traffic, it lock-serializes operations, resulting in `database is locked` errors. For production, we migrate to PostgreSQL, which supports row-level locking, enabling thousands of concurrent writes.

#### Q11: Explain Referential Integrity and how it is enforced in your database.
**A:** Referential Integrity ensures that relationships between tables remain consistent. We enforce this with `FOREIGN KEY` constraints. For instance, `posts.user_id` must point to a valid row in `users.id`.

#### Q12: What does `ON DELETE CASCADE` mean in your schema?
**A:** It ensures that when a parent record is deleted, all related child records are automatically deleted. For example, if a user deletes a post, all associated likes, comments, and notifications are deleted automatically by the database engine.

#### Q13: What is Database Normalization, and to what level is your schema normalized?
**A:** Normalization is the process of structuring a database to reduce redundancy and dependency. Our schema is in **Third Normal Form (3NF)** because all non-primary key columns depend strictly on the primary key, and there are no transitive dependencies.

#### Q14: How does a composite unique constraint work on the `likes` table?
**A:** It ensures that a user can only like a specific post once. If the user tries to insert a duplicate `(user_id, post_id)` pair, SQLite raises a `Unique Constraint Violation` error.

#### Q15: Explain the self-referencing relationship in the `followers` table.
**A:** Both columns `follower_id` and `following_id` reference the same parent table `users(id)`. This models the social graph where users follow other users within the same table.

---

### 3. Media Processing & Storage Pipeline

#### Q16: Walk through the media pipeline when a user uploads a photo.
**A:** 
1. **File Upload:** Streamlit intercepts the file stream.
2. **Validation:** Verifies format (JPG/PNG).
3. **Pillow Initialization:** Opens the image in memory.
4. **Resolution Downscale:** Downscales images with width > 1080px while locking aspect ratio.
5. **Format Conversion:** Converts RGBA (transparent) pixels to RGB.
6. **Lossy Compression:** Saves image as JPEG at 75% quality.
7. **Storage Write:** Writes file to disk, returns file path, and writes metadata to SQLite.

#### Q17: Why resize images to 1080px wide?
**A:** 1080px is the standard width for mobile apps (e.g. Instagram). Storing high-res 4000px images taken directly from modern cameras wastes storage, increases CDN delivery costs, and slows feed load times on mobile devices.

#### Q18: What is the difference between lossy and lossless compression?
**A:**
- **Lossy compression** (like JPEG) discards imperceptible visual data to significantly reduce file size (70-80% reduction).
- **Lossless compression** (like PNG) reduces size without discarding any data, but results in much larger files. Social feeds prioritize speed, making lossy compression the preferred choice.

#### Q19: Why do we convert RGBA images to RGB before saving as JPEG?
**A:** JEPG does not support transparency (Alpha channel). Saving an RGBA image as a JPEG directly raises a Python `OSError: cannot write mode RGBA as JPEG`. We convert it to RGB first, flattening transparent pixels against a black background.

#### Q20: Where are images stored in a production-scale architecture?
**A:** Images are stored in an **Object Store** like AWS S3 or Google Cloud Storage, rather than on local server disks. Object stores offer 99.999999999% durability, are cheaper, and scale infinitely.

#### Q21: What is a presigned URL, and why is it used?
**A:** A presigned URL is a temporary, cryptographically signed URL generated by the backend that gives a client direct permission to upload/download a file directly to/from AWS S3. This bypasses the backend server, preventing it from becoming a bottleneck during media transfers.

#### Q22: What are the security concerns of local image storage?
**A:** Local storage risks Directory Traversal attacks (where a user can access system files using relative paths, like `../../etc/passwd`). We prevent this by generating unique random filenames (timestamped UUIDs) and preventing direct file paths in user inputs.

#### Q23: How would you process videos instead of photos?
**A:** We would use tools like **FFmpeg** to transcode videos into formats like H.264/AAC at multiple resolutions (360p, 480p, 720p) and stream them using adaptive protocols like HLS (HTTP Live Streaming) or MPEG-DASH.

#### Q24: What is image metadata stripping (EXIF data)?
**A:** EXIF metadata (GPS coordinates, camera model, timestamp) is embedded inside photos taken by smartphones. Stripping this during compression protects user privacy and reduces file sizes.

#### Q25: Why is `Image.Resampling.LANCZOS` preferred during resizing?
**A:** Lanczos is a high-quality resampling algorithm that uses sinc filters to calculate pixel colors. It prevents aliasing (pixel jaggedness) and preserves sharpness better than simple bilinear or nearest-neighbor interpolation.

---

### 4. Feed Generation & Algorithmic Design

#### Q26: Explain the query logic behind the Chronological Home Feed.
**A:** It uses an SQL `SELECT` with a `JOIN` and subqueries. It filters posts matching the user's ID or the IDs of the users they follow (fetched from the `followers` table), annotates them with like and comment counts, and orders the results by `created_at DESC`.

#### Q27: How does your Personalized Feed work?
**A:** It ranks posts based on engagement score: `Score = Likes + (Comments * 2)`. Comments are weighted higher because writing a comment requires more user effort than clicking a like button.

#### Q28: What is the difference between Pull and Push models for feed generation (Fan-out)?
**A:**
- **Pull Model (Fan-out on Read):** When a user opens their feed, the system queries the database for all posts from followed accounts in real time. It is cheap on writes, but expensive on reads (used for active users with many followers).
- **Push Model (Fan-out on Write):** When a user uploads a post, it is immediately inserted into the pre-computed feed cache of all their followers. Reads are instant (O(1)), but writes are expensive if the poster has millions of followers (the "Celebrity Problem").

#### Q29: How do social networks solve the Celebrity Problem (e.g. Selena Gomez posting)?
**A:** They use a **Hybrid Model**. Posts by average users are pushed to their followers' feeds. Posts by celebrities are not pushed; instead, they are merged into followers' feeds dynamically when the feed is loaded (Pull model).

#### Q30: What is Feed Pagination, and how is it implemented?
**A:** Instead of loading thousands of posts at once, pagination loads posts in chunks (e.g., 10 at a time). It is implemented using `LIMIT` and `OFFSET` clauses in SQL, or keyset cursor pagination (`WHERE post_id < last_seen_id LIMIT 10`) for better performance.

#### Q31: Why is offset pagination (`LIMIT 10 OFFSET 100`) bad for high-scale systems?
**A:** Because the database must read and discard all rows up to the offset value, resulting in O(N) performance. It also causes duplicate or skipped posts if new records are inserted while the user is paging. Keyset pagination avoids this.

#### Q32: Where are generated feeds stored in production?
**A:** They are stored in an in-memory cache like **Redis** (often in a Redis Sorted Set where the score is the timestamp or engagement score).

#### Q33: How does the system track if a post is liked by the current user in the feed query?
**A:** By performing a subquery with `EXISTS` checking the `likes` table: `EXISTS(SELECT 1 FROM likes WHERE user_id = :uid AND post_id = p.id)`. This returns a boolean value for each row.

#### Q34: What is the time complexity of feed generation in your system?
**A:** O(N log N) due to sorting, where N is the number of posts in the database. In production, caching reduces this to O(1) retrieval.

#### Q35: How would you incorporate user interest categories into personalization?
**A:** We would use collaborative filtering or content-based tagging. We would extract post tags (e.g., #sports, #food), track user interaction weights, and boost matching content in the SQL/NoSQL ranking queries.

---

### 5. Scalability, Caching & Performance

#### Q36: What is Caching, and where is it applied?
**A:** Caching stores copies of frequently accessed data in fast memory (RAM). It is applied at multiple layers:
1. **Client/Browser Cache:** For static assets.
2. **CDN Cache:** For media.
3. **Application Cache:** Redis for user profiles, session tokens, and feeds.
4. **Database Query Cache:** Internally managed by DBMS.

#### Q37: What is Cache Eviction, and what are common policies?
**A:** When cache memory is full, the system must delete old entries. Common policies include:
- **LRU (Least Recently Used):** Deletes items that haven't been accessed for the longest time.
- **LFU (Least Frequently Used):** Deletes items with the lowest hit counts.
- **FIFO (First In First Out):** Deletes oldest entries.

#### Q38: Explain Cache Busting and the Cache-Aside pattern.
**A:** In the Cache-Aside pattern, the app queries the cache first. If a cache miss occurs, it queries the DB, updates the cache, and returns the data. If a write occurs, the app invalidates the cache entry (cache busting) to ensure data consistency.

#### Q39: What is Horizontal Scaling vs Vertical Scaling?
**A:**
- **Vertical Scaling (Scaling Up):** Adding more CPU, RAM, or storage to a single server. It has hardware limits and introduces a single point of failure.
- **Horizontal Scaling (Scaling Out):** Adding more servers to the network pools. It has no architectural limit, but requires load balancers.

#### Q40: What is Database Sharding?
**A:** Sharding is horizontal partitioning of a database. It splits large tables across multiple database instances based on a shard key (e.g., routing `user_id % 4` to shard 0, 1, 2, or 3).

#### Q41: Explain Read Replicas (Master-Slave replication).
**A:** It separates write and read traffic. All writes (`INSERT`/`UPDATE`) go to the Master database, which syncs changes to Slave databases. Reads are handled by the Slaves, scaling read performance.

#### Q42: What is the CAP Theorem?
**A:** CAP states that a distributed system can only guarantee two out of three properties simultaneously:
- **Consistency (C):** All nodes see the same data at the same time.
- **Availability (A):** Every request receives a response.
- **Partition Tolerance (P):** The system continues to operate despite network splits.
For global web systems, P is mandatory, forcing a choice between AP or CP.

#### Q43: Why does SnapShare choose Availability over strict Consistency (AP)?
**A:** If a network partition occurs, it is better to display stale posts to a user (Availability) than to display error pages (Consistency). Eventually, the data will sync (Eventual Consistency).

#### Q44: What is Rate Limiting, and how does it protect the app?
**A:** Rate Limiting limits the number of requests a user can make in a given time frame (e.g., 60 requests/minute). It protects the server from Denial of Service (DoS) attacks, brute-force logins, and scraping.

#### Q45: How does a Message Queue (e.g., RabbitMQ, Kafka) help with scalability?
**A:** It decouples heavy backend tasks. When a user uploads a post, the web server registers it and immediately replies to the user. It then pushes a message to a queue, where background workers handle image processing, notifications, and feed generation asynchronously.

---

### 6. Security, Session & Streamlit Specifics

#### Q46: How does password salting protect against rainbow tables?
**A:** A rainbow table is a database of precomputed hashes for common passwords. Salting appends a unique value (like the user's username) to the password before hashing, creating a completely unique hash that cannot be matched against generic tables.

#### Q47: Why is it insecure to store passwords in plaintext?
**A:** If the database is compromised, attackers gain instant access to all users' passwords. Users often reuse passwords across sites, exposing their accounts on other platforms.

#### Q48: How does Streamlit manage state between script runs?
**A:** Streamlit is reactive; it reruns the entire Python script from top to bottom whenever a user interacts with a widget. We use `st.session_state` (a key-value dictionary persistent across reruns) to store state like logged-in user details.

#### Q49: What is the risk of utilizing `unsafe_allow_html=True` in Streamlit?
**A:** It exposes the application to **Cross-Site Scripting (XSS)** attacks. If user inputs (e.g., comments) are rendered directly inside HTML blocks without escaping, an attacker could inject malicious `<script>` tags that run in other users' browsers.

#### Q50: How did you mitigate XSS in SnapShare?
**A:** We only render static layout elements (avatars, cards, dividers) using HTML wrappers, and use native Streamlit components (`st.write()`, labels, or text expanders) to render user-generated comments and captions, which sanitizes the outputs automatically.

---

## Technical Deep-Dives

### 1. Feed Generation & Ranking Algorithm
The local SnapShare application implements a dynamic SQL query mapping for both chronological and personalized feeds.

**Chronological Feed Query (`database.py`):**
```sql
SELECT p.*, u.username, u.profile_pic,
       (SELECT COUNT(*) FROM likes WHERE post_id = p.id) as likes_count,
       (SELECT COUNT(*) FROM comments WHERE post_id = p.id) as comments_count,
       EXISTS(SELECT 1 FROM likes WHERE user_id = :uid AND post_id = p.id) as user_liked
FROM posts p
JOIN users u ON p.user_id = u.id
WHERE p.user_id = :uid OR p.user_id IN (
    SELECT following_id FROM followers WHERE follower_id = :uid
)
ORDER BY p.created_at DESC;
```

**Personalized Trending Feed Query (`database.py`):**
```sql
SELECT p.*, u.username, u.profile_pic,
       (SELECT COUNT(*) FROM likes WHERE post_id = p.id) as likes_count,
       (SELECT COUNT(*) FROM comments WHERE post_id = p.id) as comments_count,
       EXISTS(SELECT 1 FROM likes WHERE user_id = :uid AND post_id = p.id) as user_liked,
       ((SELECT COUNT(*) FROM likes WHERE post_id = p.id) + (SELECT COUNT(*) FROM comments WHERE post_id = p.id) * 2.0) as engagement_score
FROM posts p
JOIN users u ON p.user_id = u.id
ORDER BY engagement_score DESC, p.created_at DESC LIMIT 50;
```
*Algorithm logic:* A comment has a weight of 2.0, while a like has a weight of 1.0. This biases the feed towards posts that spark conversation.

---

### 2. Media Compression Pipeline
Using **Pillow**, we convert all uploaded images to JPEG, downscale high-resolution assets, and compress them before saving.

```python
from PIL import Image
import os
import time

def process_and_save_image(uploaded_file, user_id, max_width=1080, quality=75):
    # Open file stream
    image = Image.open(uploaded_file)
    
    # Handle transparency
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
        
    # Scale image size down if width > 1080px
    w, h = image.size
    if w > max_width:
        aspect_ratio = h / w
        new_width = max_width
        new_height = int(max_width * aspect_ratio)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
    # Generate unique output filename
    timestamp = int(time.time() * 1000)
    file_path = f"uploads/post_{user_id}_{timestamp}.jpg"
    
    # Save using lossy JPEG compression with optimize flag
    image.save(file_path, "JPEG", quality=quality, optimize=True)
    return file_path
```

---

### 3. Scalable Production Architecture
To scale this application to support millions of active users:
1. **Load Balancing:** DNS load balancing (e.g., Cloudflare) routes traffic to Nginx reverse proxy clusters.
2. **API Gateway:** Microservices (Auth, Users, Posts, Feeds, Notifications) are hidden behind a gateway checking JWT tokens.
3. **Write Path Decoupling:** Image uploads go directly to an AWS S3 bucket using presigned URLs. S3 triggers an event to run lambda resizing tasks asynchronously.
4. **Caching Layer:** Redis stores user feed arrays (Sorted Sets of post IDs).
5. **Feed Fan-Out Workers:** Celery or Kafka processors handle feed updates in the background.
