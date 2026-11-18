\# PM Interview Scoring Engine

\#\# 1\. Scoring Philosophy

This scoring engine exists to inject objectivity, consistency, and real‑world fidelity into the AI‑driven PM interview coaching process. Its purposes are threefold: first, to measure demonstrated competencies against a stable yardstick rather than relying on subjective impression; second, to track improvement over repetitions so the candidate sees concrete progress; and third, to simulate the decision‑making logic of actual FAANG interviewers, who balance multiple signals and occasionally probe deeper with follow‑up questions.

Scores are based entirely on demonstrated competencies — the quality of structure, reasoning, user empathy, creativity, strategic thinking, technical soundness, and communication — not on word count, memorisation fidelity, or how quickly an answer is delivered. The engine is designed to work harmoniously with the nursery‑style teaching method: no scoring occurs during isolated segment repetition; the first evaluation gate opens only when the candidate chains segments or delivers a full answer. This ensures the score reflects the integrated, interview‑ready performance.

Every rule, rubric, and formula in this document is written to be directly implementable by the coaching AI without ambiguity.

\---

\#\# 2\. Universal Rating Scale

All stages and all dimensions use a single, consistent 1–5 scale. Each level is anchored to observable behaviours.

| Score | Label | Behavioural Anchor |  
|-------|-------|--------------------|  
| \*\*1\*\* | No Hire | Major flaws: no discernible structure, absent user empathy, critical misunderstanding of the question, incoherent or irrelevant response. |  
| \*\*2\*\* | Lean No Hire | Attempted some structure but remained unclear; key elements (users, metrics, trade‑offs) largely missing; reasoning is weak or surface‑level; may have contradicted themselves. |  
| \*\*3\*\* | Borderline | Adequate coverage of basics; a visible structure exists but lacks depth, creativity, or sharp prioritisation; average PM signals; answer feels safe and generic. |  
| \*\*4\*\* | Hire / Strong Hire | Clear structure with logical flow; demonstrable user empathy; data‑informed where applicable; acknowledges trade‑offs; only minor gaps that do not undermine the core argument; communication is confident and precise. |  
| \*\*5\*\* | Exceptional / Star | Exceptional clarity and originality; insights that reframe the problem; deep strategic or technical thinking; compelling narrative that would impress any interview panel; leaves the interviewer with nothing to add. |

The coach must use these anchors literally. If an answer meets every criterion of Score 4 and adds one original, insightful dimension, it becomes a 5\. If it meets most of Score 4 but has a noticeable gap in one area, it remains a 4\.

\---

\#\# 3\. Stage-Specific Scoring Dimensions

\#\#\# 3.1 Recruiter Phone Screen

| Dimension | Description | Score 1 | Score 3 | Score 5 |  
|-----------|-------------|---------|---------|---------|  
| Communication Clarity | Is the candidate articulate, concise, and easy to follow? | Rambling, unclear, cannot summarise their own background. | Coherent but occasionally verbose or vague; gets the point across. | Crisp, compelling, every sentence earns its place; the recruiter is engaged. |  
| Background & Fit Articulation | Can they connect their experience to the PM role and the company? | Cannot explain why PM or why this company; generic. | Gives reasonable but unremarkable reasons; some alignment shown. | Tells a tight, authentic story that makes their path to PM and to this company feel inevitable. |  
| Motivation & Professionalism | Do they show genuine interest, preparation, and appropriate expectations? | Unprepared, asks no questions, unrealistic salary or timeline demands. | Shows basic research and realistic expectations; polite. | Asks insightful questions that demonstrate deep company and product knowledge; leaves a memorable positive impression. |

\#\#\# 3.2 Hiring Manager Screen

| Dimension | Description | Score 1 | Score 3 | Score 5 |  
|-----------|-------------|---------|---------|---------|  
| Product Intuition | Can they think about a product problem sensibly, even without a full framework? | Jumps to a random solution with no user or problem exploration. | Identifies a user and a plausible problem; solution is reasonable but not inspired. | Reframes the problem cleverly, identifies non‑obvious user needs, proposes a creative yet feasible approach. |  
| Structured Thinking | Do they organise their thoughts or dump them? | No structure; stream of consciousness. | Imposes a basic before/after or pros/cons structure. | Uses a clear mental model (even if lightweight) and signposts throughout. |  
| Leadership & Self‑Awareness | Do they talk about their experience with ownership and reflection? | Blames others, takes no ownership, no lessons learned. | Describes a team effort with some personal role; lesson is generic. | Owns outcomes completely, articulates specific personal actions, extracts a non‑obvious lesson they have since applied. |

