from llms_kgs.logic import CMapDrawer
from llms_kgs.logic.cmap_qa import CMapQAResult
from IPython.display import HTML, display
import html
import tempfile
import os

def render_cmap_qa_result(result: CMapQAResult):
    """
    Visualizes a CMapQAResult object in HTML format for Jupyter Notebooks.
    Layout: 2 Columns (Text Left, Pyvis Graph Right).
    """

    # --- 1. Prepare Data ---
    if result.answer:
        final_answer = result.answer.final_answer
        # Get raw extracted triples for the list view
        extracted_triples_data = result.answer.triples 
        # Get domain triples for the graph highlighter
        highlight_triples = result.answer.domain_triples()
    else:
        final_answer = "No answer generated."
        extracted_triples_data = []
        highlight_triples = []

    # --- 2. Generate the Knowledge Graph (Pyvis) using YOUR CMapDrawer ---
    vis_net = CMapDrawer.draw(result.retrieved_cmaps, highlights=highlight_triples)
    
    # Customize visual options for the widget
    vis_net.width = "100%"
    # Altura ajustada para alinear con la columna de texto
    vis_net.height = "610px" 

    # Mantengo tus opciones de física
    vis_net.set_options("""
    var options = {
      "physics": {
        "stabilization": { "enabled": true, "iterations": 100 }
      },
      "edges": {
        "smooth": { "type": "dynamic" }
      }
    }
    """)

    # Generate graph HTML using tempfile pattern
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode='w+') as tmp:
        vis_net.save_graph(tmp.name)
        tmp.seek(0)
        graph_html_content = tmp.read()
    
    # Clean up
    try:
        os.unlink(tmp.name)
    except:
        pass

    # --- 3. Construct Triples List HTML (Table) ---
    triples_rows = ""
    if extracted_triples_data:
        for t in extracted_triples_data:
            # Usamos getattr por seguridad para acceder a labels o strings
            s = getattr(t, 'source', str(t))
            r = getattr(t, 'relation', '')
            o = getattr(t, 'target', '')
            
            triples_rows += f"""
            <tr>
                <td><b>{html.escape(str(s))}</b></td>
                <td class="arrow-cell">&rarr; {html.escape(str(r))} &rarr;</td>
                <td><b>{html.escape(str(o))}</b></td>
            </tr>
            """
        triples_html = f"<table class='triple-table'><thead><tr><th>Source</th><th>Relation</th><th>Target</th></tr></thead><tbody>{triples_rows}</tbody></table>"
    else:
        triples_html = "<div style='padding:10px; color:#666;'><em>No knowledge triples extracted.</em></div>"

    # --- 4. CSS Styling (GRID 2 COLUMNAS) ---
    styles = """
    <style>
        .cmap-dashboard { 
            font-family: 'Segoe UI', Helvetica, sans-serif; 
            max-width: 1400px; margin: 0 auto; color: #333; 
            display: grid; 
            grid-template-columns: 35% 65%; /* 35% Texto, 65% Grafo */
            gap: 20px; 
            align-items: start;
        }
        
        /* Column Containers */
        .left-col { display: flex; flex-direction: column; gap: 20px; }
        .right-col { display: flex; flex-direction: column; }

        /* Cards */
        .cmap-section { 
            background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; 
            overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.05); 
        }
        .cmap-header { 
            background-color: #f7f9fc; padding: 12px 16px; border-bottom: 1px solid #e0e0e0; 
            font-weight: 700; color: #2c5282; text-transform: uppercase; font-size: 0.9em;
        }
        .cmap-body { padding: 16px; background-color: #fff; }
        
        .answer-text { font-size: 1.05em; line-height: 1.6; color: #2d3748; }
        
        /* Triple Table */
        .triple-table { width: 100%; border-collapse: collapse; font-size: 0.85em; }
        .triple-table th { text-align: left; padding: 8px; background: #edf2f7; color: #4a5568; font-weight: 600; }
        .triple-table td { padding: 8px; border-bottom: 1px solid #edf2f7; color: #4a5568; word-wrap: break-word;}
        .triple-table tr:last-child td { border-bottom: none; }
        .arrow-cell { color: #cbd5e0; font-weight: bold; text-align: center; white-space: nowrap; }
        
        /* Legend */
        .legend { font-size: 0.85em; color: #718096; margin-bottom: 5px; display: flex; gap: 15px; }
        .legend-item { display: flex; align-items: center; gap: 6px; }
        .line { width: 20px; height: 3px; display: inline-block; }
    </style>
    """

    # --- 5. Assemble Dashboard ---
    dashboard_html = f"""
    <div class="cmap-dashboard">
        {styles}
        
        <div class="left-col">
            <div class="cmap-section">
                <div class="cmap-header"><span>🤖 Generated Answer</span></div>
                <div class="cmap-body">
                    <div class="answer-text">{html.escape(final_answer)}</div>
                </div>
            </div>
            
            <div class="cmap-section">
                <div class="cmap-header"><span>🔍 EVIDENCE</span></div>
                <div class="cmap-body" style="padding:0;">
                    {triples_html}
                </div>
            </div>
        </div>

        <div class="right-col">
            <div class="cmap-section">
                <div class="cmap-header"><span>🕸️ CONTEXT CMAPS</span></div>
                <div class="cmap-body" style="padding: 0;">
                    <div style="padding: 10px 16px;">
                        <div class="legend">
                            <span class="legend-item"><span class="line" style="background:blue;"></span> Context</span>
                            <span class="legend-item"><span class="line" style="background:red;"></span> Evidence Used</span>
                        </div>
                    </div>
                    <iframe 
                        srcdoc="{html.escape(graph_html_content)}" 
                        style="width: 100%; height: 620px; border: none;" 
                        sandbox="allow-scripts allow-same-origin">
                    </iframe>
                </div>
            </div>
        </div>
    </div>
    """

    return HTML(dashboard_html)