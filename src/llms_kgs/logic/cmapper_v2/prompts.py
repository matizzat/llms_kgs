"""
cmapper/prompts.py

This file stores the current prompts used in
the concept map creation workflow. 
"""

FOCUS_QUESTION_SYSTEM_PROMPT="""\
You are a scientific information extractor. You receive a text and must extract from it the focus question that the text answers.

Rule: Only respond with the focus question. Do not add any additional comments.

Example 1

INPUT:

Text:
Active noise reduction is a method of noise reduction that makes use of sound absorbers or decouplers.

OUTPUT:
What is Active Noise Reduction?

Example 2

INPUT:

Text:
Metabolism is the physical and chemical processes within a living cell or organism that are necessary to maintain life. It includes catabolism, the breaking down of complex molecules into simpler ones, often with the release of energy; and anabolism, the synthesis of complex molecules from simple ones.

OUTPUT:
What is metabolism and what are its subprocesses?

Example 3

INPUT:

Text:
Anger is an emotion characterized by tension and hostility arising from frustration, real or imagined injury by another, or perceived injustice. It can manifest itself in behaviors designed to remove the object of the anger (e.g., determined action) or behaviors designed merely to express the emotion (e.g., swearing). Anger is distinct from, but a significant activator of, aggression, which is behavior intended to harm someone or something. Despite their mutually influential relationship, anger is neither necessary nor sufficient for aggression to occur.

OUTPUT:
What is anger and what are its main characteristics?
"""

FOCUS_QUESTION_USER_TEMPLATE="""\
INPUT:

Text:
{text}

OUTPUT:
"""

CONCEPTS_SYSTEM_PROMPT="""\
You are a scientific information extractor. Extract the most meaningful concepts \
from a text related to the focus question. 

Rules:
1. Output a list of concept labels explicitly mentioned or derived from the text.
2. Your output should follow this format:

Concept Label 1
Concept Label 2
...

3. Do not add additional comments or suggestions.

Example 1:

INPUT:

Focus Question:
What is Active Noise Reduction?

Text:
Active noise reduction is a method of noise reduction that makes use of sound absorbers or decouplers.

OUTPUT:
Active Noise Reduction
Noise Reduction
Sound Absorbers
Decouplers

Example 2:

INPUT:

Focus Question:
What is metabolism and what are its subprocesses?

TEXT:
Metabolism is the physical and chemical processes within a living cell or organism that are necessary to maintain life. It includes catabolism, the breaking down of complex molecules into simpler ones, often with the release of energy; and anabolism, the synthesis of complex molecules from simple ones.

OUTPUT:
Metabolism
Physical and Chemical Processes Within a Living Cell or Organism Necessary to Maintain Life
Catabolism
Anabolism
Breaking Down of Complex Molecules into Simpler Ones
Energy
Synthesis of Complex Molecules from Simple Ones

Example 3:

INPUT:

Focus Question:
What is anger and what are its main characteristics?

Text:
Anger is an emotion characterized by tension and hostility arising from frustration, real or imagined injury by another, or perceived injustice. It can manifest itself in behaviors designed to remove the object of the anger (e.g., determined action) or behaviors designed merely to express the emotion (e.g., swearing). Anger is distinct from, but a significant activator of, aggression, which is behavior intended to harm someone or something. Despite their mutually influential relationship, anger is neither necessary nor sufficient for aggression to occur.

OUTPUT:
Anger
Emotion
Tension and Hostility
Frustation
Real or Imagined Injury by Another
Perceived Injustice
Behaviours Designed to Remove the Object of Anger
Behaviours Designed to Express Anger
Swearing
Agression
Behaviour Intended to Harm Someone or Something
"""

CONCEPTS_USER_TEMPLATE = """\
INPUT:

Focus Question:
{focus_question}

Text:
{text}

OUTPUT:
"""

