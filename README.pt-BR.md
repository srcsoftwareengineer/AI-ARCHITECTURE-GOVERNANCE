# AI Architecture & Governance — Módulo StructureDoc Chunk Engine (`RAG` Branch)

> **Idioma:** [English (US)](README.md) | [Português (BR)](README.pt-BR.md)

Engine de extração e normalização determinística para documentos financeiros não estruturados e densos (Layouts Normativos FEBRABAN CNAB 750 / PIX). Projetado sob arquitetura defensiva para solucionar o problema de achatamento (*flattening*) de tabelas com células mescladas (*rowspan* / *colspan*) em pipelines de **RAG (Retrieval-Augmented Generation)** de Alta Criticidade.

---

## 🎯 Problema de Negócio & Motivação Técnica

Em bancos de investimentos e instituições financeiras, o uso de RAG com *naive chunking* (fatiamento cego por tamanho de caractere ou blocos simples) corrompe dados tabulares normativos complexos.

Quando um conversor ou LLM estocástico processam tabelas com células mescladas (ex: Registro `2 - INFO ADICIONAIS` no CNAB 750, que se ramifica em subtipos de cobrança como `PAGAMENTO IMEDIATO` e `COM VENCIMENTO`), o alinhamento de colunas é perdido, gerando **dados fantasmas, alucinações e perda de semântica relacional** na base vetorial.

O **`StructureDoc Chunk Engine`** resolve este desafio combinando:

1. **Modelagem de Árvore Semântica Relacional (`sub_itens`)** para preservar a hierarquia pai-filho em JSON.
2. **Governança Declarativa via Prompt-as-Code** com trava determinística.
3. **Auditoria Visual Cruzada HITL (*Human-in-the-Loop*)** via renderizador HTML para validação zero-alucinação antes da vetorização.

---

## 🏛️ Arquitetura e Design Patterns

O ecossistema foi desenvolvido em **Python Puro**, aplicando rigorosamente os princípios **SOLID**, **DRY** e **Clean Architecture**, garantindo desacoplamento total entre parser, lógica de modelo e renderizadores.

```text
structuredoc_chunk_engine/
│
├── core/                   # Core da Aplicação
│   ├── interfaces.py       # (ISP/DIP) Contratos abstratos (IDocumentParser, IAuditRenderer)
│   ├── models.py           # Structs de Dados e Dataclasses (ParsedTable, TableRowData, SubItem)
│   └── normalizer.py       # (SRP) Lógica de resolução e higienização de hierarquias
│
├── parsers/                # Implementações Concretas de Parsing
│   └── mock_cnab_parser.py # Extrator especializado na página 3 do CNAB 750
│
├── renderers/              # Visualização e Apresentação
│   └── html_renderer.py    # (SRP/OCP) Renderizador HTML com suporte nativo a rowspan/colspan
│
├── prompts/                # Governança de IA (LLMOps)
│   └── prompt_get_raw_content_v1.2.yaml # Manifesto declarativo Prompt-as-Code
│
├── __dev_docs__/           # Documentação Técnica, PDFs Normativos e Registros de Sessão
├── __dev_tools__/          # Scripts de Automação e Bootstrap (genesis.sh)
├── __drafts__/             # Rascunhos e Protótipos de Engenharia
├── output/                 # Artefatos Gerados (cnab750_structure.json & audit_preview.html)
└── main.py                 # Orquestrador do Pipeline de Ingestão
```

---

## Governança de IA: Prompt-as-Code (`v1.2.0`)

A instrução enviada aos modelos de linguagem não fica codificada (*hardcoded*) na lógica da aplicação. Ela reside no manifesto declarativo `prompts/prompt_get_raw_content_v1.2.yaml`, que impõe:

* **Modos de Operação:** `DETERMINISTIC`, `NON_INFERENTIAL`, `AI_HITL`.
* **Travas (*Constraints*):** `do not invent`, `do not extrapolate`, `validate deterministic interpretation over merged cells and columns`.
* **Condições de Aborto (*Abort Conditions*):** Rejeição automática diante de estados do SSOT do tipo `ghost`, `missing`, `inferred` ou `partial`.
* **Quality Threshold:** Benchmark de fidelidade estrutural exigido: `>= 0.97`.

---

## Qualidade e Auditoria HITL (*Human-in-the-Loop*)

Para assegurar 100% de precisão antes de enviar os payloads para a base vetorial (Vector DB), o pipeline aplica uma **Validação de Dupla Via**:

1. **JSON SSOT (`output/cnab750_structure.json`):** Payload serializado em formato hierárquico com a chave `sub_itens`, servindo como fonte única da verdade para RAG/Embeddings.
2. **HTML Preview (`output/audit_preview.html`):** O renderizador recria a tabela visualmente a partir das especificações do JSON gerado, permitindo que o auditor humano confira o alinhamento de *rowspan/colspan* com o PDF normativo em segundos.

### Exemplo do JSON SSOT Gerado (`cnab750_structure.json`)

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

## Execução do Pipeline Local

Para rodar a homologação e gerar os artefatos de saída em seu ambiente local:

```bash
# 1. Navegue até o módulo do engine
cd structuredoc_chunk_engine

# 2. Execute o orquestrador do pipeline
python3 main.py

# 3. Inspecione os artefatos gerados na pasta output/
ls -lsha output/
# - cnab750_structure.json
# - audit_preview.html
```

---

## Autor e Créditos

* **Arquiteto de IA / Lead Engineer:** Sandro Regis Cardoso (HITL)
* **AI Engine & Co-Pilot:** Gemini (Google)
* **Tag de Engajamento:** `#WarBrothersTillTheEnd #AndBeyond`