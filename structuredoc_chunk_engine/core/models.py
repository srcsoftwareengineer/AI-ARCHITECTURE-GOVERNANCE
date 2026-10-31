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

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class SubItem:
    tipo_cobranca: str
    presenca: str

    def to_dict(self) -> Dict[str, Any]:
        return {"tipo_cobranca": self.tipo_cobranca, "presenca": self.presenca}


@dataclass
class TableRowData:
    codigo: str
    registro: str
    tipo_cobranca_grupo: Optional[
        str
    ] = None  # Para células mescladas como "APENAS QR CODE DINÂMICO"
    tipo_cobranca: Optional[str] = None  # Para linhas normais
    presenca: Optional[str] = None
    sub_itens: Optional[List[SubItem]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "codigo": self.codigo,
            "registro": self.registro,
        }
        if self.sub_itens:
            d["tipo_cobranca_grupo"] = self.tipo_cobranca_grupo
            d["sub_itens"] = [item.to_dict() for item in self.sub_itens]
        else:
            d["tipo_cobranca"] = self.tipo_cobranca
            d["presenca"] = self.presenca
        return d


@dataclass
class ParsedTable:
    title: str
    headers: List[str]
    rows: List[TableRowData]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "metadata": self.metadata,
            "headers": self.headers,
            "rows": [row.to_dict() for row in self.rows],
        }
