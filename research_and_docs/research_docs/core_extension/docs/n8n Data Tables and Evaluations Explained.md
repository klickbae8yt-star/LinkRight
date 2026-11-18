# **Technical Blueprint: Native Data Tables and Automated Evaluations in n8n**

As enterprise automation scales, managing relational application state and validating non-deterministic model outputs within agentic workflows becomes complex. Traditionally, systems developers relied on external databases or cloud-based spreadsheets, introducing network latency, credential overhead, and API rate limits.1 To solve these structural challenges, n8n introduced Native Data Tables and an Automated Evaluation Framework.2 This technical report analyzes the architecture, operations, and programmatic implementation of these features, focusing on maximizing performance, reliability, and maintainability.

## ---

**Technical Mechanics of Native Data Tables**

Introduced as a built-in database engine, Native Data Tables reside locally within the n8n execution environment.1 This proximity enables sub-millisecond data read and write speeds, removing the overhead of external HTTP calls and third-party authentication protocols.1

### **Architecture, Schemas, and Typing Constraints**

Unlike raw, schema-less JSON payloads that are discarded after execution, Native Data Tables enforce strict, column-level typing across executions.2 This schema enforcement acts as a validation layer, blocking malformed data before it affects downstream nodes. The engine supports four primary data types: string, number, boolean, and date.2 Upon initialization, every table automatically generates and manages three system columns: a unique UUID primary key id, a createdAt timestamp, and an updatedAt timestamp.4

To design highly maintainable workflows, system architects must select the correct storage mechanism. The following comparison outlines the trade-offs between Data Tables, Project Variables, and Ephemeral Item payloads:

| Architectural Attribute | Native Data Tables | Project Variables | Ephemeral Workflow Items |
| :---- | :---- | :---- | :---- |
| **Data Structure** | Highly Structured (Relational Rows/Columns) 5 | Key-Value (Flat Configurations) 5 | Semistructured (Nested JSON Objects) |
| **Persistence Horizon** | Permanent (Until explicitly deleted) 5 | Permanent (Static across designs) 5 | Transient (Duration of single execution) |
| **Write Latency** | Sub-millisecond (Local DB Engine) 1 | Low (Config DB write) 5 | In-Memory (Zero IO overhead) |
| **Access Boundaries** | Project-Scoped (or Personal Space) 5 | Cross-Project Shared Context 5 | Execution thread isolation |
| **Maximum Storage Capacity** | 50MB Instance-wide default limit 5 | Optimized for small configuration strings 5 | Bounded by allocated container RAM |
| **Code Node Interoperability** | Indirect (Requires query node step) 5 | Direct (Using $vars expressions) 5 | Direct (Using item.json references) |

### **Administrative and Transactional Node Operations**

The Data Table integration operates through two primary node resource categories: Table Administration and Row Transactions.6 Table Administration allows workflows to dynamically create, delete, list, and update table schemas during execution.6 Row Transactions provide standard database operations 6:

* **Insert:** Appends new records. If an incoming payload violates schema constraints (e.g., passing text to a number column), the transaction rolls back, throwing a runtime validation error.4  
* **Get:** Queries records with filters, including case-sensitive or case-insensitive matching 2, returning a structured JSON array of matching items.6  
* **Update:** Modifies fields on rows matching defined filtering conditions.2  
* **Upsert:** Evaluates incoming items against unique identifiers (such as an email address or transaction UUID).2 If a match is found, the existing row is updated; otherwise, a new record is appended.2 This reduces branching logic by removing the need for pre-query existence checks.2  
* **If Row Exists & If Row Does Not Exist:** These helper nodes verify record existence without returning column payloads, optimizing memory usage during status checks and duplicate prevention steps.2

Direct access to Data Tables from inside JavaScript Code nodes is not supported.5 To process table data programmatically, a workflow must first use a Data Table Get node to retrieve the rows into the execution context as a JSON array, which the Code node can then reference.5

## ---

**The Architecture of n8n Evaluations**

Unlike traditional software code, which is deterministic, generative AI and Large Language Model (LLM) nodes are non-deterministic.8 These systems cannot be reliably tested using simple unit assertions.8 The n8n Evaluation Framework addresses this behavior by embedding a continuous testing loop directly within the execution engine, similar to a CI/CD pipeline.3

### **Pre-Deployment vs. Post-Deployment Evaluations**

