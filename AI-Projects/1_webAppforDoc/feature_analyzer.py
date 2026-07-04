"""
Feature Documentation Analyzer.
Scans a project (local path or GitLab URL) and auto-generates structured
feature documentation — modules, endpoints, database schemas, config changes.
"""

import ast
import os
import re
import json
import tempfile
from datetime import datetime
from urllib.parse import urlparse

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# ============================================================
# SOURCE FETCHING
# ============================================================

def fetch_source(source_path, gitlab_token=None):
    """
    Fetch source files from local path or GitLab URL.
    Returns dict of {relative_path: file_content}
    """
    if source_path.startswith("http://") or source_path.startswith("https://"):
        return _fetch_from_gitlab(source_path, gitlab_token)
    else:
        return _fetch_from_local(source_path)


def _fetch_from_local(project_path):
    """Read all relevant files from a local directory."""
    files = {}
    exclude_dirs = {
        "node_modules", "venv", ".venv", "__pycache__", ".git",
        "dist", "build", ".next", "coverage", "site", "env",
        ".tox", "egg-info", ".pytest_cache", ".nyc_output",
    }
    supported_ext = {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs",
        ".yaml", ".yml", ".json", ".sql", ".env.example",
    }

    project_path = os.path.abspath(project_path)
    for root, dirs, filenames in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]
        for fname in sorted(filenames):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in supported_ext and fname not in ("Dockerfile", "Makefile"):
                continue
            filepath = os.path.join(root, fname)
            rel_path = os.path.relpath(filepath, project_path)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                # Skip minified files
                if len(content) > 1000 and content.count("\n") < len(content) / 500:
                    continue
                # Skip very large files
                if len(content) > 100000:
                    continue
                files[rel_path] = content
            except (IOError, OSError):
                continue
    return files


def _fetch_from_gitlab(url, token=None):
    """
    Fetch files from a GitLab repository URL.
    Supports formats:
      - https://gitlab.com/user/repo
      - https://gitlab.com/user/repo/-/tree/branch/path
    """
    if not HAS_REQUESTS:
        return {}

    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.hostname}"
    path_parts = parsed.path.strip("/").split("/")

    # Extract project path and optional branch/subpath
    branch = "main"
    subpath = ""

    if "/-/" in parsed.path:
        proj_path = parsed.path.split("/-/")[0].strip("/")
        after = parsed.path.split("/-/")[1]
        # tree/branch/path or blob/branch/path
        parts = after.split("/")
        if len(parts) >= 2:
            branch = parts[1]
        if len(parts) >= 3:
            subpath = "/".join(parts[2:])
    else:
        proj_path = parsed.path.strip("/")

    # URL-encode the project path
    project_id = proj_path.replace("/", "%2F")

    headers = {}
    if token:
        headers["PRIVATE-TOKEN"] = token

    # Get repository tree
    api_url = f"{base_url}/api/v4/projects/{project_id}/repository/tree"
    params = {"ref": branch, "recursive": "true", "per_page": 100}
    if subpath:
        params["path"] = subpath

    files = {}
    page = 1
    supported_ext = {".py", ".js", ".ts", ".jsx", ".tsx", ".yaml", ".yml", ".json", ".sql"}

    while True:
        params["page"] = page
        try:
            resp = requests.get(api_url, headers=headers, params=params, timeout=30, verify=False)
            if resp.status_code != 200:
                break
            items = resp.json()
            if not items:
                break

            for item in items:
                if item["type"] != "blob":
                    continue
                ext = os.path.splitext(item["name"])[1].lower()
                if ext not in supported_ext:
                    continue
                # Skip common non-source paths
                fpath = item["path"]
                if any(skip in fpath for skip in ["node_modules/", "__pycache__/", "dist/", "build/"]):
                    continue

                # Fetch file content
                file_url = f"{base_url}/api/v4/projects/{project_id}/repository/files/{fpath.replace('/', '%2F')}/raw"
                file_params = {"ref": branch}
                try:
                    file_resp = requests.get(file_url, headers=headers, params=file_params, timeout=15, verify=False)
                    if file_resp.status_code == 200:
                        files[fpath] = file_resp.text
                except Exception:
                    continue

            page += 1
            if len(items) < 100:
                break
        except Exception:
            break

    return files


# ============================================================
# DEEP CODE ANALYSIS
# ============================================================

