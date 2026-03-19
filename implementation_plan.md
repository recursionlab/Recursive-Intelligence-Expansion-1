# Implementation Plan

**Overview**  
Fix ΞKernel.py with mathematical rigor: replace random/heuristic autopoiesis with graph theory (networkx triples graph), fixed-point convergence (adjacency delta<epsilon), deterministic selection (centrality), bounded seeds (hash mod), safe parsing. Transform heuristic recursion to rigorous iteration until graph stabilization. Preserves autopoiesis as bounded graph update, adds SymbolGraph metrics to Meta-Library.json. Enables ethical recursive expansion without unbounded growth.

Improves codebase by eliminating eval/random/string hacks, adding convergence guarantees, graph serialization. High-level: triples->DiGraph, wolf_call=centrality novelty, loop until Δadj<0.01, hash uniqueness.

**Types**  
Extend XiKernel with self.graph: nx.DiGraph.  
results: Dict[str, Any] add 'convergence_delta': float, 'laplacian_eig': List[float].  
spec: Dict add 'centrality_score': float.  
No new classes/enums.

**Files**  
New: None.  
Modified:  
- ΞKernel.py: Imports (nx/np/ast), generate_triples (return G/specs), wolf_call (centrality), loop (graph iter/delta), _save_graph helper.  
- test_xikernel.py: test_generate_triples (G assert), test_triples_loop (delta<1.0).  
- TODO.md: Complete.  
- Meta-Library.json: Already SymbolGraph/TripleGraph.

**Functions**  
New (ΞKernel.py):  
- _save_graph(self, G: nx.DiGraph) -> bool: Serialize nx.to_dict_of_dicts to library SymbolGraph.  
Modified:  
- generate_triples: Build G (add_edge Seed->Mask->Ritual w/attr), ast.literal_eval, return G/specs.  
- _weighted_wolf_call(spec, G): nx.betweenness_centrality mean-normalized score >0.5 -> novel.  
- test_triples_loop: Unpack G,triples; centrality spec=max(path score); hash seed %100; graph update add_edge(feedback); adj_delta = np.linalg.norm(new-old,'fro'); save_graph; assert delta in results.  
- _save_library: Call _save_graph before dump.

**Classes**  
XiKernel: Add self.graph_cache = None; init load TripleGraph if exist nx.from_dict; loop use self.graph = G; _load/_save handle graph.

**Dependencies**  
networkx>=3.0, numpy>=1.24 (venv).

**Testing**  
pytest test_xikernel.py: Pass graph nodes>4, delta present <1.0 (small cycles), json_valid, growth>=0. New test_convergence: kernel.test_triples_loop(2), assert results['convergence_delta']<0.1.

**Implementation Order**  
1. Add _save_graph serializes nx.to_dict_of_dicts(G) to SymbolGraph, load nx.from_dict_of_dicts.  
2. Update generate_triples cache if library TripleGraph exist.  
3. wolf_call already good.  
4. Loop: while delta > 0.01 and cycles<max: select spec=max centrality, update G add_edge, recompute delta.  
5. Tests assert delta<tol.  
6. Update TODO complete. venv\Scripts\activate && pytest.
