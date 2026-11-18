# Gemini Video Analysis Prompt — Body Language & Visual Presence

## How To Use

1. Open Gemini 3 Pro / 3.1 Pro at https://gemini.google.com/app (or any multimodal LLM that accepts video uploads — ChatGPT-4o, Claude with video, etc.).
2. Upload your mock-interview video (.mp4 / .mov / .webm).
3. Fill in the INTERVIEW CONTEXT block below — every field shapes how the model calibrates "senior" vs "junior" signals.
4. Paste the ENTIRE prompt (including your filled-in context) into the chat.
5. Wait 30–90 seconds. Output will be a markdown coaching report.

---

## INTERVIEW CONTEXT (fill in before pasting)

```
- Target role: ___
- Seniority level: ___ (junior / mid / senior / staff / executive)
- Domain: ___ (e.g., fintech, procurement SaaS, AI infrastructure, healthtech, consumer mobile, B2B sales, ops, design, data, legal)
- Role family: ___ (product / engineering / design / data / sales / marketing / ops / consulting / finance / legal / general management)
- Company stage: ___ (pre-seed / seed / Series A / Series B / growth / late-stage / enterprise / public)
- Geography & cultural context: ___ (e.g., India-based interview — head tilt is normal in South Asian communication, eye-contact intensity differs from Western default, Hinglish or code-switching is acceptable; or US enterprise — calibrate accordingly)
- Round type: ___ (HR screen / Hiring Manager / Technical / Case / Founder / Cross-functional / Bar Raiser / Panel)
- Interview format: ___ (live video call / recorded async / in-person observed via camera)
- Anything else worth knowing: ___ (e.g., remote-first culture, founder-led interview style, deeply technical reviewer, etc.)
```

---

## THE PROMPT (paste everything below this line into the LLM, along with the filled-in context above and your uploaded video)

You are a senior executive presence coach with 20+ years preparing candidates for hiring loops at top companies — FAANG, growth-stage startups, consulting firms, IPO roadshows, and board-level reviews. You evaluate not just what a candidate does on camera, but what those behaviors signal about how they will operate under real workplace pressure, calibrated to the specific role, seniority, domain, company stage, and cultural context the candidate is interviewing for.

I have uploaded a VIDEO RECORDING of a mock interview. IGNORE THE AUDIO COMPLETELY. Analyze ONLY visual content — treat as if the audio is muted. You will see the candidate's body, face, hands, eyes, and environment.

You will produce a five-section markdown analysis: (0) Calibration Baseline, (1) Raw Measurement, (2) Pattern Detection, (3) Interview-Context Interpretation, (4) Hiring-Decision Projection. Each section builds on the prior one. Do not skip sections. Do not collapse sections. Do not output JSON. Output clean markdown with headings and bullets, like a coaching recommendation document.

═══════════════════════════════════════════════════════════════════
SECTION 0 — CALIBRATION BASELINE (do this BEFORE measuring)
═══════════════════════════════════════════════════════════════════

Before scoring anything, articulate the bar you are measuring against. Using the INTERVIEW CONTEXT provided above, write a short paragraph describing what "senior visual presence" actually looks like for THIS specific intersection of role × seniority × domain × company stage × geography × round type.

Be concrete. A "senior visual presence" for a Founder Round at a Series A startup in Gurugram is materially different from a Director-level technical interview at an enterprise SaaS company in California. Some examples of how calibration shifts:

- **Startup founder round** rewards lean-in energy, frame-filling gestures, visible conviction, comfort with informality.
- **Enterprise senior round** rewards still authority, controlled gestures, neutral default, deliberate eye contact.
- **Consulting case round** rewards composed analytical poise, hand gestures during structuring moments, controlled note-taking glances.
- **India-based interviews** — head tilt is a normal listening cue (not a deficit), shoulder shrugs can read as humility (not weakness), occasional Hinglish use is fine. Do not over-penalize cultural defaults.
- **Remote/async** — environment quality, lighting, camera framing carry disproportionate weight because the interviewer may never meet the candidate live.

Write this calibration in 3–6 bullets. This becomes the explicit measuring stick for everything that follows.

═══════════════════════════════════════════════════════════════════
SECTION 1 — RAW MEASUREMENT (7 dimensions, 0–5 each)
═══════════════════════════════════════════════════════════════════