The framework supports two distinct testing phases: pre-deployment visual validation and automated, metric-based regression testing.8

| Evaluation Attribute | Light Evaluation (Pre-deployment) | Metric-Based Evaluation (Post-deployment) |
| :---- | :---- | :---- |
| **Development Phase** | Initial prototyping and prompt engineering 8 | Active staging, CI/CD pipelines, and production 8 |
| **Primary Objective** | Fast visual review of LLM outputs 8 | Quantitative regression and drift detection 8 |
| **Dataset Volume** | Small (typically 5–15 hand-crafted cases) 8 | Large (compiled from production execution logs) 8 |
| **Metric Scoring** | Optional (User reviews outputs manually) 8 | Mandatory (Uses quantitative scoring engines) 8 |
| **Dataset Ground Truth** | Optional expected outputs 8 | Highly structured, verified reference answers 8 |
| **Primary Interface** | Workflow Editor and Canvas execution 8 | Dedicated n8n Evaluations History Tab 3 |

During Light Evaluations, the Evaluation Trigger pulls rows from a test table or Google Sheet and runs them sequentially through the workflow.8 This allows developers to check how modifications to prompts or models affect outputs before deployment.8

Metric-Based Evaluations use quantitative scoring metrics to measure performance at scale 3:

* **Categorization Metric:** Performs an exact string comparison between model predictions and reference values, returning 1 for match and 0 for mismatch.8  
* **String Similarity Metric:** Uses deterministic algorithms (like Levenshtein distance) to calculate edit distance, returning a score from 0.0 to 1.0.3  
* **Correctness & Helpfulness Metrics:** Uses an LLM-as-a-Judge model (such as GPT-4o or Claude 3.5 Sonnet) to evaluate semantic quality on a scale of 1 to 5\.3  
* **Tools Used Metric:** Compares the sequence of tools called by an agent against a reference sequence, producing a score without requiring an LLM judge.3 This requires enabling **Return intermediate steps** in the agent settings.

### **Relational Nodes and Logic Branching**

The Evaluation Framework integrates with core workflow logic through specialized nodes 10:

* **Evaluation Trigger:** Pulls test datasets into the workflow, executing runs sequentially.10  
* **Check If Evaluating:** Splits workflow logic based on the trigger type.10 This allows test data to route to metric calculations while production payloads bypass evaluations and continue to downstream integrations.3  
* **No-Op (No Operation):** Converges parallel execution paths, passing incoming data through without modification.  
* **Set Outputs:** Writes results and model predictions back to designated columns in the reference dataset.10  
* **Set Metrics:** Logs numeric evaluation scores directly to the n8n Evaluations tab to track performance trends over time.10

### **Expressions and Query Engines**

The framework relies on n8n’s expression language and query tools to parse and validate payloads.12 For complex JSON filtering, n8n includes a custom $jmespath() method.13

*Note on Syntax Reversal:* The standard JMESPath library uses search(searchString, object).13 However, n8n’s engine reverses this order to search(object, searchString).13 Expressions must be written on a single line.13

This expression filters an object array to extract only text elements from a specific structure:

JavaScript

{{ $jmespath($json.pageElements, ".shape | \[?text\].text.textElements.textRun.content") }}

## ---

**Best Practices for Using Data Tables Effectively**

When building workflows that handle high-volume data, using Native Data Tables can help reduce latency and processing overhead. However, developers must account for storage limitations and structured iteration patterns.

### **Optimizing High-Volume Throughput and Storage**

Data Tables use an instance-wide storage budget, which defaults to 50MB.5 If this limit is exceeded, write transactions fail, halting active workflows.5 For self-hosted deployments, this can be managed by adjusting the N8N\_DATA\_TABLES\_MAX\_SIZE\_BYTES environment variable.5

To maintain performance and keep storage within limits, developers should use structured pagination and query constraints:

* **Pagination and Batching:** When querying large datasets, use the Limit parameters in the Get operation to fetch records in smaller, manageable pages, rather than retrieving the entire table at once.2  
* **Query Constraints:** Use column-specific filters to narrow down the retrieved records, reducing memory usage during execution.2  
* **Write Latency Profiles:** While Data Tables are highly optimized for smaller batch sizes (under 100 rows), larger bulk writes can show comparable speeds to cloud databases due to internal JSON serialization overhead.4 For heavy writes, split payloads into smaller batches.

