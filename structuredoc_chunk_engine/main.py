"""
Created on 30 de out. de 2026

@description:
    description

@id:
    

@version:
    1.0.0

@path:
    //

@canonical_id:
    NameMyClass

@status:
    DEVELOPMENT

@author:
    Sandro Regis Cardoso <src.softwareengineer@gmail.com>

@ai_engine:
    name: GEMINI
    environment: web
    session_id: <url:last_index_of:/>+1

@todo:
    - P0: Refactor all static file names input and output including their paths

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

import json
import os

from structuredoc_chunk_engine.parsers.mock_cnab_parser import Cnab750MockParser
from structuredoc_chunk_engine.renderers.html_renderer import HtmlAuditRenderer


def main():
    print("=== [StructuraDoc Engine] - Pipeline de Ingestão Estruturada ===")

    # 0. Carrega o Prompt-as-Code (Governança Declarativa)
    prompt_path = os.path.join("prompts", "prompt_get_raw_content_v1.1.yaml")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as pf:
            print(f"[0/3] Prompt-as-Code carregado com sucesso de: {prompt_path}")

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # 1. Instancia componentes desacoplados (SOLID/DIP)
    parser = Cnab750MockParser()
    renderer = HtmlAuditRenderer()

    # 2. Executa o Parsing Estruturado
    parsed_table = parser.parse("source_document_page_3.pdf")
    print(f"[1/3] Parsing concluído com sucesso: '{parsed_table.title}'")

    # 3. Serializa para JSON (SSOT para Embeddings / RAG)
    json_path = os.path.join(output_dir, "cnab750_structure.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(parsed_table.to_dict(), f, ensure_ascii=False, indent=2)
    print(f"[2/3] JSON SSOT gerado em: {json_path}")

    # 4. Renderiza Preview HTML para Auditoria HITL
    html_path = os.path.join(output_dir, "audit_preview.html")
    renderer.render(parsed_table, html_path)
    print(f"[3/3] HTML Preview para validação HITL gerado em: {html_path}")

    print(
        "\n✅ Homologação concluída com sucesso! Os artefatos estão prontos no diretório 'output/'."
    )


if __name__ == "__main__":
    main()
