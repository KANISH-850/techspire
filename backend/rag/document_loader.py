import os
import logging
from typing import List, Dict, Any
import pypdf

logger = logging.getLogger(__name__)

class DocumentLoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def load_documents(self) -> List[Dict[str, Any]]:
        """
        Loads all supported documents from the data directory.
        Returns a list of dicts with 'text' and 'metadata'.
        """
        documents = []
        if not os.path.exists(self.data_dir):
            logger.warning(f"Data directory {self.data_dir} does not exist.")
            return documents

        for filename in os.listdir(self.data_dir):
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.isfile(filepath):
                continue
            
            try:
                if filename.lower().endswith(".txt"):
                    docs = self._load_txt(filepath, filename)
                    documents.extend(docs)
                elif filename.lower().endswith(".pdf"):
                    docs = self._load_pdf(filepath, filename)
                    documents.extend(docs)
                else:
                    logger.info(f"Skipping unsupported file type: {filename}")
            except Exception as e:
                logger.error(f"Error loading {filename}: {e}")
                
        return documents

    def _load_txt(self, filepath: str, filename: str) -> List[Dict[str, Any]]:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
            
        return [{
            "text": text,
            "metadata": {
                "source": filename,
                "type": "txt"
            }
        }]

    def _load_pdf(self, filepath: str, filename: str) -> List[Dict[str, Any]]:
        documents = []
        with open(filepath, "rb") as f:
            reader = pypdf.PdfReader(f)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    documents.append({
                        "text": text,
                        "metadata": {
                            "source": filename,
                            "type": "pdf",
                            "page": i + 1
                        }
                    })
        return documents
