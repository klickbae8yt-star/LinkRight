# **n8n Workflow Visual Design & System Organization Strategy**

This guide provides a complete blueprint for standardizing the visual design across your entire n8n pipeline suite and reorganizing your workflows for maximum maintainability, with a detailed breakdown for **MAIN — Amex Candidate Referral Orchestrator**.

## **1\. The Visual Design Standard (Decoded & Standardized)**

To make every workflow instantly readable without inspecting raw JSON, we adopt a strict 3-tier sticky note annotation hierarchy based on n8n's canvas grid and standard sticky colors (n8n-nodes-base.stickyNote).

### **1.1 Color Hierarchy & Standard Roles**

| Color ID | Visual Color | Role | Canvas Position | Mandatory Content & Format |
| :---- | :---- | :---- | :---- | :---- |
| **2** | **Yellow** | **Workflow Overview Panel** | Far Left (X ≈ 300–400, Y ≈ 100\) | • **Title:** \#\# 🧠 \[Workflow Name\] • **How it works:** High-level narrative, key logic, error handling. • **Setup steps:** Numbered checklist, credential names in **bold**, variables/IDs in SCREAMING\_SNAKE\_CASE. |
| **7** | **Grey** | **Logical Stage Containers** | Behind Node Groups | • **Title:** \#\# \[Emoji\] \[Stage Name\] • **Body:** 2–4 sentences describing stage purpose, key node names in backticks, and crucial edge-case behavior (e.g., fallback options, race conditions). |
| **3** | **Red / Pink** | **Credentials & Config Panel** | Far Right (X \> 3000\) | • **Title:** \#\# 🔑 Credentials Required • Bulleted list of all required API keys, database connections, and OAuth credentials. • Warning note regarding secrets and env values. |

### **1.2 Stage Container Sizing & Geometry Mechanics**

When placing grey stage containers (Color 7\) behind node clusters:

1. **Top Padding:** Leave \~110px above the top nodes inside the box to accommodate the heading and narrative text.  
2. **Side/Bottom Padding:** Leave \~80px–100px padding around the remaining edges.  
3. **Grid Alignment:** Round all positions and dimensions (width, height, x, y) to multiples of 4 or 16 for clean snapping on n8n’s canvas.

### **1.3 Emoji Taxonomy for Stage Headers**

Maintain a consistent emoji language across all workflows:

* 🧠 **Overview / Entry Point**  
* 🎯 **Matching, Filtering & Selection**  
* ✍️ **Drafting, Prompting & LLM Generation**  
* 🔁 **Queues, Loops & Reconciliation**  
* 🗄️ **Database Persistence & Ledger Operations**  
* 📄 **Document & CV Ingestion / Parsing**  
* 🗓️ **Cadence & Sequence Logic**  
* ⚖️ **Gates, Rules & Evaluators**  
* 🕸️ **Web Scraping & HTML Parsing**  
* 🔑 **Credentials & Security**  
* ⚠️ **Error Handling & Alerts**

## **2\. Organization Strategy for MAIN — Amex Candidate Referral Orchestrator**

The **Amex Candidate Referral Orchestrator** is the backbone of the referral automation pipeline. It needs to be organized both **architecturally** (decoupling heavy tasks) and **visually** (grouping canvas nodes into clear logical stages).

### **2.1 Architectural Optimization (Decoupling)**

To prevent embedding operations from blocking daily referral execution (especially as candidate pools expand):

* **Decouple Candidate Embeddings:** Remove the inline Embed New Candidates wait-block from MAIN. Schedule SUB — Amex Candidate Embeddings to run independently every 2 hours.  
* **Database Interlocking:** The main orchestrator queries candidate\_embeddings where cv\_extracted: true. This allows candidate ingestion and referral dispatching to run asynchronously without race conditions.

### **2.2 Visual Canvas Blueprint & Stage Breakdown**

For MAIN — Amex Candidate Referral Orchestrator, divide the canvas into 5 primary stage containers (Grey \- Color 7), flanked by the Overview Panel (Yellow \- Color 2\) on the left and Credentials Box (Red \- Color 3\) on the right.

┌────────────────────────┐  ┌───────────────────────┐  ┌───────────────────────┐  
│  OVERVIEW PANEL        │  │ 1\. 🔁 Queue Selection │  │ 2\. 🗓️ Sequence        │ ...  
│  (Color 2 \- Yellow)    │  │ (Color 7 \- Grey)      │  │    & Navii Branch     │  
└────────────────────────┘  └───────────────────────┘  └───────────────────────┘

#### **Stage Breakdown & Visual Layout:**

| Stage Container | Emoji / Title | Included Canvas Nodes | Critical Visual Notes / Explanations |
| :---- | :---- | :---- | :---- |
| **Overview Panel** | 🧠 Amex Candidate Referral Orchestrator | *Placed at \[352, 112\]* | Documents daily run limits, batch size parameters, and execution flow. |
| **Stage 1** | 🔁 Queue Selection & Pre-Check | Mark Processing Errors, Pick Referral Queue, Loop Over Queue | Explains fair-rotation prioritization (never-referred candidates first, then oldest referred timestamp). |
| **Stage 2** | 🗓️ Sequence Position & Navii Routing | Get Referral Count, Compute Slot, IF — Is Slot 7?, Get Navii Job for Slot 7, Merge Navii URL, No Navii Check | Documents the 12-slot message progression and highlights that Slot 7 injects a specialized Navii referral link. |
| **Stage 3** | 🎯 Job Matching & Experience Gate | Match Top Job, Normalize Amex Shortlist, Call Experience Gate (Amex), Map to Job | Documents the 0.50 cosine similarity cutoff and historical exclusion logic. |
| **Stage 4** | ✍️ Message Draft & Output | Build Message Draft, Log & Write Sheet, Wait | **Must highlight:** The Version column in the output sheet carries the complete draft message, and \[PARA\] acts as the multi-line paragraph delimiter for AHK. |
| **Credentials Box** | 🔑 Credentials Required | *Placed far right (\[3328, 992\])* | Lists MongoDB Connection, Local Ollama Instance, and Google Drive Service Account. |

