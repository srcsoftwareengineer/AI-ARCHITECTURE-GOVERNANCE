"""
Created on Oct 28, 2026

@description:
    Enterprise Financial Document Preprocessor (Structure-Aware Chunking)
    Low-level structural chunker designed for complex financial and regulatory PDFs
    with absolute table atomicity guard to prevent mid-table slicing.

@id:
    financial_document_chunker.py

@version:
    1.2.0

@path:
    structuredoc_chunk_engine/__drafts__/financial_document_chunker.py

@canonical_id:
    FINANCIAL_DOCUMENT_CHUNKER

@status:
    TESTED AND HOMOLOGATED

@author:
    Sandro Regis Cardoso <src.softwareengineer@gmail.com>

@ai_engine:
    name: GEMINI version 3
    environment: web
    session_id: 315fdd4378f66716 <not paid>

@refactor:
    Implemented Table Atomicity Guard to prevent splitting markdown/tabular blocks across chunks.
"""

import re
from typing import List, Dict, Any


class FinancialDocumentChunker:
    """
    Processes and chunks dense financial documents respecting semantic boundaries
    and enforcing absolute table atomicity.
    """

    def __init__(self, max_chunk_size: int = 300):
        self.max_chunk_size = max_chunk_size

    def parse_raw_text(
        self, raw_text: str, document_title: str
    ) -> List[Dict[str, Any]]:
        """
        Splits the document based on regulatory/structural markers and preserves
        tabular blocks as indivisible atomic units.
        """
        chunks = []

        # Clean structural section pattern matching (preventing trailing ordinal characters)
        section_pattern = re.compile(r"(?i)(CHAPTER\s+\d+|SECTION\s+\d+|Art\.\s*\d+º?)")
        splits = section_pattern.split(raw_text)

        current_header = "Introduction / General"
        current_body = ""

        if len(splits) > 1:
            if splits[0].strip():
                chunks.extend(
                    self._create_atomic_chunks(
                        splits[0], document_title, current_header
                    )
                )

            for i in range(1, len(splits), 2):
                current_header = splits[i].strip()
                current_body = splits[i + 1] if (i + 1) < len(splits) else ""

                atomic_chunks = self._create_atomic_chunks(
                    current_body, document_title, current_header
                )
                chunks.extend(atomic_chunks)
        else:
            chunks.extend(
                self._create_atomic_chunks(raw_text, document_title, "General")
            )

        return chunks

    def _is_table_line(self, line: str) -> bool:
        """
        Identifies if a single line belongs to a markdown or tabular structure.
        """
        stripped = line.strip()
        return stripped.startswith("|") and stripped.endswith("|")

    def _create_atomic_chunks(
        self, text: str, doc_title: str, section_title: str
    ) -> List[Dict[str, Any]]:
        """
        Enforces Table Atomicity Guard: prohibits chunk splits while inside a tabular block.
        """
        chunks = []
        lines = text.strip().split("\n")

        current_chunk_lines = []
        current_length = 0
        inside_table = False

        for line in lines:
            line_len = len(line)
            is_table_row = self._is_table_line(line)

            # Update table boundary state
            if is_table_row:
                inside_table = True

            # Condition to flush chunk: size limit reached AND we are NOT inside a table
            if (
                current_length + line_len > self.max_chunk_size
                and current_chunk_lines
                and not inside_table
            ):
                chunk_text = "\n".join(current_chunk_lines)
                enriched_text = (
                    f"[Doc: {doc_title} | Section: {section_title}]\n{chunk_text}"
                )

                chunks.append(
                    {
                        "metadata": {
                            "document": doc_title,
                            "section": section_title,
                            "is_table": any(
                                self._is_table_line(l) for l in current_chunk_lines
                            ),
                        },
                        "content": enriched_text,
                    }
                )

                current_chunk_lines = []
                current_length = 0

            current_chunk_lines.append(line)
            current_length += line_len

            # If we were inside a table and hit a non-table line or end of sequence, close table block state
            if inside_table and not is_table_row and line.strip() == "":
                inside_table = False

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
                        "is_table": any(
                            self._is_table_line(l) for l in current_chunk_lines
                        ),
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
