# Lost & Found Item Tracker API
Software Requirements Specification (SRS)

## 1. Introduction
**1.1 Purpose**
The purpose of this project is to develop a RESTful API backend for a platform that allows users to post, search, and match lost and found items in their locality.

**1.2 Intended Users**
- General public
- Lost item finders
- Individuals who have lost personal items
- Admins who moderate the system

**1.3 Scope**
The application will allow users to:
- Register and authenticate
- Post lost or found items
- Upload images and details
- View/search items based on filters
- Match lost and found items
- Communicate securely
- Admin will monitor and manage data abuse

## 2. Overall Description
**2.1 Product Perspective**
This is a standalone backend service providing a public RESTful API.

**2.2 Product Functions**
- User registration and authentication
- Posting item reports
- Search/filter items
- Matching suggestion system
- Admin moderation

## 3. Functional Requirements
**User Account Management**
- Register
- Login/logout
- JWT/token-based auth
- Update profile
- Password reset

**Item Management**
- Post/edit/delete item
- Mark as resolved

**Search & Filter System**
- Search by name/category/location/date
- Sort by recency/proximity

**Matching System**
- Suggest items based on category + keyword + date

**Communication System**
- Secure contact request
- Contact allowed only after match

**Admin Panel**
- View all reports
- Flag/delete inappropriate content

## 4. Non-Functional Requirements
- Fast API responses (< 500ms)
- Secure auth
- Media validation
- Rate limiting
- Swagger docs
- Unit tests

## 5. Use Case Descriptions
**Register/Login**: Guest registers and logs in.

**Post Lost Item**: User submits a lost item.

**Post Found Item**: User submits a found item.

**Search Items**: User filters/searches items.

**Match Suggestion**: System recommends items.

**Contact User**: User contacts item poster.

**Admin Moderation**: Admin deletes/flags posts.

## 6. Project Scope
**In-Scope:**
- DRF API
- Auth
- CRUD items
- Matching
- Media uploads
- Admin tools
- Swagger docs

**Out-of-Scope (MVP):**
- Real-time messaging
- Advanced geolocation
- Notifications
- Payments
- Multilingual

