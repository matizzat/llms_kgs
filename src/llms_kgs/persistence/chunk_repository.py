from llms_kgs.persistence.connection_provider import ConnectionProvider
from llms_kgs.persistence.database_error import DatabaseError
from llms_kgs.core_utils import log_error 
from llms_kgs.domain import Chunk
from typing import List

import numpy as np

class ChunkRepository:

    def _handle_exception(self, method: str, e: Exception):
        log_error('ChunkRepository', method, e) 
        raise DatabaseError(f"{method} failed: {e}") from e

    def __init__(self, connection_provider: ConnectionProvider):
        self._connection_provider = connection_provider

    def insert(self, chunk: Chunk):
        try:
       
            with self._connection_provider as conn:
                with conn.cursor() as cur:

                    cur.execute("""
                        INSERT INTO chunks
                        (chunk_title, chunk_text, chunk_embedding)
                        VALUES (%s, %s, %s)
                    """, [chunk.title, chunk.text, chunk.embedding]) 
            
                conn.commit()
        
        except Exception as e:
            self._handle_exception("insert", e)
   
    def exists_by_title(self, title: str) -> bool:
        try:
            result = True 
            with self._connection_provider as conn:
                with conn.cursor() as cur:
               
                    cur.execute("""
                        SELECT chunk_id
                        FROM chunks
                        WHERE chunk_title = %s
                    """, [title])
               
                    row = cur.fetchone()

                if row is None:
                    result = False 

            return result 
                
        except Exception as e:
            self._handle_exception("exists_by_title", e)

    def retrieve_titles(self) -> List[str]:

        try:
    
            with self._connection_provider as conn:        
                with conn.cursor() as cur:

                    cur.execute("""SELECT chunk_title FROM chunks""")
                    rows = [row[0] for row in cur.fetchall()]

            return rows

        except Exception as e:
            self._handle_exception("retrieve_titles", e)

    def retrieve_all(self) -> List[Chunk]:

        try:

            with self._connection_provider as conn:
                with conn.cursor() as cur:

                    cur.execute("""
                        SELECT chunk_id, chunk_title, chunk_text, chunk_embedding
                        FROM chunks""")

                    rows = cur.fetchall()

            return [Chunk(chunk_id = r[0], title = r[1],
                     text = r[2], embedding = r[3]) for r in rows]

        except Exception as e:
            self._handle_exception("retrieve_all", e)

    def retrieve_by_title(self, title: str) -> Chunk | None:
        try:

            with self._connection_provider as conn:        
                with conn.cursor() as cur:
                    
                    cur.execute("""
                        SELECT chunk_id, chunk_title, chunk_text, chunk_embedding
                        FROM chunks
                        WHERE chunk_title = %s
                    """, [title])
                    r = cur.fetchone()
          
            if r is None:
                return None

            return Chunk(chunk_id = r[0], title = r[1],
                         text = r[2], embedding = r[3])
                    
        except Exception as e:
            self._handle_exception("retrieve_by_title", e)

    def retrieve_by_similarity(self, embedding: np.ndarray, k_neighbors: int) -> List[Chunk]:
        try:
            
            with self._connection_provider as conn:        
                with conn.cursor() as cur:
                    
                    cur.execute("""
                        SELECT chunk_id, chunk_title, chunk_text, chunk_embedding
                        FROM chunks
                        ORDER BY chunk_embedding <=> %s LIMIT %s
                    """, [embedding, k_neighbors])
                    
                    rows = cur.fetchall()

            return  [Chunk(chunk_id = r[0], title = r[1],
                     text = r[2], embedding = r[3]) for r in rows] 

        except Exception as e:
            self._handle_exception("retrieve_by_similarity", e)

    def delete_by_title(self, title: str):
        try:

            with self._connection_provider as conn:        
                with conn.cursor() as cur:
                    
                    cur.execute("""
                        DELETE FROM inferences WHERE chunk_id = (
                        SELECT chunk_id FROM chunks WHERE chunk_title = %s)
                    """, [title])
                    
                    cur.execute("""
                        DELETE FROM chunks WHERE chunk_title = %s
                    """, [title])

                conn.commit()

        except Exception as e:
            self._handle_exception("delete_by_title", e)
