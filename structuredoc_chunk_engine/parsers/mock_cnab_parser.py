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

from structuredoc_chunk_engine.core.interfaces import IDocumentParser
from structuredoc_chunk_engine.core.models import (
    ParsedTable,
    TableRowData,
    TableCell,  # Unresolved import -> Not implemented on models.py
    SubItem,
)


class Cnab750MockParser(IDocumentParser):
    def parse(self, source: str) -> ParsedTable:  # Unused parameter 'source'
        headers = [
            "Código",
            "Registro | Tipo de Registro",
            "Tipo de Cobrança",
            "Presença",
        ]

        rows = [
            TableRowData(
                codigo="0",
                registro="HEADER",
                tipo_cobranca="QR CODE ESTÁTICO E DINÂMICOS",
                presenca="OBRIGATÓRIA",
            ),
            TableRowData(
                codigo="1",
                registro="DETALHE",
                tipo_cobranca="QR CODE ESTÁTICO E DINÂMICOS",
                presenca="OBRIGATÓRIA",
            ),
            # Registro 2 com o agrupamento correto da coluna 'APENAS QR CODE DINÂMICO' e suas duas sublinhas
            TableRowData(
                codigo="2",
                registro="INFO ADICIONAIS",
                tipo_cobranca_grupo="APENAS QR CODE DINÂMICO",
                sub_itens=[
                    SubItem(tipo_cobranca="PAGAMENTO IMEDIATO", presenca="OPCIONAL"),
                    SubItem(tipo_cobranca="COM VENCIMENTO", presenca="OPCIONAL"),
                ],
            ),
            # Registro 3 também possui subdivisão similar no PDF original
            TableRowData(
                codigo="3",
                registro="DADOS ADICIONAIS COBRANÇA COM VENCIMENTO",
                tipo_cobranca_grupo="APENAS QR CODE DINÂMICO",
                sub_itens=[
                    SubItem(
                        tipo_cobranca="COM VENCIMENTO", presenca="OBRIGATÓRIA (EMISSÃO)"
                    )
                ],
            ),
            TableRowData(
                codigo="9",
                registro="TRAILER",
                tipo_cobranca="QR CODE ESTÁTICO E DINÂMICOS",
                presenca="OBRIGATÓRIA",
            ),
        ]

        return ParsedTable(
            title="ESTRUTURA DE ENVIO DO ARQUIVO REMESSA",
            headers=headers,
            rows=rows,
            metadata={
                "document": "Layout_padrao_CNAB750_V2_1_22_02_21_2.pdf",
                "page": 3,
                "domain": "FEBRABAN CNAB 750 (PIX)",
                "quality_threshold": ">= 0.97",
            },
        )