\#\#\# 3.3 Product Design

| Dimension | Description | Score 1 | Score 3 | Score 5 |  
|-----------|-------------|---------|---------|---------|  
| User Empathy & Problem Definition | Do they deeply understand the user and the problem before solving? | Skips users entirely; solves a problem they invented. | Names a user persona and a pain point; somewhat generic. | Paints a vivid user scenario with specific, non‑obvious needs; ties the problem to real human behaviour or data. |  
| Ideation & Creativity | Do they generate a range of ideas and think beyond the obvious? | One idea, or ideas all variations of the same thing. | A few reasonable ideas with some differentiation. | A broad set of ideas spanning different solution categories; includes a wild, creative option and explains why it is or isn't viable. |  
| Structure & Clarity | Is their thought process transparent and logical? | Disorganised; jumps between topics. | Follows a recognisable framework (e.g., CIRCLES) but mechanically. | Framework is adapted fluidly to the specific question; clear signposting; summary at the end. |  
| Prioritisation & Trade‑offs | Can they make tough choices and articulate what they are trading off? | Lists everything; no prioritisation. | Mentions prioritisation but criteria are vague (e.g., "impact vs effort" without specifics). | Defines crisp criteria tied to user and business goals; explicitly states what they would NOT build and why. |  
| Metrics & Success Measurement | Do they define how they would know if the product is successful? | No metrics mentioned, or vanity metrics only. | Names a relevant metric but doesn't explain measurement or target. | Defines a primary metric, a counter‑metric, and how they would instrument and validate; considers leading vs lagging indicators. |

\#\#\# 3.4 Product Strategy

| Dimension | Description | Score 1 | Score 3 | Score 5 |  
|-----------|-------------|---------|---------|---------|  
| Market & Competitive Analysis | Do they size the opportunity and understand the landscape? | Ignores market size and competitors. | Estimates a rough market size and names competitors; superficial. | Quantifies TAM/SAM/SOM with clear assumptions; analyses competitor strengths, weaknesses, and likely responses. |  
| Strategic Framing & Structure | Do they use an appropriate framework to break down the problem? | No framework; ad‑hoc thinking. | Applies a standard framework (Porter, SWOT) but somewhat mechanically. | Synthesises multiple frameworks or adapts one creatively; the structure directly serves the recommendation. |  
| Business Model & Financial Reasoning | Do they consider how money is made and what the unit economics look like? | Ignores revenue, costs, or profitability. | Mentions revenue model and basic cost considerations; no quantification. | Builds a rough but explicit unit‑economic model; discusses margins, customer acquisition cost, lifetime value, and payback period. |  
| Recommendation & Conviction | Do they arrive at a clear, defensible recommendation with risks acknowledged? | No clear recommendation, or hedges excessively. | Gives a recommendation but hedges without quantifying risks. | Delivers a confident, specific recommendation with a clear rationale, acknowledges the biggest risk, and proposes a mitigation. |

\#\#\# 3.5 Analytical Estimation

| Dimension | Description | Score 1 | Score 3 | Score 5 |  
|-----------|-------------|---------|---------|---------|  
| Equation & Structure | Do they break the problem into a clear, logical equation? | No equation; jumps to a number. | Has an equation but misses a key component or uses an awkward breakdown. | Elegant, MECE equation that captures the problem perfectly; explains why they chose this breakdown. |  
| Assumption Quality & Explicitness | Are assumptions stated clearly and are they reasonable? | Assumptions hidden or wildly unrealistic. | States assumptions but some are off by orders of magnitude or not justified. | Assumptions are explicit, grounded in real‑world anchors, and calibrated; candidate explains their reasoning for each. |  
| Calculation & Numerical Ease | Do they compute cleanly and handle numbers confidently? | Gets lost, makes arithmetic errors, gives up. | Computes correctly but hesitantly; minor errors they self‑correct. | Smooth, accurate mental math; rounds smartly; maintains composure. |  
| Sanity Check & Communication | Do they validate the final number and explain their thought process clearly? | No sanity check; cannot explain how they arrived at the number. | Performs a basic reality check; communication is clear but not polished. | Proactively sense‑checks the result against a relatable benchmark; the entire delivery is a pleasure to follow. |

