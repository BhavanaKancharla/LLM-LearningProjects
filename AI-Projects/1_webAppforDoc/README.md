# Release Documentation Generator

A web application for creating and hosting release documentation. Reusable across all projects.

## Features

- Web form to create structured release notes (features, bug fixes, breaking changes, etc.)
- Built-in doc viewer renders Markdown to HTML
- One-click static site export (deployable anywhere)
- Delete old releases from the UI
- Only requires Flask (no extra dependencies)

## Setup

```bash
# Flask is the only dependency (already installed)
python app.py
```

Open **http://localhost:5000** in your browser.

## Usage

1. Click "Create New Release" and fill in the release details.
2. Click a release name to view the rendered documentation.
3. Click "Build Static Site" to export everything as a deployable HTML site in `site/`.

## Project Structure

```
├── app.py              # Flask web application
├── requirements.txt    # Python dependencies (flask only)
├── docs/               # Generated Markdown release docs
│   └── index.md        # Docs home page
├── templates/          # Flask HTML templates
│   ├── base.html       # Base layout
│   ├── index.html      # Dashboard
│   ├── create.html     # Release creation form
│   └── view.html       # Document viewer
└── site/               # Exported static site (after build)
```

## Deploying the Static Site

After clicking "Build Static Site", the `site/` folder contains plain HTML you can host on:
- GitHub Pages
- S3 / CloudFront
- Netlify / Vercel
- Any web server or file share
