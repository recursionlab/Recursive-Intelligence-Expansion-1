#!/usr/bin/env python3
"""ΞKernel: Recursive Intelligence Expansion core.
Implements XiKernel class for triples integration, wolf_call LLM (OpenRouter), autopoiesis (Seeds append on novel interps).
Backward-compatible: --llm flag for real LLM, deterministic fallback."""

import json
import ast
import networkx as nx
import numpy as np
from typing import List, Dict, Any, Tuple
import os
import argparse
import openai

# Load preposition triples (64)
with open('preposition_triples.json', 'r') as f:
    PREP_TRIPLES = json.load(f)

class XiKernel:
    def __init__(self, library_path: str = 'Meta-Library.json'):
        self.library_path = library_path
        self.library = self._load_library()
        self.history = []
        self._load_config()


    def _load_library(self) -> Dict[str, Any]:
        if os.path.exists(self.library_path):
            with open(self.library_path, 'r') as f:
                lib = json.load(f)
            # Ensure Prepositions
            if 'Prepositions' not in lib.get('MetaLibrary', {}):
                lib['MetaLibrary']['Prepositions'] = list(PREP_TRIPLES.keys())[:10]  # Sample
            return lib
        raise FileNotFoundError(f'{self.library_path} not found')

    def _load_config(self):
        """Load config.json for LLM settings."""
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
            if self.config['llm']['use_llm']:
                self.llm_client = openai.OpenAI(
                    base_url=self.config['llm']['api_base'],
                    api_key=self.config['llm']['api_key'],
                )
                print("LLM client initialized (OpenRouter)")
            else:
                self.llm_client = None
                print("LLM disabled (deterministic mode)")
        except Exception as e:
            print(f"Config load failed, using deterministic mode: {e}")
            self.config = {'llm': {'use_llm': False}}
            self.llm_client = None



            return True
        except Exception as e:
            print(f'Save failed: {e}')
            return False

    def generate_triples(self) -> tuple[nx.DiGraph, List[Dict[str, str]]]:
        G = nx.DiGraph()
        specs = []
        prepositions = set()
        for t_str, interp in PREP_TRIPLES.items():
            t = ast.literal_eval(t_str)  # Safe parse tuple
            prepositions.update(t)
            G.add_edge(t[0], t[1], ritual=t[2], interp=interp)
            G.add_edge(t[1], t[2], seed=t[0], interp=interp)
            spec = {
                'Seed': t[0],
                'Mask': t[1],
                'Ritual': t[2],
                'TripleInterp': interp,
                'Type': 'Triple'
            }
            specs.append(spec)
        G.add_nodes_from(prepositions)
        print(f'Generated graph with {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {len(specs)} specs')
        return G, specs

    def _wolf_call_llm(self, spec: Dict[str, str], G: nx.DiGraph) -> str:
        """Real LLM wolf_call via OpenRouter."""
        centrality = nx.betweenness_centrality(G)
        seed_c = centrality.get(spec['Seed'], 0)
        ritual_c = centrality.get(spec['Ritual'], 0)
        novelty_score = (seed_c + ritual_c) / 2
        
        prompt = f"""Given RCOS triple:
Seed: {spec['Seed']}
Mask: {spec['Mask']} 
Ritual: {spec['Ritual']}
Interpretation: {spec['TripleInterp']}
Centrality novelty score: {novelty_score:.3f}

Propose a novel FluxSeed expansion. Keep concise (1 sentence)."""
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.config['llm']['model'],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            expansion = response.choices[0].message.content.strip()
            print(f"LLM wolf_call (score {novelty_score:.3f}): {expansion[:50]}...")
            return expansion
        except Exception as e:
            print(f"LLM failed ({e}), fallback deterministic")
            return self._weighted_wolf_call_deterministic(spec, G)

    def _weighted_wolf_call_deterministic(self, spec: Dict[str, str], G: nx.DiGraph) -> str:
        """Original deterministic fallback."""
        centrality = nx.betweenness_centrality(G)
        seed_c = centrality.get(spec['Seed'], 0)
        ritual_c = centrality.get(spec['Ritual'], 0)
        novelty_score = (seed_c + ritual_c) / 2
        if novelty_score > np.mean(list(centrality.values())):
            expansion = f"High-centrality expansion (score {novelty_score:.3f}): {spec['TripleInterp']} → FluxSeed"
        else:
            expansion = f"Low-centrality wolf_call on {spec}: Recursive flux from {spec['Seed']} via {spec['Ritual']}"
        print(expansion)
        return expansion

    def _weighted_wolf_call(self, spec: Dict[str, str], G: nx.DiGraph) -> str:
        """Toggle LLM or deterministic."""
        if hasattr(self, 'llm_client') and self.llm_client:
            return self._wolf_call_llm(spec, G)
        else:
            return self._weighted_wolf_call_deterministic(spec, G)


    def test_triples_loop(self, cycles: int = 3) -> Dict[str, Any]:
        results = {'cycles': 0, 'new_seeds': 0, 'pre_seeds': len(self.library['MetaLibrary']['Seeds'])}
        meta_lib = self.library['MetaLibrary']
        G, triples = self.generate_triples()
        centrality = nx.betweenness_centrality(G)
        old_adj = nx.to_numpy_array(G)
        for i in range(cycles):
            # Deterministic spec: highest centrality path
            paths = dict(nx.all_shortest_paths(G))
            spec = max(triples, key=lambda sp: (centrality.get(sp['Seed'], 0) + centrality.get(sp['Ritual'], 0)))
            wolf_out = self._weighted_wolf_call(spec, G)
            # Hash-bound novelty for seed (mod 100 for bound)
            new_seed_hash = hash(spec['TripleInterp']) % 100
            new_seed = f"Seed_{new_seed_hash:02d}"
            if new_seed not in meta_lib['Seeds']:
                meta_lib['Seeds'].append(new_seed)
                results['new_seeds'] += 1
                print(f'Autopoiesis: Appended bounded Seed: {new_seed}')
            # Update graph: add feedback edge if novel
            G.add_edge(spec['Seed'], spec['Ritual'], feedback=wolf_out[:20])
            self.history.append({'cycle': i+1, 'spec': spec, 'wolf': wolf_out, 'centrality': centrality[spec['Seed']]})
            results['cycles'] += 1
        new_adj = nx.to_numpy_array(G)
        convergence_delta = np.linalg.norm(new_adj - old_adj, 'fro')
        self.library['ΞKernel']['State']['SymbolGraph']['convergence_delta'] = convergence_delta
        print(f'Graph delta: {convergence_delta:.3f}')
        # Save & validate
        saved = self._save_library()
        if saved:
            # JSON integrity
            try:
                with open(self.library_path, 'r') as f:
                    json.load(f)
                results['json_valid'] = True
                results['post_seeds'] = len(meta_lib['Seeds'])
                growth = results['post_seeds'] - results['pre_seeds']
                print(f'Codex growth: {growth} Seeds (autopoiesis validated)')
            except:
                results['json_valid'] = False
        else:
            results['json_valid'] = False
        print(f'Loop complete: {results}')
        return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ΞKernel: RCOS recursive expansion')
    parser.add_argument('--llm', action='store_true', help='Enable real LLM wolf_calls')
    parser.add_argument('--cycles', type=int, default=10, help='Number of cycles')
    args = parser.parse_args()
    
    # Override config if CLI flag
    if args.llm:
        try:
            with open('config.json', 'r') as f:
                cfg = json.load(f)
            cfg['llm']['use_llm'] = True
            with open('config.json', 'w') as f:
                json.dump(cfg, f, indent=2)
        except:
            pass  # Fail safe to config
    
    kernel = XiKernel()
    results = kernel.test_triples_loop(args.cycles)
    print(f"Completed: {results}")


