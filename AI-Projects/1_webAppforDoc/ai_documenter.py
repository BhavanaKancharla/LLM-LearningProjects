"""
AI-Powered Documentation Generator.
Uses AI models to analyze source code and generate rich documentation explaining:
how the code works, logic flow, architecture, data flow, and design decisions —
even without comments in the source.

Supported providers:
- Google Gemini (FREE - 15 req/min, 1M tokens/day)
- Ollama (FREE - runs locally, no API key needed)
- OpenAI (paid)
- Anthropic (paid)
"""

import os
import json
from datetime import datetime

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import requests as http_requests
    HAS_REQUESTS = True
except ImportError:
    try:
        from urllib.request import urlopen, Request
        from urllib.error import HTTPError, URLError
        HAS_REQUESTS = False
    except ImportError:
        HAS_REQUESTS = False


# ============================================================
# CONFIGURATION
# ============================================================

# Supported AI providers
PROVIDERS = {
    "gemini": {
        "name": "Google Gemini (FREE)",
        "env_key": "GEMINI_API_KEY",
        "default_model": "gemini-2.5-flash",
    },
    "ollama": {
        "name": "Ollama (FREE - Local)",
        "env_key": "",
        "default_model": "llama3",
    },
    "openai": {
        "name": "OpenAI (GPT-4o)",
        "env_key": "OPENAI_API_KEY",
        "default_model": "gpt-4o",
    },
    "anthropic": {
        "name": "Anthropic (Claude)",
        "env_key": "ANTHROPIC_API_KEY",
        "default_model": "claude-sonnet-4-20250514",
    },
}


def get_available_providers():
    """Return list of providers that have API keys configured or are available."""
    available = []
    # Gemini — free, just needs an API key from Google AI Studio
    if os.environ.get("GEMINI_API_KEY"):
        available.append("gemini")
    # Ollama — always available if running locally (no key needed)
    available.append("ollama")
    if HAS_OPENAI and os.environ.get("OPENAI_API_KEY"):
        available.append("openai")
    if HAS_ANTHROPIC and os.environ.get("ANTHROPIC_API_KEY"):
        available.append("anthropic")
    return available


# ============================================================
# SOURCE FILE COLLECTION
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs",
    ".yaml", ".yml", ".json", ".sql",
}

EXCLUDE_DIRS = {
    "node_modules", "venv", ".venv", "__pycache__", ".git",
    "dist", "build", ".next", "coverage", "site", "env",
    ".tox", "egg-info", ".pytest_cache", ".nyc_output",
}


def collect_source_files(project_path, exclude_dirs=None):
    """
    Collect source files from a project directory.
    Returns dict of {relative_path: file_content}.
    """
    if exclude_dirs is None:
        exclude_dirs = EXCLUDE_DIRS

    files = {}
    project_path = os.path.abspath(project_path)

    for root, dirs, filenames in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]

        for fname in sorted(filenames):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in SUPPORTED_EXTENSIONS and fname not in ("Dockerfile", "Makefile"):
                continue

            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, project_path)

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                # Skip minified files
                if len(content) > 1000 and content.count("\n") < len(content) / 500:
                    continue
                # Skip very large files (>50KB) — summarize these separately
                if len(content) > 50000:
                    content = content[:50000] + "\n\n# ... [FILE TRUNCATED - too large] ..."
                files[rel_path] = content
            except (IOError, OSError):
                continue

    return files


# ============================================================
# AI DOCUMENTATION GENERATION
# ============================================================

