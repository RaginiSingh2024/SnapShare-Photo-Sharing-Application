# 🏗 SnapShare System Architecture

## Overview

SnapShare is a photo-sharing social media application inspired by modern platforms such as Instagram. The system follows a layered architecture consisting of Presentation Layer, Application Layer, Database Layer, and Storage Layer.

---

## Architecture Diagram

![SnapShare Architecture](SnapShare_Final_Architecture.png)

---

## 1. User Layer

The User Layer represents the end users interacting with the application.

### Guest User

* Browse public content
* Explore posts
* View feeds

### Registered User

* Login and Logout
* Upload Images
* Like and Comment on Posts
* Follow Other Users
* Receive Notifications
* Manage Profile

---

## 2. Presentation Layer (Streamlit Frontend)

The frontend is developed using Streamlit and Custom CSS.

### Components

* Discover Page
* Login Page
* Registration Page
* Feed Page
* Upload Post Page
* Profile Page
* Notifications Page
* Theme Toggle (Dark/Light Mode)

Responsibilities:

* User Interaction
* Form Handling
* Navigation
* Data Visualization

---

## 3. Application Layer

The Application Layer contains the core business logic.

### Authentication Module

Responsible for:

* User Registration
* Login Validation
* Password Verification
* Session Management

### Feed Management Module

Responsible for:

* Loading User Feed
* Displaying Posts
* Sorting Posts

### Post Management Module

Responsible for:

* Image Upload
* Caption Management
* Post Creation
* Post Deletion

### Social Interaction Module

Responsible for:

* Likes
* Comments
* Follow System
* Unfollow System

### Profile Management Module

Responsible for:

* Profile Updates
* Profile Statistics
* Profile Picture Management

### Notification Module

Responsible for:

* Like Notifications
* Comment Notifications
* Follow Notifications

### Theme Engine

Responsible for:

* Dark Mode
* Light Mode
* UI Personalization

---

## 4. Database Layer (SQLite)

The application uses SQLite as the primary relational database.

### Users Table

Stores:

* User Information
* Credentials
* Bio
* Profile Images

### Posts Table

Stores:

* Uploaded Posts
* Captions
* Post Metadata

### Likes Table

Stores:

* Post Likes
* User Interactions

### Comments Table

Stores:

* User Comments
* Comment History

### Followers Table

Stores:

* User Relationships
* Follow Connections

### Notifications Table

Stores:

* Notification Events
* Activity Records

---

## 5. Storage Layer

The Storage Layer manages media files.

### uploads/

Stores:

* Uploaded Images
* Profile Pictures
* Media Files

---

## Technology Stack

| Layer           | Technology        |
| --------------- | ----------------- |
| Frontend        | Streamlit         |
| Backend         | Python            |
| Database        | SQLite            |
| Storage         | Local File System |
| Styling         | Custom CSS        |
| Version Control | Git & GitHub      |

---

## Data Flow

1. User interacts with Streamlit Frontend.
2. Frontend sends requests to Application Modules.
3. Application Modules process business logic.
4. Data is stored/retrieved from SQLite Database.
5. Media files are stored in uploads folder.
6. Results are displayed back to the user.

---

## Conclusion

SnapShare follows a clean layered architecture that separates presentation, business logic, data management, and storage concerns. This design improves maintainability, scalability, and overall system organization.
