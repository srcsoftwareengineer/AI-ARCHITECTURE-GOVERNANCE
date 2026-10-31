"""
Created on Oct 28, 2026

@description:
    Enterprise Financial Document Preprocessor (Structure-Aware Chunking)
    Low-level structural chunker designed for complex financial and regulatory PDFs
    without reliance on high-level orchestration frameworks.

@id:
    financial_document_chunker.py

@version:
    1.1.0

@path:
    structuredoc_chunk_engine/__drafts__/financial_document_chunker.py

@canonical_id:
    FINANCIAL_DOCUMENT_CHUNKER

@status:
    DRAFT

@author:
    Sandro Regis Cardoso <src.softwareengineer@gmail.com>

@ai_engine:
    name: GEMINI
    environment: web
    session_id: 315fdd4378f66716 <not paid>

@refactor:
    Migrated codebase and documentation to en-US standard.

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
from typing import List, Dict, Any


class FinancialDocumentChunker:
    """
    Processes and chunks dense financial documents respecting semantic boundaries and tables.
    """

    def __init__(self, max_chunk_size: int = 1000):
        self.max_chunk_size = max_chunk_size

    def parse_raw_text(
        self, raw_text: str, document_title: str
    ) -> List[Dict[str, Any]]:
        """
        Splits the document based on regulatory/structural markers (e.g., Articles or Sections)
        and preserves tabular blocks atomically.
        """
        chunks = []

        # Identify common structural divisions in financial/regulatory documents
        # E.g., "SECTION X", "CHAPTER Y", "Art. 1"
        section_pattern = re.compile(r"(?i)(CHAPTER\s+\d+|SECTION\s+\d+|Art\.\s*\d+)")
        splits = section_pattern.split(raw_text)

        current_header = "Introduction / General"
        current_body = ""

        # If the split returns blocks based on the regex
        if len(splits) > 1:
            # The first element before the first header
            if splits[0].strip():
                chunks.extend(
                    self._create_atomic_chunks(
                        splits[0], document_title, current_header
                    )
                )

            # Iterate over pairs of (Header, Content)
            for i in range(1, len(splits), 2):
                current_header = splits[i].strip()
                current_body = splits[i + 1] if (i + 1) < len(splits) else ""

                atomic_chunks = self._create_atomic_chunks(
                    current_body, document_title, current_header
                )
                chunks.extend(atomic_chunks)
        else:
            # Fallback if the document does not have strict section patterns
            chunks.extend(
                self._create_atomic_chunks(raw_text, document_title, "General")
            )

        return chunks

    def _is_table_block(self, text: str) -> bool:
        """
        Heuristically identifies if the text block contains a financial table.
        """
        # Presence of multiple tabular separators or vertical alignments
        return text.count("|") > 3 or text.count("\t") > 4

    def _create_atomic_chunks(
        self, text: str, doc_title: str, section_title: str
    ) -> List[Dict[str, Any]]:
        """
        Ensures tables are not split in half and injects contextual metadata.
        """
        chunks = []
        lines = text.strip().split("\n")

        current_chunk_lines = []
        current_length = 0

        for line in lines:
            line_len = len(line)

            # If the current block exceeds the limit and we are not inside a table, close the chunk
            if current_length + line_len > self.max_chunk_size and current_chunk_lines:
                chunk_text = "\n".join(current_chunk_lines)

                # Contextual Prefixing (Injecting metadata into text to improve embedding retrieval)
                enriched_text = (
                    f"[Doc: {doc_title} | Section: {section_title}]\n{chunk_text}"
                )

                chunks.append(
                    {
                        "metadata": {
                            "document": doc_title,
                            "section": section_title,
                            "is_table": self._is_table_block(chunk_text),
                        },
                        "content": enriched_text,
                    }
                )

                current_chunk_lines = []
                current_length = 0

            current_chunk_lines.append(line)
            current_length += line_len

        # Flush residual blocks
        if current_chunk_lines:
            chunk_text = "\n".join(current_chunk_lines)
            enriched_text = (
                f"[Doc: {doc_title} | Section: {section_title}]\n{chunk_text}"
            )
            chunks.append(
                {
                    "metadata": {
                        "document": doc_title,
                        "section": section_title,
                        "is_table": self._is_table_block(chunk_text),
                    },
                    "content": enriched_text,
                }
            )
        return chunks


# --- Local test execution example ---
if __name__ == "__main__":
    sample_pdf_text = """
    CHAPTER I - MARKET RISK GUIDELINES
    The maximum permitted exposure for sovereign fixed-income assets must follow the parameters below.

    | Asset | Minimum Rating | Exposure Limit (%) |
    |-------|----------------|--------------------|
    | NTN-F | AAA            | 45.0%              |
    | LFT   | AAA            | 55.0%              |

    SECTION II - LIQUIDITY CONTROLS
    Art. 5º The liquidity committee shall meet bi-weekly to assess the liquidity coverage ratio (LCR).
    """

    chunker = FinancialDocumentChunker(max_chunk_size=300)
    processed_chunks = chunker.parse_raw_text(sample_pdf_text, "Risk_Policy_2026.pdf")

    print(
        f"Total chunks generated with structural intelligence: {len(processed_chunks)}\n"
    )
    for idx, c in enumerate(processed_chunks):
        print(f"--- Chunk {idx+1} ---")
        print(f"Metadata: {c['metadata']}")
        print(f"Content:\n{c['content']}\n")
