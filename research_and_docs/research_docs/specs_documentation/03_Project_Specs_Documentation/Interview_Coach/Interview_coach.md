**Analytical/Estimation Interview (Fermi Problems) – Knowledge Base for AI Coaching**  
**Stage Overview**

* **Typical format:** The interviewer poses an ambiguous quantitative question (e.g., “How many golf balls fit in a plane?”). You have 5–10 minutes to think aloud, structure a solution, and arrive at a reasonable estimate. No calculators are allowed; arithmetic is done mentally or on a whiteboard.  
* **Why it’s included:** It tests quantitative reasoning, comfort with ambiguity, logical decomposition, and the ability to communicate a clear thought process under pressure. It simulates the early scoping phase of real product problems where data is scarce.

**Evaluation Rubric**

* **Logic and structure over exact numbers:** The interviewer cares far more about *how* you break down the problem than about the final figure. A well‑segmented equation tree earns high marks even if one component estimate is off.  
* **Clarity of assumptions:** Every estimate must be explicitly stated and justified. “Let’s assume a standard school bus is 8 ft wide, 6 ft tall inside” is strong; guessing without explanation is weak.  
* **Sanity checks:** After computing, compare the result to a known benchmark or perform a quick reverse calculation. “That would mean the bus holds 10,000 balls; if each ball is 2.5” in diameter, that seems plausible.”  
* **Ease with numbers:** You must handle mental multiplication/division comfortably. Use round numbers, simplify fractions, and show intermediate steps. Overly complex arithmetic signals a lack of fluency.  
* **Communication:** Talk continuously; signpost the transition from one segment to the next. A structured monologue (“Now we’re estimating the volume of the bus …”) is expected.

**Characteristics of a High-Scoring Candidate**

* Writes a step‑by‑step equation on the board (e.g., `Total balls = (Bus volume / Ball volume) × Packing efficiency`).  
* States every assumption out loud with a brief rationale (“I’ll use 8 ft width because a typical school bus is about 8 ft wide and 6 ft tall on the inside”).  
* Calculates in a clean, linear fashion, rounding numbers aggressively (e.g., π ≈ 3, cubic inches to cubic feet conversion simplified).  
* Performs a reality check at the end (“500,000 balls? That’s about 20 truckloads – feels order‑of‑magnitude correct”).  
* Explains reasoning calmly, never rushes, and shows excitement about the logic puzzle.  
* **Model example snippet (bus question):** *“Let’s assume the passenger cabin is a rectangular prism 30 ft long, 8 ft wide, 6 ft high. That gives a volume of 30×8×6 \= 1,440 ft³. A golf ball diameter is about 1.7 inches; converting to feet gives roughly 0.14 ft, so its volume is (4/3)π (0.07 ft)³ ≈ 0.0014 ft³. Using a 74% packing efficiency for spheres, the number is (1,440 / 0.0014) × 0.74 ≈ 760,000 balls. That sounds a bit high; let’s sanity‑check: 760,000 balls in a bus would form a cube about 9 ft on a side, which is smaller than the bus interior – feasible.”*

**Characteristics of a Low-Scoring Candidate**

* Jumps immediately to a number (“I think it’s 50,000”) with no visible structure.  
* Gets lost in tiny details (e.g., debating the exact curvature of the bus ceiling for minutes).  
* Cannot articulate what assumptions they are making, leaving the interviewer to guess the logic.  
* Flails when stuck, either going silent or randomly changing direction.  
* Gives a final answer without any sanity check, oblivious to an order‑of‑magnitude error.

**Question Bank with Segmented Answers**  
For each question, the **Model Answer Segmentation** breaks the solution into tiny chunks (at most 2 sentences each) that can be practiced as stand‑alone steps.  
**1\. How many golf balls can you fit in a school bus?**  
**Segments:**

