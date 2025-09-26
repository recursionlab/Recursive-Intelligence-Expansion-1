import json
import random

class XiKernel:
    def __init__(self, library_file="Meta-Library.json"):
        with open(library_file, "r", encoding="utf-8") as f:
            self.library = json.load(f)
        self.state = self.library["ΞKernel"]["State"]

    def build_spec(self):
        """Build a spec by sampling Seed, Mask, Ritual, Split"""
        seeds = self.library["MetaLibrary"]["Seeds"]
        masks = self.library["MetaLibrary"]["Masks"]
        rituals = self.library["MetaLibrary"]["Rituals"]
        splits = self.library["MetaLibrary"]["Splits"]

        spec = {
            "Seed": random.choice(seeds),
            "Mask": random.choice(masks),
            "Ritual": random.choice(rituals),
            "Split": random.choice(splits)
        }
        return spec

    def wolf_call(self, spec):
        """Placeholder for Wolf (LLM). Currently simulates output."""
        # In real usage: send spec to LLM API (e.g., OpenAI, Ollama, etc.)
        seed_feedback = f"NewSeed_{spec['Seed']}_{spec['Ritual']}"
        return {
            "HybridRun": {
                "Input": spec,
                "Mythic": {
                    "Crystallizations": [f"{spec['Mask']}({spec['Seed']}_A1)"],
                    "Ritual": spec["Ritual"],
                    "Split": spec["Split"]
                },
                "Physical": {
                    "Particles": [f"{spec['Mask']}({spec['Seed']}_A1)"],
                    "Interaction": spec["Ritual"],
                    "Split": spec["Split"]
                },
                "FeedbackSeed": seed_feedback
            }
        }

    def audit_and_update(self, run_output):
        """Audit per Codex-of-Codexes rules, then update state"""
        feedback_seed = run_output["HybridRun"]["FeedbackSeed"]
        if feedback_seed not in self.library["MetaLibrary"]["Seeds"]:
            self.library["MetaLibrary"]["Seeds"].append(feedback_seed)
        self.state["History"].append(run_output)
        return feedback_seed

    def loop(self, cycles=3):
        """Run recursive Lamb/Wolf loop for given cycles"""
        for i in range(cycles):
            print(f"\n--- Cycle {i+1} ---")
            spec = self.build_spec()
            print("Spec:", spec)

            wolf_output = self.wolf_call(spec)
            print("Wolf Output:", json.dumps(wolf_output, indent=2))

            new_seed = self.audit_and_update(wolf_output)
            print("Feedback Seed Added:", new_seed)


if __name__ == "__main__":
    kernel = XiKernel()
    kernel.loop(cycles=3)