SYSTEM_PROMPT = """You are a technical documentation writer. Analyze source code and produce COMPLETE documentation.

## For BACKEND projects, document in this order:

### 1. Project Setup
- How to install dependencies and start the server
- Environment variables needed
- Configuration files

### 2. Folder Structure
- Explain what each folder contains and its purpose
- e.g., routes/ = API endpoints, services/ = business logic, etc.

### 3. Routes (API Endpoints)
For EVERY route file, document EACH endpoint:
#### `METHOD` `/path`
- **Purpose:** What this endpoint does
- **Request Body:** JSON fields expected (with types)
- **Response:** JSON structure returned
- **Logic Flow:** Step-by-step what happens (2-4 steps)
- **Authentication:** Whether JWT/auth is required
- **Errors:** Error codes and messages

### 4. Services
For each service file:
- **What it does:** Purpose of this service
- **Functions:** Each function with what it does
- **Connects to:** What external systems it talks to (DB, Java service, Argo, etc.)

### 5. Database
- What database is used
- How connections are managed
- Tables/queries referenced in the code

---

## For FRONTEND projects, document in this order:

### 1. Project Setup
- How to install and run the app
- Environment configuration

### 2. Application Modules
List each module/page and what it does

### 3. For EACH Module/Page:
#### [Module Name]
- **What it is:** Description
- **Features in this module:**
  - Feature 1: what it does, how it works
  - Feature 2: what it does, how it works
- **Flow:** Step-by-step user flow from start to finish
- **Components used:** Key UI components in this module
- **API calls:** What backend endpoints this module calls

### 4. Shared Components
- Reusable components and what they do

### 5. State Management
- What data is stored globally
- How data flows between modules

---

## RULES:
- Document EVERY file, not just a few
- Be SPECIFIC — use actual names from the code
- Do NOT say "I will analyze" — just write the docs directly
- Do NOT skip files or endpoints
- Explain the FLOW step by step for each feature"""


def generate_ai_documentation(
    project_path,
    project_name=None,
    provider="openai",
    model=None,
    api_key=None,
    focus_areas=None,
    exclude_dirs=None,
):
    """
    Main entry point: scan a project and use AI to generate rich documentation.

    Args:
        project_path: Path to the project directory
        project_name: Display name for the project (defaults to folder name)
        provider: AI provider to use ('openai', 'anthropic', 'gemini', 'ollama')
        model: Model name override
        api_key: API key override (defaults to environment variable)
        focus_areas: List of areas to focus on (e.g., ['flow', 'architecture', 'api'])
        exclude_dirs: Directories to exclude from scanning

    Returns:
        Markdown string with AI-generated documentation
    """
    if not project_name:
        project_name = os.path.basename(os.path.abspath(project_path))

    # Collect source files
    files = collect_source_files(project_path, exclude_dirs)
    if not files:
        return f"# {project_name}\n\nNo source files found at: `{project_path}`\n"

    # For local models (Ollama) with limited context, process in batches
    if provider == "ollama":
        response = _generate_batched_documentation(project_name, files, provider, model, api_key, focus_areas)
    else:
        # For cloud models with large context, send everything at once
        user_prompt = _build_analysis_prompt(project_name, files, focus_areas)
        try:
            if provider == "gemini":
                response = _call_gemini(user_prompt, model, api_key)
            elif provider == "openai":
                response = _call_openai(user_prompt, model, api_key)
            elif provider == "anthropic":
                response = _call_anthropic(user_prompt, model, api_key)
            else:
                return f"# {project_name}\n\nUnsupported AI provider: `{provider}`\n"
        except Exception as e:
            return (
                f"# {project_name}\n\n"
                f"**Error generating AI documentation:**\n\n"
                f"`{type(e).__name__}: {str(e)}`\n\n"
                f"Please check your API key and network connection.\n"
            )

    # Format the final document
    header = (
        f"# {project_name} — AI-Generated Documentation\n\n"
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"**Source:** `{project_path}`\n"
        f"**Files Analyzed:** {len(files)}\n"
        f"**AI Provider:** {PROVIDERS.get(provider, {}).get('name', provider)}\n\n"
        f"---\n\n"
    )

    footer = (
        f"\n\n---\n\n"
        f"*AI-generated documentation — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        f"*Review for accuracy. AI may misinterpret complex logic.*\n"
    )

    return header + response + footer