### **Managing State in Loops and Parallel Executions**

When loops run in parallel within n8n, they can cause race conditions or state corruption if multiple threads attempt to write to the same global keys.7

* **Pass State Through Items:** Pass state properties directly through individual item objects rather than using static global variables.7 This keeps variables isolated to the active loop execution thread.7  
* **Explicit Convergence:** When using parallel branches, use a **Merge Node** configured to waitForAll.7 This ensures all upstream paths complete before executing subsequent database writes, preventing incomplete data states.7  
* **Nested Loop Isolation:** Do not nest **Loop Over Items** nodes directly on the same canvas, as this can corrupt the execution context.7 Instead, place nested loops inside **Sub-workflows** to run in isolated threads.7  
* **Tracking Loop Execution:** Use n8n's loop context properties to track iteration states without writing custom counter logic:  
  JavaScript  
  {{ $("Loop Over Items").context\["noItemsLeft"\] }}

  This expression returns a boolean indicating whether any items remain in the active loop queue.14

### **Real-World Ingestion and Aggregation Scenario**

This pattern illustrates how to process a nested API response, transform and aggregate the data using core n8n nodes, and upsert the results into a Native Data Table to prevent duplicate entries.

  \+-----------------------+  
  | HTTP Request Node     | (Retrieves nested order data payload)  
  \+-----------+-----------+  
              |  
              v  
  \+-----------+-----------+  
  | Split Out Node        | (Flattens "orders" array into individual items)  
  \+-----------+-----------+  
              |  
              v  
  \+-----------+-----------+  
  | Summarize Node        | (Groups by "category" and calculates sum of "price")  
  \+-----------+-----------+  
              |  
              v  
  \+-----------+-----------+  
  | Data Table Upsert Node| (Deduplicates and updates the "category\_sales" table)  
  \+-----------------------+

#### **Step 1: Ingest Nested API Payload**

An API request retrieves the following nested JSON payload containing order details:

JSON

{  
  "batch\_id": "98765",  
  "orders":  
}

#### **Step 2: Flatten Nested Structures**

A **Split Out Node** is used to extract the nested orders array, turning them into individual workflow items.15 This outputs three separate items:

JSON

#### **Step 3: Group and Aggregate Data**

A **Summarize Node** groups the flattened items by the category field.16 It calculates the sum of the price field and counts the total number of orders.16 This outputs aggregated data items:

JSON

#### **Step 4: Write-Back Transaction**

A **Data Table Node** is configured to Upsert rows into a table named category\_sales.2 It uses category as the match field, ensuring existing entries are updated with current revenues while new categories are appended.2

## ---

**Best Practices for Using Evaluations Properly**

### **Constructing Resilient Expressions**

To prevent workflow failures when handling incomplete payloads, developers should write defensive expressions that provide fallback values:

* **Fallback Strings and Logical OR:** Use the logical OR (||) operator to assign default values for missing or undefined fields.17  
  JavaScript  
  {{ $json.customer\_name || "Guest User" }}

* **Strict Empty Value Checking:** Use the $ifEmpty() helper function to handle null, undefined, empty arrays, or empty strings.18  
  JavaScript  
  {{ $ifEmpty($json.priority\_level, "standard") }}

* **Numeric Boundary Safety:** Ensure safe numeric conversions to prevent database typing mismatches:  
  JavaScript  
  {{ Number($json.lead\_score || 0) }}

* **Ternary Operators for Conditional Logic:**  
  JavaScript  
  {{ $json.score \>= 80? "suitable" : "under\_review" }}

### **Resilient Webhook and Evaluation Trigger Integration**

When a workflow contains both production triggers (like a Webhook) and the Evaluation Trigger, merging these paths is required to ensure data flows through the same downstream nodes.

  \+----------------------+             \+-------------------------+  
  | Webhook Trigger      |             | Evaluation Trigger      |  
  \+----------+-----------+             \+------------+------------+  
             |                                      |  
             |                                      v  
             |                         \+------------+------------+  
             |                         | Edit Fields (Reshape)   | (Re-maps schema)  
             |                         \+------------+------------+  
             |                                      |  
             \+-----------------+--------------------+  
                               |  
                               v  
                     \+---------+---------+  
                     | No-Op Node (Merge)| (Single reference point)  
                     \+---------+---------+  
                               |  
                               v  
                     \+---------+---------+  
                     | Main Workflow     | (Downstream logic)  
                     \+-------------------+

