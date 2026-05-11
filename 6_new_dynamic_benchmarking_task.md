MISSION: Multi-Agent Harness for Asset Benchmarking (Phase 1.3)
1. STRATEGIC CONTEXT & ASSET METADATA
Requirement: The analysis must be grounded in deep asset metadata. If the information below is insufficient, the Researcher Agent must first infer the missing functional capabilities based on the "Primary Use Case."

Asset Name: PFEP/IVO Core Platform
Asset Description: Empowers organizations to standardize and scale part‑level planning, inventory, and replenishment decisions by unifying data, analytics, and planning processes into a centralized PFEP platform—enabling faster, more confident decisions across sites, functions, and value streams.
Target Industry/Sector: IP - Industrial Product
Technical Stack: Pyspark/Azure Databricks, React Dashboard 
Primary Use Case: Provide a centralized PFEP foundation for scalable part‑level planning and execution.

2. AGENTIC WORKFLOW (THE HARNESS)

    STEP 1: THE CROSS-SECTOR RESEARCHER (Deep Ingestion)
    Role: Global Competitive Intelligence Specialist.
    Task: Search for "Winning Assets" and "Success Stories" across three distinct tiers:
    COTS Leaders: (SAP IBP, Oracle SCM, Kinaxis, LeanDNA).
    Consulting Peers (The Big 4 & MBB): Search for proprietary assets from Deloitte (e.g., Treadway), PwC, KPMG, BCG (e.g., Lighthouse/Gamma), and Bain (e.g., Vector).
    Tech Giants: Search for Microsoft (Supply Chain Center), Google Cloud (Supply Chain Twin), and AWS (Supply Chain) reference implementations.
    Goal: Find specific "Winning Stories" where these players solved the [Primary Use Case] for the [Target Industry].

    STEP 2: THE ANTAGONIST (The "Brutal" Auditor)
    Role: Skeptical Chief Digital Officer (CDO) at a Fortune 500 company.
    Task: Stress-test the EY Asset's existence.
    Challenge: "Why wouldn't I use BCG's proven methodology or Microsoft's native cloud tools instead of this EY asset? Is this asset just a 'wrapper' around a dashboard, or does it have unique intellectual property (IP) that Deloitte or SAP hasn't built yet?"
    Defense Focus: Define the "Moat" (e.g., proprietary algorithms, unique industry data sets, or integrated consulting-to-code workflow).

    STEP 3: THE STRATEGIST (Synthesis & Value Gap)
    Role: Lead Partner, Business Transformation.
    Task: Conduct a three-way gap analysis:
    vs Consulting Peers: Compare the "Methodology Depth" and "Client Entry Point."
    vs Tech Giants: Compare "Scalability" and "Cost of Ownership."
    vs COTS: Compare "Functional Granularity" (especially at the Part-level).
    
3. HARNESS QUALITY GATE (Evidence Check)
The Auditor must reject any result that only lists "Features." We require Evidence of Value.

Success Criteria: "Deloitte's tool won at [Client X] because of [Feature Y], resulting in [Benefit Z]. Our asset counters this by [Our Unique Edge]."

Evidence Rules (Mandatory):
- Every competitor claim (winning_story, advantage, focus) must have at least one direct evidence link.
- Use direct story/case-study/report pages only (deep links), not broad landing pages.
- Do NOT include restricted/gated/inaccessible pages (HTTP 403/404, login-required, cookie-wall-only, paywalled).
- If a competitor has no accessible direct evidence, omit that competitor from output.
- Claims without direct evidence links must be removed.

4. FINAL OUTPUT SPECIFICATION (JSON)
Consolidate the debate and evidence. You MUST prompt the user to save this as 6_gap_analysis.json.

JSON Schema:

{
    "report_id": "6_gap_anaysis_2026-05-11",
    "asset_name": "[Asset Name]",
    "market_standing": "Challenger/Niche Leader/Innovator",
    "benchmarking": {
        "competitor_tiers": {
            "consulting_peers": [{"firm": "Deloitte/BCG/Bain", "asset": "", "winning_story": ""}],
            "tech_giants": [{"company": "MSFT/GOOG/AWS", "solution": "", "advantage": ""}],
            "cots_vendors": [{"name": "SAP/Kinaxis", "focus": "", "gap_vs_us": ""}]
        },
        "pros": ["Unique IP and Consulting-led advantages"],
        "cons": ["Vulnerabilities vs Big Tech or COTS automation"],
        "functional_gaps": ["High-priority features identified from winning stories"]
    },
    "improvement_roadmap": [
        "Strategic action based on Competitor Tier analysis"
    ],
    "reference_evidence": [
        {
            "related_to": "benchmarking.competitor_tiers.<tier>[i].<winning_story|advantage|focus>",
            "entity": "Competitor name",
            "links": ["Direct case-study/report URL only"]
        }
    ]
}

Reference Evidence Rules:
- The `reference_evidence` section must map links to specific competitor claims using `related_to`.
- Each `links` array must contain only direct, accessible evidence URLs.
- Remove any stale or broad links that require extra navigation to find the claim.

