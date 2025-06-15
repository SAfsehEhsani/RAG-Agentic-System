import json
from datetime import datetime, timedelta
import random # To add a bit more variation if needed, though not strictly necessary

def simulate_fetch_recent_documents(days_window=7):
    """
    Simulates fetching documents published within a window of days ending today.
    In a real app, this would query an external API with date filters.
    For this demo, we return a fixed list, but assign dates based on the current run date.
    """
    today = datetime.now()
    current_date_str = today.strftime('%Y-%m-%d')
    yesterday_date_str = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    two_days_ago_str = (today - timedelta(days=2)).strftime('%Y-%m-%d')
    three_days_ago_str = (today - timedelta(days=3)).strftime('%Y-%m-%d')
    week_ago_str = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    month_ago_str = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    year_ago_str = (today - timedelta(days=365)).strftime('%Y-%m-%d')


    print(f"Simulating fetching data...")

    # Simulate data - expanded list with various dates and types
    # The dates here are relative placeholders; the logic below assigns actual dates
    sample_data_template = [
        # Data often present (can be "older" or resurface in searches)
        {
            "doc_id": "env-epa-rule-water-quality-2023-08-15",
            "title": "Final Rule on National Primary Drinking Water Regulations",
            "publication_date": "2023-08-15",
            "document_type": "Rule",
            "summary": "The Environmental Protection Agency is finalizing amendments to the National Primary Drinking Water Regulations to address contaminants."
        },
        {
            "doc_id": "health-fda-notice-drug-approval-2023-09-20",
            "title": "Notice of Approval for New Cancer Therapy Drug",
            "publication_date": "2023-09-20",
            "document_type": "Notice",
            "summary": "The Food and Drug Administration announces the approval of a new drug for treating advanced stages of cancer."
        },
        {
            "doc_id": "economy-treasury-rule-sanctions-2023-10-10",
            "title": "Treasury Department Final Rule on Sanctions Compliance",
            "publication_date": "2023-10-10",
            "document_type": "Rule",
            "summary": "This rule clarifies requirements for financial institutions regarding compliance with economic sanctions programs administered by the Treasury Department."
        },
         {
            "doc_id": "tech-ntia-notice-broadband-funding-2023-10-25",
            "title": "NTIA Notice of Funding Availability: Broadband Deployment Program",
            "publication_date": "2023-10-25",
            "document_type": "Notice",
            "summary": "The National Telecommunications and Information Administration announces available funding for expanding broadband access in underserved areas."
        },
        {
            "doc_id": "defense-dod-directive-cybersecurity-2023-11-01",
            "title": "Department of Defense Directive on Cloud Cybersecurity",
            "publication_date": "2023-11-01",
            "document_type": "Directive",
            "summary": "This directive establishes policy and assigns responsibilities for securing cloud computing environments used by the Department of Defense."
        },
         {
            "doc_id": "trade-ustr-notice-tariffs-2023-11-10",
            "title": "USTR Notice Regarding Section 301 Tariff Review",
            "publication_date": "2023-11-10",
            "document_type": "Notice",
            "summary": "The Office of the United States Trade Representative is conducting a review of tariffs imposed under Section 301 of the Trade Act of 1974."
        },
        # Data intended to appear "recent" when the pipeline runs
        # These dates will be assigned based on today's date
        {
            "doc_id": f"ai-exec-order-safety-{current_date_str}", # Tie ID to date
            "title": "Executive Order on Advancing AI Safety and Security",
            "publication_date": current_date_str, # <-- Assigned today's date
            "document_type": "Executive Order",
            "summary": "This order establishes new standards for AI safety and security, protects Americans from AI risks, supports innovation, and advances American leadership globally."
        },
         {
            "doc_id": f"climate-exec-order-goals-{current_date_str}", # Tie ID to date
            "title": "Executive Order on Climate Resilience and Adaptation",
            "publication_date": current_date_str, # <-- Assigned today's date
            "document_type": "Executive Order",
            "summary": "This order directs federal agencies to identify climate risks and develop adaptation plans to build resilience across sectors."
        },
        {
            "doc_id": f"epa-rule-emissions-{yesterday_date_str}", # Tie ID to date
            "title": "EPA Final Rule on Vehicle Emission Standards (Phase 2)",
            "publication_date": yesterday_date_str, # <-- Assigned yesterday's date
            "document_type": "Rule",
            "summary": "The Environmental Protection Agency finalizes tougher emission standards for light-duty vehicles for model years 2027 and beyond."
        },
         {
            "doc_id": f"doe-notice-energy-funding-{yesterday_date_str}", # Tie ID to date
            "title": "DOE Notice of Intent to Issue Funding Opportunity for Grid Modernization",
            "publication_date": yesterday_date_str, # <-- Assigned yesterday's date
            "document_type": "Notice",
            "summary": "The Department of Energy announces its intent to release a funding opportunity announcement for projects aimed at modernizing the nation's electricity grid."
        },
         {
            "doc_id": f"dhs-memo-security-{two_days_ago_str}", # Tie ID to date
            "title": "Presidential Memorandum on Supply Chain Security Review",
            "publication_date": two_days_ago_str, # <-- Assigned 2 days ago
            "document_type": "Presidential Memorandum",
            "summary": "This memorandum initiates a comprehensive review of critical supply chains to identify vulnerabilities and recommend resilience measures."
        },
        {
            "doc_id": f"health-cdc-notice-flu-season-{three_days_ago_str}", # Tie ID to date
            "title": "CDC Notice on Upcoming Flu Season Guidance",
            "publication_date": three_days_ago_str, # <-- Assigned 3 days ago
            "document_type": "Notice",
            "summary": "The Centers for Disease Control and Prevention issues guidance for the public and healthcare providers ahead of the anticipated flu season."
        },
         {
            "doc_id": f"transportation-rule-aviation-safety-{week_ago_str}", # Tie ID to date
            "title": "FAA Proposed Rule on Drone Operations Over People",
            "publication_date": week_ago_str, # <-- Assigned 7 days ago (approx a week)
            "document_type": "Proposed Rule",
            "summary": "The Federal Aviation Administration is proposing new regulations to allow routine drone operations over people and at night under certain conditions."
        },
        {
            "doc_id": f"education-doe-notice-student-aid-{month_ago_str}", # Tie ID to date
            "title": "Department of Education Notice Regarding FAFSA Simplification",
            "publication_date": month_ago_str, # <-- Assigned ~30 days ago
            "document_type": "Notice",
            "summary": "This notice provides updates on the implementation timeline and changes related to the Free Application for Federal Student Aid (FAFSA) simplification process."
        },
         {
            "doc_id": f"justice-doj-rule-firearms-stabilizers-{year_ago_str}", # Tie ID to date
            "title": "DOJ Final Rule on Definition of 'Firearm' and Related Definitions",
            "publication_date": year_ago_str, # <-- Assigned ~365 days ago
            "document_type": "Rule",
            "summary": "The Department of Justice, Bureau of Alcohol, Tobacco, Firearms, and Explosives (ATF) finalizes a rule clarifying the definition of 'firearm,' particularly as it applies to stabilizing braces."
        }
    ]

    # In a real scenario, you'd filter these based on the date window requested
    # by the pipeline scheduler. For this demo, we'll just return the full list
    # and rely on process_data.py's INSERT OR IGNORE and the agent's date filtering.
    # If you wanted to strictly simulate fetching *only* recent, you'd add a filter here:
    # fetched_data = [item for item in sample_data_template if datetime.strptime(item['publication_date'], '%Y-%m-%d') >= today - timedelta(days=days_window)]

    fetched_data = sample_data_template # Return the whole list for the demo

    print(f"Simulated fetching {len(fetched_data)} documents.")
    # print(json.dumps(fetched_data, indent=2)) # Uncomment to see fetched data structure
    return fetched_data

