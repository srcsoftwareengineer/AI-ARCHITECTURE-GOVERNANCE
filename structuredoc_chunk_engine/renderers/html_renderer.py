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

import html
from structuredoc_chunk_engine.core.interfaces import IAuditRenderer
from structuredoc_chunk_engine.core.models import ParsedTable


class HtmlAuditRenderer(IAuditRenderer):
    def render(self, table: ParsedTable, output_path: str) -> None:
        headers_html = "".join([f"<th>{html.escape(h)}</th>" for h in table.headers])

        rows_html = []
        for row in table.rows:
            if row.sub_itens:
                sub_rows = []
                for idx, item in enumerate(row.sub_itens):
                    if idx == 0:
                        sub_rows.append(
                            f"  <tr>\n"
                            f'    <td rowspan="{len(row.sub_itens)}">{html.escape(row.codigo)}</td>\n'
                            f'    <td rowspan="{len(row.sub_itens)}">{html.escape(row.registro)}</td>\n'
                            f'    <td rowspan="{len(row.sub_itens)}">{html.escape(row.tipo_cobranca_grupo or "")}</td>\n'
                            f"    <td>{html.escape(item.tipo_cobranca)}</td>\n"
                            f"    <td>{html.escape(item.presenca)}</td>\n"
                            f"  </tr>"
                        )
                    else:
                        sub_rows.append(
                            f"  <tr>\n"
                            f"    <td>{html.escape(item.tipo_cobranca)}</td>\n"
                            f"    <td>{html.escape(item.presenca)}</td>\n"
                            f"  </tr>"
                        )
                rows_html.extend(sub_rows)
            else:
                rows_html.append(
                    f"  <tr>\n"
                    f"    <td>{html.escape(row.codigo)}</td>\n"
                    f"    <td>{html.escape(row.registro)}</td>\n"
                    f'    <td colspan="2">{html.escape(row.tipo_cobranca or "")}</td>\n'
                    f'    <td>{html.escape(row.presenca or "")}</td>\n'
                    f"  </tr>"
                )

        table_body = "\n".join(rows_html)

        html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>HITL Audit Preview - {table.title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 30px; background-color: #f8f9fa; }}
        h2 {{ color: #0d6efd; }}
        table {{ border-collapse: collapse; width: 100%; background: #fff; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-radius: 6px; overflow: hidden; }}
        th, td {{ border: 1px solid #dee2e6; padding: 14px; text-align: left; vertical-align: top; }}
        th {{ background-color: #212529; color: #fff; }}
        tr:nth-child(even) {{ background-color: #f8f9fa; }}
        .badge {{ background: #198754; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8em; }}
    </style>
</head>
<body>
    <h2>StructuraDoc Engine <span class="badge">HITL Audit v1.2.1 SSOT Corrected</span></h2>
    <h3>Documento: {html.escape(table.title)}</h3>
    <table>
        <thead>
            <tr>{headers_html}</tr>
        </thead>
        <tbody>{table_body}
        </tbody>
    </table>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