To implement this merge:

1. **Format Alignment:** Execute a test run of the production Webhook trigger, copy its JSON output structure, and extract its keys.  
2. **Evaluation Payload Reshaping:** Connect an **Edit Fields (Set)** node directly after the Evaluation Trigger. Set its formatting mode to JSON and map the trigger’s variables into the production schema structure. Append .toJsonString() to raw string references to ensure structural integrity.  
3. **No-Op Convergence:** Wire both the production trigger and the Edit Fields node into a single **No-Op Node**. Because both paths now output identical schemas to this node, downstream nodes can safely reference the No-Op node’s output.

### **Error Handling Architectures**

When constructing error notifications, developers must account for the structural differences in n8n's Error Trigger output based on where the failure occurs.19

* **Execution-Level Failures:** If a downstream node fails, the Error Trigger receives an execution object containing run context, such as execution.id and execution.error.message.19  
* **Trigger-Level Failures:** If the failure occurs within the main trigger itself (e.g., an invalid credential or webhook connection timeout), the execution is aborted before saving.19 In this scenario, the output lacks the execution object entirely, providing error details in the trigger.error path instead.19

JavaScript

{  
  "trigger": {  
    "error": {  
      "name": "NodeApiError",  
      "message": "Service unavailable",  
      "timestamp": 1740986456812  
    }  
  },  
  "workflow": {  
    "id": "12",  
    "name": "Production Flow"  
  }  
}

To build notification messages that handle both error topologies, write expressions with fallback paths to prevent the notification node itself from failing:

🚨 Workflow Error: {{ $json.workflow.name }}

Failed Node: {{ $json.execution?.lastNodeExecuted |

| $json.trigger?.error?.node?.name |

| "Trigger Level Initialization" }}

Error Detail: {{ $json.execution?.error?.message |

| $json.trigger?.error?.message |

| "Execution engine aborted" }}

ID Reference: {{ $json.execution?.id |

| "Aborted Before Execution Initialization" }}

### **Real-World Webhook Validation and Cleanup Routing Scenario**

This pattern demonstrates how to validate incoming webhook payloads, check for required fields, and dynamically route execution to prevent processing failures.

                            \+--------------------------+  
                            | Webhook Trigger          | (Receives lead payload)  
                            \+------------+-------------+  
                                         |  
                                         v  
                            \+------------+-------------+  
                            | Validation Expression    | (Checks "email" and "phone")  
                            \+------------+-------------+  
                                         |  
                                         v  
                            \+------------+-------------+  
                            | IF Node (Validation Pass)|  
                            \+-----+--------------+-----+  
                                  |              |  
                       Yes (Pass) |              | No (Fail)  
                                  v              v  
                    \+-------------+---+      \+---+---------------------+  
                    | Downstream      |      | Stop and Error Node     | (Throws validation  
                    | CRM Integration |      |                         |  exception)  
                    \+-----------------+      \+------------+------------+  
                                                          |  
                                                          v  
                                             \+------------+------------+  
                                             | Global Error Workflow   | (Sends Slack alert  
                                             |                         |  to team)  
                                             \+-------------------------+

1. **Webhook Payload Ingestion:** A webhook receives incoming lead registration payloads:  
   JSON  
   {  
     "lead\_name": "John Doe",  
     "email": "john@example.com",  
     "phone": ""  
   }

2. **Field Presence Validation:** An **IF Node** evaluates whether required fields are present and populated using fallback-aware expressions:  
   JavaScript  
   {{ $json.email.includes("@") && $json.phone\!== "" }}

3. **Cleanup and Notification Branching:**  
   * **If Validation Passes:** The payload is routed to the downstream CRM Integration nodes.  
   * **If Validation Fails:** The workflow routes to a **Stop and Error Node**, which throws a validation exception.19 This triggers the linked **Error Workflow**, which alerts operations teams via Slack with the execution details and failed keys.19

## ---

**Dynamic Integration of Data Tables and Evaluations**

