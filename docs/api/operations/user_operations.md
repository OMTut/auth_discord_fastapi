# User Operations API Documentation

This document describes all user operations available in the Auth API.

## Overview

The user operations module provides functions for managing Discord users in the authentication system. All operations interact with the PostgreSQL database and handle user registration, retrieval, and status management.

## Core Operations

### 1. `store_user_pending_approval(user_data: Dict[str, Any]) -> Optional[User]`

**Purpose**: Store a new user in the database with PENDING status awaiting admin approval.

**Parameters**:
- `user_data` (Dict): User information from Discord OAuth
  - `id` (str): Discord user ID (required)
  - `username` (str): Discord username (required)
  - `server_nickname` (str): Server-specific nickname (optional)
  - `email` (str): User's email address (optional)

**Returns**: 
- `User` object if successful
- `None` if failed (duplicate Discord ID or other error)

**Usage Example**:
```python
user_data = {
    "id": "55555555",
    "username": "someuser.",
    "server_nickname": "some_nickname",
    "email": "user@example.com"
}
new_user = store_user_pending_approval(user_data)
```

**Error Handling**:
- Handles `IntegrityError` for duplicate Discord IDs
- Logs errors and returns `None` on failure
- Automatically rolls back database transaction on error

---

### 2. `get_user_by_id(user_id: int) -> Optional[User]`

**Purpose**: Retrieve a user by their internal database ID.

**Parameters**:
- `user_id` (int): The internal database ID of the user

**Returns**:
- `User` object if found
- `None` if not found or error occurs

**Usage Example**:
```python
user = get_user_by_id(123)
if user:
    print(f"Found user: {user.discord_username}")
```

---

### 3. `get_user_by_discord_id(discord_id: str) -> Optional[User]`

**Purpose**: Retrieve a user by their Discord ID (primary lookup method).

**Parameters**:
- `discord_id` (str): The Discord user ID (e.g., "361713262733033473")

**Returns**:
- `User` object if found
- `None` if not found

**Usage Example**:
```python
user = get_user_by_discord_id("361713262733033473")
if user:
    print(f"User status: {user.status.value}")
```

**Note**: This is the primary method for user lookup during authentication flows.

---

### 4. `get_server_nickname_by_user_id(user_id: int) -> Optional[str]`

**Purpose**: Get a user's server-specific nickname by their database ID.

**Parameters**:
- `user_id` (int): The internal database ID of the user

**Returns**:
- `str` with the server nickname if found
- `None` if user not found or no nickname set

**Usage Example**:
```python
nickname = get_server_nickname_by_user_id(123)
display_name = nickname or user.discord_username  # Fallback to username
```

---

### 5. `is_user_approved(user: User) -> bool`

**Purpose**: Check if a user has been approved by an admin.

**Parameters**:
- `user` (User): The user object to check

**Returns**:
- `True` if user status is APPROVED
- `False` for any other status or if user is None

**Usage Example**:
```python
user = get_user_by_discord_id("361713262733033473")
if is_user_approved(user):
    # Allow access
    create_session(user.id)
else:
    # Deny access
    return "Account pending approval"
```

## User Status Values

The system uses the following user statuses:

| Status | Description |
|--------|-----------|
| `PENDING` | User registered but awaiting admin approval |
| `APPROVED` | User approved and can access the system |
| `REJECTED` | User application rejected by admin |
| `BANNED` | User banned from the system |


