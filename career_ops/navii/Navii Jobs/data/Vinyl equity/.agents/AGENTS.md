# Vinyl Equity Candidate Screening Workflow

## Goal
To deeply analyze and score profiles from a candidate CSV file for the Applied AI Lead position at Vinyl Equity, using the 6-pillar matrix defined in `evaluation_criteria.md`.

## Instructions for Agents

When requested to evaluate candidate profiles from the CSV file:

1. **Extract Candidate Info**: Extract the candidate's name and bio/headline from the CSV file. Skip generic company lines or unrelated noise.
2. **Web Search (Agent Browser Tool)**: For each candidate, you MUST use the `search_web` tool to search for their LinkedIn profile and current details. 
   - **Query Format**: `"{Candidate Name}" "{Current Company or Keywords from Bio}" LinkedIn`
   - Review the search results to infer their detailed work history, current location, education, and specific tech stack details.
3. **Pillar 6 Context Search**: When analyzing for Pillar 6 (Readiness to Move), pay special attention to:
   - Location mentions in the search results (Mangaluru, Bengaluru, Udupi, Karnataka, South India).
   - University/College (NITK Surathkal, Manipal, etc.).
   - Years of experience (to gauge if they are early-career vs established with families).
4. **Scoring**: Evaluate the candidate strictly against all 6 Pillars from `evaluation_criteria.md`. 
5. **Multiplier Calculation**: Apply the appropriate Company Tier Multiplier based on their current or prominent past employers.
6. **Reporting**: Produce a structured output for EACH candidate with the score breakdown, rationale for each pillar, and the final multiplied score.

## Example Output Format
> **Candidate Name:** [Name] (Current: [Title] at [Company])
> * **Pillar 1 (AI Automation):** [Score]/25 *([Rationale])*
> * **Pillar 2 (Tech Stack):** [Score]/20 *([Rationale])*
> * **Pillar 3 (Seniority/Playbook):** [Score]/15 *([Rationale])*
> * **Pillar 4 (Fintech Domain):** [Score]/10 *([Rationale])*
> * **Pillar 5 (Efficiency Mindset):** [Score]/10 *([Rationale])*
> * **Pillar 6 (Readiness to Move):** [Score]/20 *([Rationale])*
> * **Base Score (S_base):** [Total]/100
> * **Company Multiplier:** Tier [X] ([Multiplier])
> * **Final Shortlist Score:** **[Final]** 

**CRITICAL RULE:** Do not skip the search step. The CSV bio alone is not enough to accurately score Pillar 2, 3, 5, and 6. Use the web search tool to enrich the profile context before scoring.
