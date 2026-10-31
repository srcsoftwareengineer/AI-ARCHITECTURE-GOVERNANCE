#!/usr/bin/env python3
"""
Created on Oct 29, 2026

@description:
    Structured JSON Lines Logger (jsonl_logger.py) - Draft with Self-Validation Unit Test
    Provides append-only, schema-compliant structured event logging for
    parsing turns, chunk metrics, and governance audit trails.

@id:
    JSONL_LOGGER_ENGINE

@version:
    1.0.0

@path:
    structuredoc_chunk_engine/__drafts__/jsonl_logger.py

@canonical_id:
    JSONL_LOGGER

@status:
    DRAFT (PENDING EMPIRICAL VALIDATION)

@author:
    Sandro Regis Cardoso <src.softwareengineer@gmail.com>

@ai_engine:
    name: GEMINI
    session_id: fe4950b8807286c4 <not paid>

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
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional


class StructuredJSONLLogger:
    """
    Append-only JSON Lines logger for structured audit telemetry.
    """

    def __init__(self, log_file_path: Path, session_id: Optional[str] = None):
        self.log_file_path = log_file_path
        self.session_id = session_id or "UNTRACKED_ORCHESTRATOR_MISSING"

        # Garante que o diretório de destino exista
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)

    def log_event(self, event_type: str, payload: Dict[str, Any], status: str = "SUCCESS") -> None:
        """
        Appends a structured JSON line containing telemetry, session context, and UTC timestamp.
        """
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "event_type": event_type,
            "status": status,
            "payload": payload
        }

        try:
            with open(self.log_file_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"[FATAL] Failed to write JSONL log entry: {e}")


if __name__ == "__main__":
    print("==================================================")
    print("  AI ARCHITECTURE GOVERNANCE - JSONL LOGGER TEST  ")
    print("==================================================")

    # Configuração do teste unitário na sandbox
    test_session_id = "fe4950b8807286c4"
    test_log_path = Path(__file__).resolve().parents[1] / "output" / f"execution_{test_session_id}_audit.jsonl"

    # Limpa log anterior de teste se existir para garantir ambiente limpo
    if test_log_path.exists():
        test_log_path.unlink()

    logger = StructuredJSONLLogger(test_log_path, session_id=test_session_id)

    # Simula eventos do pipeline RAG
    logger.log_event(
        event_type="CHUNK_EXTRACTION_STARTED",
        payload={"target_file": "Layout_padrao_CNAB750_V2_1_22_02_21_2.pdf", "engine": "Table Atomicity Guard v1.2.0"},
        status="INFO"
    )

    logger.log_event(
        event_type="CHUNK_TABLE_GUARD_VERIFIED",
        payload={"tables_detected": 4, "atomicity_preserved": True},
        status="SUCCESS"
    )

    print(f"[*] Eventos gravados com sucesso em: {test_log_path}")
    print(f"[*] Iniciando leitura de validação (Read-back & Schema Assert)...")

    # Validação Empírica (Read-back)
    assert test_log_path.exists(), "ERRO CRÍTICO: O arquivo .jsonl não foi gerado!"

    lines = test_log_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2, f"ERRO CRÍTICO: Esperado 2 linhas, encontrado {len(lines)}"

    for idx, line in enumerate(lines, 1):
        parsed = json.loads(line) # Garante que cada linha é um JSON válido
        assert "timestamp" in parsed, f"Linha {idx} sem timestamp"
        assert parsed["session_id"] == test_session_id, f"Linha {idx} com session_id incorreto"
        assert "event_type" in parsed, f"Linha {idx} sem event_type"
        assert "payload" in parsed, f"Linha {idx} sem payload"
        print(f"  [OK] Linha {idx} validada: Evento -> {parsed['event_type']} | Status -> {parsed['status']}")

    print("==================================================")
    print(" [SUCCESS] Teste unitário concluído! O output .jsonl passou em todas as asserções.")
    print("==================================================")