def _generate_batched_documentation(project_name, files, provider, model, api_key, focus_areas):
    """
    For local models with limited context: process files in logical batches,
    then combine results into a single document.
    """
    # Categorize files by type/role
    route_files = {}
    component_files = {}
    service_files = {}
    store_files = {}
    config_files = {}
    page_files = {}
    other_files = {}

    for path, content in files.items():
        lower = path.lower().replace("\\", "/")
        if any(k in lower for k in ["route", "endpoint", "controller", "handler"]):
            route_files[path] = content
        elif any(k in lower for k in ["page", "view", "screen"]):
            page_files[path] = content
        elif any(k in lower for k in ["component", "widget", "ui/"]):
            component_files[path] = content
        elif any(k in lower for k in ["service", "api", "http", "request"]):
            service_files[path] = content
        elif any(k in lower for k in ["store", "state", "redux", "zustand", "pinia"]):
            store_files[path] = content
        elif any(k in lower for k in ["config", "env", ".yaml", ".yml", "setting"]):
            config_files[path] = content
        elif any(k in lower for k in ["app.", "main.", "index."]):
            # Main entry points — add to routes/pages
            page_files[path] = content
        else:
            other_files[path] = content

    sections = []

    # 1. Generate project overview from main/entry files
    entry_files = {k: v for k, v in files.items()
                   if any(e in k.lower() for e in ["app.", "main.", "index.", "package.json", "readme", "router", "route", "nav"])}
    if entry_files:
        overview = _call_for_batch(
            project_name, entry_files, provider, model, api_key,
            f"""Analyze these entry-point/router files for the project "{project_name}".

Generate a USER GUIDE overview:

## Application Overview
- What is this application? What does it do for the user?
- What are ALL the main pages/modules/tabs in the navigation? (look at router config, nav menu, tabs)
- How does the user navigate between them?
- What does the Home/Landing page show?

## Navigation Structure
List every page/section the user can access, like:
- **Home** — What the user sees on the home page
- **Module 1** — Brief description
- **Module 2** — Brief description
etc.

Be specific — use actual page names, route paths, and menu labels from the code."""
        )
        sections.append(overview)

    # 2. Pages/Views
    if page_files:
        page_doc = _call_for_batch(
            project_name, page_files, provider, model, api_key,
            f"""Analyze these PAGE/VIEW files for "{project_name}".

Write USER GUIDE documentation for each page. For EACH page:

### [Page Name]

**What this page is for:** (one-line description from user's perspective)

**Sections on this page:**
- Section 1 — what it shows
- Section 2 — what it shows

**What the user can do here:**
- Feature/action 1
- Feature/action 2

**How to use it (step-by-step):**
1. First, the user does...
2. Then they see...
3. They can click... to...

**UI Elements:**
- Buttons: what each button does
- Tables: what data is shown, what columns
- Dropdowns: what options are available
- Forms: what fields to fill

Write from the USER's perspective. Describe what they see and do, not how the code works."""
        )
        sections.append("\n## Pages & Views\n\n" + page_doc)

    # 3. Components
    if component_files:
        # Limit to most important components (first 15 files by size)
        sorted_comps = sorted(component_files.items(), key=lambda x: len(x[1]), reverse=True)[:15]
        comp_subset = dict(sorted_comps)
        comp_doc = _call_for_batch(
            project_name, comp_subset, provider, model, api_key,
            f"""Analyze these COMPONENT files for "{project_name}".

Write USER GUIDE documentation describing what each component provides to the user.
For EACH component, describe:

### [Component Name]
- **What the user sees:** Describe the visual element (tree, table, chart, form, dialog, etc.)
- **What it does:** What action or information it provides
- **How to use it:** Step-by-step interaction
- **Options available:** Buttons, checkboxes, settings the user can control
- **What happens when used:** The result/output

Focus on USER EXPERIENCE, not code structure. Describe buttons, tables, charts, forms, dialogs."""
        )
        sections.append("\n## UI Components & Features\n\n" + comp_doc)

    # 4. Routes/Endpoints (backend)
    if route_files:
        # Process route files in small batches of 4 for speed + quality balance
        route_docs = []
        route_items = [(path, content) for path, content in sorted(route_files.items())
                       if len(content.strip()) >= 100 and "__init__" not in path]

        # Group into batches of 4
        batch_size = 4
        for i in range(0, len(route_items), batch_size):
            batch = dict(route_items[i:i + batch_size])
            doc = _call_for_batch(
                project_name, batch, provider, model, api_key,
                f"""Read these files and document EVERY API endpoint you find.

For EACH endpoint/route, write EXACTLY this:

### `METHOD` `/path`
**Purpose:** What this endpoint does (one sentence)
**Request fields:** List the JSON/form fields expected
**Response:** What JSON fields are returned
**Logic:** 2-3 sentences — what happens step by step inside
**Errors:** Error codes or messages returned

DO NOT say "I will analyze" — just write the documentation directly.
Document ALL endpoints in ALL files provided."""
            )
            if doc and doc.strip():
                route_docs.append(doc)

        if route_docs:
            sections.append("\n## API Endpoints\n\n" + "\n\n---\n\n".join(route_docs))

    # 5. Services
    if service_files:
        svc_doc = _call_for_batch(
            project_name, service_files, provider, model, api_key,
            f"""Analyze these SERVICE/API files for "{project_name}".

Describe what features these services enable for the user:

### [Feature Name]
- **What the user can do:** (e.g., "Export data to CSV", "Share requests with other users")
- **How it works behind the scenes:** Brief explanation of what the system does
- **Dependencies:** What external systems are involved (databases, Argo server, Java service, etc.)

Focus on what these services ENABLE for the user, not code internals."""
        )
        sections.append("\n## System Features & Integrations\n\n" + svc_doc)

    # 6. Stores/State
    if store_files:
        store_doc = _call_for_batch(
            project_name, store_files, provider, model, api_key,
            f"""Analyze these STORE/STATE files for "{project_name}".

Describe what data the application manages and what the user can do with it:

### [Data Area]
- **What data is stored:** (e.g., "Selected test combination", "User's data requests")
- **Where the user sees it:** Which page/section displays this data
- **What the user can do with it:** Actions available (filter, select, export, etc.)

Write from the user's perspective — what information is available to them and what they can do with it."""
        )
        sections.append("\n## Data & State Management\n\n" + store_doc)

    # 7. Config
    if config_files:
        cfg_doc = _call_for_batch(
            project_name, config_files, provider, model, api_key,
            f"""Analyze these CONFIG files for "{project_name}".

Document:
- Environment variables used and their purpose
- Configuration settings and what they control
- Build/deployment configuration"""
        )
        sections.append("\n## Configuration\n\n" + cfg_doc)

    if not sections:
        # Fallback: send everything at once
        user_prompt = _build_analysis_prompt(project_name, files, focus_areas)
        try:
            return _call_ollama(user_prompt, model)
        except Exception as e:
            return f"Error: {e}"

    return "\n".join(sections)


