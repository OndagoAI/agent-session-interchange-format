"""Publish repository documents at their existing relative paths without copying sources."""
from pathlib import Path
import re

from mkdocs.structure.files import File, Files, InclusionLevel

ROOT = Path(__file__).resolve().parents[2]

# Explicit publication inputs keep environments and build output out of the site.
PATTERNS = (
    "*.md", "LICENSE", "*.py", "*.ts", "requirements*.txt", "package*.json", "tsconfig.json",
    "docs/*.md", "docs/*.json", "docs/build_reference.py", "docs/site/assets/*",
    "schemas/*.json", "schemas/*.py", "licenses/*.txt",
    "examples/*.md", "examples/*.json", "examples/*.zip", "examples/*.key", "examples/*.py",
    "examples/continuation/*.md", "examples/continuation/*.json", "examples/assets/*",
    "reference/*.py", "reference/typescript/*.ts", "reference/typescript/*.json",
    "tests/*.py", "tests/*.ts", "tests/*.json",
)


class ResourceFile(File):
    """Markdown attachments are exact-byte resources, not documentation pages."""

    def is_documentation_page(self):
        return False


def on_files(files, config):
    # Retain theme assets, replacing only the default docs_dir inventory.
    published = Files(file for file in files if file.src_dir != config.docs_dir)
    sources = sorted({path for pattern in PATTERNS for path in ROOT.glob(pattern)})
    for path in sources:
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(ROOT).as_posix()
        file_type = ResourceFile if relative.startswith("examples/assets/") else File
        file = file_type(
            relative, str(ROOT), config.site_dir, config.use_directory_urls,
            inclusion=InclusionLevel.INCLUDED,
        )
        # Source links keep working while the site has a dedicated landing page.
        if relative == "docs/home.md":
            file.dest_uri = "index.html"
        elif relative == "README.md":
            file.dest_uri = "overview/index.html" if config.use_directory_urls else "overview.html"
        published.append(file)
    return published


def on_serve(server, config, builder):
    # Root documents and example inputs live outside MkDocs' default watch directory.
    for pattern in ("*.md", "requirements*.txt", "examples", "schemas", "reference", "tests", "licenses"):
        for path in ROOT.glob(pattern):
            server.watch(str(path))
    return server


def on_page_markdown(markdown, page, config, files):
    if page.file.src_uri in ("docs/objects.md", "docs/continuation-objects.md", "docs/report-objects.md"):
        page.meta["asif_reference"] = True
        # The sidebar already lists every object; keep the authored index in a disclosure.
        markdown = re.sub(
            r'^## Contents\n\n(.*?)(?=^<a id=)',
            '<details class="asif-object-index" markdown="1">\n'
            '<summary id="contents">Browse all objects on this page</summary>\n\n'
            r'\1</details>\n\n', markdown, flags=re.MULTILINE | re.DOTALL,
        )
    # Generated references have explicit anchors for GitHub. Attach those IDs to
    # the rendered headings so MkDocs does not emit the same ID twice.
    return re.sub(
        r'^<a id="([^"]+)"></a>\n\n(#{1,6} [^\n]+)$',
        r'\2 {#\1}', markdown, flags=re.MULTILINE,
    )