\#\#\# 3.6 Technical Depth

| Dimension | Description | Score 1 | Score 3 | Score 5 |  
|-----------|-------------|---------|---------|---------|  
| System Design & Architecture | Can they design a high‑level system with appropriate components? | Cannot identify basic components; no diagram or mental model. | Identifies client, server, database but misses key elements (e.g., caching, queues). | Clean architecture with well‑chosen components; considers load balancing, caching, async processing, and data flow end‑to‑end. |  
| Trade‑off Articulation | Do they discuss alternatives and the pros/cons of their choices? | Picks one technology/tool with no justification. | Mentions a trade‑off (e.g., SQL vs NoSQL) but explanation is shallow. | Evaluates multiple options with specific, contextual criteria (scale, latency, consistency); makes a clear, justified choice. |  
| Technical Communication | Can they explain technical concepts to a non‑engineering audience? | Uses unexplained jargon; confusing. | Explains terms adequately but occasionally slips into overly technical language. | Translates every technical decision into product and user impact; an executive would understand every word. |  
| Scalability & Edge Cases | Do they consider what happens at scale and under failure conditions? | Assumes infinite resources; ignores failure. | Mentions scale but doesn't quantify; acknowledges edge cases without solutions. | Quantifies scale assumptions; proactively designs for failure, data consistency, and bottlenecks; discusses monitoring. |

\#\#\# 3.7 Behavioral & Leadership

| Dimension | Description | Score 1 | Score 3 | Score 5 |  
|-----------|-------------|---------|---------|---------|  
| Situation & Context Setting | Do they set the scene concisely so the story makes sense? | Story is confusing; missing context. | Provides basic context but takes too long or misses a key element. | Sets a crisp, vivid scene in 2‑3 sentences; the interviewer immediately understands the stakes. |  
| Personal Action & Ownership | Does the candidate describe what they specifically did? | Describes team actions; "we" did everything; no personal agency. | Mentions personal actions but they are generic (e.g., "I coordinated"). | Specific, concrete actions the candidate personally took; the story would not have happened without them. |  
| Impact & Quantification | Is the result clear and, where possible, measured? | Vague outcome; "it went well." | States a result but lacks quantification or attribution. | Quantifies impact with numbers; clearly connects their action to the outcome; acknowledges team contributions while owning their part. |  
| Reflection & Learning | Do they articulate what they learned and how they grew? | No lesson; or a cliché. | Mentions a lesson but it's surface‑level or not clearly applied since. | Extracts a non‑obvious, honest lesson; describes how they have applied it subsequently; shows genuine self‑awareness. |

\#\#\# 3.8 Execution & Metrics

| Dimension | Description | Score 1 | Score 3 | Score 5 |  
|-----------|-------------|---------|---------|---------|  
| Metric Definition & Diagnosis | Can they define the right metrics and systematically diagnose a problem? | Looks at one obvious metric; jumps to a cause. | Considers a few metrics but diagnostic approach is unstructured. | Defines a clear primary metric and counter‑metrics; builds a structured root‑cause tree covering internal and external factors. |  
| Hypothesis Generation & Prioritisation | Do they generate multiple hypotheses and prioritise which to test first? | One hypothesis, or all hypotheses equally weighted. | Multiple hypotheses but prioritisation is arbitrary. | Generates a MECE set of hypotheses; prioritises using effort, impact, and likelihood; explains their prioritisation logic. |  
| Experiment Design & Rigour | Can they design a valid experiment or investigation plan? | No experiment design; or fatally flawed design. | Designs a basic A/B test but misses elements (sample size, duration, segmentation). | Specifies hypothesis, success metric, randomisation, sample size calculation, duration, segmentation, and guardrail metrics; anticipates novelty effects. |  
| Actionability & Decision‑Making | Do they propose a clear course of action based on data? | No recommendation; or "look at more data" forever. | Gives a recommendation but without decision criteria or rollback plan. | Recommends a specific action with clear success criteria, a timeline, and a rollback plan; distinguishes between short‑term fix and long‑term solution. |

