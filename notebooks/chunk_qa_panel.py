from llms_kgs.logic.chunk_qa import ChunkQAResult
from IPython.display import HTML, display
import html

def render_qa_result(result: ChunkQAResult):
    """
    Visualizes a ChunkQAResult object in HTML format using a 2-column layout.
    Left col: Answer + Evidence. Right col: Retrieved Chunks.
    """
    
    # 1. CSS Styling (Updated for 2-Column Layout)
    styles = """
    <style>
        .qa-dashboard { 
            font-family: 'Segoe UI', sans-serif; 
            max-width: 1200px; /* Increased width for 2 cols */
            margin: 0 auto; 
            color: #333; 
            display: grid;
            grid-template-columns: 40% 1fr; /* 40% Left, Rest Right */
            gap: 24px;
            align-items: start;
        }
        
        .qa-column {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }

        .qa-section { 
            border: 1px solid #e0e0e0; 
            border-radius: 8px; 
            overflow: hidden; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.05); 
            background-color: #fff;
        }
        
        .qa-header { 
            background-color: #f7f9fc; 
            padding: 12px 16px; 
            border-bottom: 1px solid #e0e0e0; 
            font-weight: 600; 
            color: #4a5568; 
            display: flex; 
            justify-content: space-between; 
            align-items: center;
        }
        
        .qa-body { padding: 16px; }
        
        /* Final Answer Styles */
        .answer-box { font-size: 1.05em; line-height: 1.6; color: #2d3748; }
        .no-answer { color: #e53e3e; font-style: italic; }
        
        /* Chunk Styles */
        .chunk-grid { 
            display: flex; 
            flex-direction: column; 
            gap: 16px; 
        }
        .chunk-card { border: 1px solid #edf2f7; border-radius: 6px; background: #fff; }
        .chunk-title { background: #edf2f7; padding: 8px 12px; font-size: 0.85em; font-weight: bold; color: #718096; }
        .chunk-text { padding: 12px; font-size: 0.9em; line-height: 1.5; white-space: pre-wrap; color: #4a5568; }
        
        /* Highlighting */
        .highlight { background-color: #fefcbf; color: #744210; padding: 2px 0; border-radius: 2px; border-bottom: 2px solid #ecc94b; font-weight: 500; }
        
        /* Passage List Styles */
        .passage-list { list-style: none; padding: 0; margin: 0; }
        .passage-item { padding: 8px; border-bottom: 1px solid #edf2f7; font-size: 0.9em; display: flex; gap: 10px; flex-direction: column; }
        .passage-item:last-child { border-bottom: none; }
        .badge { background: #e2e8f0; color: #4a5568; padding: 2px 6px; border-radius: 4px; font-size: 0.75em; font-weight: bold; width: fit-content;}
        
        /* Error Box */
        .error-box { grid-column: 1 / -1; background: #fff5f5; border: 1px solid #feb2b2; padding: 10px; border-radius: 6px; margin-bottom: 10px; color: #c53030; }
    </style>
    """

    # 2. Logic to Prepare Data
    if not result.reader_result:
        final_answer_html = "<div class='no-answer'>No answer generated.</div>"
        passages_list_html = "<div class='no-answer'>No passages extracted.</div>"
        passages_map = {}
    else:
        # Final Answer
        final_answer_html = f"<div class='answer-box'>{html.escape(result.reader_result.final_answer)}</div>"
        
        # Organize passages
        passages_map = {}
        passage_list_items = []
        
        for p in result.reader_result.passages:
            if p.chunk_number not in passages_map:
                passages_map[p.chunk_number] = []
            passages_map[p.chunk_number].append(p.text)
            
            passage_list_items.append(
                f"<li class='passage-item'><span class='badge'>Chunk {p.chunk_number}</span> <span>{html.escape(p.text)}</span></li>"
            )
        
        passages_list_html = f"<ul class='passage-list'>{''.join(passage_list_items)}</ul>" if passage_list_items else "<em>No specific evidence extracted.</em>"

    # 3. Process Chunks
    chunks_html = []
    for i, chunk in enumerate(result.retrieved_chunks):
        safe_text = html.escape(chunk.text.strip())
        
        if i in passages_map:
            texts_to_highlight = sorted(passages_map[i], key=len, reverse=True)
            for text_snippet in texts_to_highlight:
                escaped_snippet = html.escape(text_snippet)
                safe_text = safe_text.replace(
                    escaped_snippet, 
                    f'<span class="highlight">{escaped_snippet}</span>'
                )
        
        chunks_html.append(f"""
            <div class="chunk-card">
                <div class="chunk-title">Chunk {i}</div>
                <div class="chunk-text">{safe_text}</div>
            </div>
        """)
    
    chunks_grid_html = f"<div class='chunk-grid'>{''.join(chunks_html)}</div>" if chunks_html else "<em>No chunks retrieved.</em>"

    # 4. Notifications/Errors
    errors_html = ""
    if result.notification.has_errors():
         errors_html = f"""
         <div class="error-box">
            <strong>Errors:</strong> {', '.join(result.notification.get_errors())}
         </div>
         """

    # 5. Assemble Dashboard (New 2-Column Structure)
    dashboard_html = f"""
    <div class="qa-dashboard">
        {styles}
        {errors_html}
        
        <div class="qa-column">
            <div class="qa-section">
                <div class="qa-header"><span>🤖 Generated Answer</span></div>
                <div class="qa-body">
                    {final_answer_html}
                </div>
            </div>

            <div class="qa-section">
                <div class="qa-header"><span>🔍 Extracted Evidence</span></div>
                <div class="qa-body">
                    {passages_list_html}
                </div>
            </div>
        </div>

        <div class="qa-column">
            <div class="qa-section">
                <div class="qa-header"><span>📚 Retrieved Context</span></div>
                <div class="qa-body">
                    {chunks_grid_html}
                </div>
            </div>
        </div>
    </div>
    """

    return HTML(dashboard_html)