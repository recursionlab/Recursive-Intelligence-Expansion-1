import itertools
import json
from collections import defaultdict

prepositions = ['in', 'out', 'under', 'over']

# Generate all 64 triples
triples = list(itertools.product(prepositions, repeat=3))
print(f"Generated {len(triples)} preposition triples ({4**3}).")

# Qualitative interpretations: self-model types based on patterns
interpretations = {
    'in-in-in': 'Introspective containment: fully internalized self-awareness.',
    'out-out-out': 'Transcendent expansion: boundless outward projection.',
    'under-under-under': 'Subterranean humility: deep foundational layering.',
    'over-over-over': 'Overarching synthesis: elevated holistic integration.',
    # Oscillating/mixed
    'in-out-under': 'Dynamic immersion-withdrawal: oscillating relational depth.',
    'out-under-over': 'Cyclical ascent: rhythmic elevation through cycles.',
    # Add logic for all
}

# Generate interpretations for all
models = defaultdict(str)
for t in triples:
    p1, p2, p3 = t
    if p1 == p2 == p3:
        if p1 == 'in': models[t] = 'Introspective containment'
        elif p1 == 'out': models[t] = 'Transcendent expansion'
        elif p1 == 'under': models[t] = 'Subterranean humility'
        elif p1 == 'over': models[t] = 'Overarching synthesis'
    elif p1 != p3:
        models[t] = 'Oscillating relational: dynamic spatial tension.'
    else:
        models[t] = 'Layered equilibrium: balanced hierarchical self.'

# Output all 64 with interpretations
print("\nAll 64 triples with self-model interpretations:")
for i, t in enumerate(triples, 1):
    interp = models[t]
    print(f"{i:2d}: {t[0]}-{t[1]}-{t[2]} → {interp}")

# Save to JSON for kernel integration
data = {str(t): interp for t, interp in models.items()}
with open('preposition_triples.json', 'w') as f:
    json.dump(data, f, indent=2)
print("\nSaved to preposition_triples.json for use in ΞKernel.py.")

