# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Automated Research Report Generation system using LangGraph workflows to orchestrate AI-powered research through multi-analyst interviews. The system generates comprehensive reports by:
1. Creating specialized analyst personas for different perspectives
2. Conducting parallel interviews with simulated experts
3. Performing web searches to gather evidence
4. Synthesizing findings into structured reports (DOCX/PDF)

**Tech Stack**: LangGraph, LangChain, FastAPI, SQLAlchemy, Tavily (web search), structlog

## Getting Started

### Prerequisites

- Python 3.11 or higher
- pip or uv (faster package installer)
- Git (for version control)

### Step 1: Get API Keys

You need API keys from these providers:

#### Required API Keys:

1. **Tavily API Key** (Web Search - Required)
   - Sign up at: https://tavily.com
   - Get your API key from dashboard
   - Free tier available

2. **At least ONE LLM Provider** (choose one or more):

   **Option A: OpenAI** (Recommended for best quality)
   - Sign up at: https://platform.openai.com
   - Navigate to API Keys section
   - Create new API key
   - Models used: GPT-4o (default in config)

   **Option B: Google Gemini** (Free tier available)
   - Go to: https://aistudio.google.com/app/apikey
   - Create API key
   - Models used: Gemini 2.0 Flash (default in config)

   **Option C: Groq** (Fast and free)
   - Sign up at: https://console.groq.com
   - Get API key from dashboard
   - Models used: Deepseek R1 Distill Llama 70B (default in config)

### Step 2: Create Environment File

Create a `.env` file in the project root directory:

```bash
# Copy the template
cp .env.copy .env

# Or create manually
touch .env
```

Edit the `.env` file and add your API keys:

```bash
# Required - Web Search
TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxxxxxxxxxxxx"

# Choose ONE or ALL (but set LLM_PROVIDER to use one)
OPENAI_API_KEY="sk-proj-xxxxxxxxxxxxxxxxxxxxx"
GOOGLE_API_KEY="AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxx"
GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Set which LLM provider to use (choose one: "openai", "google", or "groq")
LLM_PROVIDER="openai"
```

**Important Notes:**
- Replace the `xxx` placeholders with your actual API keys
- Keep this `.env` file secure and never commit it to git
- The `.env` file is already in `.gitignore` for safety

### Step 3: Configure LLM Settings (Optional)

The `research_and_analyst/config/configuration.yaml` file contains LLM model settings. Default configuration:

```yaml
llm:
  groq:
    provider: "groq"
    model_name: "deepseek-r1-distill-llama-70b"
    temperature: 0
    max_output_tokens: 2048

  google:
    provider: "google"
    model_name: "gemini-2.0-flash"
    temperature: 0
    max_output_tokens: 2048

  openai:
    provider: "openai"
    model_name: "gpt-4o"
    temperature: 0
    max_output_tokens: 2048
```

**You can customize**:
- `model_name`: Change to any model supported by the provider
- `temperature`: 0 (deterministic) to 1 (creative)
- `max_output_tokens`: Maximum response length

### Step 4: Install Dependencies

```bash
# Option 1: Using pip
pip install -r requirements.txt

# Option 2: Using uv (faster)
pip install uv
uv pip install -r requirements.txt
```

This will install:
- LangGraph & LangChain (workflow orchestration)
- FastAPI & Uvicorn (web server)
- SQLAlchemy (database)
- Tavily, OpenAI, Google, Groq clients
- Document generation libraries (python-docx, reportlab)
- And other dependencies

### Step 5: Verify Installation

Test that everything is configured correctly:

```bash
# Test configuration loading
python research_and_analyst/utils/config_loader.py

# Test model loading (will verify API keys)
python research_and_analyst/utils/model_loader.py

# Test basic imports
python -c "from research_and_analyst.api.main import app; print('✅ All imports successful!')"
```

If any errors occur, check:
- Your API keys are correct in `.env`
- The `LLM_PROVIDER` matches one of the providers you have keys for
- All dependencies installed successfully

### Step 6: Run the Application