if __name__ == "__main__":
    # Example of running fetch
    fetched_data = simulate_fetch_recent_documents(days_window=7)
    print(f"Fetched {len(fetched_data)} items.")



'''import json
from datetime import datetime, timedelta

def simulate_fetch_recent_documents(days=7):
    """
    Simulates fetching documents published in the last `days` days.
    In a real app, this would query an external API.
    """
    today = datetime.now()
    recent_date = (today - timedelta(days=days-1)).strftime('%Y-%m-%d')
    current_date = today.strftime('%Y-%m-%d') 

    print(f"Simulating fetch for data published on or after {recent_date}...")

    sample_data = [
        {
            "doc_id": "2023-10-05-exec-order-1",
            "title": "Executive Order on Advancing AI Safety",
            "publication_date": current_date, 
            "document_type": "Executive Order",
            "summary": "This order establishes new standards for AI safety and security, protects Americans from AI risks, supports innovation, and advances American leadership globally."
        },
        {
            "doc_id": "2023-10-04-rule-epa-1",
            "title": "EPA Final Rule on Emissions Standards",
            "publication_date": (today - timedelta(days=1)).strftime('%Y-%m-%d'), 
            "document_type": "Rule",
            "summary": "The Environmental Protection Agency is finalizing new standards for vehicle emissions, aimed at reducing pollution and improving air quality."
        },
         {
            "doc_id": "2023-10-05-notice-doe-1",
            "title": "Notice of Funding Opportunity for Renewable Energy",
            "publication_date": current_date, 
            "document_type": "Notice",
            "summary": "The Department of Energy announces a funding opportunity for projects focused on developing and deploying innovative renewable energy technologies."
        },
         {
            "doc_id": "2023-10-03-presidential-memo-1",
            "title": "Memorandum on Critical Infrastructure Security",
            "publication_date": (today - timedelta(days=2)).strftime('%Y-%m-%d'), 
            "document_type": "Presidential Memorandum",
            "summary": "This memorandum directs agencies to assess and enhance the security of critical infrastructure against emerging threats."
        },
    ]
    print(f"Simulated fetching {len(sample_data)} documents.")
    return sample_data

if __name__ == "__main__":
    fetched_data = simulate_fetch_recent_documents(days=7)'''