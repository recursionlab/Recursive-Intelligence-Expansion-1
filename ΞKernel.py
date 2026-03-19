#!/usr/bin/env python3
\"\"\"Test preposition triples integration in ΞKernel.\"\"\"

import sys
sys.path.append('.')

from ΞKernel import XiKernel
import json

kernel = XiKernel()

print("1. Generate triples:")
triples = kernel.generate_triples()
print(f"Loaded {len(triples)} annotated triples.")

print("\n2. Sample triple specs:")
for t, interp in triples[:3]:
    spec = {
        "Seed": t[0], "Mask": t[1], "Ritual": t[2],
        "TripleInterp": interp, "Type": "Sample"
    }
    print(spec)

print("\n3. Run triples test loop (3 cycles):")
kernel.test_triples_loop(cycles=3)

print("\n4. Check library update (prepositions loaded):")
preps = kernel.library["MetaLibrary"].get("Prepositions", [])
print(f"Prepositions: {preps}")

print("\\nTriples test complete. Full integration ready.")