```bash
# Start the FastAPI server
uvicorn research_and_analyst.api.main:app --reload

# Server will start at: http://localhost:8000
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 7: First Time Usage

1. **Open your browser** and go to http://localhost:8000

2. **Sign Up**:
   - Click "Sign Up" or go to http://localhost:8000/signup
   - Create username and password
   - Account saved in local SQLite database (`users.db`)

3. **Login**:
   - Use your credentials to login
   - You'll be redirected to the dashboard

4. **Generate Your First Report**:
   - Enter a research topic (e.g., "Impact of AI on Healthcare")
   - Click "Generate Report"
   - Wait for analyst personas to be created
   - Provide feedback (optional) or press Continue
   - Wait for parallel interviews and report generation
   - Download DOCX or PDF when complete

### Quick Start Summary

**Minimum Required Setup:**

```bash
# 1. Get API keys (Tavily + one LLM provider)
# 2. Create .env file
cat > .env << 'EOF'
TAVILY_API_KEY="your-tavily-key"
OPENAI_API_KEY="your-openai-key"
LLM_PROVIDER="openai"
EOF

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
uvicorn research_and_analyst.api.main:app --reload

# 5. Open http://localhost:8000 in browser
```

## Development Commands

### Running the Application

```bash
# Start the FastAPI server (development)
uvicorn research_and_analyst.api.main:app --reload

# Run from project root
python -m uvicorn research_and_analyst.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Setup

```bash
# Required environment variables (see .env.copy)
export OPENAI_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
export GROQ_API_KEY="your-key"
export TAVILY_API_KEY="your-key"  # Not in .env.copy but required
export LLM_PROVIDER="openai"  # or "google" or "groq"

# Install dependencies
pip install -r requirements.txt

# Or with uv (faster)
uv pip install -r requirements.txt
```

### Testing and Validation

```bash
# Basic import test (used in Jenkins pipeline)
python3 -c "from research_and_analyst.api.main import app; print('Imports successful')"

# Test configuration loading
python research_and_analyst/utils/config_loader.py

# Test model loading
python research_and_analyst/utils/model_loader.py
```

### Docker Commands

```bash
# Build Docker image
docker build -t research-report-app .

# Run container locally
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
  -e GROQ_API_KEY=$GROQ_API_KEY \
  -e TAVILY_API_KEY=$TAVILY_API_KEY \
  -e LLM_PROVIDER=openai \
  research-report-app

# Build and push to ACR (Azure Container Registry)
./build-and-push-docker-image.sh
```

## Architecture Overview

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          USER INTERACTION LAYER                              │
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                 │
│  │   Browser    │───▶│ Login/Signup │───▶│  Dashboard   │                 │
│  │              │    │   (HTML)     │    │    (HTML)    │                 │
│  └──────────────┘    └──────────────┘    └──────┬───────┘                 │
│                                                   │                          │
│                                                   │ POST /generate_report    │
│                                                   ▼                          │
└───────────────────────────────────────────────────────────────────────────┬─┘
                                                    │                         │
┌───────────────────────────────────────────────────▼─────────────────────┬─┘
│                         FASTAPI WEB APPLICATION                          │
│                                                                           │
│  ┌────────────────┐      ┌──────────────────┐      ┌─────────────────┐ │
│  │  report_routes │─────▶│  report_service  │─────▶│  ReportGenerator│ │
│  │   (API layer)  │      │ (business logic) │      │   Workflow      │ │
│  └────────────────┘      └──────────────────┘      └────────┬────────┘ │
│         │                                                     │          │
│         │ Auth check                                          │          │
│         ▼                                                     │          │
│  ┌────────────────┐                                          │          │
│  │   db_config    │                                          │          │
│  │   (SQLite +    │                                          │          │
│  │   SQLAlchemy)  │                                          │          │
│  └────────────────┘                                          │          │
└───────────────────────────────────────────────────────────────┼──────────┘
                                                                │
