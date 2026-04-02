import pytest

from app.config import Config
from app.modules.engine.service import RagEngine

# def test_document_loader():
#     config_service = Config()
#     engine = RagEngine(
#         config_service,
#         collection_name="integration_test"
#     )

#     docs = engine.load_document("https://lilianweng.github.io/posts/2023-06-23-agent/")

#     assert len(docs) > 0

# def test_retrieve_content():
#     config_service = Config()
#     engine = RagEngine(
#         config_service,
#         collection_name="integration_test"
#     )
#     engine.load_document("https://lilianweng.github.io/posts/2023-06-23-agent/")
#     serialized, retrieved_docs = engine.retrieve_content("What is Task Decomposition?")

#     assert len(retrieved_docs) > 0
#     assert len(serialized) > 0
#     assert all(doc.page_content for doc in retrieved_docs)

def test_enrich_retrieved_content():
    config_service = Config()
    engine = RagEngine(
        config_service,
        collection_name="integration_test"
    )
    engine.load_document("https://lilianweng.github.io/posts/2023-06-23-agent/")
    content = engine.enrich_retrieved_content("What is Task Decomposition?")

    assert len(content) > 0
