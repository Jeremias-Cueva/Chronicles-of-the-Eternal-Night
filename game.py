!pip install groq gradio

import gradio as gr
import json
from groq import Groq

# ==================== CONFIG ====================
GROQ_API_KEY = "YOUR_APY_KEY"

try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception:
    client = None

# ==================== ENGINE ====================
class DarkEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.health = 100
        self.sanity = 85
        self.inventory = ["Daga Oxidada", "Amuleto de Hueso"]
        self.environment = "cripta"
        self.is_active = True
        self.history = []

    def process(self, action):
        if not self.is_active:
            self.history.append(f"**Tú:** {action}\n**GM:** ☠ Tu aventura ya terminó...")
            return

        if not client:
            self.history.append(f"**Tú:** {action}\n**GM:** Error de API Key con Groq.")
            return

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Eres Game Master de horror cósmico. Responde SOLO con JSON válido: {\"narrativa\": \"texto\", \"cambio_salud\": 0, \"cambio_cordura\": 0, \"item_nuevo\": \"\", \"ambiente_visual\": \"cripta\"}. Opciones ambiente_visual: cripta, fuego, sangre, vacio."},
                    {"role": "user", "content": action}
                ],
                response_format={"type": "json_object"},
                temperature=0.8,
                max_tokens=650
            )
            data = json.loads(response.choices[0].message.content)

            narrativa = data.get("narrativa", "Las sombras se mueven...")
            self.health = max(0, min(100, self.health + data.get("cambio_salud", 0)))
            self.sanity = max(0, min(100, self.sanity + data.get("cambio_cordura", 0)))
            self.environment = data.get("ambiente_visual", "cripta")

            if data.get("cambio_salud", 0) < -12:
                self.environment = "sangre"

            item = data.get("item_nuevo", "")
            if item and item not in self.inventory:
                self.inventory.append(item)

            if self.health <= 0 or self.sanity <= 0:
                self.is_active = False
                self.environment = "vacio"
                narrativa += "\n\n☠ HAS SIDO CONSUMIDO POR LA OSCURIDAD"

            self.history.append(f"**Tú:** {action}\n**GM:** {narrativa}")
        except Exception as e:
            self.history.append(f"**Tú:** {action}\n**GM:** El vacío distorsiona tu voluntad... (Fallo: {str(e)})")

engine = DarkEngine()

# ==================== HELPERS ====================
def create_canvas(env):
    return f"""
    <iframe srcdoc='
    <!DOCTYPE html>
    <html><head><style>
        body {{ margin:0; background:#0a0714; overflow:hidden; }}
        canvas {{ display:block; width:100%; height:100%; }}
    </style></head><body>
    <canvas id="c"></canvas>
    <script>
    var canvas = document.getElementById("c");
    var ctx = canvas.getContext("2d");
    function resize() {{
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }}
    window.addEventListener("resize", resize);
    resize();
    var env = "{env}"; 
    var tick = 0;
    function draw() {{
        tick++;
        ctx.fillStyle = env === "sangre" ? "#2a0a0a" : env === "vacio" ? "#050008" : "#110d1f";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        var cx = canvas.width / 2;
        var cy = canvas.height / 2;
        ctx.fillStyle = "#7c3aed";
        ctx.fillRect(cx - 22, cy - 20, 45, 75);
        ctx.fillStyle = "#1e1b4b";
        ctx.fillRect(cx - 12, cy - 45, 28, 32);
        ctx.fillStyle = "#67e8f9";
        ctx.fillRect(cx - 4, cy - 37, 6, 6);
        ctx.fillRect(cx + 10, cy - 37, 6, 6);
    }}
    setInterval(draw, 80);
    </script>
    </body></html>' 
    style="width:100%; height:260px; border:2px solid #6b21a8; border-radius:12px; background:#0a0714;">
    </iframe>"""

def ejecutar_accion(accion):
    try:
        engine.process(accion)
        historial_texto = "\n\n---\n\n".join(engine.history[-2:]) if engine.history else ""
        inventario_texto = "◆ " + "\n◆ ".join(engine.inventory)
        return historial_texto, engine.health, engine.sanity, inventario_texto, create_canvas(engine.environment)
    except Exception as e:
        return f"Error crítico: {str(e)}", engine.health, engine.sanity, "Error", create_canvas("vacio")