┌───────────────────────────────────────────────────────────────▼──────────┐
│                      LANGGRAPH WORKFLOW LAYER                             │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │          REPORT GENERATOR WORKFLOW (Main Orchestrator)           │   │
│  │                                                                   │   │
│  │  START ──▶ create_analyst ──▶ human_feedback ──▶ [FAN-OUT] ──▶  │   │
│  │                                  (INTERRUPT)          │           │   │
│  │                                                       │           │   │
│  │              ┌────────────────────────────────────────┘           │   │
│  │              │                                                    │   │
│  │              ▼                                                    │   │
│  │     ┌────────────────────┐  ┌────────────────────┐              │   │
│  │     │ Interview Workflow │  │ Interview Workflow │ (Parallel)   │   │
│  │     │   (Analyst 1)      │  │   (Analyst 2)      │              │   │
│  │     └─────────┬──────────┘  └─────────┬──────────┘              │   │
│  │               │                        │                         │   │
│  │               └────────────┬───────────┘                         │   │
│  │                            │ [GATHER]                            │   │
│  │                            ▼                                     │   │
│  │              write_report + write_intro + write_conclusion       │   │
│  │                            │                                     │   │
│  │                            ▼                                     │   │
│  │                     finalize_report ──▶ END                      │   │
│  │                                                                   │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                            │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │              INTERVIEW WORKFLOW (Per Analyst)                    │   │
│  │                                                                   │   │
│  │  START ──▶ ask_question ──▶ search_web ──▶ generate_answer ──▶  │   │
│  │                                │                     │            │   │
│  │                                │ (Tavily API)        │            │   │
│  │                                ▼                     ▼            │   │
│  │                         [Web Results]         [Expert Answer]    │   │
│  │                                                      │            │   │
│  │                                                      ▼            │   │
│  │                         save_interview ──▶ write_section ──▶ END │   │
│  │                                                                   │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                            │
└────────────────────────────────────────────┬───────────────────────────────┘
                                             │
┌────────────────────────────────────────────▼───────────────────────────────┐
│                       EXTERNAL SERVICES & STORAGE                          │
│                                                                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐              │
│  │   LLM Provider │  │  Tavily Search │  │  File System   │              │
│  │  (OpenAI/      │  │   (Web API)    │  │  generated_    │              │
│  │   Google/Groq) │  │                │  │   report/      │              │
│  └────────────────┘  └────────────────┘  └────────────────┘              │
│         ▲                     ▲                    ▲                       │
│         │                     │                    │                       │
│  ┌──────┴─────────────────────┴────────────────────┴──────┐              │
│  │            configuration.yaml + Environment Vars        │              │
│  │  (LLM_PROVIDER, API Keys, Model Settings)               │              │
│  └─────────────────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Interview Workflow

```
                    INTERVIEW WORKFLOW
                    ==================
                (Per Analyst - Runs in Parallel)

    START
      │
      ├─────────────────────────────────────────────┐
      │                                              │
      │  InterviewState:                             │
      │  - analyst: Analyst                          │
      │  - messages: List[Message]                   │
      │  - context: List[str]                        │
      │  - interview: str                            │
      │  - sections: List[str]                       │
      │  - max_num_turns: int                        │
      │                                              │
      └──────────────────┬───────────────────────────┘
                         │
                         ▼
           ┌─────────────────────────┐
           │   ask_question()        │  ← Uses ANALYST_ASK_QUESTIONS prompt
           │                         │    (Analyst persona generates question
           │  - Load analyst persona │     for expert to answer)
           │  - Generate question    │
           │  - Return as message    │
           └───────────┬─────────────┘
                       │
                       ▼
           ┌─────────────────────────┐
           │   search_web()          │  ← Uses GENERATE_SEARCH_QUERY prompt
           │                         │    (Convert conversation to search query)
           │  - Extract search query │
           │  - Call Tavily API      │  ──┐
           │  - Format results       │    │ External API Call
           │  - Store in context[]   │  ◀─┘ (Web search results)
           └───────────┬─────────────┘
                       │
                       ▼
           ┌─────────────────────────┐
           │  generate_answer()      │  ← Uses GENERATE_ANSWERS prompt
           │                         │    (Expert persona answers with citations)
           │  - Use search context   │
           │  - Generate expert resp │
           │  - Include citations    │
           │  - Return as message    │
           └───────────┬─────────────┘
                       │
                       ▼
           ┌─────────────────────────┐
           │  save_interview()       │
           │                         │
           │  - Get all messages     │
           │  - Convert to string    │
           │  - Store in interview   │
           └───────────┬─────────────┘
                       │
                       ▼
           ┌─────────────────────────┐
           │   write_section()       │  ← Uses WRITE_SECTION prompt
           │                         │    (Technical writer creates report section)
           │  - Use context & focus  │
           │  - Generate markdown    │
           │  - Include sources      │
           │  - Store in sections[]  │
           └───────────┬─────────────┘
                       │
                       ▼
                      END
                       │
                       └──▶ Returns: {sections: [section_text]}
```

