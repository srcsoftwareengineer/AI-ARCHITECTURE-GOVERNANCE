#!/usr/bin/env python3
"""
Created on Oct 29, 2026

@description:
    Metadata Cross-Validation Linter (meta_linter.py) - SSOT Consumer Edition
    Enforces structural and metadata parity between Markdown documentation
    (YAML Frontmatter) and Python module docstrings based on governance_schema.yaml.

@id:
    META_LINTER_ENGINE

@version:
    2.0.0

@path:
    structuredoc_chunk_engine/__dev_tools__/meta_linter.py

@canonical_id:
    META_LINTER

@status:
    PRODUCTION READY (HITL VALIDATED / SCHEMA-DRIVEN)

@todo:
    Remove all hard coded paths

@author:
    Sandro Regis Cardoso <src.softwareengineer@gmail.com>

@ai_engine:
    name: GEMINI
    session_id: fe4950b8807286c4 <not paid>

@note:
    The __drafts__ directory should not participate on production environment

@license:
    MIT License

    Copyright (c) 2026 Sandro Regis Cardoso <src.softwareengineer@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import re
import sys
from pathlib import Path
from typing import Dict, Any, List


class SSOTSchemaParser:
    """
    Parses the governance_schema.yaml manifest using standard library (Zero Dependencies).
    """
    @staticmethod
    def load_schema(schema_path: Path) -> Dict[str, Any]:
        if not schema_path.exists():
            raise FileNotFoundError(f"Governance schema not found at: {schema_path}")

        content = schema_path.read_text(encoding="utf-8")
        schema = {
            "markdown_keys": [],
            "python_keys": []
        }

        current_section = None
        for line in content.splitlines():
            stripped = line.strip()
            if "mandatory_markdown_frontmatter:" in stripped:
                current_section = "markdown"
                continue
            elif "mandatory_python_docstrings:" in stripped:
                current_section = "python"
                continue
            elif stripped.startswith("governance_rules:"):
                current_section = "rules"
                continue

            if stripped.startswith("- ") and current_section in ["markdown", "python"]:
                key = stripped.lstrip("- ").strip()
                if current_section == "markdown":
                    schema["markdown_keys"].append(key)
                elif current_section == "python":
                    schema["python_keys"].append(key)

        return schema


class MetadataLinter:
    """
    Validates metadata contracts between Markdown docs and Python modules using an SSOT schema.
    @todo:
      parameter schema_file: Must replaced by schema_files => scan dirs (schemas json and yaml)
    """

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.errors = 0
        schema_file = root_dir / "structuredoc_chunk_engine" / "schemas" / "yaml" / "governance_schema.yaml"
        self.schema = SSOTSchemaParser.load_schema(schema_file)

    def parse_markdown_frontmatter(self, file_path: Path) -> Dict[str, Any]:
        try:
            content = file_path.read_text(encoding="utf-8")
            match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if not match:
                return {}

            frontmatter_text = match.group(1)
            metadata = {}
            for line in frontmatter_text.splitlines():
                if ":" in line and not line.strip().startswith("-"):
                    parts = line.split(":", 1)
                    metadata[parts[0].strip()] = parts[1].strip()
            return metadata
        except Exception as e:
            print(f"  [ERROR] Failed to parse Markdown {file_path.name}: {e}")
            self.errors += 1
            return {}

    def parse_python_docstring(self, file_path: Path) -> Dict[str, str]:
        try:
            content = file_path.read_text(encoding="utf-8")
            match = re.match(r'^\s*"""\s*\n(.*?)\n\s*"""', content, re.DOTALL)
            if not match:
                return {}

            doc_text = match.group(1)
            metadata = {}
            for line in doc_text.splitlines():
                line = line.strip()
                if line.startswith("@"):
                    parts = line.lstrip("@").split(":", 1)
                    if len(parts) == 2:
                        metadata[parts[0].strip().lower()] = parts[1].strip()
                elif ":" in line and not line.startswith("http"):
                    parts = line.split(":", 1)
                    metadata[parts[0].strip().lower()] = parts[1].strip()
            return metadata
        except Exception as e:
            print(f"  [ERROR] Failed to parse Python file {file_path.name}: {e}")
            self.errors += 1
            return {}

    def validate_repository(self) -> int:
        print("==================================================")
        print("  AI ARCHITECTURE GOVERNANCE - SSOT META LINTER   ")
        print("==================================================")

        docs_dir = self.root_dir / "structuredoc_chunk_engine" / "docs"
        drafts_dir = self.root_dir / "structuredoc_chunk_engine" / "__drafts__"    # remove for production environment

        md_files = list(docs_dir.glob("*.md")) + list(self.root_dir.glob("*.md"))
        py_files = list(drafts_dir.glob("*.py"))

        print(f"[*] Loaded SSOT Schema with {len(self.schema['markdown_keys'])} MD keys and {len(self.schema['python_keys'])} PY keys.")
        print(f"[*] Analyzing {len(md_files)} Markdown document(s) and {len(py_files)} Python draft(s)...")

        for md in md_files:
            meta = self.parse_markdown_frontmatter(md)
            if meta:
                missing = [k for k in self.schema["markdown_keys"] if k not in meta]
                if missing:
                    print(f"  [FAIL] {md.name} is missing mandatory SSOT keys: {missing}")
                    self.errors += len(missing)
                else:
                    print(f"  [OK] Valid YAML Frontmatter in: {md.name} (Module: {meta.get('module', 'N/A')})")
            else:
                print(f"  [WARN] Missing or invalid YAML Frontmatter in: {md.name}")
                self.errors += 1

        for py in py_files:
            meta = self.parse_python_docstring(py)
            if meta:
                missing = [k for k in self.schema["python_keys"] if k not in meta]
                if missing:
                    print(f"  [FAIL] {py.name} is missing mandatory SSOT keys: {missing}")
                    self.errors += len(missing)
                else:
                    print(f"  [OK] Valid Docstring Metadata in: {py.name} (Version: {meta.get('version', 'N/A')})")
            else:
                print(f"  [WARN] Missing structured docstring metadata in: {py.name}")
                self.errors += 1

        print("==================================================")
        print(f"Linter finished with {self.errors} fatal error(s).")
        return self.errors


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[2]
    linter = MetadataLinter(repo_root)
    sys.exit(linter.validate_repository())