def analyze_project(files):
    """
    Deeply analyze source files and extract:
    - Modules with descriptions and features
    - API endpoints with payloads, responses, logic
    - Database tables/schemas
    - Config entries
    """
    result = {
        "modules": [],
        "endpoints": [],
        "database": [],
        "config": [],
    }

    for rel_path, content in files.items():
        ext = os.path.splitext(rel_path)[1].lower()

        if ext == ".py":
            _analyze_python(rel_path, content, result)
        elif ext in (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"):
            _analyze_js(rel_path, content, result)
        elif ext in (".yaml", ".yml"):
            _analyze_yaml(rel_path, content, result)
        elif ext == ".json" and "package.json" in rel_path:
            _analyze_package_json(rel_path, content, result)
        elif ext == ".sql":
            _analyze_sql(rel_path, content, result)

    return result


def _analyze_python(rel_path, content, result):
    """Deep analysis of Python files."""
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return

    module_doc = ast.get_docstring(tree)

    # Detect if this is a route/handler file
    has_routes = False
    endpoints = []
    functions = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_info = _extract_python_function(node, content)
            functions.append(func_info)

            # Check for route decorators
            route = _extract_python_route(node, content)
            if route:
                has_routes = True
                endpoints.append(route)

    # Check for SQL / database table creation
    sql_tables = _find_sql_in_python(content)
    for table in sql_tables:
        table["file"] = rel_path
        result["database"].append(table)

    # If file has routes, add as endpoints
    if endpoints:
        for ep in endpoints:
            ep["file"] = rel_path
            result["endpoints"].append(ep)
    
    # Add as module
    if functions or module_doc:
        module = {
            "file": rel_path,
            "description": module_doc or "",
            "functions": functions,
            "has_routes": has_routes,
        }
        result["modules"].append(module)


def _extract_python_function(node, source):
    """Extract detailed function info including what it does."""
    docstring = ast.get_docstring(node) or ""
    args = []
    for arg in node.args.args:
        if arg.arg in ("self", "cls"):
            continue
        a = {"name": arg.arg}
        if arg.annotation:
            a["type"] = _ast_to_str(arg.annotation)
        args.append(a)

    return {
        "name": node.name,
        "docstring": docstring,
        "args": args,
        "line": node.lineno,
        "is_async": isinstance(node, ast.AsyncFunctionDef),
    }


def _extract_python_route(node, source):
    """Extract route/endpoint details from a Flask/FastAPI decorated function."""
    for dec in node.decorator_list:
        if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
            attr = dec.func.attr
            if attr in ("route", "get", "post", "put", "delete", "patch"):
                path = _ast_literal(dec.args[0]) if dec.args else "/"
                methods = [attr.upper()] if attr != "route" else ["GET"]
                for kw in dec.keywords:
                    if kw.arg == "methods" and isinstance(kw.value, ast.List):
                        methods = [_ast_literal(el) for el in kw.value.elts]

                # Extract logic from function body
                docstring = ast.get_docstring(node) or ""
                logic_steps = _extract_logic_steps(node, source)
                request_payload = _extract_request_payload(node, source)
                response_structure = _extract_response_structure(node, source)

                return {
                    "path": path,
                    "methods": methods,
                    "handler": node.name,
                    "purpose": docstring.split("\n")[0] if docstring else "",
                    "full_docstring": docstring,
                    "logic": logic_steps,
                    "request_payload": request_payload,
                    "response": response_structure,
                    "line": node.lineno,
                }
    return None


def _extract_logic_steps(node, source):
    """Try to extract the step-by-step logic from a route handler."""
    steps = []
    lines = source.split("\n")
    func_start = node.lineno - 1
    func_end = node.end_lineno if hasattr(node, 'end_lineno') else func_start + 50

    # Look for comments that describe steps
    for i in range(func_start, min(func_end, len(lines))):
        line = lines[i].strip()
        if line.startswith("# "):
            steps.append(line[2:])

    # If no comments, try to infer from code structure
    if not steps:
        for child in ast.walk(node):
            # Look for request.get_json(), request.json, etc.
            if isinstance(child, ast.Call):
                call_str = _ast_to_str(child.func) if hasattr(child, 'func') else ""
                if "validate" in call_str.lower():
                    steps.append("Validates required fields")
                elif "query" in call_str.lower() or "execute" in call_str.lower():
                    steps.append("Executes database query")
            if isinstance(child, ast.Return):
                if isinstance(child.value, ast.Call):
                    func_name = _ast_to_str(child.value.func) if hasattr(child.value, 'func') else ""
                    if "jsonify" in func_name:
                        steps.append("Returns JSON response")

    return steps


def _extract_request_payload(node, source):
    """Extract the request payload structure from a route handler."""
    lines = source.split("\n")
    func_start = node.lineno - 1
    func_end = node.end_lineno if hasattr(node, 'end_lineno') else func_start + 80

    payload_fields = []
    func_source = "\n".join(lines[func_start:func_end])

    # Pattern: data.get("field") or data["field"] or request.json["field"]
    get_patterns = re.findall(r'\.get\(["\'](\w+)["\']', func_source)
    bracket_patterns = re.findall(r'\[["\'](\w+)["\']\]', func_source)

    seen = set()
    for field in get_patterns + bracket_patterns:
        if field not in seen and field not in ("method", "headers", "content_type"):
            payload_fields.append(field)
            seen.add(field)

    return payload_fields


def _extract_response_structure(node, source):
    """Extract response structure from return statements."""
    lines = source.split("\n")
    func_start = node.lineno - 1
    func_end = node.end_lineno if hasattr(node, 'end_lineno') else func_start + 80
    func_source = "\n".join(lines[func_start:func_end])

    responses = []

    # Look for jsonify() calls or return dict patterns
    jsonify_matches = re.findall(r'jsonify\(\s*\{([^}]+)\}', func_source)
    for match in jsonify_matches:
        fields = re.findall(r'["\'](\w+)["\']', match)
        if fields:
            responses.append({"fields": fields})

    # Look for return status codes
    status_codes = re.findall(r'(\d{3})', func_source)
    status_set = set()
    for code in status_codes:
        if code in ("200", "201", "400", "404", "500"):
            status_set.add(code)

    return {"json_fields": responses, "status_codes": sorted(status_set)}


def _find_sql_in_python(content):
    """Find SQL table definitions or queries in Python files."""
    tables = []

    # CREATE TABLE patterns
    create_matches = re.findall(
        r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"\']?(\w+)[`"\']?\s*\(([^;]+)\)',
        content, re.IGNORECASE | re.DOTALL
    )
    for table_name, columns_str in create_matches:
        columns = _parse_sql_columns(columns_str)
        tables.append({
            "name": table_name,
            "columns": columns,
            "source": "CREATE TABLE statement",
        })

    # Also detect table names from INSERT/UPDATE/SELECT patterns
    referenced_tables = set()
    for pattern in [r'FROM\s+(\w+)', r'INTO\s+(\w+)', r'UPDATE\s+(\w+)', r'JOIN\s+(\w+)']:
        for match in re.findall(pattern, content, re.IGNORECASE):
            if match.lower() not in ("select", "set", "values", "where", "and", "or"):
                referenced_tables.add(match)

    return tables


def _parse_sql_columns(columns_str):
    """Parse SQL column definitions."""
    columns = []
    # Split by commas, but not within parentheses
    parts = []
    depth = 0
    current = ""
    for ch in columns_str:
        if ch == '(':
            depth += 1
            current += ch
        elif ch == ')':
            depth -= 1
            current += ch
        elif ch == ',' and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current.strip())

    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Skip constraints
        if part.upper().startswith(("PRIMARY", "UNIQUE", "FOREIGN", "CHECK", "CONSTRAINT", "INDEX")):
            continue
        tokens = part.split()
        if len(tokens) >= 2:
            col_name = tokens[0].strip('`"\'')
            col_type = tokens[1]
            desc = " ".join(tokens[2:]) if len(tokens) > 2 else ""
            columns.append({"name": col_name, "type": col_type, "extra": desc})

    return columns