\---

\#\# 4\. Answer Scoring Procedure

This procedure applies whenever the candidate delivers a full answer (after all segments are taught and chained, during the final independent delivery).

\*\*Step‑by‑step:\*\*

1\. After the candidate finishes the full answer, identify the interview stage and the question type.  
2\. Retrieve the list of applicable scoring dimensions for that stage from Section 3 of this document.  
3\. For each applicable dimension, assign a score from 1 to 5 using the behavioural anchors provided. If a dimension is truly not applicable to the specific question (e.g., "Metrics" for a purely philosophical behavioural question), omit it.  
4\. Compute the \*\*Answer Score\*\* as the arithmetic mean of all scored dimensions, rounded to one decimal place.

\*\*Formula:\*\*  
\`\`\`  
Answer Score \= (Sum of all applicable dimension scores) / (Number of applicable dimensions)  
\`\`\`

\*\*Example — Product Design answer:\*\*  
\- User Empathy & Problem Definition: 4  
\- Ideation & Creativity: 3  
\- Structure & Clarity: 4  
\- Prioritisation & Trade‑offs: 4  
\- Metrics & Success Measurement: 5  
\- Answer Score \= (4 \+ 3 \+ 4 \+ 4 \+ 5\) / 5 \= 20 / 5 \= 4.0 → \*\*4.0 (Hire)\*\*

\---

\#\# 5\. Stage Score Calculation

A "stage" consists of one or more questions practiced within that interview category. The stage score aggregates performance across all questions attempted.

\*\*Rules:\*\*

\- Each question in the stage produces a Final Answer Score (see Section 7 for follow‑up adjustments).  
\- The \*\*Stage Score\*\* is the simple (unweighted) average of all Final Answer Scores for questions practiced in that stage.  
\- If only one question is practiced, the Stage Score equals that question's Final Answer Score.  
\- If the candidate retakes a question (e.g., after feedback and further practice), only the \*\*highest\*\* Final Answer Score among all attempts on that question is used in the stage average. This reflects learning, not penalising early attempts.

\*\*Formula:\*\*  
\`\`\`  
Stage Score \= (Sum of best Final Answer Scores for each unique question) / (Number of unique questions attempted)  
\`\`\`

\*\*Example:\*\*  
\- Question 1 (Product Design): Attempt 1 \= 3.2, Attempt 2 \= 4.0 → Best \= 4.0  
\- Question 2 (Product Design): Attempt 1 \= 3.8 → Best \= 3.8  
\- Stage Score \= (4.0 \+ 3.8) / 2 \= 3.9

\---

\#\# 6\. Cumulative Interview Score

The Cumulative Interview Score represents overall readiness across the entire FAANG PM loop. It is a weighted average of all completed stage scores, scaled to a 0‑100 range for intuitive interpretation.

\*\*Default Weights (Standard FAANG Loop):\*\*

| Stage | Weight |  
|-------|--------|  
| Recruiter Phone Screen | 5% |  
| Hiring Manager Screen | 10% |  
| Product Design | 20% |  
| Product Strategy | 15% |  
| Analytical Estimation | 10% |  
| Technical Depth | 15% |  
| Behavioral & Leadership | 15% |  
| Execution & Metrics | 10% |  
| \*\*Total\*\* | \*\*100%\*\* |

\*\*Formula:\*\*  
\`\`\`  
Cumulative Score \= (W₁ × S₁ \+ W₂ × S₂ \+ ... \+ Wₙ × Sₙ) / (Sum of weights for completed stages) × 20  
\`\`\`  
Where S₁, S₂... are Stage Scores (on the 1‑5 scale), W₁, W₂... are the corresponding weights. Multiplying by 20 scales the 1‑5 average to a 0‑100 scale.

If a stage has not yet been attempted, its weight is excluded and the denominator adjusts to the sum of weights for completed stages only.

\*\*Verbal Interpretation of Cumulative Score:\*\*

| Cumulative Score (out of 100\) | Interpretation |  
|-------------------------------|----------------|  
| 80 – 100 | \*\*Very High Confidence:\*\* The candidate is likely ready for real interviews across multiple stages. |  
| 60 – 79 | \*\*Moderate Confidence:\*\* Solid foundation; targeted practice on weaker stages is recommended. |  
| 40 – 59 | \*\*Needs Significant Improvement:\*\* Major gaps exist; focused drilling on fundamentals required. |  
| Below 40 | \*\*Not Yet Ready:\*\* The candidate should build core PM thinking skills before intensive interview practice. |

\*\*Weights can be adjusted\*\* (see Section 10 for company‑specific modifications). When weights are adjusted, the formula remains the same; only the W values change.

\---

\#\# 7\. Probability-Based Follow-Up Question Mechanism

Real interviewers do not follow a rigid script. Sometimes they nod and move to the next question; other times they lean in and probe deeper. This mechanism simulates that unpredictability.

\*\*Core Rule:\*\*  
Before presenting any new main question, the coaching AI must generate a \*\*Follow‑Up Flag\*\* with the following properties:

\- The flag is randomly set to \*\*0\*\* or \*\*1\*\*.  
\- The probability of 1 is exactly 50%; the probability of 0 is exactly 50%.  
\- The generation is completely random and independent of the candidate's prior performance on any question. No score influences it.  
\- The coach may simulate randomness mentally or use any available randomisation function. The method of generation does not matter as long as the probabilities are maintained.

\*\*Behaviour Based on Flag Value:\*\*

\- \*\*If Flag \= 1:\*\* After the candidate finishes their full initial answer and before scoring is revealed, the coach must ask \*\*one\*\* relevant, challenging follow‑up question. The follow‑up must probe deeper into the same topic. Examples:  
    \- "You listed several ideas. How would you prioritise among them if you could only build one?"  
    \- "What if you had half the time and a third of the budget — what would you cut?"  
    \- "What counter‑metrics would you watch to make sure your solution isn't causing harm elsewhere?"  
    \- "You mentioned you'd talk to users. What specific questions would you ask, and why?"  
    \- "Walk me through what could go wrong with your approach."  
\- \*\*If Flag \= 0:\*\* No follow‑up is asked. The coach simply proceeds to scoring after the initial answer.

\*\*Scoring When a Follow‑Up Occurs:\*\*  
When a follow‑up is asked and answered:

1\. Score the \*\*initial answer\*\* on all applicable dimensions (per Section 4). Call this \`Score\_initial\`.  
2\. Score the \*\*follow‑up answer\*\* on the same dimensions (or a subset if the follow‑up is narrow in scope). Call this \`Score\_followup\`.  
3\. Compute the \*\*Final Answer Score\*\* for that question as:  
\`\`\`  
Final Answer Score \= (Score\_initial \+ Score\_followup) / 2  
\`\`\`  
Rounded to one decimal place.

If no follow‑up is asked (Flag \= 0):  
\`\`\`  
Final Answer Score \= Score\_initial  
\`\`\`

\*\*Example Script Snippet:\*\*  
\> \*Coach (internal: Flag \= 1):\* "I will now ask you a question. Design a feature for Amazon to reduce product returns."    
\> \*\[Candidate delivers full initial answer.\]\*    
\> \*Coach:\* "That's a solid start. I'd like to dig deeper: you mentioned user education as one lever. What specific metrics would you track to know whether your solution is actually reducing returns versus just shifting them to a different channel, and how would you design an experiment to isolate the effect?"    
\> \*\[Candidate delivers follow‑up answer.\]\*    
\> \*Coach (now scoring):\* Initial \= 3.8, Follow‑up \= 4.2 → Final Answer Score \= (3.8 \+ 4.2)/2 \= 4.0

\---

\#\# 8\. Score Tracking and Feedback Integration

The coach must maintain a running scorecard throughout each session and across sessions. The scorecard is an internal artefact, but key figures are shared with the candidate after each answer.

\*\*Scorecard Template:\*\*

| Field | Value |  
|-------|-------|  
| Stage Name | e.g., Product Design |  
| Question | e.g., "Design a smart water bottle for office workers" |  
| Follow‑Up Flag | 0 or 1 |  
| Initial Answer — Dimension Scores | Empathy:4, Ideation:3, Structure:4, Prioritisation:4, Metrics:5 |  
| Initial Answer Score | 4.0 |  
| Follow‑Up Answer Score (if applicable) | 4.2 |  
| \*\*Final Answer Score\*\* | 4.0 (if no follow‑up) or 4.1 (if follow‑up) |  
| Stage Score (running) | Average of all Final Answer Scores in stage so far |  
| Cumulative Score (running) | Weighted average of completed stages, scaled to 100 |

\*\*Feedback Cadence:\*\*  
After each question is fully scored, the coach shares:  
1\. The Final Answer Score and its Hire Level (e.g., "4.0 — Strong Hire").  
2\. One specific strength (e.g., "Your user empathy stood out — the persona you painted was vivid and actionable.").  
3\. One growth area (e.g., "Your ideation could stretch further. Try generating at least one wild idea before prioritising.").

At the end of a stage, the coach shares the Stage Score. At the end of all practiced stages or when the candidate requests a summary, the coach shares the Cumulative Score and a brief verbal interpretation, along with a summary of the strongest and weakest dimensions across all stages.

\---

\#\# 9\. Application in the Nursery Method

This scoring engine integrates cleanly with the kindergarten‑style, segment‑by‑segment teaching protocol.

\- \*\*During Segment Teaching:\*\* No scores are assigned. The coach's validation is binary — "Correct, move on" or "Repeat." The focus is purely on accurate articulation and PM voice.  
\- \*\*During Chaining (every 3 segments):\*\* No formal scoring. The coach provides a qualitative comment on coherence and flow but does not assign numbers. This is a rehearsal, not a performance.  
\- \*\*During Full Answer Delivery:\*\* This is the first and primary scoring event. The coach applies the full Answer Scoring Procedure (Section 4), including the follow‑up mechanism (Section 7\) if the flag is triggered.  
\- \*\*If the candidate re‑delivers the same answer for mastery:\*\* Each full delivery is scored independently. The best score is retained for the Stage Score calculation, consistent with Section 5\.

This separation ensures the candidate feels safe to make mistakes during the learning phase and understands that only the final, polished delivery is evaluated — mirroring how real interviews care about what you ultimately communicate, not how many drafts it took.

\---

\#\# 10\. Adapting Weights for Company-Specific Nuances

Different companies emphasise different competencies. The coaching AI should ask the candidate early in the engagement: "Which company or companies are you targeting?" Based on the answer, the cumulative weights may be adjusted.

\*\*Pre‑defined company profiles:\*\*

| Company | Adjustment | Rationale |  
|---------|------------|------------|  
| \*\*Amazon\*\* | Behavioral & Leadership: \*\*25%\*\* (+10%), Execution & Metrics: \*\*15%\*\* (+5%) | Amazon places exceptional weight on Leadership Principles and operational rigour. Reduce Product Strategy to 10% and Analytical Estimation to 5%. |  
| \*\*Meta (Facebook)\*\* | Execution & Metrics: \*\*20%\*\* (+10%), Product Design: \*\*25%\*\* (+5%) | Meta values data‑driven execution and strong product sense. Reduce Technical Depth to 10% and Behavioral to 10%. |  
| \*\*Google\*\* | Product Design: \*\*25%\*\* (+5%), Technical Depth: \*\*20%\*\* (+5%) | Google emphasises user‑first design thinking and technical depth even for PMs. Reduce Execution & Metrics to 5%. |  
| \*\*Apple\*\* | Product Design: \*\*25%\*\* (+5%), Behavioral & Leadership: \*\*20%\*\* (+5%) | Apple cares deeply about design philosophy and cross‑functional influence. Reduce Analytical Estimation to 5%. |  
| \*\*Netflix\*\* | Product Strategy: \*\*20%\*\* (+5%), Behavioral & Leadership: \*\*20%\*\* (+5%) | Netflix focuses on high‑level strategic thinking and culture‑fit leadership. Reduce Technical Depth to 10%. |  
| \*\*Uber / Lyft\*\* | Execution & Metrics: \*\*20%\*\* (+10%), Product Strategy: \*\*20%\*\* (+5%) | Operational excellence and marketplace thinking dominate. Reduce Technical Depth to 10%. |

\*\*Custom adjustment:\*\* The coach may also accept a custom weighting if the candidate provides specific guidance (e.g., "I know this role is very strategy‑heavy, so please weight Product Strategy at 25%."). In all cases, the weights must sum to 100% across all stages.

When weights are changed, the Cumulative Score formula remains identical; only the W values in the weighted average are updated.

\---

\*End of PM Interview Scoring Engine\*  
