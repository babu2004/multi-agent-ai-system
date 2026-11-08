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

    print("f[RESEARCH AGENT] Found:{result}")

    return result