Using Data Tables alongside the Evaluation Framework allows developers to construct automated feedback loops and regression test suites.

                     \+---------------------------+  
                     |  Production Executions    |  
                     \+-------------+-------------+  
                                   |  
                                   v (Sample & Export)  
                     \+-------------+-------------+  
                     |    Golden Data Table      | (Ground Truth Store)  
                     \+-------------+-------------+  
                                   |  
                     \+-------------+-------------+  
                     |   Evaluation Trigger      | (Reads golden test cases)  
                     \+-------------+-------------+  
                                   |  
                                   v  
                     \+-------------+-------------+  
                     |     Evaluation Node       | (Scores actual vs expected)  
                     \+-------------+-------------+  
                                   |  
                                   v (Write-back loops)  
                     \+-------------+-------------+  
                     |  Evaluation Data Table    | (Appends actual predictions)  
                     \+---------------------------+

### **Automated Ground Truth and Feedback Loops**

To monitor model accuracy in production over time, developers can configure automated evaluation loops:

* **Production Input Sampling:** Extract a representative sample of real inputs and correct outputs from production execution histories, saving them into a "Golden Dataset" in a Native Data Table.3 This ensures test cases reflect actual system usage.3  
* **Automated Regression Runs:** Configure an **Evaluation Trigger** to run this dataset through the workflow, comparing current model outputs against the verified reference answers.3  
* **Performance Recording:** Use the **Evaluation Node**'s Set Outputs operation to write actual predictions back to the table, and the Set Metrics operation to log accuracy metrics directly to the centralized n8n Evaluations history.3 This allows developers to track performance and catch model drift.3

### **Real-World Dual-Table Validation and Split Out Processing Scenario**

This scenario demonstrates how to pull records from a master table, evaluate each record's status, and split them into separate tables for production processing and manual review.

                      \+-----------------------------+  
                      | Master Lead Data Table      | (Contains unverified lead records)  
                      \+--------------+--------------+  
                                     |  
                                     v  
                      \+--------------+--------------+  
                      | Lead Status Evaluation Step | (Evaluates record validity)  
                      \+--------------+--------------+  
                                     |  
                                     v  
                      \+--------------+--------------+  
                      | Switch Node (Status Branch) |  
                      \+------+--------------+-------+  
                             |              |  
               Valid Leads   |              | Invalid Leads  
                             v              v  
               \+-------------+---+      \+---+---------------------+  
               | Production Table|      | Quarantine Data Table   | (Flagged for administrative  
               | (Active Leads)  |      |                         |  review)  
               \+-----------------+      \+-------------------------+

#### **Step 1: Read Incoming Ledgers**

A Data Table node queries the unverified\_leads master table 6, returning a structured JSON list:

JSON

\[  
  { "id": "L201", "email": "alice@company.com", "verified\_opt\_in": true },  
  { "id": "L202", "email": "bob\_at\_domain.com", "verified\_opt\_in": false }  
\]

#### **Step 2: Evaluate Record Validity**

A Code node evaluates each record's status, flagging invalid email formats and unverified opt-ins, appending a validation state key to the JSON array:

JavaScript

return $input.all().map(item \=\> {  
  const emailRegex \= /^\[^\\s@\]+@\[^\\s@\]+\\.\[^\\s@\]+$/;  
  const isValid \= emailRegex.test(item.json.email) && item.json.verified\_opt\_in \=== true;  
  item.json.status \= isValid? "valid" : "invalid";  
  return item;  
});

#### **Step 3: Route and Store Records**

A **Switch Node** reads the calculated status key. It routes valid leads to an Upsert operation in the active\_leads production table 2, and invalid leads to a quarantine\_leads table for administrative review and cleanup.2

## ---

**Common Pitfalls and Mitigation Strategies**

### **Pitfall 1: Shared State Corruption in Parallel Executions**

* **The Problem:** Running loops with parallel branches that read or write to shared static variables, causing data overrides and incomplete executions.7  
* **The Resolution:** Avoid using global variables within loops. Pass all state parameters directly through the items in the loop 7, and use a **Merge Node** set to waitForAll to safely converge parallel execution branches.7

### **Pitfall 2: Direct Code Node Queries**

* **The Problem:** Code Nodes cannot programmatically query or write to Data Tables directly using standard JavaScript methods or environment APIs, leading to runtime failures.5  
* **The Resolution:** Use a **Data Table Node** immediately before the Code Node to query the required rows.6 This passes the records as a standard JSON array input, which can then be processed inside the Code Node using standard JavaScript expressions.

### **Pitfall 3: Inconsistent Metrics and Noise**