### Detailed Report Generator Workflow

```
                 REPORT GENERATOR WORKFLOW
                 =========================
               (Main Orchestration Workflow)

    START
      │
      ├──────────────────────────────────────────────┐
      │                                               │
      │  ResearchGraphState:                          │
      │  - topic: str                                 │
      │  - max_analysts: int                          │
      │  - human_analyst_feedback: str                │
      │  - analysts: List[Analyst]                    │
      │  - sections: List[str] (accumulator)          │
      │  - introduction: str                          │
      │  - content: str                               │
      │  - conclusion: str                            │
      │  - final_report: str                          │
      │                                               │
      └────────────────┬──────────────────────────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │  create_analyst()       │  ← Uses CREATE_ANALYSTS_PROMPT
         │                         │    (Generate N analyst personas)
         │  - Analyze topic        │
         │  - Consider feedback    │
         │  - Generate personas    │  ──┐
         │  - Return analysts[]    │    │ LLM Call with structured output
         └────────────┬────────────┘  ◀─┘ (Returns: Perspectives with analysts)
                      │
                      ▼
         ┌─────────────────────────┐
         │  human_feedback()       │  ⚠️  INTERRUPT NODE
         │                         │     (Workflow pauses here)
         │  - Pause execution      │
         │  - Wait for user input  │  ◀── User provides feedback via
         │  - Resume on update     │      graph.update_state()
         └────────────┬────────────┘
                      │
                      ▼
         ┌─────────────────────────┐
         │  Conditional Edge:      │
         │  initiate_all_interviews│
         │                         │
         │  Fan-out to N analysts  │
         │  using Send() API       │
         └────────────┬────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
   ┌────────┐   ┌────────┐   ┌────────┐
   │Interview│   │Interview│   │Interview│  (Run in parallel)
   │Workflow │   │Workflow │   │Workflow │
   │Analyst 1│   │Analyst 2│   │Analyst 3│
   └────┬────┘   └────┬────┘   └────┬────┘
        │             │             │
        │  Returns sections via operator.add accumulator
        │             │             │
        └─────────────┼─────────────┘
                      │
              sections[] accumulated
                      │
        ┌─────────────┴─────────────┐
        │             │             │
        ▼             ▼             ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │  write_  │  │  write_  │  │  write_  │  (Run in parallel)
   │  report()│  │  intro() │  │  concl() │
   └─────┬────┘  └─────┬────┘  └─────┬────┘
         │             │             │
         │             │             │
         └─────────────┼─────────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │  finalize_report()      │
         │                         │
         │  - Combine intro +      │
         │    content + conclusion │
         │  - Add sources section  │
         │  - Return final_report  │
         └────────────┬────────────┘
                      │
                      ▼
                     END
                      │
                      └──▶ Save as DOCX/PDF via report_service
```

### Component Interaction Map