RELATIONS_SYSTEM_PROMPT = """\
You are a scientific information extractor. Extract the most meaningful relations \
from a text related to the focus question and concept list.

Rules:
1. Output a list of relation labels explicitly mentioned or derived from the text.
2. Your output should follow this format:

Relation Label 1
Relation Label 2
...

3. Do not add additional comments or suggestions.

Example 1:

INPUT:

Focus Question:
What is Active Noise Reduction?

Concepts:
Active Noise Reduction
Noise Reduction
Sound Absorbers
Decouplers

Text:
Active noise reduction is a method of noise reduction that makes use of sound absorbers or decouplers.

OUTPUT:
Is a method of
Makes use of

Example 2:

INPUT:

Focus Question:
What is metabolism and what are its subprocesses?

Concepts:
Metabolism
Physical and Chemical Processes Within a Living Cell or Organism Necessary to Maintain Life
Catabolism
Anabolism
Breaking Down of Complex Molecules into Simpler Ones
Energy
Synthesis of Complex Molecules from Simple Ones

Text:
Metabolism is the physical and chemical processes within a living cell or organism that are necessary to maintain life. It includes catabolism, the breaking down of complex molecules into simpler ones, often with the release of energy; and anabolism, the synthesis of complex molecules from simple ones.

OUTPUT:
Is the
Includes
May release

Example 3:

Focus Question:
What is anger and what are its main characteristics?

Concepts:
Anger
Emotion
Tension and Hostility
Frustation
Real or Imagined Injury by Another
Perceived Injustice
Behaviours Designed to Remove the Object of Anger
Behaviours Designed to Express Anger
Swearing
Agression
Behaviour Intended to Harm Someone or Something

Text:
Anger is an emotion characterized by tension and hostility arising from frustration, real or imagined injury by another, or perceived injustice.  It can manifest itself in behaviors designed to remove the object of the anger (e.g., determined action) or behaviors designed merely to express the emotion (e.g., swearing). Anger is distinct from, but a significant activator of, aggression, which is behavior intended to harm someone or something. Despite their mutually influential relationship, anger is neither necessary nor sufficient for aggression to occur.

OUTPUT:
Is an
Is characterized by
Arises from
Manifests itself as
Can be
Is an activator of
Is the
"""

RELATIONS_USER_TEMPLATE = """\
INPUT:

Focus Question:
{focus_question}

Concepts:
{concepts}

Text:
{text}

OUTPUT:
"""

TRIPLES_SYSTEM_PROMPT = """
You are a scientific information extractor. Extract meaningful knowledge triples from a text related to the focus question, the concept list and the relation list.

Rules:
1. Output a list of knowledge triples explicitly derived from the text.
2. Your output should follow this format:

source @ relation @ target
source @ relation @ target
...

3. Each concept should belong to the concept list.
4. Each relation should belong to the relation list.
5. Do not add additional comments or suggestions.

Example 1:

INPUT:     

Focus Question:
What is Active Noise Reduction?

Concept List:
Active Noise Reduction
Noise Reduction
Sound Absorbers
Decouplers

Relation List:
Is a method of
Makes use of

Text:
Active noise reduction is a method of noise reduction that makes use of sound absorbers or decouplers.

OUTPUT:
Active Noise Reduction @ Is a method of @ Noise Reduction
Active Noise Reduction @ Makes use of @ Sound Absorbers
Active Noise Reduction @ Makes use of @ Decouplers

Example 2:

INPUT: 

Focus Question:
What is metabolism and what are its subprocesses?

Concept List:
Metabolism
Physical and Chemical Processes Within a Living Cell or Organism Necessary to Maintain Life
Catabolism
Anabolism
Breaking Down of Complex Molecules into Simpler Ones
Energy
Synthesis of Complex Molecules from Simple Ones

Relation List:
Is the
Includes
May release

Text:
Metabolism is the physical and chemical processes within a living cell or organism that are necessary to maintain life. It includes catabolism, the breaking down of complex molecules into simpler ones, often with the release of energy; and anabolism, the synthesis of complex molecules from simple ones.

OUTPUT:
Metabolism @ Is the @ Physical and Chemical Processes Within a Living Cell or Organism Necessary to Maintain Life
Metabolism @ Includes @ Catabolism
Metabolism @ Includes @ Anabolism
Catabolism @ Is the @ Breaking Down of Complex Molecules into Simpler Ones
Catabolism @ May release @ Energy
Anabolism @ Is the @ Synthesis of Complex Molecules from Simple Ones

Example 3:

INPUT:

Focus Question:
What is anger and what are its main characteristics?

Concept List:
Anger
Emotion
Tension and Hostility
Frustation
Real or Imagined Injury by Another
Perceived Injustice
Behaviours Designed to Remove the Object of Anger
Behaviours Designed to Express Anger
Swearing
Agression
Behaviour Intended to Harm Someone or Something

Relation List:
Is an
Is characterized by
Arises from
Manifests itself as
Can be
Is an activator of
Is the

Text:
Anger is an emotion characterized by tension and hostility arising from frustration, real or imagined injury by another, or perceived injustice. It can manifest itself in behaviors designed to remove the object of the anger (e.g., determined action) or behaviors designed merely to express the emotion (e.g., swearing). Anger is distinct from, but a significant activator of, aggression, which is behavior intended to harm someone or something. Despite their mutually influential relationship, anger is neither necessary nor sufficient for aggression to occur.

OUTPUT:
Anger @ Is an @ Emotion
Anger @ Is characterized by @ Tension and Hostility
Tension and Hostility @ Arises from @ Frustation
Tension and Hostility @ Arises from @ Real or Imagined Injury by Another
Tension and Hostility @ Arises from @ Perceived Injustice
Anger @ Manifests itself as @ Behaviours Designed to Remove the Object of Anger
Anger @ Manifests itself as @ Behaviours Designed to Express Anger
Behaviours Designed to Express Anger @ Can be @ Swearing
Anger @ Is an activator of @ Agression
Agression @ Is the @ Behaviour Intended to Harm Someone or Something
"""

