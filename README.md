# Miraya Lead Magnet - Agentic Environment

This project follows a 3-layer architecture for reliable AI-assisted automation.

## Architecture

### Layer 1: Directives (`directives/`)
Standard Operating Procedures (SOPs) written in Markdown. These define:
- Goals and objectives
- Required inputs
- Tools/scripts to use
- Expected outputs
- Edge cases to handle

### Layer 2: Orchestration (AI Agent)
The AI agent reads directives and orchestrates execution by:
- Intelligent routing and decision-making
- Calling execution scripts in the right order
- Handling errors and asking for clarification
- Updating directives with learnings

### Layer 3: Execution (`execution/`)
Deterministic Python scripts that handle:
- API calls
- Data processing
- File operations
- Database interactions

## Directory Structure

```
.
├── directives/          # SOPs and instruction sets
├── execution/           # Python automation scripts
├── .tmp/               # Temporary/intermediate files (auto-generated)
├── .env                # Environment variables and API keys
├── .gitignore          # Git ignore rules
├── GEMINI.md           # Agent instructions
└── README.md           # This file
```

## Getting Started

1. Add your API keys and credentials to `.env`
2. Create directives in `directives/` for your workflows
3. Develop Python scripts in `execution/` for deterministic tasks
4. Let the AI agent orchestrate between directives and execution

## Key Principles

- **Deliverables**: Live in cloud services (Google Sheets, Slides, etc.)
- **Intermediates**: Temporary files in `.tmp/` (can be deleted/regenerated)
- **Self-annealing**: System learns and improves from errors
- **Deterministic execution**: Complex logic in Python, not LLM calls

## Operating Principles

1. **Check for tools first** - Always check `execution/` before creating new scripts
2. **Self-anneal** - Fix errors, update tools, test, update directives
3. **Update directives** - Keep SOPs current with learnings and constraints
