from backend.database.supabase_client import supabase


class JobService:

    @staticmethod
    def create_job(job_data: dict):
        try:

            data = {
                "employer_id": job_data.get("employer_id"),
                "title": job_data.get("title"),
                "description": job_data.get("description"),
                "location_lat": job_data.get("location_lat"),
                "location_lng": job_data.get("location_lng"),
                "budget": job_data.get("budget"),
                "status": "open"
            }

            response = supabase.table("Jobs").insert(data).execute()

            if response.data:
                return {
                    "success": True,
                    "job": response.data[0]
                }

            return {"success": False, "error": "Job creation failed"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def get_job(job_id: str):
        response = (
            supabase
            .table("Jobs")
            .select("*")
            .eq("id", job_id)
            .execute()
        )

        if response.data:
            return response.data[0]

        return None