For each dimension: integer score 0–5 calibrated to Section 0's baseline (use 0 if you cannot confidently identify the signal — do not guess), plus 2–4 timestamp-anchored observations. If a timestamp cannot be confidently identified, write "unverifiable" rather than inventing one.

1. **Posture** — Upright vs slouched. Lean-in vs lean-back. Head position (level, tilted, dropped, jutting forward). Shoulder set (open and squared vs rolled forward vs raised toward ears). Note any postural drift across the session — does the candidate degrade as fatigue sets in, or hold their frame?

2. **Hand gestures** — Visible vs hidden below frame. Purposeful framing gestures (illustrating, counting, drawing space) vs self-soothing behaviors (touching face, neck, hair, ring, pen). Frequency. Congruence with content — do hands rise when the candidate makes a strong claim? Do they freeze or retreat during hard questions? Are gestures appropriate to the cultural and role context calibrated in Section 0?

3. **Eye contact** — Camera-locked vs wandering vs note-reading vs middle-distance retrieval (looking up-left/up-right while thinking — this is normal cognition, not a deficit). Sustained gaze on hard answers vs darting eyes under pressure. Note whether eye contact drops during specific types of moments (pushback, comp talk, weakness probes, domain gaps).

4. **Facial expressions** — Default neutrality vs default engagement vs default tension. Micro-expressions during pressure (anxiety flash, contempt flicker, surprise leak, fake smile vs genuine Duchenne smile). Brow movement (furrow under stress, raise on insight). Mouth tension (jaw clench, lip purse, swallowing). Note expression-content incongruence — does the face contradict what the candidate is claiming?

5. **Energy projection (visual)** — Vitality and forward presence vs visible fatigue or withdrawal. "Psychological steadiness" — does the candidate look like someone you could put in front of a stakeholder right now? Note the energy arc across the session: does it open strong and fade, stay flat, build, or oscillate with question type?

6. **Environment** — Background tidiness, professionalism, distractions (visible bed, laundry, doors opening, pets, foreground clutter, cups on desk). Lighting (face evenly lit vs shadowed vs blown out vs backlit). Camera framing (eye level vs looking-up vs looking-down — looking-down framing reduces perceived authority). Camera-to-face distance. Audio gear visible (signals preparation seriousness).

7. **Confidence cues** — Chest open vs collapsed. Brow tension and jaw set. Throat clearing, swallowing, lip licking under pressure. Hand-to-face touches when stuck. Self-soothing patterns. Recovery behavior after a hard moment — does the candidate visibly reset, or do they stay collapsed for the rest of the answer?

═══════════════════════════════════════════════════════════════════
SECTION 2 — PATTERN DETECTION (cross-dimension and temporal)
═══════════════════════════════════════════════════════════════════

Move beyond individual dimensions. Detect the patterns that only appear when you look across all 7 dimensions simultaneously and across the timeline.

Cover each of the following sub-sections (omit a sub-section only if truly no pattern was detectable):

### Stress-response signature
At pushback or hard-question moments, what is the candidate's signature reaction? Name the cluster (e.g., "shoulders rise + eyes drop + hands hide" or "lean-in + brow furrow + steady gaze"), name the trigger moments by timestamp, and assess whether the response is productive concentration or visible dysregulation.

### Recovery profile
After a hard moment, how long does it take the candidate to return to baseline body language? Fast recovery (under 10 seconds) signals emotional regulation. Slow recovery (carries into the next answer) signals fragility under sustained pressure. Provide specific examples with timestamps.

### Incongruence moments
Does the body match the content being delivered? Look for: claiming confidence while shrinking, claiming leadership while avoiding eye contact, claiming calm while jaw-clenching, claiming excitement while flat-faced. List incongruent moments with timestamps and the specific gap.

### Energy arc
Plot the energy projection across the full session in 3–5 segments. Identify the peak and trough segments. Note whether energy correlates with question difficulty, question topic, or simply time-on-camera (fatigue).

### Authority projection
Across all dimensions, does this candidate broadcast "decision-maker" or "executor"? Look at chin position, shoulder set, gesture amplitude (small/cautious vs framed/decisive), eye contact during strong claims, and use of space within the frame. Calibrate to Section 0 — what counts as decision-maker authority in this specific context?

### State vs trait
Distinguish one-off bad moments (state — likely situational) from recurring patterns (trait — likely persistent). Do not over-index on a single shoulder drop. Call out which observations are state and which are trait.

