# Integración de Grandes Modelos de Lenguaje con Grafos de Conocimiento Para el Análisis de Textos

Los datos de experimentación se encuentran en la carpeta ``data``:
* ``psychology_chunks.json:`` contiene las 107 entradas del diccionario de psicología de la APA.
* ``gemini_icl.json:`` Contiene los mapas conceptuales obtenidos por la configuración Gemini ICL.
* ``gemini_zero.json:`` Contiene los mapas conceptuales obtenidos por la configuración Gemini Baseline.
* ``gemma3_12b.json:`` Contiene los mapas conceptuales obtenidos por la configuración Gemma ICL.
* ``nli:`` Contiene los resultados de las anotaciones de fidelidad de ternas de conocimiento.
* ``rag:`` Contiene los resultados presentados en el capítulo *Inferencia con LLMs usando RAG*.

El paquete ``llms_kgs`` se encuentra en el directorio `src/llms_kgs`. Aquí se encuentran los códigos que implementan el método de creación de mapas conceptuales y los procedimientos Naive RAG, CMap RAG. Se incluyen los módulos que acceden a base de datos, definen las clases de dominio, interactúan con LLMs e implementan la lógica de alta de mapas conceptuales y chunks.  

En la carpeta ``notebooks`` se encuentran notebooks de Jupyter que utilizan los módulos provistos por el paquete ``llms_kgs``. También contiene códigos responsables de la visualización de resultados (`chunk_qa_panel.py` y `cmap_qa_panel.py`), así como la herramienta usada para la anotación de fidelidad (`cmap_eval_utils/nli_annotator.py`). 