## **3\. Comprehensive Visual Structure Across All Pipelines**

Apply this layout blueprint systematically across all remaining sub-workflows and job sync tools:

### **3.1 Sub-Workflow Annotations Overview**

                                  WORKFLOW SUITE VISUAL MAP  
┌──────────────────────────────────────────────────────────────────────────────────────────┐  
│                                                                                          │  
│  \[ Amex Candidate Pipeline \]                                                             │  
│   ├── MAIN — Amex Candidate Referral Orchestrator ── \[ Overview | Queue | Match | Draft \]│  
│   ├── SUB — Pick Referral Queue ─────────────────── \[ Overview | Fetch | Rank & Limit \]  │  
│   ├── SUB — Candidate to Job Top 5 ──────────────── \[ Overview | Load | Cosine Score \]  │  
│   ├── SUB — Experience Gate ─────────────────────── \[ Overview | Extract | Gate Eval \]  │  
│   ├── SUB — Build Message Draft ─────────────────── \[ Overview | Templates | LLM Draft \] │  
│   └── SUB — Log & Write Referral Sheet ──────────── \[ Overview | Dedup | Sheet Write \]   │  
│                                                                                          │  
│  \[ Job Sync & Embedding Pipelines \]                                                      │  
│   ├── MAIN — Amex Job Sync Orchestrator ─────────── \[ Overview | Fetch | Reconcile \]     │  
│   ├── MAIN — Navii Job Sync Orchestrator ────────── \[ Overview | Scrape | Embed \]        │  
│   └── SUB — Amex Candidate Embeddings ──────────── \[ Overview | Fetch | PDF Embed \]     │  
│                                                                                          │  
└──────────────────────────────────────────────────────────────────────────────────────────┘

#### **Key Documentation Requirements per Sub-Workflow:**

1. **SUB — Experience Gate**  
   * **Stage Focus:** Split into *Candidate Extraction*, *Job Extraction*, and *Eligibility Evaluation*.  
   * **Crucial Annotation:** Explain why evaluation is decomposed into distinct micro-tasks (preventing LLM compound-reasoning hallucinations).  
2. **SUB — Build Message Draft**  
   * **Stage Focus:** Split into *Template Selection*, *LLM Customization*, and *Sanitisation*.  
   * **Crucial Annotation:** Detail the full 12-slot cadence table and explain the \[PARA\] delimiter replacement required for AHK bot CSV parsing.  
3. **SUB — Log & Write Referral Sheet**  
   * **Stage Focus:** Split into *Record Preparation*, *MongoDB Ledger Write*, and *Sheet Export*.  
   * **Crucial Annotation:** Clarify that Version holds raw body copy and document the first\_referred\_at initialization check.  
4. **SUB — Amex Candidate Embeddings**  
   * **Stage Focus:** Split into *Fetch Pending*, *CV Text Extraction*, *Ollama Embedding*, and *Status Update*.  
   * **Crucial Annotation:** Explicitly document the Pending ![][image1] Processed state machine to prevent re-processing loops.

## **4\. Implementation Checklist & Order of Execution**

Execute the visual redesign and workflow restructuring in the following sequence:

1. **Decouple Candidate Embeddings (Architecture):**  
   * Remove Embed New Candidates from MAIN — Amex Candidate Referral Orchestrator.  
   * Create MAIN — Candidate Embedding Scheduler on a 2-hour cron trigger calling SUB — Amex Candidate Embeddings.  
2. **Database Performance Indexing:**  
   * Run the required indexes in MongoDB before expanding candidate volume:  
     db.candidate\_embeddings.createIndex({ cv\_extracted: 1, email\_id: 1 });  
     db.candidate\_embeddings.createIndex({ candidate\_key: 1 }, { unique: true });  
     db.job\_embeddings.createIndex({ status: 1 });

3. **Apply Visual Documentation (Workflow by Workflow):**  
   * Extract target workflow JSON.  
   * Calculate node boundaries (minX, maxX, minY, maxY).  
   * Append standard Yellow, Grey, and Red stickyNote nodes into the JSON structure.  
   * Re-import to n8n canvas and verify padding and visual hierarchy.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABUAAAAYCAYAAAAVibZIAAAAcklEQVR4XmNgGAWjYOCBvLz8XnQxigHQ0H/oYhQDOTk5GyAuQxenGABde05BQcEcXRwOZGVlTcjBQENvAQ3fh24eRQBo4F8gxYguTjYAGvgfXYwiAPT2BBUVFXZ0cYoA0JW/0cUoBkCXGqCLjYJRQEMAAMSsFY9fiDqtAAAAAElFTkSuQmCC>