def reiniciar_juego():
    engine.reset()
    return "", 100, 85, "◆ Daga Oxidada\n◆ Amuleto de Hueso", create_canvas("cripta")

# ==================== UI ====================
tema = gr.themes.Soft(primary_hue="violet", neutral_hue="slate")
css_code = """
.gradio-container { max-width: 1100px !important; margin: auto !important; background: #0a0714; padding: 10px !important; }
h1 { color: #c4b5fd; text-align: center; text-shadow: 0 0 10px #7c3aed; margin-bottom: 10px; font-size: 1.5em; }
.historia-caja textarea { font-size: 0.95em !important; line-height: 1.4; resize: none !important; overflow-y: auto !important; }
.fila-horizontal { display: flex !important; flex-wrap: nowrap !important; width: 100% !important; gap: 15px; }
.col-izq { min-width: 200px !important; flex: 1 !important; }
.col-der { min-width: 400px !important; flex: 3 !important; }
.btn-horizontal { flex: 1 !important; min-width: 0 !important; font-size: 0.9em !important; padding: 10px 5px !important; white-space: normal; }
"""

with gr.Blocks(fill_width=True, theme=tema, css=css_code) as demo:
    
    gr.Markdown("# ⚔ CHRONICLES OF THE ETERNAL NIGHT")
    
    with gr.Row(elem_classes="fila-horizontal"):
        with gr.Column(elem_classes="col-izq"):
            gr.Markdown("### Estado")
            health = gr.Slider(0, 100, 100, label="❤ Vitalidad", interactive=False)
            sanity = gr.Slider(0, 100, 85, label="🧠 Cordura", interactive=False)
            gr.Markdown("### Inventario")
            inv = gr.Textbox(value="◆ Daga Oxidada\n◆ Amuleto de Hueso", lines=4, max_lines=4, interactive=False, show_label=False)

        with gr.Column(elem_classes="col-der"):
            canvas = gr.HTML(value=create_canvas("cripta"))
            history = gr.Textbox(lines=4, max_lines=4, interactive=False, show_label=False, elem_classes="historia-caja", placeholder="Historia (Últimos sucesos)...")

    with gr.Row(elem_classes="fila-horizontal"):
        btn_avanzar = gr.Button("Avanzar", variant="primary", elem_classes="btn-horizontal")
        btn_examinar = gr.Button("Examinar", variant="primary", elem_classes="btn-horizontal")
        btn_atacar = gr.Button("Atacar", variant="primary", elem_classes="btn-horizontal")
        btn_buscar = gr.Button("Buscar", variant="primary", elem_classes="btn-horizontal")
        btn_amuleto = gr.Button("Usar Amuleto", variant="secondary", elem_classes="btn-horizontal")
        btn_gritar = gr.Button("Gritar", variant="secondary", elem_classes="btn-horizontal")
        btn_reiniciar = gr.Button("🔄 Reiniciar", variant="stop", elem_classes="btn-horizontal")

    outputs_lista = [history, health, sanity, inv, canvas]

    btn_avanzar.click(lambda: ejecutar_accion("Avanzo con mucho cuidado"), outputs=outputs_lista)
    btn_examinar.click(lambda: ejecutar_accion("Examino detenidamente todo a mi alrededor"), outputs=outputs_lista)
    btn_atacar.click(lambda: ejecutar_accion("Ataco con mi daga oxidada"), outputs=outputs_lista)
    btn_buscar.click(lambda: ejecutar_accion("Registro el área buscando algo útil"), outputs=outputs_lista)
    btn_amuleto.click(lambda: ejecutar_accion("Uso el Amuleto de Hueso"), outputs=outputs_lista)
    btn_gritar.click(lambda: ejecutar_accion("Grito con todas mis fuerzas"), outputs=outputs_lista)
    btn_reiniciar.click(reiniciar_juego, outputs=outputs_lista)

demo.launch(share=True)