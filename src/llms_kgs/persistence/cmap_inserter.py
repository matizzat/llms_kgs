from .connection_provider import ConnectionProvider
from .database_error import DatabaseError
from llms_kgs.core_utils import log_error
from llms_kgs.domain import CMap, Chunk
import numpy as np

class CMapInserter:

    _query_insert_attributes = """
        INSERT into concept_maps (cmap_title, cmap_focus_question, cmap_embedding)
        VALUES (%s, %s, %s)
        RETURNING cmap_id
    """

    _query_insert_concept = """
        WITH inserted_row AS (
            INSERT INTO concepts (concept_label)
            VALUES (%s)
            ON CONFLICT DO NOTHING
            RETURNING concept_id
        )
        SELECT concept_id 
        FROM inserted_row
        UNION 
            SELECT concept_id
            FROM concepts 
            WHERE concept_label = %s
    """
    
    _query_insert_relation = """
        WITH inserted_row AS (
            INSERT INTO relations (relation_label)
            VALUES (%s)
            ON CONFLICT DO NOTHING
            RETURNING relation_id
        )
        SELECT relation_id
        FROM inserted_row
        UNION 
            SELECT relation_id
            FROM relations
            WHERE relation_label = %s
    """

    _query_insert_knowledge_triple = """
        INSERT INTO knowledge_triples 
        (kt_cmap_id, kt_source_id, kt_target_id, kt_relation_id, kt_embedding)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING kt_id        
    """

    _query_insert_inference = """
        INSERT INTO inferences (chunk_id, kt_id)
        VALUES (%s, %s);
    """
    
    def _handle_exception(self, method_name: str, e: Exception):
        log_error("CMapInserter", method_name, e=e)
        raise DatabaseError(f"{method_name} failed: {e}") from e

    def __init__(self, connection_provider: ConnectionProvider):
        self._connection_provider = connection_provider

    def insert(self, cmap: CMap, chunk: Chunk | None = None):
        try:
            with self._connection_provider as conn:
                with conn.cursor() as cur:
                    
                    cur.execute(self._query_insert_attributes,
                            [cmap.title, cmap.focus_question, cmap.embedding])
                    cmap_id = cur.fetchone()[0] 

                    for tr in cmap.triples: 
                        cur.execute(self._query_insert_concept, [tr.source.label, tr.source.label]) 
                        s_id = cur.fetchone()[0]

                        cur.execute(self._query_insert_concept, [tr.target.label, tr.target.label]) 
                        t_id = cur.fetchone()[0]
                        
                        cur.execute(self._query_insert_relation, [tr.relation.label, tr.relation.label]) 
                        r_id = cur.fetchone()[0]

                        cur.execute(self._query_insert_knowledge_triple,
                                [cmap_id, s_id, t_id, r_id, tr.embedding])
                        kt_id = cur.fetchone()[0]

                        if(chunk != None):
                            cur.execute(self._query_insert_inference, [chunk.id, kt_id])

                conn.commit()

        except Exception as e:
            self._handle_exception('insert', e) 
