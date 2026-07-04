"""
Release Documentation Web App
Create release documents via a web form, auto-generate docs from source code,
and browse them in a built-in docs viewer.
No external dependencies beyond Flask.
"""

import os
import re
import json
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from ai_documenter import (
    generate_ai_documentation,
    get_available_providers,
)

app = Flask(__name__)
app.secret_key = "release-docs-secret-key"

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
SITE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")


def slugify(text):
    """Convert text to a URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text


def md_to_html(md_text):
    """Simple Markdown to HTML converter for release notes."""
    lines = md_text.split("\n")
    html_lines = []
    in_list = False

    for line in lines:
        # Headings
        if line.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h3>{line[4:]}</h3>")
        # List items
        elif line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{line[2:]}</li>")
        # Horizontal rule
        elif line.strip() == "---":
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append("<hr>")
        # Bold text and italics inline
        elif line.strip():
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            # Handle **bold** and *italic*
            processed = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
            processed = re.sub(r"\*(.+?)\*", r"<em>\1</em>", processed)
            # Handle `code`
            processed = re.sub(r"`(.+?)`", r"<code>\1</code>", processed)
            html_lines.append(f"<p>{processed}</p>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False

    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)


def get_existing_releases():
    """List existing release documents."""
    releases = []
    if os.path.exists(DOCS_DIR):
        for filename in sorted(os.listdir(DOCS_DIR), reverse=True):
            if filename.startswith("release-") and filename.endswith(".md"):
                name = filename[:-3].replace("release-", "").replace("-", " ").title()
                releases.append({"filename": filename, "name": name, "slug": filename[:-3]})
    return releases


@app.route("/")
def index():
    """Home page showing existing releases and create form link."""
    releases = get_existing_releases()
    return render_template("index.html", releases=releases)


@app.route("/view/<slug>")
def view_release(slug):
    """View a rendered release document."""
    filename = f"{slug}.md"
    filepath = os.path.join(DOCS_DIR, filename)

    if not os.path.exists(filepath):
        flash("Release document not found.", "error")
        return redirect(url_for("index"))

    with open(filepath, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = md_to_html(md_content)
    name = slug.replace("release-", "").replace("-", " ").title()
    return render_template("view.html", name=name, content=html_content, raw_md=md_content)


@app.route("/build", methods=["POST"])
def build():
    """Build a static HTML site from all docs."""
    os.makedirs(SITE_DIR, exist_ok=True)
    releases = get_existing_releases()

    # Build index page
    nav_links = []
    for rel in releases:
        nav_links.append(f'<li><a href="{rel["slug"]}.html">{rel["name"]}</a></li>')

    index_html = build_static_page(
        title="Release Documentation",
        content=f"<h1>Release Documentation</h1><p>All release notes for this project.</p><ul>{''.join(nav_links)}</ul>",
        nav_items=releases,
    )
    with open(os.path.join(SITE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # Build each release page
    for rel in releases:
        filepath = os.path.join(DOCS_DIR, rel["filename"])
        with open(filepath, "r", encoding="utf-8") as f:
            md_content = f.read()
        html_content = md_to_html(md_content)
        page = build_static_page(title=rel["name"], content=html_content, nav_items=releases)
        with open(os.path.join(SITE_DIR, f"{rel['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(page)

    flash(f"Static site built with {len(releases)} pages in 'site/' folder.", "success")
    return redirect(url_for("index"))


def build_static_page(title, content, nav_items):
    """Generate a standalone static HTML page."""
    nav_html = ""
    for item in nav_items:
        nav_html += f'<a href="{item["slug"]}.html">{item["name"]}</a>\n'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Release Docs</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8f9fa; color: #333; }}
        .layout {{ display: flex; min-height: 100vh; }}
        .sidebar {{ width: 260px; background: #3f51b5; color: white; padding: 1.5rem; position: fixed; height: 100vh; overflow-y: auto; }}
        .sidebar h2 {{ font-size: 1.1rem; margin-bottom: 1rem; opacity: 0.9; }}
        .sidebar a {{ display: block; color: rgba(255,255,255,0.85); text-decoration: none; padding: 0.4rem 0.6rem; border-radius: 4px; margin-bottom: 0.3rem; font-size: 0.9rem; }}
        .sidebar a:hover {{ background: rgba(255,255,255,0.15); color: white; }}
        .main {{ margin-left: 260px; padding: 2rem 3rem; max-width: 800px; }}
        .main h1 {{ color: #3f51b5; margin-bottom: 0.5rem; }}
        .main h2 {{ color: #3f51b5; margin-top: 1.5rem; margin-bottom: 0.5rem; }}
        .main ul {{ padding-left: 1.5rem; margin-bottom: 1rem; }}
        .main li {{ margin-bottom: 0.3rem; }}
        .main p {{ margin-bottom: 0.8rem; line-height: 1.7; }}
        .main hr {{ border: none; border-top: 1px solid #ddd; margin: 1.5rem 0; }}
        .main code {{ background: #e8eaf6; padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.9em; }}
        .main strong {{ color: #222; }}
    </style>
</head>
<body>
    <div class="layout">
        <nav class="sidebar">
            <h2>📄 Release Docs</h2>
            <a href="index.html">Home</a>
            <hr style="border-color: rgba(255,255,255,0.2); margin: 0.8rem 0;">
            {nav_html}
        </nav>
        <main class="main">
            {content}
        </main>
    </div>
</body>
</html>"""


@app.route("/ai-docs", methods=["GET", "POST"])
def ai_docs():
    """Generate documentation using AI to explain code flow and logic."""
    providers = get_available_providers()

    if request.method == "POST":
        project_path = request.form.get("project_path", "").strip()
        project_name = request.form.get("project_name", "").strip()
        provider = request.form.get("provider", "openai").strip()
        api_key = request.form.get("api_key", "").strip()
        model = request.form.get("model", "").strip()
        focus_areas = request.form.getlist("focus")
        exclude = request.form.get("exclude_dirs", "").strip()

        if not project_path:
            flash("Project path is required.", "error")
            return render_template("ai_docs.html", providers=providers)

        if not os.path.isdir(project_path):
            flash(f"Path not found: {project_path}", "error")
            return render_template("ai_docs.html", providers=providers)

        exclude_dirs = None
        if exclude:
            exclude_dirs = set(d.strip() for d in exclude.split(",") if d.strip())

        # Generate AI documentation
        md_content = generate_ai_documentation(
            project_path=project_path,
            project_name=project_name or None,
            provider=provider,
            model=model or None,
            api_key=api_key or None,
            focus_areas=focus_areas or None,
            exclude_dirs=exclude_dirs,
        )

        # Save the file
        safe_name = slugify(project_name or os.path.basename(project_path))
        filename = f"release-aidoc-{safe_name}.md"
        filepath = os.path.join(DOCS_DIR, filename)

        os.makedirs(DOCS_DIR, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)

        flash(f"AI documentation generated: {filename}", "success")
        return redirect(url_for("view_release", slug=filename[:-3]))

    return render_template("ai_docs.html", providers=providers)


@app.route("/delete/<slug>", methods=["POST"])
def delete_release(slug):
    """Delete a release document."""
    filename = f"{slug}.md"
    filepath = os.path.join(DOCS_DIR, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f"Deleted: {filename}", "success")
    else:
        flash("File not found.", "error")

    return redirect(url_for("index"))


if __name__ == "__main__":
    os.makedirs(DOCS_DIR, exist_ok=True)
    app.run(debug=True, port=5000)
