def run_research_agent(query: str)-> dict:
    """
    Demo research agent.
    Returns simulated data to demonstrate agent communication.
    """

    print("\n [RESEARCH AGENT] Processing request....")

    result = {
        "country":"India",
        "metric": "Population",
        "value": 1_400_000_000,
        "unit": "people",
        "source": "simulated demo data"
    } 

    # Validate the research result
    if not isinstance(result, dict):
        raise ValueError("Reseach result must be a dictionary.")
    
    if not isinstance(result.get("value"), (int,float)):
        raise ValueError("Reseach result contains an invalid value.")
    
    if result["value"] <= 0 :
        raise ValueError("Reseach value must be positive.")
    print(f"[RESEARCH AGENT] Fount: {result}")

    return result 