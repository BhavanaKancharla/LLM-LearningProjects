"""
Multi-language auto-documentation generator.
Supports: Python, JavaScript, TypeScript, React (JSX/TSX), Node.js
Extracts: docstrings, classes, functions, API endpoints, components, config.
"""

import ast
import os
import re
from datetime import datetime


# ============================================================
# PYTHON ANALYZER (AST-based)
# ============================================================

class PythonAnalyzer:
    """Analyze Python files using the ast module."""

    def analyze(self, source, filepath):
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return None

        result = {
            "module_docstring": ast.get_docstring(tree),
            "classes": [],
            "functions": [],
            "routes": [],
            "constants": [],
            "imports": [],
        }

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                result["classes"].append(self._parse_class(node))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func = self._parse_function(node)
                result["functions"].append(func)
                route = self._extract_route(node)
                if route:
                    result["routes"].append(route)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.isupper():
                        val = self._literal(node.value)
                        result["constants"].append({"name": target.id, "value": val, "line": node.lineno})
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        result["imports"].append(alias.name)
                else:
                    mod = node.module or ""
                    for alias in node.names:
                        result["imports"].append(f"{mod}.{alias.name}")

        return result

    def _parse_class(self, node):
        cls = {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "methods": [],
            "bases": [self._dotted(b) for b in node.bases],
            "line": node.lineno,
        }
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                cls["methods"].append(self._parse_function(item))
        return cls

    def _parse_function(self, node):
        args = []
        for arg in node.args.args:
            if arg.arg in ("self", "cls"):
                continue
            a = {"name": arg.arg}
            if arg.annotation:
                a["type"] = self._annotation(arg.annotation)
            args.append(a)
        return {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "args": args,
            "returns": self._annotation(node.returns) if node.returns else None,
            "decorators": [self._dotted_dec(d) for d in node.decorator_list],
            "is_async": isinstance(node, ast.AsyncFunctionDef),
            "line": node.lineno,
        }

    def _extract_route(self, node):
        for dec in node.decorator_list:
            if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                attr = dec.func.attr
                if attr in ("route", "get", "post", "put", "delete", "patch"):
                    path = self._literal(dec.args[0]) if dec.args else "/"
                    methods = [attr.upper()] if attr != "route" else ["GET"]
                    for kw in dec.keywords:
                        if kw.arg == "methods" and isinstance(kw.value, ast.List):
                            methods = [self._literal(el) for el in kw.value.elts]
                    return {
                        "path": path, "methods": methods,
                        "function": node.name,
                        "docstring": ast.get_docstring(node),
                        "line": node.lineno,
                    }
        return None

    def _annotation(self, node):
        if node is None:
            return None
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Constant):
            return repr(node.value)
        if isinstance(node, ast.Attribute):
            return self._dotted(node)
        if isinstance(node, ast.Subscript):
            return f"{self._annotation(node.value)}[{self._annotation(node.slice)}]"
        return "..."

    def _dotted(self, node):
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return f"{self._dotted(node.value)}.{node.attr}"
        return "?"

    def _dotted_dec(self, node):
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return self._dotted(node)
        if isinstance(node, ast.Call):
            return self._dotted_dec(node.func)
        return "?"

    def _literal(self, node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return node.id
        return "<expr>"


# ============================================================
# JAVASCRIPT / TYPESCRIPT / REACT ANALYZER (Regex-based)
# ============================================================

class JSAnalyzer:
    """Analyze JS/TS/JSX/TSX files using regex patterns."""

    # Patterns for JSDoc comments
    JSDOC_RE = re.compile(r'/\*\*\s*(.*?)\s*\*/', re.DOTALL)

    # Function patterns
    FUNC_DECL_RE = re.compile(
        r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*'
        r'(?:<[^>]*>)?\s*\(([^)]*)\)(?:\s*:\s*([^\s{]+))?\s*\{',
        re.MULTILINE
    )
    ARROW_FUNC_RE = re.compile(
        r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*'
        r'(?::\s*[^=]+?)?\s*=\s*(?:async\s+)?'
        r'(?:<[^>]*>)?\s*\(([^)]*)\)(?:\s*:\s*([^\s=>{]+))?\s*=>',
        re.MULTILINE
    )

    # Class pattern
    CLASS_RE = re.compile(
        r'(?:export\s+)?(?:abstract\s+)?class\s+(\w+)'
        r'(?:\s+extends\s+([\w.]+))?'
        r'(?:\s+implements\s+([\w.,\s]+))?\s*\{',
        re.MULTILINE
    )

    # Method pattern inside classes
    METHOD_RE = re.compile(
        r'(?:(?:public|private|protected|static|async|readonly)\s+)*'
        r'(\w+)\s*(?:<[^>]*>)?\s*\(([^)]*)\)(?:\s*:\s*([^\s{]+))?\s*\{',
        re.MULTILINE
    )

    # React component patterns
    COMPONENT_RE = re.compile(
        r'(?:export\s+)?(?:default\s+)?(?:const|function)\s+(\w+)\s*'
        r'(?::\s*React\.FC(?:<[^>]*>)?)?\s*[=(]',
        re.MULTILINE
    )

    # Express/Node route patterns
    EXPRESS_ROUTE_RE = re.compile(
        r'(?:app|router)\.(get|post|put|delete|patch|all)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]',
        re.MULTILINE
    )

    # Import patterns
    IMPORT_RE = re.compile(
        r'import\s+.*?from\s+[\'"`]([^\'"`]+)[\'"`]',
        re.MULTILINE
    )
    REQUIRE_RE = re.compile(
        r'(?:const|let|var)\s+.*?=\s*require\s*\(\s*[\'"`]([^\'"`]+)[\'"`]\s*\)',
        re.MULTILINE
    )

    # Constants
    CONST_UPPER_RE = re.compile(
        r'(?:export\s+)?(?:const|let|var)\s+([A-Z][A-Z_0-9]+)\s*=\s*(.+?)(?:;|$)',
        re.MULTILINE
    )

    # Interface / Type patterns
    INTERFACE_RE = re.compile(
        r'(?:export\s+)?(?:interface|type)\s+(\w+)(?:\s+extends\s+([\w.,\s]+))?\s*[={]',
        re.MULTILINE
    )

    def analyze(self, source, filepath):
        result = {
            "module_docstring": None,
            "classes": [],
            "functions": [],
            "routes": [],
            "constants": [],
            "imports": [],
            "components": [],
            "interfaces": [],
        }

        lines = source.split("\n")

        # Module-level comment (first JSDoc or // comment block)
        first_jsdoc = self.JSDOC_RE.search(source[:500])
        if first_jsdoc and first_jsdoc.start() < 50:
            result["module_docstring"] = self._clean_jsdoc(first_jsdoc.group(1))

        # Build a map of JSDoc comments by their end line
        jsdoc_map = self._build_jsdoc_map(source)

        # Extract functions
        for m in self.FUNC_DECL_RE.finditer(source):
            line_num = source[:m.start()].count("\n") + 1
            doc = jsdoc_map.get(line_num)
            result["functions"].append({
                "name": m.group(1),
                "args": self._parse_js_args(m.group(2)),
                "returns": m.group(3),
                "docstring": doc,
                "is_async": "async" in source[max(0, m.start()-10):m.start()],
                "line": line_num,
                "decorators": [],
            })

        # Arrow functions
        for m in self.ARROW_FUNC_RE.finditer(source):
            line_num = source[:m.start()].count("\n") + 1
            doc = jsdoc_map.get(line_num)
            name = m.group(1)
            # Skip if it looks like a React component (starts uppercase)
            result["functions"].append({
                "name": name,
                "args": self._parse_js_args(m.group(2)),
                "returns": m.group(3),
                "docstring": doc,
                "is_async": "async" in source[m.start():m.end()],
                "line": line_num,
                "decorators": [],
            })

        # Classes
        for m in self.CLASS_RE.finditer(source):
            line_num = source[:m.start()].count("\n") + 1
            doc = jsdoc_map.get(line_num)
            # Find methods within class body
            class_start = m.end()
            class_body = self._extract_block(source, class_start - 1)
            methods = []
            for mm in self.METHOD_RE.finditer(class_body):
                mline = source[:class_start].count("\n") + class_body[:mm.start()].count("\n") + 1
                mdoc = jsdoc_map.get(mline)
                methods.append({
                    "name": mm.group(1),
                    "args": self._parse_js_args(mm.group(2)),
                    "returns": mm.group(3),
                    "docstring": mdoc,
                    "is_async": False,
                    "line": mline,
                    "decorators": [],
                })
            bases = []
            if m.group(2):
                bases.append(m.group(2).strip())
            result["classes"].append({
                "name": m.group(1),
                "docstring": doc,
                "methods": methods,
                "bases": bases,
                "line": line_num,
            })

        # React components (uppercase function names in JSX/TSX files)
        ext = os.path.splitext(filepath)[1].lower()
        if ext in (".jsx", ".tsx"):
            for m in self.COMPONENT_RE.finditer(source):
                name = m.group(1)
                if name[0].isupper():
                    line_num = source[:m.start()].count("\n") + 1
                    doc = jsdoc_map.get(line_num)
                    # Try to find props interface
                    props = self._find_props(source, name)
                    result["components"].append({
                        "name": name,
                        "docstring": doc,
                        "props": props,
                        "line": line_num,
                    })

        # Express/Node routes
        for m in self.EXPRESS_ROUTE_RE.finditer(source):
            line_num = source[:m.start()].count("\n") + 1
            # Try to get the handler function name or inline doc
            doc = jsdoc_map.get(line_num)
            result["routes"].append({
                "path": m.group(2),
                "methods": [m.group(1).upper()],
                "function": f"handler (line {line_num})",
                "docstring": doc,
                "line": line_num,
            })

        # Interfaces and types
        for m in self.INTERFACE_RE.finditer(source):
            line_num = source[:m.start()].count("\n") + 1
            doc = jsdoc_map.get(line_num)
            result["interfaces"].append({
                "name": m.group(1),
                "extends": m.group(2).strip() if m.group(2) else None,
                "docstring": doc,
                "line": line_num,
            })

        # Constants
        for m in self.CONST_UPPER_RE.finditer(source):
            val = m.group(2).strip()[:60]
            result["constants"].append({
                "name": m.group(1),
                "value": val,
                "line": source[:m.start()].count("\n") + 1,
            })

        # Imports
        for m in self.IMPORT_RE.finditer(source):
            result["imports"].append(m.group(1))
        for m in self.REQUIRE_RE.finditer(source):
            result["imports"].append(m.group(1))

        return result

    def _build_jsdoc_map(self, source):
        """Map: line_number_after_comment -> jsdoc text."""
        jsdoc_map = {}
        for m in self.JSDOC_RE.finditer(source):
            end_line = source[:m.end()].count("\n") + 2  # next line after comment
            jsdoc_map[end_line] = self._clean_jsdoc(m.group(1))
        return jsdoc_map

    def _clean_jsdoc(self, raw):
        """Clean JSDoc comment text."""
        lines = raw.split("\n")
        cleaned = []
        for line in lines:
            line = re.sub(r'^\s*\*\s?', '', line)
            cleaned.append(line)
        return "\n".join(cleaned).strip()

    def _parse_js_args(self, args_str):
        """Parse JS/TS function arguments."""
        args = []
        if not args_str.strip():
            return args
        # Simple split (doesn't handle nested generics perfectly but works for most cases)
        depth = 0
        current = ""
        for ch in args_str:
            if ch in "<({":
                depth += 1
                current += ch
            elif ch in ">)}":
                depth -= 1
                current += ch
            elif ch == "," and depth == 0:
                args.append(self._parse_single_arg(current.strip()))
                current = ""
            else:
                current += ch
        if current.strip():
            args.append(self._parse_single_arg(current.strip()))
        return args

    def _parse_single_arg(self, arg_str):
        """Parse a single argument like 'name: string = default'."""
        # Remove destructuring
        if arg_str.startswith("{") or arg_str.startswith("["):
            return {"name": arg_str.split(":")[0].strip()}

        parts = arg_str.split("=", 1)
        name_type = parts[0].strip()
        default = parts[1].strip() if len(parts) > 1 else None

        type_parts = name_type.split(":", 1)
        name = type_parts[0].strip().lstrip(".")  # handle ...rest
        type_ann = type_parts[1].strip() if len(type_parts) > 1 else None

        result = {"name": name}
        if type_ann:
            result["type"] = type_ann
        if default:
            result["default"] = default
        return result

    def _extract_block(self, source, start_pos):
        """Extract a {} block from source starting at start_pos."""
        depth = 0
        i = start_pos
        while i < len(source) and source[i] != '{':
            i += 1
        if i >= len(source):
            return ""
        start = i
        while i < len(source):
            if source[i] == '{':
                depth += 1
            elif source[i] == '}':
                depth -= 1
                if depth == 0:
                    return source[start + 1:i]
            i += 1
        return source[start + 1:]

    def _find_props(self, source, component_name):
        """Try to find Props interface for a component."""
        # Look for ComponentNameProps or IComponentNameProps
        patterns = [
            f"interface {component_name}Props",
            f"type {component_name}Props",
            f"interface I{component_name}Props",
        ]
        for pat in patterns:
            idx = source.find(pat)
            if idx != -1:
                block = self._extract_block(source, idx)
                return self._parse_props_block(block)
        return []

    def _parse_props_block(self, block):
        """Parse props from an interface/type block."""
        props = []
        for line in block.split("\n"):
            line = line.strip().rstrip(";").rstrip(",")
            if not line or line.startswith("//"):
                continue
            match = re.match(r'(\w+)(\?)?:\s*(.+)', line)
            if match:
                props.append({
                    "name": match.group(1),
                    "optional": match.group(2) == "?",
                    "type": match.group(3).strip(),
                })
        return props


# ============================================================
# PROJECT SCANNER
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".jsx": "react",
    ".tsx": "react-ts",
    ".mjs": "javascript",
    ".cjs": "javascript",
}

