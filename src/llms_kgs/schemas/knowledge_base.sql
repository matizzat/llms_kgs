CREATE EXTENSION vector;

CREATE TABLE chunks
(
     chunk_id    SERIAL PRIMARY KEY,
     chunk_title VARCHAR UNIQUE,
     chunk_text  VARCHAR,
     chunk_embedding vector(%s)
);

CREATE TABLE concept_maps
(
     cmap_id             SERIAL PRIMARY KEY,
     cmap_title          VARCHAR UNIQUE,
     cmap_focus_question VARCHAR,
     cmap_embedding vector(%s)
);

CREATE TABLE concepts
(
    concept_id    SERIAL PRIMARY KEY,
    concept_label VARCHAR UNIQUE
);

CREATE TABLE relations
(
    relation_id    SERIAL PRIMARY KEY,
    relation_label VARCHAR UNIQUE
);

CREATE TABLE knowledge_triples
(
    kt_id      SERIAL PRIMARY KEY,
    kt_cmap_id     INT REFERENCES concept_maps(cmap_id),
    kt_source_id   INT REFERENCES concepts(concept_id),
    kt_target_id   INT REFERENCES concepts(concept_id),
    kt_relation_id INT REFERENCES relations(relation_id),
    kt_embedding vector(%s)
);

CREATE TABLE inferences
(
	kt_id 	 INT REFERENCES knowledge_triples(kt_id), 
	chunk_id INT REFERENCES chunks(chunk_id),
	
	CONSTRAINT unique_inference UNIQUE (kt_id, chunk_id)
);

