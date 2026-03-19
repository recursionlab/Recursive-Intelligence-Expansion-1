# Meta-Inverse Debug Prompts (15 new, 2 per category)
Applied DSRP/ΞKernel meta to absences ('not there'): Distinctions in gaps, Systems from voids, Relations inverse, Perspectives counterfactual. Vector collapse to singularity prompts.

**1. Lint Gaps (Absence: Uncovered code)**
- Meta-inverse: Scan dead/unreachable code (vulture), distinguish 'never-exec' from essential voids.
- Collapse: Generate 'shadow tests' for removed features (git blame).

**2. Dep Shadows (Absence: Ghost deps)**
- Meta-inverse: pipdeptree orphans, relate unused to vulns.
- Collapse: Simulate dep failure (mock missing pkg).

**3. Runtime Silences (Absence: Silent fails)**
- Meta-inverse: Log-absent paths (strace), distinguish logged/unlogged.
- Collapse: Inject silent-crash (os._exit random).

**4. Schema Void (Absence: Missing constraints)**
- Meta-inverse: Null-permissive cols, relate to injection vectors.
- Collapse: Fuzz NULL/empty DB inserts.

**5. Test Blindspots (Absence: Unmocked externals)**
- Meta-inverse: Dependency inversion (unmocked Redis/LLM), counterfactual mocks.
- Collapse: Chaos monkey external calls.

**6. Load Breaking (Absence: Scale cliffs)**
- Meta-inverse: Locust ramp to OOM, distinguish steady/collapse.
- Collapse: Resource exhaustion repro (ulimit).

**7. Unicode Ghosts (Absence: Hidden chars)**
- Meta-inverse: Hexdump files for BOM/zero-width, relate to parse fails.
- Collapse: Input adversarial unicode crash LLM.

**8. E2E Shadows (Absence: UI-DB drift)**
- Meta-inverse: Playwright snapshot diffs, counterfactual UI states.
- Collapse: Race-condition script (multi-tab).

**9. Memory Phantoms (Absence: Leak detectors off)**
- Meta-inverse: Objgraph cycles in GIL, distinguish retained/gc.
- Collapse: Long-run no-GC sim.

**10. Fuzz Singularity (Absence: Edge universe)**
- Meta-inverse: Hypothesis strategies from schema voids.
- Collapse: Genetic fuzz to segfault.
