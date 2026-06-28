# Gewu · 格物

**La IA respondió tu pregunta — "lo entendiste", pero no puedes explicarlo.**

> Convierte "preguntarle a la IA cuando tengo una duda" en "preguntarle a la IA con un objetivo" — te guía para explicar con claridad; si no puedes explicarlo, no lo entiendes de verdad.
>
> > Estudia una cosa a fondo para alcanzar el verdadero conocimiento: si puedes explicarla con claridad, de verdad la entiendes.
>

[![License](https://img.shields.io/github/license/YuhangZho/gewu-skill?style=flat-square&color=green)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/stargazers)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/deps-none%20%28stdlib%29-success?style=flat-square)
![Offline](https://img.shields.io/badge/offline-ready-success?style=flat-square)
![Agent Skills](https://img.shields.io/badge/Agent_Skills-Standard-3fb950?style=flat-square)
[![skills.sh](https://skills.sh/b/YuhangZho/gewu-skill)](https://skills.sh/YuhangZho/gewu-skill)
![Runtime](https://img.shields.io/badge/Runtime-Claude_·_Codex_·_Cursor_·_Kimi·_OpenClaw·_WorkBuddy-8957e5?style=flat-square)

[Para quién es](#deja-que-gewu-te-guie) · [Qué obtendrás](#tu-solo-aprendes-nosotros-nos-encargamos-del-resto) · [Cómo empezar](#cómo-empezar) · [Instalación](#instalación) · [Estructura de directorios](#estructura-de-directorios)

**Otros idiomas:** [简体中文](README.md) · [English](README_EN.md)

---

## **Deja que Gewu te guíe —**

> - 🃏 Conviértete en un experto en Doudizhu (Lucha contra el Terrateniente): entiende **por qué los expertos guardan bombas pero no las juegan primero**
> - 🧮 Comprende qué calcula realmente el problema de "gallinas y conejos en una jaula" — y ayuda a **tu hijo** a entenderlo de verdad (no solo memorizar una fórmula)
> - 💼 Cambia al desarrollo de aplicaciones de IA — traza un mapa de aprendizaje **con prioridades** desde cero
> - 📖 Tres semanas para el CET-4 — primero aclara **qué necesitas aprender de verdad**
> - 💗 Conquista a tu pareja, negocia un aumento: entiende **por qué funciona la estrategia**

```
Tú  : Un token es simplemente dividir el texto en trozos, ¿no?
Gewu: ¿En cuántos trozos se dividiría "unhappiness"? ¿Por qué no por letra ni por palabra completa?
Tú  : Eh… ¿por palabra? No, hay demasiadas palabras… no puedo explicarlo.
Gewu: Exacto — ahí es donde te atascaste. ¿Qué equilibra la tokenización por subpalabras? Vamos a cubrir eso.
```

La contrapartida de Gewu:

> Gewu no es un bot de preguntas y respuestas instantáneas. Es **lento** y tiene un proceso, porque te está "obligando" a entender de verdad.

**Si quieres una respuesta rápida al momento, no es para ti; si quieres dominar algo de verdad, es para eso que está hecho.**

----

## Tú solo aprendes — nosotros nos encargamos del resto

Solo tienes que dominar cada concepto. Notas, enlaces bidireccionales, grafos de conocimiento, progreso de objetivos — Gewu los genera mientras aprendes, sin que escribas una palabra extra ni traces una sola línea.

### Una ruta de aprendizaje planificada

Solo di "quiero aprender IA / frontend / CET-4", y Gewu desglosará una ruta progresiva según tu objetivo.

### Estación de conocimiento local generada automáticamente

- **Hoja de ruta de aprendizaje**: dónde estás ahora y cuál es la siguiente parada.
- **Grafo de conocimiento**: cómo se conectan los conceptos.
- **Planificación de objetivos**: subobjetivos y progreso actual.
- **Documentos de conceptos**: repasa cada concepto que has aprendido.
  - Posicionamiento en una frase
  - Aprendizajes clave
  - Puntos de bloqueo y correcciones
  - Límites, errores comunes
  - Diagramas de flujo y referencias visuales


<img src="./assets/学习站示例.gif" alt="Ejemplo de estación de conocimiento" width="100%" style="display:block;margin-left:0;margin-right:auto;">

---

## Instalación

Gewu sigue el estándar abierto de Agent Skills y puede usarse en agentes que soporten skills.

### Comprobación del entorno

```bash
python3 --version
```

- Requiere `Python 3.8` o superior;
- Instalación o actualización de Python:
  - Windows: [python.org/downloads](https://www.python.org/downloads/), marca `Add Python to PATH` durante la instalación
  - macOS (con Homebrew instalado): `brew install python`
  - Ubuntu / Debian: `sudo apt install python3`

### Opción 1: Instalación con un clic

Dile al agente que estés usando:

```text
Ayúdame a instalar este skill: https://github.com/YuhangZho/gewu-skill
```

O ejecuta por línea de comandos:

```bash
npx skills add YuhangZho/gewu-skill
```

### Opción 2: Instalación manual

Copia la carpeta `gewu-skill` a la ruta correspondiente del agente.

<details>
<summary>Desplegar: directorios de skills para agentes comunes</summary>


| Agente                 | directorio de skills                                                  |
| ---------------------- | ------------------------------------------------------------ |
| Claude Code            | `~/.claude/skills/`                                          |
| Claude Escritorio / Cowork | Ajustes → Capabilities, añade la carpeta `gewu`                      |
| Codex                  | `~/.codex/skills/`                                           |
| Cursor                 | `~/.cursor/skills/`                                          |
| WorkBuddy              | `~/.workbuddy/skills/`                                       |
| Kimi Work              | `~/AppData/Roaming/kimi-desktop/daimon-share/daimon/skills/` |
| Marvis                 | `~/AppData/Roaming/Tencent/Marvis/User/xx/skills/custom/`    |
| Trae CN                | `~/.trae-cn/skills/`                                         |
| Qoder CN               | `~/.qoder-cn/skills/`                                        |
| OpenClaw               | `~/.openclaw/skills/`                                        |
| Otros 50+ agentes      | Las rutas varían, ver [tabla de soporte vercel-labs/skills](https://github.com/vercel-labs/skills#supported-agents) |

</details>

---

## Cómo empezar

Dile una frase a tu IA:

```text
Usa Gewu para ayudarme a convertirme en un experto en Doudizhu
```

También puedes decir:

```text
Tres semanas para el CET-4 — primero ayúdame a aclarar qué necesito aprender de verdad
```

```text
Quiero cambiar al desarrollo de aplicaciones de IA — planifica una ruta de aprendizaje desde cero
```

```text
Ayúdame a entender el problema de "gallinas y conejos en una jaula" de mi hijo para poder examinarlo
```

En el primer uso, Gewu te preguntará dónde se guarda tu base de conocimiento. Elige una ubicación a largo plazo, por ejemplo:

```text
D:\gewu-vault
```

Después, la misma base de conocimiento seguirá acumulándose — no hace falta configurarla cada vez (la ruta se puede ajustar manualmente en ~/.gewu/glb_vault_path.json).

---

## Cómo funciona Gewu

Las acciones centrales de Gewu:

1. **Pregunta el objetivo primero**: estudiarlo para un examen, entrevista, cambio de rol, incorporación a un proyecto o puro interés.
2. **Trazar la ruta**: ordena la secuencia de aprendizaje según dependencias previas e importancia.
3. **Aprender concepto por concepto**: plantea preguntas, explica, te pide que lo reformules, indaga en los puntos de bloqueo.
4. **Validar para cerrar**: solo cuando puedes explicarlo con otras palabras y sabes cuándo falla, se da por aprendido.
5. **Asentar de inmediato**: actualiza notas, hoja de ruta, grafo de conocimiento y progreso del objetivo.

Credo central: **La salida empuja a la entrada. Si puedes explicarlo con claridad, de verdad lo entiendes.**

---

## Estructura de directorios

```text
gewu-skill/
  SKILL.md                        Archivo principal del skill
  templates/concept-template.md   Plantilla de nota de concepto
  scripts/render_viz.py           Genera diagramas de estructura de conceptos
  scripts/build_graph.py            Genera el grafo de conocimiento
  scripts/plan_path.py              Genera la estación de conocimiento
  scripts/set_goal.py               Escribe objetivos y refresca las páginas
  assets/merged_output_720p.webp    Vídeo de demostración
```

Tras ejecutar, tu base de conocimiento se ve más o menos así:

```text
gewu-vault/
  AI/
    Token.md
    Context.md
    AI-路线图.html
    AI-知识图谱.html
    _viz/
      Token.model.json
      Token.mmd
      Token.svg
    _transcript/
      Token.jsonl
  fragment/
    conceptos-pequeños-aprendidos-al-vuelo.md
  _system/
    graph_data.json
    roadmap_data.json
    goals.json
    config.json
```

---

## Autor

Yuhang 🧪 destilándose a sí mismo.

<p align="left">
  <img src="./assets/wechat-search.png" alt="Búsqueda WeChat: Zhou Yuhang" width="620" style="display:block;margin-left:0;margin-right:auto;">
</p>

## Licencia

**MIT** © 2026 Yuhang ([@YuhangZho](https://github.com/YuhangZho)). Libre de usar y modificar, solo conserva el aviso de copyright y licencia.
