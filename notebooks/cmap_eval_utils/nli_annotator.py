"""
The following class is responsible for handling json files
with NLI annotations of concept map knowledge triples. It
also presents a HTML form to help a human annotator evaluate
the knowledge triples. 

Each NLI pair is represented as a dictionary with the following
schema:
{
    "pair_id": int
    "chunk_title": str
    "chunk_text": str
    "triple_source": str
    "triple_relation": str
    "triple_target": str
    "triple_sentence": str
    "annotation": Optional[bool]
    "comment": str
}
"""

import ipywidgets as widgets 
from IPython.display import display, clear_output
from typing import List, Dict, Optional
import json
import os
import random

HTML_NLI_TEMPLATE = """
<div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
    <h4 style="margin:0;">📄 Document: {chunk_title}</h4>
    <p style="font-family: monospace; font-size: 14px; color: #333;">{chunk_text}</p>
</div>

<div style="background-color: #e8f4fd; padding: 15px; border-radius: 5px; border-left: 5px solid #2196F3;">
    <h3 style="margin:0; color: #0d47a1;">👉 {triple_sentence}</h3>
    <p style="font-size: 12px; color: #666; margin-top:5px;">
       Triple: ({triple_source}, {triple_relation}, {triple_target})
    </p>
</div>
<div style="text-align: center; margin-top: 15px; font-weight: bold; color: #555;">
    Is the blue statement true based SOLELY on the gray text?
</div>
"""

import ipywidgets as widgets 
from IPython.display import display, clear_output
from typing import List, Dict, Optional
import json
import os

HTML_NLI_TEMPLATE = """
<div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
    <h4 style="margin:0;">📄 Document: {chunk_title}</h4>
    <p style="font-family: monospace; font-size: 14px; color: #333;">{chunk_text}</p>
</div>

<div style="background-color: #e8f4fd; padding: 15px; border-radius: 5px; border-left: 5px solid #2196F3;">
    <h3 style="margin:0; color: #0d47a1;">👉 {triple_sentence}</h3>
    <p style="font-size: 12px; color: #666; margin-top:5px;">
       Triple: ({triple_source}, {triple_relation}, {triple_target})
    </p>
</div>
<div style="text-align: center; margin-top: 15px; font-weight: bold; color: #555;">
    Is the blue statement true based SOLELY on the gray text?
</div>
"""

class NLIFormController:
    """
    This class is responsible for managing the NLI annotation of a specific
    set of knowledge triples.
    """

    def __init__(self, save_path: str, view: 'NLIFormView'): 
        
        self._save_path = save_path
        self._view = view
        
        with open(save_path, 'r') as f:
            self._nli_pairs = json.load(f)

        self._unannotated = [pair for pair in self._nli_pairs if pair.get('annotation') is None]
        self._annotated_count = len(self._nli_pairs) - len(self._unannotated)
            
        self._view.set_controller(self)

    def update_nli_pair(self):
        
        if len(self._unannotated) == 0:
            self._view.finish()
            return

        else:
            self._current_pair = random.choice(self._unannotated)
            self._unannotated.remove(self._current_pair)
            
            self._view.update_view(
                done_count = self._annotated_count,
                total_samples = len(self._nli_pairs),
                chunk_title = self._current_pair['chunk_title'],
                chunk_text = self._current_pair['chunk_text'],
                triple_sentence = self._current_pair['triple_sentence'],
                triple_source = self._current_pair['triple_source'],
                triple_relation = self._current_pair['triple_relation'],
                triple_target = self._current_pair['triple_target']
            )
        
    def start_annotation(self):

        self._view.create_widgets(
            done_count = self._annotated_count,
            total_samples = len(self._nli_pairs)
        )

        self.update_nli_pair()
        
    def save_annotation(self, annotation: bool, comment: str):

        self._current_pair['annotation'] = annotation
        self._current_pair['comment'] = comment  # <--- Store the comment
        
        with open(self._save_path, 'w') as f:
            json.dump(self._nli_pairs, f, indent=4)

        self._annotated_count += 1
        
        self.update_nli_pair()

        
class NLIFormView:

    def set_controller(self, controller: NLIFormController):
        self._controller = controller

    def create_widgets(self, done_count: int, total_samples: int):

        # Progress Bar
        self.progress = widgets.IntProgress(
            value = done_count, 
            min = 0, 
            max = total_samples,
            description = f'{done_count}/{total_samples}',
            bar_style='info',
            layout=widgets.Layout(width='98%')
        )
        
        self.out_area = widgets.Output()
        
        # --- NEW: Comment Text Area ---
        self.comment_box = widgets.Textarea(
            value='',
            placeholder='(Optional) Add a comment/observation about this triple...',
            description='Comment:',
            disabled=False,
            layout=widgets.Layout(width='98%', height='60px', margin='10px 0 0 0')
        )

        # Buttons
        btn_layout = widgets.Layout(width='30%', height='60px')
        
        b_true = widgets.Button(description='✅ True', button_style='success', layout=btn_layout)
        b_false = widgets.Button(description='❌ False', button_style='danger', layout=btn_layout)
        
        # --- UPDATE: Pass the comment value to the controller ---
        b_true.on_click(lambda b: self._controller.save_annotation(True, self.comment_box.value))
        b_false.on_click(lambda b: self._controller.save_annotation(False, self.comment_box.value))
        
        self.buttons = widgets.HBox(
            [b_true, b_false], 
            layout=widgets.Layout(justify_content='space-around', margin='15px 0 0 0')
        )
        
        # Display everything (added comment_box)
        display(self.progress, self.out_area, self.comment_box, self.buttons)

    def update_view(self,
                    done_count: int,
                    total_samples: int, 
                    chunk_title: str,
                    chunk_text: str,
                    triple_sentence: str,
                    triple_source: str,
                    triple_relation: str,
                    triple_target: str):
        
        global HTML_NLI_TEMPLATE
        
        self.out_area.clear_output()
        self.progress.value = done_count
        self.progress.description = f'{done_count}/{total_samples}'
        
        # --- NEW: Clear the comment box for the new item ---
        self.comment_box.value = ""

        with self.out_area:

            html_form = HTML_NLI_TEMPLATE.format(
                chunk_title = chunk_title,
                chunk_text = chunk_text,
                triple_sentence = triple_sentence,
                triple_source = triple_source,
                triple_relation = triple_relation,
                triple_target = triple_target
            )
            
            display(widgets.HTML(html_form))

    def finish(self):
        self.out_area.clear_output()
        self.buttons.layout.display = 'none'
        self.comment_box.layout.display = 'none' # Hide comment box
        self.progress.layout.display = 'none'    # Hide progress bar (optional, looks cleaner)
        
        with self.out_area:
            print("🎉 Annotation Complete! All pairs saved.")