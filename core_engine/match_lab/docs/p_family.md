# F-2: past family read from the resume only (13 Oct 2026)

Method: `src/cvfamily.py` on 3,586 stored CVs (`raw_cv`). Read-only export, git-ignored. Tier S, confidence 0.6 (no gold labels yet; see F-3).

## Source mix
- titles: 2377 (66%)
- text: 658 (18%)
- headline: 539 (15%)
- None: 12 (0%)

## Family mix
- engineer: 2081
- data: 810
- product: 205
- finance_risk: 157
- ops: 156
- sales_travel: 128
- manager: 37
- None: 12

Share with confidence below 0.6: 21.5%.
Old top-3-vote family agrees with the resume family in 66% of 3574 CVs. Agreement by source: titles 65%, headline 74%, text 60%.

## 30 random samples (resume family | source | confidence | role titles found | old top-3 vote)

|#|family|source|conf|titles|old vote|
|--|--|--|--|--|--|
|1|data|text|0.38||data|
|2|engineer|titles|1.00|Smart Software Services B.V.; Engineering Intern Remote – CA, USA|data|
|3|engineer|titles|1.00|Software Development Intern, OnlineJaoo.|engineer|
|4|ops|titles|0.84|Performed data extraction, cleaning, and|data|
|5|engineer|titles|0.95|Software Engineer Associate, Accenture –; TECHNICAL DEEP DIVE & CAREER INVESTMENT|engineer|
|6|engineer|titles|0.97|MAQ Software - Software Developer; Machine Learning Research Intern|engineer|
|7|engineer|text|0.64||engineer|
|8|engineer|titles|0.87|Founding Engineer | Ploughback (; Software Engineer | Flex recruit (Ivans |engineer|
|9|engineer|titles|0.73|Data Analyst Intern at HR Department; Associate Engineer|data|
|10|engineer|titles|1.00|Software Developer; Software Intern|engineer|
|11|data|titles|0.76|Engineered in-house asset management wor; Developed Python/Linux automation for ma|data|
|12|engineer|titles|1.00|Software Developer — Java, Spring Boot, ; Android Developer — Java, OOPs, Firebase|engineer|
|13|engineer|titles|1.00|Software Development Intern Kolkata, WB; ments, bug fixes, and collaborative soft|engineer|
|14|data|headline|1.00||data|
|15|engineer|titles|1.00|Software Developer Engineer - 2|engineer|
|16|engineer|titles|1.00|Software Engineer Intern; Software Engineer Intern|engineer|
|17|data|titles|0.95|ACKO General Insurance | Data Analyst In|data|
|18|engineer|titles|1.00|Software Engineer; Software Engineer Intern|engineer|
|19|data|titles|1.00|JioHotstar (previously known as Disney+ ; ZS Associates (Decision Analytics Associ|data|
|20|data|text|0.32||ops|
|21|data|titles|0.85|Data Analyst Intern (Fincor)|data|
|22|product|titles|1.00|Business Analyst|finance_risk|
|23|engineer|headline|0.60||engineer|
|24|engineer|titles|1.00|Software Developer — Java, Spring Boot, ; SDE Intern @ ITJOBXS|sales_travel|
|25|product|titles|0.90|Product Manager; Product Analyst|product|
|26|sales_travel|titles|1.00|Senior Consultant; Business Consultant|finance_risk|
|27|ops|text|0.26||data|
|28|data|titles|1.00|IBM SkillsBuild, Data Analytics|data|
|29|engineer|titles|1.00|▶ Shipped a multi-section portfolio plat|engineer|
|30|data|titles|0.54|Specialist Programmer; Specialist Programmer Intern|data|

## F-3: gold check (13 Oct 2026, tier S, confidence 0.6)
150 CVs, stratified by source (50 titles, 50 text, 40 headline, 10 none). Labelled by Claude from a scrubbed 400-700 character snippet: one family or `other`, plus 0 to 1 confidence. File: `data/gold/cv_family_labels.jsonl`. 97 usable (family not `other`, confidence >= 0.6): engineer 54, data 23, product 9, finance_risk 4, sales_travel 4, ops 3. The 53 others are blank or garbled snippets, fresh graduates with no work, or fields outside the 7 families.
Limits: the labeller saw only a snippet; labels are mine, not the candidates'; 4 of 7 families have under 10 examples, so only engineer, data and the tech total mean anything.

| Method | Top-1 accuracy | 95% interval |
|---|---|---|
| Old way: vote of the top-3 cosine jobs | 0.629 | 0.53 to 0.72 |
| Embedding classifier alone (trained on job titles) | 0.753 | 0.66 to 0.84 |
| `cvfamily` (resume titles + summary) | 0.773 | 0.68 to 0.86 |
| `cvfamily` 50/50 with embedding classifier | 0.794 | 0.71 to 0.87 |
| Same, but engineer and data counted as one "tech" family | 0.907 | 0.85 to 0.96 |

- By source: summary 0.89 (35), titles 0.79 (38), whole-text keywords 0.58 (24). When `cvfamily` confidence is 0.9 or more: 0.897 (39 CVs).
- Of 22 mistakes, 11 are engineer versus data. Many CVs honestly sit between them (data engineer, ML engineer, SWE with data projects). That is real overlap, not only a parser fault.
- Pass mark was 0.90. Exact 7-family: NOT met (0.79). With engineer and data merged: met (0.91).
- Reading: the resume-only family is clearly better than the top-3 vote (+0.15 to +0.17). A hard gate on 7 exact families would wrongly block about 1 in 5 CVs; a hard gate on the merged "tech" family is safe, and the engineer-vs-data choice inside tech should be a soft preference, not a wall.