def _call_for_batch(project_name, file_batch, provider, model, api_key, specific_prompt):
    """Call AI for a specific batch of files with a targeted prompt."""
    # Build source block from this batch
    file_sections = []
    total_chars = 0
    max_chars = 50000  # Allow more content per batch for detailed analysis

    for rel_path, content in file_batch.items():
        if total_chars + len(content) > max_chars:
            file_sections.append(f"\n--- FILE: {rel_path} ---\n[TRUNCATED]\n")
            continue
        file_sections.append(f"\n--- FILE: {rel_path} ---\n{content}\n")
        total_chars += len(content)

    source_block = "\n".join(file_sections)

    prompt = f"""{specific_prompt}

Here are the files:

{source_block}

IMPORTANT: Write the documentation directly. Do NOT say "I will analyze" or "I need to review".
Just produce the final documentation NOW."""

    try:
        if provider == "ollama":
            return _call_ollama(prompt, model)
        elif provider == "gemini":
            return _call_gemini(prompt, model, api_key)
        elif provider == "openai":
            return _call_openai(prompt, model, api_key)
        elif provider == "anthropic":
            return _call_anthropic(prompt, model, api_key)
    except Exception as e:
        return f"*Error processing batch: {type(e).__name__}: {str(e)}*\n"


def generate_file_documentation(
    file_path,
    project_path=None,
    provider="openai",
    model=None,
    api_key=None,
):
    """
    Generate documentation for a single file with detailed flow analysis.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except (IOError, OSError) as e:
        return f"# Error\n\nCannot read file: `{e}`\n"

    filename = os.path.basename(file_path)
    rel_path = os.path.relpath(file_path, project_path) if project_path else filename

    user_prompt = f"""Analyze this source file and produce detailed documentation:

