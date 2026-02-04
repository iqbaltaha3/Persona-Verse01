# persona.py

import uuid
from copy import deepcopy
from datetime import datetime
from llm import call_llm

class InteractionEvent:
    def __init__(self, text, signals, source):
        self.text = text
        self.signals = signals
        self.source = source
        self.time = datetime.utcnow()


class Persona:
    def __init__(self, name, traits, plasticity=0.1):
        self.id = str(uuid.uuid4())[:6]
        self.name = name
        self.traits = traits
        self.plasticity = plasticity
        self.memory = []

    def speak(self, topic: str) -> InteractionEvent:
        prompt = f"""
You are a persona in a simulation.

TRAITS:
{self.traits}

TOPIC:
{topic}

TASK:
1. Think briefly.
2. Speak one short paragraph.
3. Output emotional signals.

Return ONLY JSON:
{{
  "text": "...",
  "signals": {{
    "warmth": -1 to 1,
    "dominance": -1 to 1,
    "curiosity": -1 to 1
  }}
}}
"""

        result = call_llm(prompt)

        return InteractionEvent(
            text=result["text"],
            signals=self._clamp_signals(result["signals"]),
            source=self.name
        )

    def listen(self, event: InteractionEvent):
        before = deepcopy(self.traits)

        prompt = f"""
You are interpreting a message as a biased persona.

YOUR TRAITS:
{self.traits}

MESSAGE:
{event.text}

SIGNALS:
{event.signals}

Suggest SMALL trait changes (max ±0.05).

Return ONLY JSON:
{{
  "trait_changes": {{
    "openness": number,
    "trust": number,
    "empathy": number,
    "assertiveness": number
  }}
}}
"""

        result = call_llm(prompt)

        self._apply_changes(result["trait_changes"])
        self._clamp_traits()

        self.memory.append({
            "from": event.source,
            "before": before,
            "after": deepcopy(self.traits),
        })

    def _apply_changes(self, changes):
        for trait, delta in changes.items():
            if trait in self.traits:
                self.traits[trait] += delta * self.plasticity

    def _clamp_traits(self):
        for t in self.traits:
            self.traits[t] = max(0.0, min(1.0, self.traits[t]))

    def _clamp_signals(self, signals):
        return {
            k: max(-1.0, min(1.0, float(v)))
            for k, v in signals.items()
        }
