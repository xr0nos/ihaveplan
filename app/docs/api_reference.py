import mkdocs_gen_files
from pathlib import Path

nav = mkdocs_gen_files.Nav()

app_dir = Path(__file__).parent.parent

for path in sorted(app_dir.rglob("*.py")):
    if "__pycache__" in path.parts or path.name == "__init__.py":
        continue

    module_path = path.relative_to(app_dir).with_suffix("")
    doc_path = Path("api", module_path).with_suffix(".md")

    ident = ".".join(module_path.parts)

    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"# `{ident}`\n\n::: {ident}\n")

    mkdocs_gen_files.set_edit_path(doc_path, path)
    nav[module_path.parts] = str(doc_path)

with mkdocs_gen_files.open("api/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