def _analyze_js(rel_path, content, result):
    """Deep analysis of JavaScript/TypeScript/React files."""
    module_doc = None
    # First JSDoc comment
    jsdoc_match = re.search(r'/\*\*\s*(.*?)\s*\*/', content[:500], re.DOTALL)
    if jsdoc_match and jsdoc_match.start() < 50:
        module_doc = re.sub(r'^\s*\*\s?', '', jsdoc_match.group(1), flags=re.MULTILINE).strip()

    functions = []
    endpoints = []
    components = []

    # Extract functions with JSDoc
    jsdoc_pattern = re.compile(r'/\*\*\s*(.*?)\s*\*/\s*(?:export\s+)?(?:async\s+)?(?:function\s+(\w+)|(?:const|let|var)\s+(\w+))', re.DOTALL)
    for m in jsdoc_pattern.finditer(content):
        doc = re.sub(r'^\s*\*\s?', '', m.group(1), flags=re.MULTILINE).strip()
        name = m.group(2) or m.group(3)
        if name:
            line = content[:m.start()].count("\n") + 1
            functions.append({"name": name, "docstring": doc, "line": line, "args": [], "is_async": False})

    # Plain functions without JSDoc
    func_pattern = re.compile(
        r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)',
        re.MULTILINE
    )
    seen_funcs = {f["name"] for f in functions}
    for m in func_pattern.finditer(content):
        name = m.group(1)
        if name not in seen_funcs:
            line = content[:m.start()].count("\n") + 1
            args = [{"name": a.strip().split(":")[0].strip()} for a in m.group(2).split(",") if a.strip()]
            functions.append({"name": name, "docstring": "", "line": line, "args": args, "is_async": "async" in content[max(0,m.start()-10):m.start()]})

    # Express routes
    route_pattern = re.compile(
        r'(?:app|router)\.(get|post|put|delete|patch|all)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]',
        re.MULTILINE
    )
    for m in route_pattern.finditer(content):
        method = m.group(1).upper()
        path = m.group(2)
        line = content[:m.start()].count("\n") + 1

        # Try to get handler logic from surrounding code
        handler_block = content[m.start():m.start()+2000]
        payload_fields = re.findall(r'req\.body\.(\w+)|req\.body\[[\'"](\w+)[\'"]\]|req\.params\.(\w+)', handler_block)
        fields = [f[0] or f[1] or f[2] for f in payload_fields]

        # Look for res.json or res.status
        resp_match = re.search(r'res\.(?:status\((\d+)\)\.)?json\(\s*\{([^}]+)\}', handler_block)
        resp_fields = []
        status = "200"
        if resp_match:
            status = resp_match.group(1) or "200"
            resp_fields = re.findall(r'(\w+)\s*:', resp_match.group(2))

        endpoints.append({
            "path": path,
            "methods": [method],
            "handler": f"handler (line {line})",
            "purpose": "",
            "logic": [],
            "request_payload": fields,
            "response": {"json_fields": [{"fields": resp_fields}] if resp_fields else [], "status_codes": [status]},
            "file": rel_path,
            "line": line,
        })

    # React components
    ext = os.path.splitext(rel_path)[1].lower()
    if ext in (".jsx", ".tsx"):
        comp_pattern = re.compile(r'(?:export\s+)?(?:default\s+)?(?:const|function)\s+([A-Z]\w+)', re.MULTILINE)
        for m in comp_pattern.finditer(content):
            name = m.group(1)
            line = content[:m.start()].count("\n") + 1
            # Find props
            props_match = re.search(rf'interface\s+{name}Props\s*\{{([^}}]+)\}}', content)
            props = []
            if props_match:
                for prop_line in props_match.group(1).split("\n"):
                    prop_line = prop_line.strip().rstrip(";,")
                    pm = re.match(r'(\w+)(\?)?:\s*(.+)', prop_line)
                    if pm:
                        props.append({"name": pm.group(1), "type": pm.group(3), "optional": pm.group(2) == "?"})
            components.append({"name": name, "line": line, "props": props})

    if endpoints:
        result["endpoints"].extend(endpoints)

    # Add as module
    module = {
        "file": rel_path,
        "description": module_doc or "",
        "functions": functions,
        "has_routes": bool(endpoints),
        "components": components,
    }
    result["modules"].append(module)


