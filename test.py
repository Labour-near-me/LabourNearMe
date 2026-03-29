from backend.services.worker_service import WorkerService

test_data = {
    "full_name": "Rajesh Kumar",
    "phone": "9876543210",
    "category": "Construction",
    "skills": ["Masonry", "Plastering"],
    "experience_years": 5,
    "expected_wage": 800,
    "location_lat": 23.1765,
    "location_lng": 75.7885
}

result = WorkerService.register_new_worker(test_data)
print(f"Result: {result}")