* **Clarify scope:** I assume a standard full‑size school bus in the U.S., considering only the interior passenger compartment (no engine bay, no seats). The shape is approximated by a rectangular box.  
* **Define formula:** Total golf balls \= (Interior volume of bus / Volume of one golf ball) × Packing efficiency of random close‑packed spheres (≈ 0.64–0.74; I’ll use 0.7).  
* **Estimate bus volume:** A typical school bus is roughly 35 ft long, 8 ft wide, and 6 ft tall inside. Volume \= 35 × 8 × 6 \= 1,680 ft³.  
* **Estimate golf ball volume:** A golf ball has a diameter of 1.68 in. Convert to feet: 1.68 in / 12 ≈ 0.14 ft. Radius \= 0.07 ft. Volume \= (4/3)π(0.07)³. Use π ≈ 3.14, (0.07)³ \= 0.000343, so volume ≈ (4/3)×3.14×0.000343 ≈ 0.00144 ft³.  
* **Crunch numbers:** Balls \= (1,680 ft³ / 0.00144 ft³) × 0.7. 1,680 / 0.00144 \= 1,680 / (1.44×10⁻³) \= (1,680 / 1.44) × 1,000 ≈ 1,167 × 1,000 \= 1,167,000. Multiply by 0.7 → ≈ 817,000 golf balls.  
* **Sanity check:** 800,000 balls, each \~1.7″ diameter, lined up would span about 1.1 million inches ≈ 17 miles – far longer than the bus, but packed in 3D it forms a cube of (800,000)^(1/3) ≈ 93 balls per side, or \~130 inches ≈ 11 ft, which fits within the 6×8 ft cross‑section. Reasonable.

**2\. Estimate the annual revenue of a coffee shop in downtown San Francisco.**  
**Segments:**

* **Clarify scope:** I’ll consider a typical independent specialty coffee shop (not a chain like Starbucks) in a high‑foot‑traffic downtown area, with only coffee and basic pastries as revenue sources.  
* **Define formula:** Annual revenue \= (Avg. customers per hour × Operating hours per day × Days open per year) × Average ticket size.  
* **Estimate customers per hour:** During peak morning rush (7–10 AM) maybe 60 customers/hour; midday 30/hour; afternoon 20/hour; early evening 15/hour. A weighted average across a 14‑hour day (6 AM–8 PM) yields roughly 25–30 customers/hour. I’ll use 25\.  
* **Estimate operating days & hours:** Open 6 AM to 8 PM → 14 hours/day. 360 days/year (closed a few holidays). So total serving hours per year \= 14 × 360 \= 5,040 hours.  
* **Estimate average ticket:** Assume a typical order is a $4 latte plus a $3 pastry → $7. Some customers only buy a $3 coffee, so average ≈ $6.  
* **Crunch numbers:** Annual revenue \= 25 customers/hr × 5,040 hr × $6 \= 25 × 5,040 \= 126,000; 126,000 × $6 \= $756,000.  
* **Sanity check:** 756*kperyearmeans* 2,100/day. At 25 customers/hr × 14 hr \= 350 customers/day, $2,100/350 \= $6 avg ticket, consistent. Rent in downtown SF for a small shop might be $10k/month \= $120k/year, leaving room for labor, COGS, and profit—plausible.

**3\. How many queries does Google process per second?**  
**Segments:**

* **Clarify scope:** Queries here means user searches entered on Google.com (text, voice) globally, averaged over a year, excluding API calls from other services. Use current year data assumptions.  
* **Define formula:** Queries per second \= (Annual global queries) / (Seconds per year).  
* **Estimate annual queries:** There are \~8 billion people, \~60% internet penetration → 4.8 billion internet users. Assume 90% use Google at least occasionally, but daily active users might be \~3 billion. Average daily searches per user: some do 0, some 10+; I’ll assume a heavy‑tail average of 3 searches per day per internet user (based on typical media reports). So daily global searches \= 4.8B users × 3 \= 14.4 billion searches/day. Annual \= 14.4B × 365 ≈ 5,256 billion (5.26 trillion) searches/year.  
* **Estimate seconds per year:** 60 × 60 × 24 × 365 \= 31,536,000 ≈ 31.5 million seconds.  
* **Crunch numbers:** QPS \= 5.26 trillion / 31.5 million \= (5.26 × 10¹²) / (3.15 × 10⁷) \= (5.26 / 3.15) × 10⁵ ≈ 1.67 × 10⁵ \= 167,000 queries per second.  
* **Sanity check:** Publicly known estimates (e.g., 2016 data: 40,000 QPS; growth suggests \~100k‑200k now). 167k QPS aligns with ballpark figures from tech reports. It means roughly 10 million queries per minute, which feels high but plausible for global reach.