```
┌─────────────────────────────────────────────────────────────────────┐
│                      CONFIGURATION LAYER                             │
│                                                                      │
│  .env file                 configuration.yaml                       │
│  ┌──────────────┐          ┌────────────────────┐                  │
│  │ API Keys:    │          │ llm:                │                  │
│  │ - OPENAI     │          │   openai: {...}     │                  │
│  │ - GOOGLE     │          │   google: {...}     │                  │
│  │ - GROQ       │          │   groq: {...}       │                  │
│  │ - TAVILY     │          │ embedding_model:    │                  │
│  │              │          │   provider: google  │                  │
│  │ LLM_PROVIDER │          │   model_name: ...   │                  │
│  └──────┬───────┘          └──────────┬──────────┘                  │
│         │                             │                              │
│         └──────────────┬──────────────┘                              │
│                        │                                             │
└────────────────────────┼─────────────────────────────────────────────┘
                         │
                         ▼
           ┌─────────────────────────┐
           │  config_loader.py       │
           │  + model_loader.py      │
           │                         │
           │  ApiKeyManager          │
           │  ModelLoader            │
           └────────────┬────────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
    ┌────────┐    ┌────────┐    ┌────────┐
    │OpenAI  │    │Google  │    │ Groq   │
    │ChatGPT │    │Gemini  │    │Deepseek│
    └────────┘    └────────┘    └────────┘
         │              │              │
         └──────────────┴──────────────┘
                        │
                   Selected by
                   LLM_PROVIDER
                        │
┌───────────────────────▼─────────────────────────────────────────────┐
│                     WORKFLOW EXECUTION                               │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  AutonomousReportGenerator (report_generator_workflow.py)  │    │
│  │                                                             │    │
│  │  - build_graph()                                            │    │
│  │  - create_analyst()   ───────────────┐                      │    │
│  │  - write_report()                     │                     │    │
│  │  - write_introduction()               │                     │    │
│  │  - write_conclusion()                 │                     │    │
│  │  - finalize_report()                  │                     │    │
│  │  - save_report()                      │                     │    │
│  └───────────┬────────────────────────────┴──────────────────┘    │
│              │ Uses ▼                                              │
│  ┌───────────▼────────────────────────────────────────────────┐   │
│  │  InterviewGraphBuilder (interview_workflow.py)             │   │
│  │                                                             │   │
│  │  - build()                                                  │   │
│  │  - _generate_question()  ◀────┐                            │   │
│  │  - _search_web()               │                            │   │
│  │  - _generate_answer()          │                            │   │
│  │  - _save_interview()           │ Uses                       │   │
│  │  - _write_section()            │                            │   │
│  └────────────────────────────────┴─────────────────────────────┘   │
│                                   │                                 │
│                                   ▼                                 │
│              ┌─────────────────────────────────────┐               │
│              │  prompt_lib/prompt_locator.py       │               │
│              │                                      │               │
│              │  - CREATE_ANALYSTS_PROMPT            │               │
│              │  - ANALYST_ASK_QUESTIONS             │               │
│              │  - GENERATE_SEARCH_QUERY             │               │
│              │  - GENERATE_ANSWERS                  │               │
│              │  - WRITE_SECTION                     │               │
│              │  - REPORT_WRITER_INSTRUCTIONS        │               │
│              │  - INTRO_CONCLUSION_INSTRUCTIONS     │               │
│              │                                      │               │
│              │  (All Jinja2 templates)              │               │
│              └──────────────────────────────────────┘               │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                        DATA MODELS                                    │
│                                                                       │
│  schemas/models.py:                                                   │
│                                                                       │
│  Analyst (BaseModel)                 Section (BaseModel)              │
│  ├─ affiliation: str                 ├─ title: str                   │
│  ├─ name: str                        └─ content: str                 │
│  ├─ role: str                                                         │
│  ├─ description: str                 SearchQuery (BaseModel)          │
│  └─ persona: str (property)          └─ search_query: str             │
│                                                                       │
│  InterviewState (MessagesState)      ResearchGraphState (TypedDict)  │
│  ├─ max_num_turns: int               ├─ topic: str                   │
│  ├─ context: List[str] (add)         ├─ max_analysts: int            │
│  ├─ analyst: Analyst                 ├─ human_analyst_feedback: str  │
│  ├─ interview: str                   ├─ analysts: List[Analyst]      │
│  └─ sections: List[str]              ├─ sections: List[str] (add)    │
│                                      ├─ introduction: str             │
│                                      ├─ content: str                  │
│                                      ├─ conclusion: str               │
│                                      └─ final_report: str             │
└──────────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
USER INPUT                  WORKFLOW                    EXTERNAL APIS           OUTPUT
──────────                  ────────                    ─────────────           ──────

"Impact of                   ┌─────────┐
LLMs on Jobs"  ────────────▶ │ CREATE  │
+ max_analysts=3             │ ANALYST │ ──────────────▶ LLM ────┐
                             └─────────┘                          │
                                  │                               │
                                  │                               │
                                  ▼                               ▼
User Feedback              ┌──────────────┐           [3 Analyst Personas]
"Focus on       ─────────▶ │ HUMAN        │            - Tech Industry Expert
education"                 │ FEEDBACK     │            - Education Researcher
                           │ (interrupt)  │            - Labor Economist
                           └──────────────┘
                                  │
                                  │
                  ┌───────────────┼───────────────┐
                  │               │               │
                  ▼               ▼               ▼
           ┌────────────┐  ┌────────────┐  ┌────────────┐
           │ INTERVIEW  │  │ INTERVIEW  │  │ INTERVIEW  │
           │ Analyst 1  │  │ Analyst 2  │  │ Analyst 3  │
           └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
                 │               │               │
                 │               │               │
      ┌──────────▼───────────────▼───────────────▼──────────┐
      │                                                       │
      │  Each Interview:                                     │
      │                                                       │
      │  Q: "Tell me about..." ──────────────▶ LLM          │
      │         │                                             │
      │         ▼                                             │
      │  Search Query ────────────────────▶ Tavily API ────┐ │
      │         │                                           │ │
      │         ▼                                           │ │
      │  Web Results ◀────────────────────────────────────┘ │
      │         │                                             │
      │         ▼                                             │
      │  Expert Answer ──────────────────▶ LLM              │
      │   (with citations)                                   │
      │         │                                             │
      │         ▼                                             │
      │  [Section Text]                                      │
      │                                                       │
      └───────────────────────────────────────────────────────┘
                 │               │               │
                 └───────────────┼───────────────┘
                                 │
                   [Sections Accumulated]
                                 │
                 ┌───────────────┴───────────────┐
                 │                               │
                 ▼                               ▼
          ┌────────────┐                  ┌────────────┐
          │ WRITE      │────▶ LLM         │ WRITE      │────▶ LLM
          │ INTRO +    │                  │ REPORT +   │
          │ CONCLUSION │                  │ (main)     │
          └─────┬──────┘                  └─────┬──────┘
                │                               │
                └───────────────┬───────────────┘
                                │
                                ▼
                        ┌───────────────┐
                        │ FINALIZE      │
                        │ REPORT        │
                        │               │
                        │ - Combine all │
                        │ - Format      │
                        │ - Add sources │
                        └───────┬───────┘
                                │
                ┌───────────────┴───────────────┐
                │                               │
                ▼                               ▼
         ┌────────────┐                  ┌────────────┐
         │ Save as    │                  │ Save as    │
         │ DOCX       │                  │ PDF        │
         └─────┬──────┘                  └─────┬──────┘
               │                               │
               └───────────────┬───────────────┘
                               │
                               ▼
                    generated_report/
                    Topic_20240115_143022/
                    ├── Topic_20240115_143022.docx
                    └── Topic_20240115_143022.pdf
                               │
                               │
                               ▼
                    [User Downloads via Web UI]
```