**File:** `{rel_path}`

```
{content[:40000]}
```

Generate documentation covering:
1. **Purpose** — What this file/module does
2. **Key Components** — Classes, functions, and their roles
3. **Logic Flow** — Step-by-step flow for each major function
4. **Data Flow** — Inputs, transformations, outputs
5. **Dependencies** — What this file depends on
6. **Side Effects** — Database writes, API calls, file I/O, etc.

Be specific about HOW each function works, not just what it's named."""

    try:
        if provider == "gemini":
            response = _call_gemini(user_prompt, model, api_key)
        elif provider == "ollama":
            response = _call_ollama(user_prompt, model)
        elif provider == "openai":
            response = _call_openai(user_prompt, model, api_key)
        elif provider == "anthropic":
            response = _call_anthropic(user_prompt, model, api_key)
        else:
            return f"Unsupported provider: {provider}"
    except Exception as e:
        return f"# Error\n\n`{type(e).__name__}: {str(e)}`\n"

    return response


# ============================================================
# PROMPT BUILDING
# ============================================================

def _build_analysis_prompt(project_name, files, focus_areas=None):
    """Build the user prompt containing the project source for AI analysis."""

    # Determine focus instructions
    focus_instruction = ""
    if focus_areas:
        focus_parts = []
        if "flow" in focus_areas:
            focus_parts.append("- Detailed step-by-step FLOW of all major operations")
        if "architecture" in focus_areas:
            focus_parts.append("- System ARCHITECTURE: how components connect and communicate")
        if "api" in focus_areas:
            focus_parts.append("- All API ENDPOINTS: request/response formats, auth, error handling")
        if "data" in focus_areas:
            focus_parts.append("- DATA FLOW: how data moves through the entire system")
        if "security" in focus_areas:
            focus_parts.append("- SECURITY: authentication, authorization, data protection")
        if "deployment" in focus_areas:
            focus_parts.append("- DEPLOYMENT & INFRASTRUCTURE: how the app is deployed and configured")
        focus_instruction = "\n**Focus especially on:**\n" + "\n".join(focus_parts) + "\n"

    # Build file listing — group by directory
    file_sections = []
    total_chars = 0
    max_total = 120000  # Stay within token limits

    # Sort files by importance (route files, main app files first)
    priority_files = []
    other_files = []
    for path, content in files.items():
        lower = path.lower()
        if any(k in lower for k in ["app.", "main.", "index.", "route", "server.", "api"]):
            priority_files.append((path, content))
        else:
            other_files.append((path, content))

    ordered_files = priority_files + other_files

    for rel_path, content in ordered_files:
        if total_chars + len(content) > max_total:
            # Include a summary for remaining files
            file_sections.append(f"\n--- FILE: {rel_path} ---\n[TRUNCATED — file too large for context]\n")
            continue
        file_sections.append(f"\n--- FILE: {rel_path} ---\n{content}\n")
        total_chars += len(content)

    source_block = "\n".join(file_sections)

    prompt = f"""Analyze the following project "{project_name}" and generate COMPLETE documentation.

The project contains {len(files)} source files. Here is the complete source code:

{source_block}

---

Detect if this is a FRONTEND or BACKEND project and generate documentation accordingly:

## For BACKEND projects, write documentation in this EXACT structure:

### 1. Project Setup
- How to install dependencies and start the server (look for requirements.txt, package.json, run.py, gunicorn_config)
- Environment variables needed (look for os.getenv() calls)
- Configuration files used

### 2. Folder Structure
Explain what EACH folder contains:
- `routes/` — what it contains and its purpose
- `services/` — what it contains and its purpose
- `tests/` — what it contains
- etc.

### 3. API Endpoints (Routes)
For EVERY route file, document EVERY endpoint:

#### `METHOD` `/path` — [file name]
- **Purpose:** What this endpoint does
- **Request:** JSON fields expected (list each field with type)
- **Response:** JSON fields returned
- **Flow:** Step 1 → Step 2 → Step 3 (what happens inside)
- **Auth:** Whether authentication is required
- **Errors:** Error codes/messages

### 4. Services
For EACH service file, explain:
- What it does
- Key functions and their purpose
- What external systems it connects to (database, Java service, Argo, DLL, etc.)

### 5. Database & External Connections
- What databases are used (MSSQL, SQLite, etc.)
- How connections are managed
- External services called (Java backend, Argo workflows, etc.)

---

## For FRONTEND projects, write documentation in this EXACT structure:

### 1. Project Setup
- How to install and run the app
- Configuration needed

### 2. Application Modules (Pages)
List ALL modules/pages with brief description

### 3. For EACH Module:
#### [Module Name]
- **What it does:** Purpose of this module
- **Features:**
  - Feature 1: What it does and how it works (step-by-step flow)
  - Feature 2: What it does and how it works
- **Components used:** Key components in this module
- **API calls:** What backend endpoints this module calls
- **State/Data:** What data it reads and writes

### 4. Shared Components
- Each reusable component and what it does

### 5. State Management / Stores
- What data is stored
- How it flows between modules

---

## CRITICAL RULES:
- Document EVERY endpoint in EVERY route file — do NOT skip any
- Be SPECIFIC — use actual field names, function names, paths from the code
- Explain the LOGIC FLOW for each endpoint (what happens step by step)
- Include request/response field names you find in the actual code
- Do NOT say "I will analyze" or "let me review" — just WRITE the documentation
- Do NOT write generic descriptions — read the actual code and describe what it does
{focus_instruction}"""

    return prompt


