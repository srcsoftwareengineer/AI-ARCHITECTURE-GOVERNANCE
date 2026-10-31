# Changelog

All notable changes to the **StructureDoc Chunk Engine** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Language Translations:** [English (US)](CHANGELOG.md) | [Português (BR)](CHANGELOG.pt-BR.md)

## \[1.2.1\] - 2026-10-28

### Fixed

* **Visual Alignment & Layout Correction (Record 2):** Resolved column inversion detected during HITL visual audit. Properly separated the grouping column `tipo_cobranca_grupo` ("APENAS QR CODE DINÂMICO") from child sub-rows (`PAGAMENTO IMEDIATO` and `COM VENCIMENTO`), restoring exact fidelity to the FEBRABAN CNAB 750 regulatory specification.

* Updated dataclasses in `core/models.py` and HTML rendering logic in `renderers/html_renderer.py` to support dynamic `rowspan` handling for merged grouping columns.

## \[1.2.0\] - 2026-10-27

### Added

* **Hierarchical Prompt-as-Code Modeling (`sub_itens`):** Upgraded YAML manifesto (`prompt_get_raw_content_v1.2.yaml`) to enforce parent/child tree mapping over merged cells, preventing stochastic flattening of 2D matrices in RAG pipelines.

* Schema support for nested compound objects in JSON output for Records 2 and 3.

## \[1.1.0\] - 2026-10-27

### Added

* **Deterministic Attention Gates:** Introduced strict execution rules in YAML manifesto (`constraints` and `rules`) focused on merged cell interpretation (`rowspan`/`colspan`).

* **Enterprise Quality Threshold:** Established benchmark quality gate (`quality_threshold: >= 0.97`) with expected embedding quality metrics against SSOT.

## \[1.0.0\] - 2026-10-27

### Added

* **Clean Architecture & SOLID Core:** Initial bootstrap featuring decoupled interface contracts (`IDocumentParser`, `IAuditRenderer`) adhering to DIP and SRP.

* **Low-Level Parsing Engine:** Clean data structs (`core/models.py`) for atomic representation of table cells and rows.

* **Visual HITL Audit Renderer:** Created HTML renderer (`renderers/html_renderer.py`) capable of converting SSOT JSON payloads back into formatted tables for human verification prior to vector database ingestion.

* **Declarative Governance (Prompt-as-Code):** Initial YAML manifesto version for deterministic data extraction from CNAB 750 Page 3.