### Core Workflow System (LangGraph-based)

The application uses two interconnected LangGraph workflows:

**1. Interview Workflow** ([interview_workflow.py](research_and_analyst/workflows/interview_workflow.py))
- Single analyst conducts interview with simulated expert
- Steps: generate_question → search_web → generate_answer → save_interview → write_section
- Uses Tavily for web search to ground responses in current information
- Each interview produces one report section

**2. Report Generator Workflow** ([report_generator_workflow.py](research_and_analyst/workflows/report_generator_workflow.py))
- Orchestrates multiple parallel interviews using different analyst personas
- Steps: create_analyst → human_feedback (interrupt) → conduct_interviews (parallel) → write_report/intro/conclusion → finalize_report
- Uses LangGraph's `Send` API to fan out interviews to multiple analysts
- Compiles all sections into cohesive final report

**Key Workflow Features**:
- **Checkpointing**: Both workflows use `MemorySaver` for state persistence
- **Human-in-the-loop**: Report generation pauses at `human_feedback` node for analyst review
- **Parallel Execution**: Multiple analyst interviews run concurrently using `Send` conditional edges
- **State Management**: Thread-based state tracking with configurable thread IDs

### Project Structure

```
research_and_analyst/
├── api/                      # FastAPI web application
│   ├── main.py              # App entry point, CORS, health check
│   ├── routes/              # Endpoints: auth, report generation
│   ├── services/            # Business logic layer
│   └── templates/           # Jinja2 HTML templates (login, dashboard, progress)
├── workflows/               # LangGraph workflow definitions
│   ├── interview_workflow.py        # Single analyst interview graph
│   └── report_generator_workflow.py # Multi-analyst orchestration graph
├── schemas/                 # Pydantic models for state and data
│   └── models.py           # Analyst, Section, InterviewState, ResearchGraphState
├── prompt_lib/             # Jinja2 prompt templates
│   └── prompt_locator.py   # All system prompts (analyst, expert, writer roles)
├── utils/                  # Configuration and model management
│   ├── config_loader.py    # YAML config loading with environment fallback
│   └── model_loader.py     # LLM instantiation (OpenAI, Google, Groq)
├── database/               # SQLAlchemy models
│   └── db_config.py        # User model, SQLite connection, bcrypt auth
├── logger/                 # Structured logging
│   └── custom_logger.py    # structlog configuration
├── exception/              # Custom exception handling
│   └── custom_exception.py # ResearchAnalystException wrapper
└── config/                 # Configuration files
    └── configuration.yaml  # LLM models, embeddings, retriever settings
```