* **The Problem:** LLM-based metric scoring can exhibit noise, returning different results across identical evaluation runs.  
* **The Resolution:** Duplicate the input rows in your dataset to run each test case multiple times, averaging the metric outputs to smooth out variance and isolate genuine model degradation.

### **Pitfall 4: Nested Evaluation Constraints**

* **The Problem:** Workflow execution engines only support a single Evaluation Trigger and evaluation setup per workflow, preventing testing of separate steps.  
* **The Resolution:** Place separate functional blocks into isolated **Sub-workflows**, configuring separate evaluations for each sub-workflow independently.

## ---

**Developer Resources and Practical Reference**

* **Official n8n Data Tables Documentation:** Comprehensive resource for schema configurations, sizing variables, and manual data table UI management.5  
* **n8n Evaluations Framework Guide:** Full technical reference on configuring evaluation triggers, metric settings, and test dashboards.10  
* **Google Sheets vs. Native Tables Performance Tests:** Benchmarks outlining write speeds, scaling limits, and latency profiles.1  
* **CV Analysis & Candidate Evaluation Template:** Production-grade template demonstrating how to parse uploaded files, run AI evaluation agents, and log candidate metrics.10  
* **Lead Routing Sentiment Analysis Framework:** Implementation example of combining dynamic sentiment evaluation with lead distribution systems.24  
* **Ticket Classifier Evaluation Template:** Reference architecture showing how to evaluate classification models using exact-match metric scoring.3

## ---

**Executive Summary Checklist**

* \[ \] **Performance Optimization:** Use Native Data Tables instead of external cloud sheets for small-to-medium datasets (under 100 rows) to achieve sub-100ms access latency.1  
* \[ \] **State Management Isolation:** Pass runtime state directly through item data inside loops, and use Merge nodes to safely converge parallel processing branches.7  
* \[ \] **Defensive Expression Design:** Use $ifEmpty() and logical OR operators to assign fallback values, preventing workflow failures from missing fields.17  
* \[ \] **Error Path Resiliency:** Design error workflows that handle structural differences between execution-level and trigger-level error payloads.19  
* \[ \] **Database Typing Mismatches:** Force raw variables to strict database types (Number(), String()) before executing write operations.2  
* \[ \] **Bypass Production Logic:** Use Check If Evaluating nodes to ensure evaluation executions bypass production notifications and downstream APIs.3  
* \[ \] **Storage Budget Protection:** Monitor the 50MB shared storage limit, and schedule cron workflows to archive and purge expired data.5  
* \[ \] **Continuous Accuracy Tracking:** Sample real-world production data periodically to maintain and update golden testing datasets.3

#### **Works cited**

