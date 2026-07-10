from .connection_provider import ConnectionProvider
from .database_error import DatabaseError
from llms_kgs.core_utils import log_error

class CMapDeleter:

    _query_retrieve_cmap_id = """
        SELECT cmap_id FROM concept_maps WHERE cmap_title = %s
    """

    _query_delete_inferences = """
        DELETE FROM inferences
        WHERE kt_id IN (
            SELECT kt_id FROM knowledge_triples WHERE kt_cmap_id = %s
        )
    """

    _query_delete_knowledge_triples = """
        DELETE FROM knowledge_triples
        WHERE kt_cmap_id = %s
        RETURNING kt_source_id, kt_target_id, kt_relation_id
    """

    _query_delete_concept = """
        DELETE FROM concepts
        WHERE concept_id = %s
          AND NOT EXISTS (
                SELECT 1
                FROM knowledge_triples
                WHERE kt_source_id = %s
                   OR kt_target_id = %s
          )
    """

    _query_delete_relation = """
        DELETE FROM relations
        WHERE relation_id = %s
          AND NOT EXISTS (
                SELECT 1
                FROM knowledge_triples
                WHERE kt_relation_id = %s
          )
    """

    _query_delete_cmap = """
        DELETE FROM concept_maps WHERE cmap_id = %s
    """

    def _handle_exception(self, method_name: str, e: Exception):
        log_error("CMapDeleter", method_name, e=e)
        raise DatabaseError(f"{method_name} failed: {e}") from e

    def __init__(self, connection_provider: ConnectionProvider):
        self._connection_provider = connection_provider

    def delete_by_title(self, title: str):
        try:
            with self._connection_provider as conn:
                with conn.cursor() as cur:

                    cur.execute(self._query_retrieve_cmap_id, [title])
                    row = cur.fetchone()
                    if not row:
                        return
                    
                    cmap_id = row[0]

                    cur.execute(self._query_delete_inferences, [cmap_id])

                    cur.execute(self._query_delete_knowledge_triples, [cmap_id])
                    orphan_triples = cur.fetchall()

                    for source_id, target_id, relation_id in orphan_triples:
                        cur.execute(self._query_delete_concept,
                                    [source_id, source_id, source_id])
                        cur.execute(self._query_delete_concept,
                                    [target_id, target_id, target_id])
                        cur.execute(self._query_delete_relation,
                                    [relation_id, relation_id])

                    cur.execute(self._query_delete_cmap, [cmap_id])

                conn.commit()

        except Exception as e:
            self._handle_exception("delete_by_title", e)

