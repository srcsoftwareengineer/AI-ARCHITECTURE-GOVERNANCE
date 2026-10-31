"""
Created on 30 de out. de 2026

@description:
    <description>

@id:
    interfaces.py

@version:
    1.0.0

@path:
    structuredoc_chunk_engine/core/interfaces.py

@canonical_id:
    INTERFACES

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


from abc import ABC, abstractmethod
from typing import Any
from structuredoc_chunk_engine.core.models import ParsedTable


class IDocumentParser(ABC):
    @abstractmethod
    def parse(self, source: Any) -> ParsedTable:
        pass


class IAuditRenderer(ABC):
    @abstractmethod
    def render(self, table: ParsedTable, output_path: str) -> None:
        pass
