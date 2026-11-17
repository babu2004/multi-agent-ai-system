

from agents.crewai_hierarchical import run_hierarchical_crew


def test_hierarchical_crew():
    result = run_hierarchical_crew()

    print("\n[FINAL MANAGER-COORDINATED RESULT]")
    print(result)


if __name__ == "__main__":
    test_hierarchical_crew()