# ============================================================
# AI PROVIDER CALLS
# ============================================================

def _call_gemini(prompt, model=None, api_key=None):
    """Call Google Gemini API (FREE tier) and return the response text."""
    import urllib.request
    import urllib.error

    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError(
            "Gemini API key not found. Get a FREE key from https://aistudio.google.com/apikey "
            "then set GEMINI_API_KEY environment variable or paste it in the form."
        )

    model_name = model or "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT + "\n\n" + prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 65000,
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Gemini API error ({e.code}): {error_body[:500]}")

    # Extract text from Gemini response
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected Gemini response format: {json.dumps(result)[:500]}")


def _call_ollama(prompt, model=None):
    """
    Call Ollama (local, FREE) and return the response text.
    Requires Ollama running locally: https://ollama.com
    """
    import urllib.request
    import urllib.error

    model_name = model or "llama3"
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model_name,
        "prompt": SYSTEM_PROMPT + "\n\n" + prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 8000,
        }
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise RuntimeError(
            f"Cannot connect to Ollama at localhost:11434. "
            f"Make sure Ollama is running: https://ollama.com\n"
            f"Then pull a model: ollama pull llama3\n"
            f"Error: {e}"
        )
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Ollama error ({e.code}): {error_body[:500]}")

    return result.get("response", "")


def _call_openai(prompt, model=None, api_key=None):
    """Call OpenAI API and return the response text."""
    if not HAS_OPENAI:
        raise ImportError(
            "The 'openai' package is not installed. "
            "Install it with: pip install openai"
        )

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError(
            "OpenAI API key not found. Set the OPENAI_API_KEY environment variable "
            "or pass it via the form."
        )

    client = openai.OpenAI(api_key=key)
    model_name = model or "gpt-4o"

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=8000,
    )

    return response.choices[0].message.content


def _call_anthropic(prompt, model=None, api_key=None):
    """Call Anthropic Claude API and return the response text."""
    if not HAS_ANTHROPIC:
        raise ImportError(
            "The 'anthropic' package is not installed. "
            "Install it with: pip install anthropic"
        )

    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError(
            "Anthropic API key not found. Set the ANTHROPIC_API_KEY environment variable "
            "or pass it via the form."
        )

    client = anthropic.Anthropic(api_key=key)
    model_name = model or "claude-sonnet-4-20250514"

    response = client.messages.create(
        model=model_name,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=8000,
    )

    return response.content[0].text
