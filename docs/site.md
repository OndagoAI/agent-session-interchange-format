# Documentation maintenance

The GitHub Pages site uses [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/). It reads the repository's existing Markdown files, generated references, schemas and examples directly. Edit the original documents; there is no second copy to maintain.

## Validate and preview locally

Run these commands from the repository root with Python 3.11 or newer:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-docs.txt
.venv/bin/python tests/check_documentation.py
.venv/bin/python -m mkdocs build --strict
.venv/bin/python -m mkdocs serve
```

Open the local address printed by `mkdocs serve`. The development server watches the source documents and reloads after edits. The static build is written to the ignored `site/` directory.

The strict build rejects missing navigation entries, broken local links and missing anchors. The existing documentation checker also verifies the generated object references and all their schema examples.

## Publish on GitHub Pages

The repository includes a **Documentation** Actions workflow. Pull requests build and validate the site; pushes to `main` build and deploy it. The workflow can also be run manually from `main`.

1. In the repository's **Settings → Pages → Build and deployment**, set **Source** to **GitHub Actions**.
2. Push the documentation and workflow to `main`, or run **Actions → Documentation → Run workflow** from that branch.
3. Open the deployment URL shown by the `github-pages` environment after the workflow succeeds.

The configured project URL is [ondagoai.github.io/agent-session-interchange-format](https://ondagoai.github.io/agent-session-interchange-format/). It becomes available after the first successful deployment. For a fork or custom domain, update `site_url`, `repo_url` and `repo_name` in `mkdocs.yml` and adjust the workflow branch if needed.

The build job has read access to repository contents. Only the deployment job receives Pages write and OIDC permissions. See GitHub's [custom Pages workflow documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) for the deployment contract.

## Add or update a page

Add authored Markdown at the repository root or directly under `docs/`, then add it to `nav` in `mkdocs.yml`. Keep relative Markdown links so the same source works on GitHub and on the site. The landing page is authored in [home.md](home.md) and published at the site root; the repository [README](../README.md) appears under `overview/`. Other `README.md` files become their directory's index.

The hook at `docs/site/hooks.py` selects publication inputs explicitly and maps the landing and overview pages while retaining their source-link identities. It also publishes schemas, sample data and linked source files. Files under `examples/assets/` remain byte-for-byte downloads, even when their extension is `.md`. Extend the hook's input patterns if a new documentation directory or asset type is needed.

The visual theme lives in `docs/site/assets/styles.css`, with templates under `docs/site/overrides/`. The homepage's session illustration uses `docs/site/assets/site.js` for keyboard-accessible tabs; it makes no provider calls. Object-reference indexes become collapsible on the website, while the generated Markdown remains unchanged. Both the homepage and reference pages stay in the normal search index.

Generated object pages come from the schemas and authored metadata. After changing those inputs, regenerate the pages and rerun validation:

```sh
.venv/bin/python docs/build_reference.py
.venv/bin/python tests/check_documentation.py
.venv/bin/python -m mkdocs build --strict
```

The site banner and project pages retain ASIF's proposal status. Publishing documentation does not close the [P0 implementation, evidence or release gaps](../GAPS.md).