**4\. How many piano tuners are there in New York City?**  
**Segments:**

* **Clarify scope:** I’ll estimate the number of full‑time equivalent piano tuners serving all pianos in NYC (5 boroughs), assuming a tuner works 250 days/year and each piano needs tuning once a year.  
* **Define formula:** Number of tuners \= (Total pianos in NYC × Tunings per year per piano) / (Tunings one tuner can do per year).  
* **Estimate total pianos:** NYC population \~8.5 million. Household size \~2.5 → 3.4 million households. Pianos in homes: maybe 2% of households have a piano (NYC apartments are small, but cultural affinity) → 68,000 home pianos. Add schools, music venues, hotels, studios: estimate 1 per 500 people? Another 17,000 institutional pianos. Total ≈ 85,000 pianos.  
* **Estimate tunings per year per piano:** All pianos need at least one tuning annually (some need two, but assume average 1.2). Use 1.2 to be safe.  
* **Estimate tuner capacity:** A tuner works 5 days/week × 50 weeks \= 250 days/year. Each tuning takes \~2 hours including travel, so 4 tunings/day → 250 × 4 \= 1,000 tunings/year.  
* **Crunch numbers:** Total annual tunings needed \= 85,000 × 1.2 \= 102,000. Number of tuners \= 102,000 / 1,000 \= 102 tuners.  
* **Sanity check:** That’s about 1 tuner per 83,000 people, which seems plausible for a specialized trade in a large city. If each tuner earns \~80*pertuning*,*annualrevenue* 80k, so a sustainable number of professionals.

**5\. What is the market size for electric toothbrushes in India?**  
**Segments:**

* **Clarify scope:** Market size in annual revenue (USD) for consumer electric toothbrushes (replaceable brush heads, not battery‑operated disposables), sold in India, current year.  
* **Define formula:** Annual revenue \= (Number of households that could buy) × (Adoption rate) × (Average price per unit) \+ replacement head revenue.  
* **Estimate addressable households:** India population \~1.4B, average household size \~4.5 → \~310 million households. Electric toothbrushes are a premium product; target urban/semi‑urban, mid‑to‑high income. Approx 35% urbanization, and within that, maybe top 40% income can afford it. So addressable households ≈ 310M × 0.35 × 0.4 ≈ 43 million households.  
* **Estimate adoption rate:** Electric toothbrush penetration in India is low, say 4% of addressable households already own one, and annual new purchases (primary market) maybe 1.5% of addressable households? Let’s model both existing users’ replacement and new buyers. Better: annual units sold \= new adopters \+ replacements. Assume 2% of addressable households buy a new unit each year (new adopters). For installed base, if 4% own, that’s \~1.7M households. Replacement cycle 3 years, so replacements/year ≈ 1.7M / 3 ≈ 0.57M. Total annual units ≈ 43M × 2% \+ 0.57M \= 0.86M \+ 0.57M \= 1.43M units.  
* **Estimate average price:** An entry‑level sonic toothbrush (e.g., Oral‑B) costs \~₹1,500 (18\)*inIndia*;*premiummodelshigher*.*Averagesellingprice*≈₹2,000(25). Replacement heads (2‑3 per year) add \~₹400/year per user. So annual value per unit including heads ≈ $25 \+ $5 \= $30.  
* **Crunch numbers:** Annual revenue ≈ 1.43M units × $30 ≈ $43 million USD.  
* **Sanity check:** Indian oral care market is \~$2B; electric brushes are niche. $43M is \~2% of that, sensible. A known report from 2022 pegged it at $35M, growing; order of magnitude correct.

**6\. How many iPhones are currently in use worldwide?**  
**Segments:**