DEFAULT_EXCLUDE = {
    "venv", ".venv", "env", "__pycache__", ".git", "node_modules",
    ".tox", "site", "dist", "build", ".next", "coverage",
    ".nyc_output", ".pytest_cache", "egg-info",
}


def scan_project(project_path, exclude_dirs=None):
    """Scan a project and return analysis results for all supported files."""
    if exclude_dirs is None:
        exclude_dirs = DEFAULT_EXCLUDE

    results = {}
    project_path = os.path.abspath(project_path)
    py_analyzer = PythonAnalyzer()
    js_analyzer = JSAnalyzer()

    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]

        for filename in sorted(files):
            ext = os.path.splitext(filename)[1].lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue

            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, project_path)

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    source = f.read()
            except (IOError, OSError):
                continue

            # Skip minified files
            if len(source) > 500 and source.count("\n") < len(source) / 500:
                continue

            lang = SUPPORTED_EXTENSIONS[ext]
            if lang == "python":
                analysis = py_analyzer.analyze(source, rel_path)
            else:
                analysis = js_analyzer.analyze(source, rel_path)

            if analysis:
                analysis["language"] = lang
                results[rel_path] = analysis

    return results


# ============================================================
# MARKDOWN DOCUMENT GENERATOR
# ============================================================

