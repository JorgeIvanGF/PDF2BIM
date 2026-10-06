from __future__ import annotations

import hashlib
import tempfile
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from app.domain.documents import DocumentMetadata, DocumentPreflight


@dataclass(frozen=True)
class StoredDocument:
    metadata: DocumentMetadata
    path: Path
    sha256: str


class DocumentStore:
    def __init__(self) -> None:
        self._root = Path(tempfile.mkdtemp(prefix="pdf2bim-"))
        self._documents: dict[str, StoredDocument] = {}

    def save(
        self,
        *,
        filename: str,
        content_type: str,
        data: bytes,
        preflight: DocumentPreflight,
    ) -> StoredDocument:
        document_id = uuid4().hex
        path = self._root / f"{document_id}.pdf"
        path.write_bytes(data)
        sha256 = hashlib.sha256(data).hexdigest()
        metadata = DocumentMetadata(
            document_id=document_id,
            filename=filename,
            content_type=content_type,
            size_bytes=len(data),
            preflight=preflight,
        )
        stored = StoredDocument(metadata=metadata, path=path, sha256=sha256)
        self._documents[document_id] = stored
        return stored

    def get(self, document_id: str) -> StoredDocument | None:
        return self._documents.get(document_id)


store = DocumentStore()
