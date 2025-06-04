from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from typing import Dict, Any
import os
import httpx
from datetime import datetime

# User database operations
from database.operations.user_operations import (
    get_user_by_discord_id,
    store_user_pending_approval,
    is_user_approved
)
from database.models.user import UserStatus


from .session import get_session, is_session_expired, update_session_access

router = APIRouter()

async def exchange_code_for_token(code: str) -> Dict[str, Any]:
    """Exchange Discord authorization code for access token"""
    token_url = os.getenv("DISCORD_TOKEN_URL")
    
    data = {
        "client_id": os.getenv("DISCORD_CLIENT_ID"),
        "client_secret": os.getenv("DISCORD_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": os.getenv("DISCORD_REDIRECT_URI"),
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=data, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to exchange code for token")
        
        return response.json()

async def get_discord_user_info(access_token: str) -> Dict[str, Any]:
    """Get Discord user information using access token"""
    user_url = os.getenv("DISCORD_USER_URL")
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(user_url, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get user info from Discord")
        
        return response.json()
    
# async def get_discord_user_guilds(access_token: str) -> Dict[str, Any]:
#     """Get Discord user's guilds (servers) using access token"""
#     guilds_url = "https://discord.com/api/users/@me/guilds"
    
#     headers = {
#         "Authorization": f"Bearer {access_token}"
#     }
    
#     async with httpx.AsyncClient() as client:
#         response = await client.get(guilds_url, headers=headers)
        
#         if response.status_code != 200:
#             raise HTTPException(status_code=400, detail="Failed to get user guilds from Discord")
        
#         return response.json()


# Testing version
@router.get("/discord/callback")
async def discord_callback(code: str = None, error: str = None):
    """
    Handle Discord OAuth callback
    """
    frontend_url = os.getenv("FRONTEND_URL")

    # Check for errors from Discord
    if error:
        return RedirectResponse(
            url=f"{frontend_url}/?error=discord_auth_failed&message=Access Denied. Error connecting to Discord"
        )
    if not code:
        return RedirectResponse(
            url=f"{frontend_url}/?error=discord_auth_failed&message=ERROR: No code provided"
        )
    try:
        # Exchange code for access token
        token_data = await exchange_code_for_token(code)
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="No access token received")
        
        # Get user info from Discord
        discord_user = await get_discord_user_info(access_token)
        print(discord_user)

        # Check if user already exists
        existing_user = get_user_by_discord_id(discord_user["id"])
        print(existing_user)
        if existing_user:
            if not is_user_approved(existing_user):
                return RedirectResponse(
                    url=f"{frontend_url}/?error=pending_approval&message=Your account is pending admin approval"
                )
            # If user is approved, create session and redirect (TODO: implement session creation)
            # For now, just redirect with success message
            return RedirectResponse(
                url=f"{frontend_url}/?auth=success&message=Login successful"
            )
        else:
            new_user = store_user_pending_approval(discord_user)
            if new_user:
                # Redirect with pending message
                return RedirectResponse(
                    url=f"{frontend_url}/?auth=pending&message=Your account has been submitted for admin approval"
                )
            else:
                # User already exists or error occurred
                return RedirectResponse(
                    url=f"{frontend_url}/?error=user_exists&message=Account already exists"
                )

        # user_guilds = await get_discord_user_guilds(access_token)
        # for guild in user_guilds:
        #     print(f"Guild: {guild['name']} (ID: {guild['id']})")

    
    except HTTPException as e:
        return RedirectResponse(
            url=f"{frontend_url}/?error=discord_auth_failed&message={e.detail}"
        )
    except Exception as e:
        return RedirectResponse(
            url=f"{frontend_url}/?error=discord_auth_failed&message=An unexpected error occurred"
        )


# Full version
# @router.get("/discord/callback")
# async def discord_callback(code: str = None, error: str = None):
#     """
#     Handle Discord OAuth callback
#     """
#     frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
#     # Check for errors from Discord
#     if error:
#         return RedirectResponse(
#             url=f"{frontend_url}/?error=discord_auth_failed&message={error}"
#         )
    
#     if not code:
#         return RedirectResponse(
#             url=f"{frontend_url}/?error=discord_auth_failed&message=no_code_provided"
#         )
    
#     try:
#         # Exchange code for access token
#         token_data = await exchange_code_for_token(code)
#         access_token = token_data.get("access_token")
        
#         if not access_token:
#             raise HTTPException(status_code=400, detail="No access token received")
        
#         # Get user info from Discord
#         discord_user = await get_discord_user_info(access_token)
        
#         # Check if user already exists
#         existing_user = get_user_by_discord_id(discord_user["id"])
        
#         if existing_user:
#             # User exists, check if approved
#             if is_user_approved(existing_user):
#                 # Create session and redirect to success
#                 session_id = create_session(existing_user["id"])
                
#                 # Set session cookie
#                 redirect_response = RedirectResponse(url=f"{frontend_url}/?auth=success")
#                 redirect_response.set_cookie(
#                     key="session_id",
#                     value=session_id,
#                     httponly=True,
#                     secure=os.getenv("ENVIRONMENT") == "production",
#                     samesite="lax",
#                     max_age=86400 * 7  # 7 days
#                 )
#                 return redirect_response
#             else:
#                 # User exists but not approved
#                 return RedirectResponse(
#                     url=f"{frontend_url}/?error=pending_approval&message=Your account is pending admin approval"
#                 )
#         else:
#             # New user - store for approval
#             user_data = {
#                 "discord_id": discord_user["id"],
#                 "discord_username": discord_user['username'],
#                 "discord_avatar": f"https://cdn.discordapp.com/avatars/{discord_user['id']}/{discord_user['avatar']}.png" if discord_user.get('avatar') else None,
#                 "email": discord_user.get("email"),
#                 "status": "pending",
#                 "created_at": datetime.utcnow().isoformat()
#             }
            
#             store_user_pending_approval(user_data)
            
#             # TODO: Send notification to admin about new user
            
#             return RedirectResponse(
#                 url=f"{frontend_url}/?auth=pending&message=Your account has been submitted for admin approval"
#             )
            
#     except HTTPException as e:
#         return RedirectResponse(
#             url=f"{frontend_url}/?error=discord_auth_failed&message={e.detail}"
#         )
#     except Exception as e:
#         return RedirectResponse(
#             url=f"{frontend_url}/?error=discord_auth_failed&message=An unexpected error occurred"
#         )