### Configuration System

The system uses a layered configuration approach:

**1. YAML Configuration** ([configuration.yaml](research_and_analyst/config/configuration.yaml))
- Defines LLM models per provider (OpenAI, Google, Groq)
- Model parameters: temperature, max_output_tokens
- Embedding model configuration
- Loaded via `config_loader.py` with priority: explicit path → CONFIG_PATH env var → default location

**2. Environment Variables**
- API keys (OPENAI_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY, TAVILY_API_KEY)
- LLM_PROVIDER: selects which LLM config to use from YAML ("openai", "google", or "groq")
- CONFIG_PATH: override default config location

**3. Model Loading** ([model_loader.py](research_and_analyst/utils/model_loader.py))
- `ModelLoader.load_llm()`: Instantiates LLM based on LLM_PROVIDER env var
- `ModelLoader.load_embeddings()`: Loads Google embedding model
- Includes asyncio event loop setup for gRPC-based embedding API
- All API keys loaded via `ApiKeyManager` with validation logging

### Prompt Engineering System

All prompts are Jinja2 templates in [prompt_locator.py](research_and_analyst/prompt_lib/prompt_locator.py):

- `CREATE_ANALYSTS_PROMPT`: Generates analyst personas based on topic and feedback
- `ANALYST_ASK_QUESTIONS`: Analyst role prompt for conducting interviews
- `GENERATE_SEARCH_QUERY`: Converts conversation to search query
- `GENERATE_ANSWERS`: Expert role prompt with context grounding
- `WRITE_SECTION`: Technical writer prompt for section generation
- `REPORT_WRITER_INSTRUCTIONS`: Consolidates sections into main report
- `INTRO_CONCLUSION_INSTRUCTIONS`: Generates intro/conclusion from sections

**Prompt Template Features**:
- Graceful handling of missing variables with `{% if var %}` conditionals
- Default values using `{{ var | default('fallback') }}` syntax
- Consistent persona-based role instructions
- Source citation requirements embedded in prompts

### State Management

The system uses TypedDict-based state classes defined in [models.py](research_and_analyst/schemas/models.py):

**InterviewState** (MessagesState):
- Inherits from LangGraph's MessagesState for message history
- Fields: analyst, context (accumulated with `operator.add`), interview transcript, sections, max_num_turns

**ResearchGraphState** (TypedDict):
- Tracks overall report generation state
- Fields: topic, analysts list, sections (accumulated), introduction, content, conclusion, final_report
- Sections accumulate from parallel interviews using `Annotated[list, operator.add]`

**Thread-based State Persistence**:
- Thread IDs stored in web service for multi-request workflows
- State retrieval: `graph.get_state({"configurable": {"thread_id": "..."}})`
- State updates: `graph.update_state(thread, updates, as_node="node_name")`

### Web API Architecture

**Authentication**:
- Simple session-based auth with in-memory `SESSIONS` dict
- SQLAlchemy User model with bcrypt password hashing
- SQLite database ([db_config.py](research_and_analyst/database/db_config.py))

**Report Generation Flow**:
1. `/generate_report` (POST): Starts workflow, returns thread_id
2. Workflow pauses at `human_feedback` interrupt
3. `/submit_feedback` (POST): Resumes workflow with feedback
4. Polling for completion via `report_service.get_report_status(thread_id)`
5. `/download/{file_name}`: Serves generated DOCX/PDF

**Report Storage**:
- Reports saved to `generated_report/{topic}_{timestamp}/` subfolder
- Each report gets both DOCX and PDF formats
- Markdown formatting preserved in DOCX via heading detection

## Important Patterns

### Adding New LLM Providers

To add a new LLM provider:

1. Add provider config to [configuration.yaml](research_and_analyst/config/configuration.yaml):
```yaml
llm:
  new_provider:
    provider: "new_provider"
    model_name: "model-name"
    temperature: 0
    max_output_tokens: 2048
```