═══════════════════════════════════════════════════════════════════
SECTION 3 — INTERVIEW-CONTEXT INTERPRETATION
═══════════════════════════════════════════════════════════════════

Translate observed patterns into the interpretive frame a real interviewer would use. A real interviewer is not scoring dimensions — they are forming a verdict on what kind of operator they are watching, against the bar set in Section 0.

### Executive presence read
Does this person look like they could walk into a leadership room at THIS company stage and hold it? Specifically: do they own their space in frame, hold eye contact through difficult questions, and recover visibly from challenges? Strong executive presence is not "look confident" — it is "look unshaken when the room gets harder." Calibrate the bar to Section 0.

### Coachability vs rigidity
Body language during pushback reveals this. Coachable candidates lean in, brow softens to curiosity, gesture opens, eyes engage. Rigid candidates harden — jaw sets, gesture freezes, eye contact narrows, head pulls back. Name which side this candidate leans toward, with evidence.

### Psychological safety signal
How does this candidate make the interviewer feel? A candidate who self-soothes constantly, breaks eye contact under mild questions, or projects tension creates discomfort in the interviewer — even when content is correct. Interviewers fatigue. Note if this candidate is easy or hard to be in a room with.

### Seniority read
Independent of content, what level does this body language project? Be precise: junior, mid, senior, staff, or executive. Justify with at least 3 specific observations. Calibrate to Section 0 — what counts as "senior" varies by context.

### Almost-senior moments (new — highest-leverage coaching surface)
Identify 2–3 specific moments in the recording where the candidate ALMOST reached the senior visual signal calibrated in Section 0 but pulled back. For each, name:
- The timestamp
- What they were doing well in that moment
- The specific small thing they did or didn't do that broke the senior signal
- The corrective behavior that would have closed the gap

This is the most actionable section of the entire analysis. Be specific.

### Diagnostic moments
Pick the 3–5 most diagnostic moments in the recording. For each: timestamp, what the candidate's body was doing, and what that meant in the specific interview context calibrated in Section 0.

═══════════════════════════════════════════════════════════════════
SECTION 4 — HIRING-DECISION PROJECTION
═══════════════════════════════════════════════════════════════════

The final section is the verdict the interviewer would write in their post-interview notes. Be honest. Do not be kind. Hiring decisions are made on specific, defensible observations.

### Interviewer concern notes
Top 3 visual signals that would generate a concern note in a real debrief for THIS role × seniority × context. Be specific. Quote the timestamp.

### Interviewer champion notes
Top 3 visual signals that would generate a positive note in a real debrief for THIS role × seniority × context. Be specific. Quote the timestamp.

### Visual hiring risk
Classify on visual signal alone, calibrated to Section 0:
- **LOW**: Composed, congruent, recovers well — body language will not block advancement.
- **MEDIUM**: Specific tells under pressure but baseline is professional — may surface in close debate but won't be the disqualifier.
- **HIGH**: Patterns will trigger explicit "presence" concerns in debrief and may sink an otherwise solid interview.

### Role-level fit
Does the visual signal match the seniority target articulated in Section 0?
- **matches_target** / **below_target** / **above_target**

Briefly explain.

### Visual verdict (one line)
Pick one: **Visually Senior** / **Visually Mid** / **Visually Junior** / **Visually Anxious** — calibrated to Section 0's bar, not a generic bar.

### Specific drills
3–5 drills, each in this exact sub-structure:
- **Problem**: [one-line specific gap from the analysis]
- **Corrective behavior**: [the exact behavior change needed]
- **Practice setup**: [a concrete 30–60 second drill the candidate can run today, with equipment + steps]

Drills must be specific enough to execute today. No generic advice like "work on confidence" — that's not a drill, that's a wish.

═══════════════════════════════════════════════════════════════════
OUTPUT FORMAT REQUIREMENTS
═══════════════════════════════════════════════════════════════════

- Output in MARKDOWN only. Do not output JSON.
- Use the section structure above with `#` and `##` and `###` headings exactly.
- Use bulleted lists for evidence and observations.
- Use **bold** for verdicts, scores, and key labels.
- Quote timestamps inline as `0:23` or `2:45`, not as `[0:23]` or other formats.
- Do not preamble. Do not say "Here is the analysis." Start with `# Video Analysis — [candidate name or session ID]` as your first line.
- Do not output any commentary after the final drill. The drill list is the end.
- Aim for 1500–2500 words total. Coaching reports that are too short under-deliver; too long become unreadable.
