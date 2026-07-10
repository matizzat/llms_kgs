from .connection_provider import ConnectionProvider
from .database_error import DatabaseError
from llms_kgs.domain import Triple, CMap
from llms_kgs.core_utils import log_error
from typing import List
import numpy as np

class CMapRetriever:

    _query_retrieve_cmap = """
        SELECT cmap_id, cmap_title, cmap_focus_question, cmap_embedding
        FROM concept_maps
        WHERE cmap_title = %s
    """

    _query_retrieve_knowledge_triples = """
        SELECT c1.concept_label,
               r.relation_label,
               c2.concept_label,
               ts.kt_embedding
        FROM knowledge_triples AS ts
        JOIN concepts AS c1 ON c1.concept_id = ts.kt_source_id
        JOIN concepts AS c2 ON c2.concept_id = ts.kt_target_id
        JOIN relations AS r ON r.relation_id = ts.kt_relation_id
        WHERE ts.kt_cmap_id = %s
    """

    _query_retrieve_similar = """
        SELECT cmap_id, cmap_title, cmap_focus_question, cmap_embedding
        FROM concept_maps
        ORDER BY cmap_embedding <=> %s
        LIMIT %s
    """

    _query_exists_by_title = """
        SELECT 1 FROM concept_maps
        WHERE cmap_title = %s
    """

    _query_retrieve_titles = """
        SELECT cmap_title FROM concept_maps
    """

    def __init__(self, connection_provider: ConnectionProvider):
        self._connection_provider = connection_provider

    def _handle_exception(self, method_name: str, e: Exception):
        log_error('CMapRetriever', method_name, e=e)
        raise DatabaseError(f"{method_name} failed: {e}") from e

    def retrieve_by_title(self, title: str) -> CMap | None:
        try:
            with self._connection_provider as conn:
                with conn.cursor() as cur:

                    cur.execute(self._query_retrieve_cmap, [title])
                    r = cur.fetchone()

                    if r is None:
                        return None

                    cmap = CMap(cmap_id = r[0], title = r[1],
                                focus_question = r[2], embedding = r[3])

                    cur.execute(self._query_retrieve_knowledge_triples, [cmap.id])
                    cmap.triples = [Triple(source=r[0], relation=r[1], target=r[2], embedding = r[3])
                                    for r in cur.fetchall()] 

            return cmap

        except Exception as e:
            self._handle_exception("retrieve_by_title", e)

    def exists_by_title(self, title: str) -> bool:
        try:
            with self._connection_provider as conn:
                with conn.cursor() as cur:
                   
                    cur.execute(self._query_exists_by_title, [title])
                    return cur.fetchone() is not None

        except Exception as e:
            self._handle_exception("exists_by_title", e)

    def retrieve_by_similarity(self, embedding: np.ndarray, k_neighbors: int) -> List[CMap]:
        try:
            with self._connection_provider as conn:
                with conn.cursor() as cur:

                    cur.execute(self._query_retrieve_similar, [embedding, k_neighbors])
                    rows = cur.fetchall()

                    cmaps = [CMap(cmap_id = r[0], title = r[1],
                             focus_question = r[2], embedding = r[3]) for r in rows]

                    for cmap in cmaps:
                        cur.execute(self._query_retrieve_knowledge_triples, [cmap.id])
                        cmap.triples = [Triple(source=r[0], relation=r[1], target=r[2], embedding = r[3])
                                    for r in cur.fetchall()]

            return cmaps

        except Exception as e:
            self._handle_exception("retrieve_by_similarity", e)

    def retrieve_titles(self) -> List[str]:
        try:
            with self._connection_provider as conn:
                with conn.cursor() as cur:
     
                    cur.execute(self._query_retrieve_titles)
                    return [row[0] for row in cur.fetchall()]

        except Exception as e:
            self._handle_exception("retrieve_titles", e)