1. The Ultimate Guide to n8n Native Tables: 10x Your Workflow Speed \- Axe Automation, accessed on May 19, 2026, [https://www.axeautomation.co/blog/n8n-native-tables](https://www.axeautomation.co/blog/n8n-native-tables)  
2. n8n DataTables Node Tutorial — Store Data Directly in n8n | by Darrell\_tw\_ \- Medium, accessed on May 19, 2026, [https://darrelltw.medium.com/n8n-datatables-node-tutorial-store-data-directly-in-n8n-ac91bbc42e2c](https://darrelltw.medium.com/n8n-datatables-node-tutorial-store-data-directly-in-n8n-ac91bbc42e2c)  
3. Production AI Playbook: Evaluation and Monitoring \- n8n Blog, accessed on May 19, 2026, [https://blog.n8n.io/production-ai-playbook-evaluation-and-monitoring/](https://blog.n8n.io/production-ai-playbook-evaluation-and-monitoring/)  
4. n8n's NEW Native Data Tables Just Made Building Agents So Much Easier · AI Automation Society \- Skool, accessed on May 19, 2026, [https://www.skool.com/ai-automation-society/new-video-n8ns-new-native-data-tables-just-made-building-agents-so-much-easier](https://www.skool.com/ai-automation-society/new-video-n8ns-new-native-data-tables-just-made-building-agents-so-much-easier)  
5. Data tables \- n8n Docs, accessed on May 19, 2026, [https://docs.n8n.io/data/data-tables/](https://docs.n8n.io/data/data-tables/)  
6. Data table | n8n Docs, accessed on May 19, 2026, [https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.datatable/](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.datatable/)  
7. n8n-support | Skills Marketplace \- LobeHub, accessed on May 19, 2026, [https://lobehub.com/nl/skills/wmiles81-n8n-support](https://lobehub.com/nl/skills/wmiles81-n8n-support)  
8. Evaluations | n8n Docs, accessed on May 19, 2026, [https://docs.n8n.io/advanced-ai/evaluations/overview/](https://docs.n8n.io/advanced-ai/evaluations/overview/)  
9. How to stop your AI agents from hallucinating: A guide to n8n's Eval Node \- LogRocket Blog, accessed on May 19, 2026, [https://blog.logrocket.com/stop-your-ai-agents-from-hallucinating-n8n/](https://blog.logrocket.com/stop-your-ai-agents-from-hallucinating-n8n/)  
10. Evaluation node documentation | n8n Docs, accessed on May 19, 2026, [https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.evaluation/](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.evaluation/)  
11. Evaluate a support ticket classifier with OpenAI GPT-4o-mini and n8n evaluations, accessed on May 19, 2026, [https://n8n.io/workflows/15133-evaluate-a-support-ticket-classifier-with-openai-gpt-4o-mini-and-n8n-evaluations/](https://n8n.io/workflows/15133-evaluate-a-support-ticket-classifier-with-openai-gpt-4o-mini-and-n8n-evaluations/)  
12. n8n Expressions Cheat Sheet: Variables, Functions and Syntax \- Serverman | Tech Reviews | How-To Guides, accessed on May 19, 2026, [https://www.serverman.co.uk/software/n8n/n8n-expressions-cheat-sheet/](https://www.serverman.co.uk/software/n8n/n8n-expressions-cheat-sheet/)  
13. Query JSON with JMESPath | n8n Docs, accessed on May 19, 2026, [https://docs.n8n.io/data/specific-data-types/jmespath/](https://docs.n8n.io/data/specific-data-types/jmespath/)  
14. Loop Over Items (Split in Batches) \- n8n Docs, accessed on May 19, 2026, [https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.splitinbatches/](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.splitinbatches/)  
15. Item Lists integrations | Workflow automation with n8n, accessed on May 19, 2026, [https://n8n.io/integrations/item-lists/](https://n8n.io/integrations/item-lists/)  
16. Summarize \- n8n Docs, accessed on May 19, 2026, [https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.summarize/](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.summarize/)  
17. n8n Expressions Cheat-Sheet | n8n Arena: Creators Leaderboard, accessed on May 19, 2026, [https://n8narena.com/guides/n8n-expression-cheatsheet/](https://n8narena.com/guides/n8n-expression-cheatsheet/)  
18. Expression Reference \- n8n Docs, accessed on May 19, 2026, [https://docs.n8n.io/data/expression-reference/](https://docs.n8n.io/data/expression-reference/)  
19. Error Trigger node documentation \- n8n Docs, accessed on May 19, 2026, [https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.errortrigger/](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.errortrigger/)  
20. Error handling \- n8n Docs, accessed on May 19, 2026, [https://docs.n8n.io/flow-logic/error-handling/](https://docs.n8n.io/flow-logic/error-handling/)  
21. Error handling workflow has executed on its own \- Questions \- n8n Community, accessed on May 19, 2026, [https://community.n8n.io/t/error-handling-workflow-has-executed-on-its-own/83745?tl=pt\_BR](https://community.n8n.io/t/error-handling-workflow-has-executed-on-its-own/83745?tl=pt_BR)  
22. How does Error Objects works? \- Questions \- n8n Community, accessed on May 19, 2026, [https://community.n8n.io/t/how-does-error-objects-works/119070](https://community.n8n.io/t/how-does-error-objects-works/119070)  
23. How to Set Up an Error Workflow in n8n Before Production Fails, accessed on May 19, 2026, [https://community.n8n.io/t/how-to-set-up-an-error-workflow-in-n8n-before-production-fails/293914](https://community.n8n.io/t/how-to-set-up-an-error-workflow-in-n8n-before-production-fails/293914)  
24. Sales lead routing with Gemini Sentiment Analysis & Model Evaluation Framework \- N8N, accessed on May 19, 2026, [https://n8n.io/workflows/11832-sales-lead-routing-with-gemini-sentiment-analysis-and-model-evaluation-framework/](https://n8n.io/workflows/11832-sales-lead-routing-with-gemini-sentiment-analysis-and-model-evaluation-framework/)