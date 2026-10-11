from fastapi import APIRouter, Depends, HTTPException
from backend.database.supabase_client import supabase
from backend.auth import get_authenticated_user

router = APIRouter()

@router.post("/register")
def register_employer(data: dict, user=Depends(get_authenticated_user)):
    try:
        profile_id = str(user.id)
        existing = (
            supabase.table("Profiles")
            .select("id")
            .eq("auth_user_id", profile_id)
            .execute()
        )
        if existing.data:
            raise HTTPException(status_code=409, detail="A profile already exists for this account")

        # 1. Identity (Profiles table)
        profile_resp = supabase.table("Profiles").insert({
            "auth_user_id": profile_id,
            "full_name": data.get("full_name"),
            "phone": data.get("phone"),
            "role": "employer"
        }).execute()
        
        if not profile_resp.data:
            raise Exception("Profile creation failed")

        new_id = profile_resp.data[0]["id"]

        # 2. Employer Profile
        supabase.table("Employers").insert({
            "id": new_id,
            "employer_name": data.get("employer_name"),
            "description": data.get("description"),
            "location_lat": data.get("location_lat"),
            "location_lng": data.get("location_lng")
        }).execute()

        return {"status": "success", "employer_id": new_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