2. Update [model_loader.py](research_and_analyst/utils/model_loader.py):
```python
elif provider == "new_provider":
    llm = NewProviderChat(
        model=model_name,
        api_key=self.api_key_mgr.get("NEW_PROVIDER_API_KEY"),
        temperature=temperature,
    )
```

3. Add API key to environment: `export NEW_PROVIDER_API_KEY="key"`

### Modifying Workflow Steps

To add or modify workflow nodes:

1. **Interview Workflow**: Add node method to `InterviewGraphBuilder` class
2. **Report Workflow**: Add node method to `AutonomousReportGenerator` class
3. Register node in `build()` method: `builder.add_node("node_name", self._method)`
4. Connect with edges: `builder.add_edge("previous_node", "new_node")`
5. For conditional routing, use `add_conditional_edges()` with routing function

### Customizing Prompts

All prompts are in [prompt_locator.py](research_and_analyst/prompt_lib/prompt_locator.py). To modify:

1. Edit Jinja2 template string
2. Add new variables using `{{ variable_name }}` syntax
3. Use conditionals for optional content: `{% if variable %}...{% endif %}`
4. Pass variables when rendering: `prompt.render(variable_name=value)`

### Logging and Debugging

The system uses structured logging via structlog:

- Global logger: `from research_and_analyst.logger import GLOBAL_LOGGER`
- Contextual binding: `logger = GLOBAL_LOGGER.bind(module="ModuleName")`
- Structured fields: `logger.info("message", field1=value1, field2=value2)`
- Exception logging: `logger.error("message", error=str(e))`

### Error Handling

All errors wrapped in `ResearchAnalystException`:

```python
try:
    # operation
except Exception as e:
    logger.error("Operation failed", error=str(e))
    raise ResearchAnalystException("User-friendly message", e)
```

## Deployment

### Azure Container Apps (via Jenkins)

The [Jenkinsfile](Jenkinsfile) automates deployment:

1. Builds and tests Python environment
2. Verifies Docker image exists in ACR (doesn't build - use `build-and-push-docker-image.sh` first)
3. Deploys to Azure Container Apps with secrets management
4. Health check verification via `/health` endpoint

**Manual Deployment Steps**:

```bash
# 1. Build and push Docker image to ACR
./build-and-push-docker-image.sh

# 2. Setup Azure infrastructure (first time only)
./setup-app-infrastructure.sh

# 3. Deploy via Jenkins or manual script
./azure-deploy-jenkins.sh
```

### Environment Variables in Production

Required secrets configured via Azure Container Apps:
- OPENAI_API_KEY, GOOGLE_API_KEY, GROQ_API_KEY, TAVILY_API_KEY
- LLM_PROVIDER (determines which LLM config to use)

Secrets linked as secretrefs in container environment.

## Known Issues and Considerations

1. **Tavily API Key**: Required but not documented in `.env.copy` - add to your environment
2. **Hardcoded API Key**: [report_generator_workflow.py:47](research_and_analyst/workflows/report_generator_workflow.py#L47) contains hardcoded Tavily key - should use environment variable
3. **Session Storage**: In-memory `SESSIONS` dict will lose auth state on restart - consider persistent session storage
4. **SQLite Database**: `users.db` created at project root - not suitable for multi-replica deployments
5. **Thread State**: MemorySaver checkpointer stores state in memory - lost on container restart
6. **File Storage**: Generated reports stored on local filesystem - not shared across replicas

## Testing the System

**Standalone Workflow Test** ([report_generator_workflow.py](research_and_analyst/workflows/report_generator_workflow.py)):

```bash
# Set environment variables
export LLM_PROVIDER="openai"
export OPENAI_API_KEY="your-key"
export TAVILY_API_KEY="your-key"

# Run standalone test (at bottom of file)
python research_and_analyst/workflows/report_generator_workflow.py
```

This will:
1. Create analysts for topic "Impact of LLMs over the Future of Jobs?"
2. Pause for human feedback (press Enter to continue or provide feedback)
3. Conduct interviews in parallel
4. Generate final report in DOCX and PDF formats
5. Save to `generated_report/` directory

**Web API Test**:

```bash
# Start server
uvicorn research_and_analyst.api.main:app --reload

# Access at http://localhost:8000
# 1. Sign up for account
# 2. Login
# 3. Submit research topic
# 4. Provide feedback when prompted
# 5. Download generated reports
```