* **Clarify scope:** Active iPhones (not just sold, but turned on and used at least occasionally) globally, as of today. I’ll use cumulative sales adjusted for attrition.  
* **Define formula:** Active iPhones \= Cumulative historical sales – iPhones that have been retired (broken, lost, replaced).  
* **Estimate cumulative sales:** Apple started selling iPhones in 2007\. Major sales milestones: 1B sold by 2016, 2B by 2020, cumulative sales likely \~2.5B by 2024\. I’ll assume 2.5 billion total units ever sold.  
* **Estimate retirement rate:** iPhones are typically used for 3‑4 years before being retired or handed down, but many are still active as secondary devices. A common industry estimate: \~75% of all iPhones ever sold are still in use. Let’s assume 75% survival rate. So active iPhones \= 2.5B × 0.75 \= 1.875B.  
* **Refine with installed base data:** Apple has reported active installed base of iPhones crossing 1 billion in 2019 and 1.5 billion recently (2023). Current likely \~1.6‑1.7B. I’ll use 1.65 billion.  
* **Crunch numbers:** Active iPhones ≈ 1.65 billion.  
* **Sanity check:** Global smartphone users \~4.6B, iPhone market share \~18‑20% in units, but active base share may be \~25% due to longer usage. 1.65B / 4.6B ≈ 36%? That seems high; wait, iPhones are \~25% of global smartphone installed base per Counterpoint (2023: \~1.5B out of 6B? Let’s adjust: Actually, total smartphone installed base \~6.5B; 1.65B/6.5B ≈ 25%. Plausible.

**7\. Estimate the number of gas stations in the United States.**  
**Segments:**

* **Clarify scope:** Retail gas stations (including convenience store fuel outlets) that serve public vehicles, excluding private fleet depots. All 50 states.  
* **Define formula:** Number of gas stations \= (Total vehicle miles traveled per year / Average miles refueled per station per year) or supply‑side: population per station. I’ll use demand‑side: stations needed to service daily fuel demand.  
* **Estimate number of vehicles and fuel consumption:** U.S. has \~330M people, \~0.8 vehicles per capita → \~264 million vehicles. Average miles driven per vehicle per year ≈ 12,000 miles, average fuel economy \~25 mpg → 480 gallons/year per vehicle. Total gasoline demand ≈ 264M × 480 ≈ 126.7 billion gallons/year.  
* **Estimate fuel sold per station:** A typical gas station sells \~1.5 million gallons per year? I’ll check: A busy station may pump 100,000 gallons/month \= 1.2M gal/year, smaller ones less. Weighted average maybe 80,000 gal/month \= 960,000 gal/year. Use 1 million gallons/year per station.  
* **Crunch numbers:** Stations \= 126.7B gal / 1M gal/station \= 126,700 stations. Round to \~125,000–130,000.  
* **Sanity check:** NACS (convenience store association) reports \~150,000 fueling stations in the U.S. (includes diesel, etc.). Our gasoline‑only estimate 127k, plus diesel stations might add a few thousand, so 130k‑145k aligns. Population‑based check: 330M / 130k ≈ 2,500 people per station, which matches a rule of thumb (1 per 2,000–3,000). Reasonable.

**Frameworks and Cheatsheets**  
Memorize these constants and typical assumptions; they are the building blocks of most Fermi estimates.

| Category | Constant / Typical Value | Notes |
| ----- | ----- | ----- |
| **World** | Population: 8.0 billion | 2024 approx. |
|  | Internet users: 5.3 billion (\~66%) |  |
|  | Smartphone users: \~4.6 billion |  |
|  | Urban population: 57% |  |
| **USA** | Population: 330 million |  |
|  | Households: \~130 million (2.5 people/household) |  |
|  | Vehicles: \~280 million |  |
|  | Smartphone penetration: \~90% |  |
|  | Gas stations: \~145,000 | For sanity checks |
| **India** | Population: 1.4 billion |  |
|  | Households: \~300 million (4.5 people/hh) |  |
|  | Urbanization: \~35% |  |
|  | Internet penetration: \~50% |  |
|  | Middle class / upper income: \~30% of pop |  |
| **Volumes & Dimensions** | 1 cubic foot \= 1,728 cubic inches |  |
|  | 1 foot \= 0.3048 meters (use 0.3) |  |
|  | Golf ball diameter: 1.68 in (0.14 ft) | Standard |
|  | School bus interior: 35 ft × 8 ft × 6 ft | Typical full size |
|  | Spherical packing efficiency: 0.64 (random loose) to 0.74 (face-centered cubic) | Use 0.7 as average |
| **Speed/Time** | Days per year: 365 (or 360 for ease) |  |
|  | Hours per year: 8,760; seconds per year: 31.5 million |  |
|  | Working days per year (US): 250 | 5 days × 50 weeks |
| **Economy** | US median household income: \~$75k |  |
|  | Coffee shop average ticket: $5–7 |  |
|  | Typical small business revenue per employee: $100k–200k |  |
| **Digital** | Google search queries per day: \~8.5 billion (2023) | For calibration |
|  | iPhone active installed base: \~1.5 billion | Apple disclosures |
|  | Average smartphone replacement cycle: 3 years |  |
| **Assorted** | Piano tuning frequency: 1–2 times per year |  |
|  | Tuner capacity: 2–4 tunings per day | Includes travel |

**Practice Approach – The Nursery Method**  
The nursery method builds fluency by repeating segmented answers until each step feels automatic. Here’s how to apply it to this knowledge base:

1. **Print or display one segmented model answer** (e.g., golf balls in bus) on a flashcard. The front shows the question; the back shows the list of tiny segments (each ≤ 2 sentences).  
2. **Read the question aloud, then recite the first segment** (“I assume a standard full‑size school bus …”). Check against the card. If correct, move to the next segment.  
3. **Chain segments** – after mastering each in isolation, recite the entire sequence from “Clarify scope” to “Sanity check” without peeking.  
4. **Vary the numbers** – once the pattern is memorized, slightly change the assumptions (e.g., bus length 40 ft) and recalculate on the fly. The goal is to internalize the equation structure, not the specific digits.  
5. **Use a metronome** – set a timer for 4–5 minutes and work through the problem, practicing calm, signposted speech.  
6. **Pair with a partner** – one person asks the question, the other answers while the listener ticks off each segment. Swap roles.  
7. **Progress through all 7 questions** in the bank, then create your own variants (e.g., tennis balls in a 747, dry cleaners in Chicago). Always force yourself to state the formula first.

**Full Walkthrough: “How many golf balls fit in a school bus?” (Segmented Monologue)**  
Below is the exact text a high‑scoring candidate might say, broken into the segments from the model answer. Use it to drill the thinking‑out‑loud rhythm.  
**1\. Clarify scope:** “I’m going to consider a standard full‑size U.S. school bus, just the rectangular passenger cabin with the seats removed. I’ll ignore the driver’s area, engine compartment, and the curvature of the ceiling.”  
**2\. Define formula:** “The number of golf balls equals the interior volume of the cabin divided by the volume of a single golf ball, multiplied by a packing efficiency factor. For random close‑packed spheres I’ll use an efficiency of 0.7, which is between random loose and perfect arrangement.”  
**3\. Estimate bus volume:** “A typical school bus interior is about 35 feet long, 8 feet wide, and 6 feet high. So the volume is 35 times 8 times 6, which gives 1,680 cubic feet.”  
**4\. Estimate golf ball volume:** “A golf ball has a diameter of 1.68 inches. Converting to feet, that’s 1.68 divided by 12, or 0.14 feet. The radius is 0.07 feet. Volume of a sphere is four‑thirds pi r‑cubed. I’ll use pi equals 3.14. r‑cubed is 0.07 times 0.07 times 0.07, which is about 0.000343. Multiply: four‑thirds is roughly 1.33, times 3.14 is about 4.18, times 0.000343 gives 0.00144 cubic feet.”  
**5\. Crunch numbers:** “Now divide 1,680 cubic feet by 0.00144 cubic feet per ball. That’s the same as 1,680 divided by 1.44 times 10 to the minus 3, which equals 1,167 times 1,000, or about 1,167,000 balls. Multiply by the 0.7 packing efficiency and I get roughly 817,000 golf balls.”  
**6\. Sanity check:** “Let’s check: 800,000 balls, each roughly 1.7 inches across, if arranged in a cube would be the cube root of 800,000, about 93 balls per side. That’s 93 times 1.7 inches, about 158 inches, or 13 feet per side – which fits inside a bus that is 35 by 8 by 6 feet. The number feels order‑of‑magnitude correct.”  
That’s it. Practice until this structure becomes second nature, and you’ll walk into any Fermi interview ready to impress.  