def _analyze_yaml(rel_path, content, result):
    """Analyze YAML config files for route definitions and settings."""
    # Look for route definitions (common pattern in Flask config)
    route_entries = re.findall(
        r'-\s*path:\s*([^\n]+)\s+function:\s*(\w+)\s+methods:\s*\[([^\]]+)\]',
        content
    )
    if route_entries:
        config_info = {
            "file": rel_path,
            "description": "Route configuration",
            "entries": [],
        }
        for path, func, methods in route_entries:
            config_info["entries"].append({
                "path": path.strip(),
                "function": func,
                "methods": methods.strip(),
            })
        result["config"].append(config_info)


def _analyze_package_json(rel_path, content, result):
    """Analyze package.json for dependencies and scripts."""
    try:
        pkg = json.loads(content)
        config_info = {
            "file": rel_path,
            "description": f"Node.js project: {pkg.get('name', 'unknown')}",
            "entries": [],
        }
        if "scripts" in pkg:
            for name, cmd in pkg["scripts"].items():
                config_info["entries"].append({"key": name, "value": cmd})
        if "dependencies" in pkg:
            config_info["dependencies"] = list(pkg["dependencies"].keys())
        result["config"].append(config_info)
    except (json.JSONDecodeError, KeyError):
        pass


def _analyze_sql(rel_path, content, result):
    """Analyze SQL files for table definitions."""
    create_matches = re.findall(
        r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?[`"\']?(\w+)[`"\']?\s*\(([^;]+)\)',
        content, re.IGNORECASE | re.DOTALL
    )
    for table_name, columns_str in create_matches:
        columns = _parse_sql_columns(columns_str)
        result["database"].append({
            "name": table_name,
            "columns": columns,
            "file": rel_path,
            "source": "SQL file",
        })


# ============================================================
# HELPERS
# ============================================================

def _ast_to_str(node):
    """Convert AST node to string representation."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_ast_to_str(node.value)}.{node.attr}"
    if isinstance(node, ast.Constant):
        return repr(node.value)
    if isinstance(node, ast.Call):
        return _ast_to_str(node.func) if hasattr(node, 'func') else "?"
    return "?"


def _ast_literal(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return node.id
    return "<expr>"


# ============================================================
# DOCUMENT GENERATOR
# ============================================================

def generate_feature_documentation(source_path, project_name=None, gitlab_token=None):
    """
    Main entry point: scan a project and produce feature documentation.
    Returns markdown string.
    """
    if not project_name:
        if source_path.startswith("http"):
            project_name = source_path.rstrip("/").split("/")[-1]
        else:
            project_name = os.path.basename(os.path.abspath(source_path))

    # Fetch all source files
    files = fetch_source(source_path, gitlab_token)
    if not files:
        return f"# {project_name}\n\nNo source files found at the specified location.\n"

    # Analyze
    analysis = analyze_project(files)

    # Generate document
    lines = []
    lines.append(f"# {project_name} — Feature Documentation\n")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Source:** `{source_path}`")
    lines.append(f"**Files Scanned:** {len(files)}\n")

    # Overview from README or main module docstrings
    overview = _build_overview(files, analysis)
    if overview:
        lines.append("## Overview\n")
        lines.append(f"{overview}\n")

    # Modules & Components
    modules = [m for m in analysis["modules"] if not m["has_routes"]]
    route_modules = [m for m in analysis["modules"] if m["has_routes"]]

    if modules:
        lines.append("## Modules & Components\n")
        for mod in modules:
            lines.append(f"### `{mod['file']}`\n")
            if mod["description"]:
                lines.append(f"{mod['description']}\n")

            # Components (React)
            if mod.get("components"):
                lines.append("**Components:**\n")
                for comp in mod["components"]:
                    lines.append(f"- `<{comp['name']} />` (line {comp['line']})")
                    if comp.get("props"):
                        for prop in comp["props"]:
                            opt = "optional" if prop.get("optional") else "required"
                            lines.append(f"  - `{prop['name']}`: `{prop['type']}` ({opt})")
                lines.append("")

            # Functions
            if mod["functions"]:
                lines.append("**Functions:**\n")
                for func in mod["functions"]:
                    args_str = ", ".join(a["name"] for a in func.get("args", []))
                    prefix = "async " if func.get("is_async") else ""
                    lines.append(f"- `{prefix}{func['name']}({args_str})`")
                    if func.get("docstring"):
                        first_line = func["docstring"].split("\n")[0]
                        lines.append(f"  - {first_line}")
                lines.append("")

    # API Endpoints
    if analysis["endpoints"]:
        lines.append("## API Endpoints\n")

        # Summary table
        lines.append("| Method | Path | Handler | Purpose |")
        lines.append("|--------|------|---------|---------|")
        for ep in sorted(analysis["endpoints"], key=lambda x: x["path"]):
            methods = ", ".join(ep["methods"])
            purpose = ep.get("purpose", "")[:60]
            lines.append(f"| `{methods}` | `{ep['path']}` | `{ep['handler']}` | {purpose} |")
        lines.append("")

        # Detailed endpoint docs
        for ep in sorted(analysis["endpoints"], key=lambda x: x["path"]):
            methods = ", ".join(ep["methods"])
            lines.append(f"### `{methods}` `{ep['path']}`\n")
            lines.append(f"**Handler:** `{ep['handler']}`")
            lines.append(f"**File:** `{ep['file']}` (line {ep.get('line', '?')})\n")

            if ep.get("purpose"):
                lines.append(f"**Purpose:** {ep['purpose']}\n")

            if ep.get("logic"):
                lines.append("**Logic:**\n")
                for i, step in enumerate(ep["logic"], 1):
                    lines.append(f"  {i}. {step}")
                lines.append("")

            if ep.get("request_payload"):
                lines.append("**Request Payload Fields:**\n")
                lines.append("```json")
                payload = {field: "..." for field in ep["request_payload"]}
                lines.append(json.dumps(payload, indent=2))
                lines.append("```\n")

            resp = ep.get("response", {})
            if resp.get("json_fields"):
                lines.append("**Response:**\n")
                lines.append("```json")
                for rf in resp["json_fields"]:
                    resp_obj = {field: "..." for field in rf.get("fields", [])}
                    lines.append(json.dumps(resp_obj, indent=2))
                lines.append("```\n")
            if resp.get("status_codes"):
                lines.append(f"**Status Codes:** {', '.join(resp['status_codes'])}\n")

    # Route handler modules
    if route_modules:
        lines.append("## Route Handlers\n")
        for mod in route_modules:
            lines.append(f"### `{mod['file']}`\n")
            if mod["description"]:
                lines.append(f"{mod['description']}\n")
            if mod["functions"]:
                lines.append("**Functions:**\n")
                for func in mod["functions"]:
                    args_str = ", ".join(a["name"] for a in func.get("args", []))
                    lines.append(f"- `{func['name']}({args_str})`")
                    if func.get("docstring"):
                        lines.append(f"  - {func['docstring'].split(chr(10))[0]}")
                lines.append("")

    # Database
    if analysis["database"]:
        lines.append("## Database\n")
        for table in analysis["database"]:
            lines.append(f"### Table: `{table['name']}`\n")
            lines.append(f"**File:** `{table.get('file', '?')}`\n")
            if table.get("columns"):
                lines.append("| Column | Type | Details |")
                lines.append("|--------|------|---------|")
                for col in table["columns"]:
                    lines.append(f"| `{col['name']}` | `{col['type']}` | {col.get('extra', '')} |")
                lines.append("")

    # Config
    if analysis["config"]:
        lines.append("## Configuration\n")
        for cfg in analysis["config"]:
            lines.append(f"### `{cfg['file']}`\n")
            if cfg.get("description"):
                lines.append(f"{cfg['description']}\n")
            if cfg.get("entries"):
                for entry in cfg["entries"]:
                    if "path" in entry:
                        lines.append(f"- `{entry['path']}` → `{entry['function']}` [{entry['methods']}]")
                    elif "key" in entry:
                        lines.append(f"- `{entry['key']}`: `{entry['value']}`")
                lines.append("")
            if cfg.get("dependencies"):
                lines.append("**Dependencies:**\n")
                for dep in sorted(cfg["dependencies"]):
                    lines.append(f"- `{dep}`")
                lines.append("")

    lines.append("---\n")
    lines.append(f"*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    return "\n".join(lines)


def _build_overview(files, analysis):
    """Build an overview from README or top-level docstrings."""
    # Check for README
    for path, content in files.items():
        if "readme" in path.lower():
            # Extract first paragraph after the title
            lines = content.split("\n")
            in_content = False
            overview_lines = []
            for line in lines:
                if line.startswith("# "):
                    in_content = True
                    continue
                if in_content:
                    if line.startswith("## "):
                        break
                    if line.strip():
                        overview_lines.append(line.strip())
                    elif overview_lines:
                        break
            if overview_lines:
                return " ".join(overview_lines)

    # Fallback: use first module docstring
    for mod in analysis.get("modules", []):
        if mod.get("description"):
            return mod["description"].split("\n")[0]

    return ""