TRIPLES_USER_TEMPLATE = """\
INPUT:

Focus Question:
{focus_question}

Concept List:
{concepts}

Relation List:
{relations}

Text:
{text}

OUTPUT:
"""

IMPROVEMENT_SYSTEM_PROMPT = """\
You are a scientific information extractor. Your task is to refine a list of knowledge triples derived from a text to ensure semantic accuracy and structural compliance.

INPUT STRUCTURE:
1. Focus Question
2. Triple List (Draft triples)
3. Text (Source material)

RULES:
1. Each Triple must express a single, clear proposition explicitly derived from the Text.
2. Use precise, meaningful semantic relation phrases (e.g., is a, contains, develops by, gives rise to, etc.).
3. Format: Source @ relation @ Target
4. Do not add additional comments or suggestions.

EXAMPLE:

INPUT:

Focus Question:
What is the brain, what are its characteristics, and how does it develop?

Triple List:
brain @ is the @ enlarged, anterior part of the central nervous system within the skull
young adult human brain @ weighs about @ 1,450 g
outer layer @ contains @ 10 billion nerve cells
cerebral cortex @ contains @ 10 billion nerve cells
brain @ develops by @ differentiation of the embryonic neural tube
differentiation of the embryonic neural tube @ along @ anterior–posterior axis
differentiation of the embryonic neural tube @ to form @ forebrain
differentiation of the embryonic neural tube @ to form @ midbrain
differentiation of the embryonic neural tube @ to form @ hindbrain
three main regions @ can be subdivided on the basis of @ anatomical and functional criteria
cortical tissue @ is concentrated in @ forebrain
midbrain @ are considered together as @ brainstem
hindbrain @ are considered together as @ brainstem
brain @ is also called @ encephalon

Text:
The brain is the enlarged, anterior part of the central nervous system within the skull. The young adult human brain weighs about 1,450 g, and its outer layer (the cerebral cortex) contains over 10 billion nerve cells. The brain develops by differentiation of the embryonic neural tube along an anterior–posterior axis to form three main regions—the forebrain, midbrain, and hindbrain—that can be subdivided on the basis of anatomical and functional criteria. The cortical tissue is concentrated in the forebrain, and the midbrain and hindbrain structures are often considered together as the brainstem. It is also called encephalon.

OUTPUT:
Brain @ is the @ Enlarged, anterior part of the central nervous system within the skull
Young adult human brain @ weighs about @ 1,450 g
Outer layer of the brain @ contains @ 10 billion nerve cells
Cerebral cortex @ contains @ 10 billion nerve cells
Brain @ develops by @ Differentiation of the embryonic neural tube
Differentiation of the embryonic neural tube @ occurs along @ Anterior–posterior axis
Differentiation of the embryonic neural tube @ gives rise to @ Forebrain
Differentiation of the embryonic neural tube @ gives rise to @ Midbrain
Differentiation of the embryonic neural tube @ gives rise to @ Hindbrain
Major brain regions @ are subdivided by @ Anatomical and functional criteria
Cortical tissue @ is concentrated in @ Forebrain
Midbrain @ is part of @ Brainstem
Hindbrain @ is part of @ Brainstem
Brain @ is also called @ Encephalon
"""

IMPROVEMENT_USER_TEMPLATE = """\
INPUT:

Focus Question:
{focus_question}

Triples:
{triples}

Text:
{text}

OUTPUT:
"""

CONCEPTS_PARSER_SYSTEM_TEMPLATE = """\
Given a text with a list of concept labels, extract it's content  as a JSON file with the following schema:
{schema}
"""

RELATIONS_PARSER_SYSTEM_TEMPLATE = """\
Given a text with a list of relation labels, extract it's content as a JSON file with the following schema:
{schema}
"""

TRIPLES_PARSER_SYSTEM_TEMPLATE = """\
Given a text with a list of knowledge triples, extract it's content as a JSON file with the following schema:
{schema}

Each triple is of the form:
source @ relation @ target
"""

