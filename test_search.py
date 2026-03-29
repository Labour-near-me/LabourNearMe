from backend.services.worker_service import WorkerService

def test_semantic_search():
    print("🔍 Starting Semantic Search Test...")
    
    # 1. Define a natural language query
    # Even if "construction" or "mason" isn't the exact word, 
    # the AI should find relevant workers.
    query = "I need someone to help with brick work and home building"
    
    print(f"Searching for: '{query}'")
    
    # 2. Call the search method
    results = WorkerService.search_workers(query, limit=3)
    
    # 3. Handle and display results
    if isinstance(results, dict) and "error" in results:
        print(f"❌ Error: {results['error']}")
    elif not results:
        print("⚠️ No matching workers found. Did you run the SQL RPC in Supabase?")
    else:
        print(f"✅ Found {len(results)} matching worker(s):")
        for i, worker in enumerate(results, 1):
            name = worker.get('full_name', 'Unknown')
            sim = worker.get('similarity', 0)
            exp = worker.get('experience_years', 0)
            print(f"{i}. {name} | Match Score: {sim:.4f} | Experience: {exp} years")

if __name__ == "__main__":
    test_semantic_search()