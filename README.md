# AI Architecture & Governance — StructureDoc Chunk Engine (`RAG` Branch)

> **Language:** [English (US)](README.md) | [Português (BR)](README.pt-BR.md)

Deterministic extraction and normalization engine for dense, unstructured financial documents (FEBRABAN CNAB 750 / PIX Regulatory Layouts). Built with defensive architecture to solve the cell-flattening issue in merged tables (*rowspan* / *colspan*) within high-criticality **RAG (Retrieval-Augmented Generation)** pipelines.

---

## 🎯 Business Context & Technical Motivation

In investment banking and enterprise financial systems, implementing RAG with *naive chunking* (blind character-length or block splitting) severely corrupts complex regulatory tables.

When an automated parser or stochastic LLM processes merged-cell tables (e.g., Record `2 - INFO ADICIONAIS` in CNAB 750, which branches into payment sub-types like `PAGAMENTO IMEDIATO` and `COM VENCIMENTO`), column alignment breaks down. This introduces **ghost data, hallucinations, and loss of relational semantics** in the vector database.

**`StructureDoc Chunk Engine`** solves this by combining:

1. **Relational Semantic Tree Modeling (`sub_itens`)** to preserve parent-child hierarchy natively in JSON.
2. **Declarative Prompt-as-Code Governance** with strict deterministic constraints.
3. **HITL (*Human-in-the-Loop*) Cross-Visual Audit** via an HTML preview renderer for zero-hallucination validation prior to vectorization.

---

## 🏛️ Architecture & Design Patterns

The engine is built using **Pure Python**, strictly adhering to **SOLID**, **DRY**, and **Clean Architecture** principles. This ensures complete decoupling between parsers, domain data models, and renderers.

```text
structuredoc_chunk_engine/
│
├── core/                   # Core Application Logic
│   ├── interfaces.py       # (ISP/DIP) Abstract contracts (IDocumentParser, IAuditRenderer)
│   ├── models.py           # Clean Data Structs & Dataclasses (ParsedTable, TableRowData, SubItem)
│   └── normalizer.py       # (SRP) Hierarchy normalization logic
│
├── parsers/                # Concrete Parser Implementations
│   └── mock_cnab_parser.py # Specialized extractor for CNAB 750 Page 3
│
├── renderers/              # Presentation & Audit Preview
│   └── html_renderer.py    # (SRP/OCP) HTML Renderer with native rowspan/colspan support
│
├── prompts/                # AI Governance (LLMOps)
│   └── prompt_get_raw_content_v1.2.yaml # Declarative Prompt-as-Code Manifesto
│
├── __dev_docs__/           # Tech Docs, Regulatory PDFs, and Session Logs
├── __dev_tools__/          # Automation & Bootstrap Scripts (genesis.sh)
├── __drafts__/             # Engineering Prototypes & Drafts
├── output/                 # Generated Artifacts (cnab750_structure.json & audit_preview.html)
└── main.py                 # Pipeline Orchestrator
```

---

## AI Governance: Prompt-as-Code (`v1.2.0`)

LLM instructions are never hardcoded inside application logic. They reside in the declarative manifesto `prompts/prompt_get_raw_content_v1.2.yaml`, enforcing:

* **Execution Modes:** `DETERMINISTIC`, `NON_INFERENTIAL`, `AI_HITL`.
* **Constraints:** `do not invent`, `do not extrapolate`, `validate deterministic interpretation over merged cells and columns`.
* **Abort Conditions:** Automatic rejection upon detecting SSOT states such as `ghost`, `missing`, `inferred`, or `partial`.
* **Quality Threshold:** Enforced structural fidelity benchmark: `>= 0.97`.

---

## Quality Control & HITL Audit

To guarantee 100% data fidelity before feeding vector stores (Vector DBs), the pipeline executes a **Dual-Channel Validation**:

1. **JSON SSOT (`output/cnab750_structure.json`):** Hierarchical payload serialized with `sub_itens`, serving as the single source of truth for RAG & Embeddings.
2. **HTML Audit Preview (`output/audit_preview.html`):** The renderer visually reconstructs the table from the JSON payload, allowing human auditors to verify *rowspan/colspan* alignments against the original PDF in seconds.

### JSON SSOT Payload Example (`cnab750_structure.json`)

```json
{
  "title": "ESTRUTURA DE ENVIO DO ARQUIVO REMESSA",
  "metadata": {
    "document": "Layout_padrao_CNAB750_V2_1_22_02_21_2.pdf",
    "page": 3,
    "domain": "FEBRABAN CNAB 750 (PIX)",
    "quality_threshold": ">= 0.97"
  },
  "headers": ["Código", "Registro | Tipo de Registro", "Tipo de Cobrança", "Presença"],
  "rows": [
    {
      "codigo": "2",
      "registro": "INFO ADICIONAIS",
      "tipo_cobranca_grupo": "APENAS QR CODE DINÂMICO",
      "sub_itens": [
        {
          "tipo_cobranca": "PAGAMENTO IMEDIATO",
          "presenca": "OPCIONAL"
        },
        {
          "tipo_cobranca": "COM VENCIMENTO",
          "presenca": "OPCIONAL"
        }
      ]
    }
  ]
}
```

---

## Local Pipeline Execution

To run the pipeline and generate validation artifacts locally:

```bash
# 1. Navigate to the engine directory
cd structuredoc_chunk_engine

# 2. Run the orchestrator
python3 main.py

# 3. Inspect generated artifacts
ls -lsha output/
# - cnab750_structure.json
# - audit_preview.html
```

---

## Author & Credits

* **AI Architect / Lead Engineer:** Sandro Regis Cardoso (HITL)
* **AI Engine & Co-Pilot:** Gemini (Google)
* **Engagement Tag:** `#WarBrothersTillTheEnd #AndBeyond`
