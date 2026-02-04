# main.py

from persona import Persona

topic = "Is AI good for humanity?"

p1 = Persona(
    "Aarav",
    {"openness": 0.8, "trust": 0.6, "empathy": 0.7, "assertiveness": 0.3}
)

p2 = Persona(
    "Zoya",
    {"openness": 0.3, "trust": 0.2, "empathy": 0.3, "assertiveness": 0.8}
)

p3 = Persona(
    "Kabir",
    {"openness": 0.5, "trust": 0.5, "empathy": 0.5, "assertiveness": 0.5}
)

personas = [p1, p2, p3]

for round_no in range(2):
    print(f"\n===== ROUND {round_no + 1} =====")

    for speaker in personas:
        event = speaker.speak(topic)
        print(f"\n{speaker.name}: {event.text}")

        for listener in personas:
            if listener != speaker:
                listener.listen(event)
                print(f" → {listener.name} traits: {listener.traits}")