def generate_project_docs(project_path, project_name=None, exclude_dirs=None):
    """Generate complete project documentation as Markdown."""
    if not project_name:
        project_name = os.path.basename(os.path.abspath(project_path))

    results = scan_project(project_path, exclude_dirs)

    if not results:
        return f"# {project_name}\n\nNo supported source files found.\n"

    sections = []
    sections.append(f"# {project_name} — Documentation\n")
    sections.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Gather all items
    all_routes = []
    all_classes = []
    all_functions = []
    all_components = []
    all_interfaces = []
    all_constants = []
    all_imports = set()

    for rel_path, analysis in results.items():
        lang = analysis.get("language", "")
        all_routes.extend([(r, rel_path, lang) for r in analysis.get("routes", [])])
        all_classes.extend([(c, rel_path, lang) for c in analysis.get("classes", [])])
        all_functions.extend([(f, rel_path, lang) for f in analysis.get("functions", [])
                              if not f["name"].startswith("_")])
        all_components.extend([(c, rel_path) for c in analysis.get("components", [])])
        all_interfaces.extend([(i, rel_path) for i in analysis.get("interfaces", [])])
        all_constants.extend([(c, rel_path) for c in analysis.get("constants", [])])
        for imp in analysis.get("imports", []):
            all_imports.add(imp.split(".")[0].split("/")[0])

    # File summary
    lang_counts = {}
    for analysis in results.values():
        lang = analysis.get("language", "unknown")
        lang_counts[lang] = lang_counts.get(lang, 0) + 1

    sections.append("## Project Overview\n")
    sections.append(f"**Files scanned:** {len(results)}\n")
    lang_summary = ", ".join(f"{lang}: {count}" for lang, count in sorted(lang_counts.items()))
    sections.append(f"**Languages:** {lang_summary}\n")

    # TOC
    sections.append("## Table of Contents\n")
    toc = []
    if all_routes:
        toc.append("- [API Endpoints](#api-endpoints)")
    if all_components:
        toc.append("- [React Components](#react-components)")
    if all_interfaces:
        toc.append("- [Interfaces & Types](#interfaces--types)")
    toc.append("- [Modules](#modules)")
    if all_classes:
        toc.append("- [Classes](#classes)")
    if all_functions:
        toc.append("- [Functions](#functions)")
    if all_constants:
        toc.append("- [Configuration](#configuration)")
    toc.append("- [Dependencies](#dependencies)")
    sections.append("\n".join(toc) + "\n")

    # API Endpoints
    if all_routes:
        sections.append("## API Endpoints\n")
        sections.append("| Method | Path | Handler | Description |")
        sections.append("|--------|------|---------|-------------|")
        for route, fpath, lang in sorted(all_routes, key=lambda x: x[0]["path"]):
            methods = ", ".join(route["methods"])
            desc = (route["docstring"] or "").split("\n")[0][:80] if route["docstring"] else ""
            sections.append(f"| `{methods}` | `{route['path']}` | `{route['function']}` | {desc} |")
        sections.append("")

    # React Components
    if all_components:
        sections.append("## React Components\n")
        for comp, fpath in sorted(all_components, key=lambda x: x[0]["name"]):
            sections.append(f"### `<{comp['name']} />`\n")
            sections.append(f"**File:** `{fpath}` (line {comp['line']})\n")
            if comp["docstring"]:
                sections.append(f"{comp['docstring']}\n")
            if comp.get("props"):
                sections.append("**Props:**\n")
                sections.append("| Prop | Type | Required |")
                sections.append("|------|------|----------|")
                for prop in comp["props"]:
                    req = "No" if prop.get("optional") else "Yes"
                    sections.append(f"| `{prop['name']}` | `{prop.get('type', 'any')}` | {req} |")
                sections.append("")

    # Interfaces & Types
    if all_interfaces:
        sections.append("## Interfaces & Types\n")
        for iface, fpath in sorted(all_interfaces, key=lambda x: x[0]["name"]):
            ext_str = f" extends `{iface['extends']}`" if iface.get("extends") else ""
            sections.append(f"### `{iface['name']}`{ext_str}\n")
            sections.append(f"**File:** `{fpath}` (line {iface['line']})\n")
            if iface.get("docstring"):
                sections.append(f"{iface['docstring']}\n")

    # Modules
    sections.append("## Modules\n")
    for rel_path, analysis in sorted(results.items()):
        lang_badge = analysis.get("language", "").upper()
        sections.append(f"### `{rel_path}` [{lang_badge}]\n")
        if analysis.get("module_docstring"):
            sections.append(f"{analysis['module_docstring']}\n")
        else:
            sections.append("*No module-level documentation.*\n")

    # Classes
    if all_classes:
        sections.append("## Classes\n")
        for cls, fpath, lang in sorted(all_classes, key=lambda x: x[0]["name"]):
            bases = f"({', '.join(cls['bases'])})" if cls["bases"] else ""
            sections.append(f"### `{cls['name']}{bases}`\n")
            sections.append(f"**File:** `{fpath}` (line {cls['line']})\n")
            if cls["docstring"]:
                sections.append(f"{cls['docstring']}\n")
            if cls["methods"]:
                sections.append("**Methods:**\n")
                for method in cls["methods"]:
                    if method["name"].startswith("__") and method["name"] != "__init__":
                        continue
                    args_str = _format_args(method["args"])
                    ret = f" → `{method['returns']}`" if method.get("returns") else ""
                    prefix = "async " if method.get("is_async") else ""
                    sections.append(f"- `{prefix}{method['name']}({args_str})`{ret}")
                    if method.get("docstring"):
                        sections.append(f"  - {method['docstring'].split(chr(10))[0]}")
                sections.append("")

    # Functions
    if all_functions:
        sections.append("## Functions\n")
        for func, fpath, lang in sorted(all_functions, key=lambda x: x[0]["name"]):
            args_str = _format_args(func["args"])
            ret = f" → `{func['returns']}`" if func.get("returns") else ""
            prefix = "async " if func.get("is_async") else ""
            sections.append(f"### `{prefix}{func['name']}({args_str})`{ret}\n")
            sections.append(f"**File:** `{fpath}` (line {func['line']})\n")
            if func.get("docstring"):
                sections.append(f"{func['docstring']}\n")
            else:
                sections.append("*No documentation.*\n")

    # Configuration
    if all_constants:
        sections.append("## Configuration\n")
        sections.append("| Constant | Value | File |")
        sections.append("|----------|-------|------|")
        for const, fpath in sorted(all_constants, key=lambda x: x[0]["name"]):
            value = str(const["value"])[:50]
            sections.append(f"| `{const['name']}` | `{value}` | `{fpath}` |")
        sections.append("")

    # Dependencies
    if all_imports:
        sections.append("## Dependencies\n")
        # Separate Node built-ins from third-party
        node_builtins = {
            "fs", "path", "http", "https", "url", "os", "util", "events",
            "stream", "crypto", "child_process", "net", "dns", "tls",
            "cluster", "readline", "zlib", "buffer", "querystring",
            "assert", "process", "module", "worker_threads", "timers",
        }
        py_stdlib = {
            "os", "sys", "re", "json", "ast", "datetime", "pathlib", "typing",
            "collections", "functools", "itertools", "subprocess", "io", "abc",
            "dataclasses", "enum", "math", "hashlib", "uuid", "logging",
            "unittest", "contextlib", "copy", "shutil", "tempfile", "time",
            "threading", "multiprocessing", "socket", "http", "urllib",
        }
        builtins = node_builtins | py_stdlib
        third_party = sorted(all_imports - builtins)
        if third_party:
            sections.append("**Third-party packages:**\n")
            for pkg in third_party:
                if not pkg.startswith("."):
                    sections.append(f"- `{pkg}`")
            sections.append("")

    sections.append("---\n")
    sections.append(f"*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    return "\n".join(sections)


def _format_args(args):
    """Format function arguments into a readable string."""
    parts = []
    for arg in args:
        s = arg["name"]
        if "type" in arg:
            s += f": {arg['type']}"
        if "default" in arg and arg["default"] is not None:
            s += f" = {arg['default']}"
        parts.append(s)
    return ", ".join(parts)
