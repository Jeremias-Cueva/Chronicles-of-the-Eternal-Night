# ⚔ Chronicles of the Eternal Night

A web-based, responsive **Cosmic Horror Text RPG** powered by the **Groq API** (using the `llama-3.3-70b-versatile` model) and built with **Gradio**.

The game delivers a dynamic, AI-generated narrative based on the player's actions. The AI returns structured JSON payloads that the Python engine parses in real time to update the player's state (Vitality, Sanity, Inventory) and modify the embedded HTML5 canvas environment.

---

## 🚀 Features

- **Dynamic AI Game Master:** Fully driven by LLaMA 3.3, delivering immersive and contextual cosmic horror storytelling.
- **State & Inventory Management:** Real-time tracking of Vitality, Sanity, and a dynamically expanding inventory system.
- **Interactive Visual Canvas:** Embedded HTML5/JavaScript canvas that dynamically adapts environments (e.g. "crypt", "blood", "void") based on player decisions.
- **Responsive Design:** Custom CSS grid optimized for wide screens and desktop gameplay.
- **Smart Text Input:** Multi-line input handling with overflow protection for a clean user experience.

---

## 🛠️ Prerequisites & Installation

Make sure you have **Python 3.8+** installed.

### 1. Install dependencies

```bash
pip install gradio groq

2. Get your Groq API KeyCreate an account at Groq Console and generate your API key. Configuration & Execution1. Set your API keyEdit your main script (app.py) and replace:python

GROQ_API_KEY = "your_actual_groq_api_key_here"

2. Run the applicationbash

python app.py

3. Open the gameLocal: http://127.0.0.1:7860
Or use the public .gradio.live link generated in the terminal.

 How to PlayInterfaceLeft Panel: Monitor your Vitality, Sanity, and Inventory.
Right Panel: Animated canvas + story history log.

Available ActionsAdvance
Examine
Attack
Search
Use Amulet
Scream

ConsequencesLow Vitality or Sanity may trigger Game Over.
The canvas may collapse into a "void state".
Use the  Restart button to begin a new run.

 ConceptChronicles of the Eternal Night is a cosmic horror experience where the AI acts as Game Master, generating unpredictable narrative branches while the engine maintains structured game state.Every choice matters. Every message can reshape reality.

