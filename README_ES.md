# 格物 · Gewu

**a Feynman-method learning system · sistema de aprendizaje con el método Feynman**

> *"Investiga una cosa para alcanzar el conocimiento verdadero — si puedes explicarlo con claridad, lo entiendes de verdad."*

<video src="./assets/merged_output.mp4" controls=""></video>



[![License](https://img.shields.io/github/license/YuhangZho/gewu-skill?style=flat-square&color=green)](./LICENSE)
[![Stars](https://img.shields.io/github/stars/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/YuhangZho/gewu-skill?style=flat-square)](https://github.com/YuhangZho/gewu-skill/commits)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/deps-none%20%28stdlib%29-success?style=flat-square)
![Offline](https://img.shields.io/badge/offline-ready-success?style=flat-square)
![Agent Skills](https://img.shields.io/badge/Agent_Skills-Standard-3fb950?style=flat-square)
[![skills.sh](https://skills.sh/b/YuhangZho/gewu-skill)](https://skills.sh/YuhangZho/gewu-skill)
![Runtime](https://img.shields.io/badge/Runtime-Claude_·_ChatGPT_·_Codex_·_Cursor_·_Kimi-8957e5?style=flat-square)

<br>

**格物 · Gewu — deja de guardar y coleccionar; aprende de verdad hasta que tu conocimiento empiece a «respirar».**

<br>

Gewu aprende *contigo* mediante preguntas y respuestas al estilo Feynman, hasta que lo entiendes de verdad.<br>

Trae tu objetivo y aprende para aplicarlo.<br>

Obtén automáticamente un grafo de conocimiento + ruta de aprendizaje + planificación de objetivos.

[Qué hace](#qué-hace) · [Inicio rápido](#inicio-rápido) · [Instalación](#instalación) · [Licencia](#licencia)

<br>

**Otros idiomas / 其他语言:**

[中文](README.md) · [English](README_EN.md) · [Español](README_ES.md)

<br>

---

## Qué hace

**Gewu te guía a "decir un concepto en voz alta" — no para tomar notas que acumulan polvo, sino para entenderlo de verdad y hacer crecer todo lo aprendido hasta convertirlo en un sitio de conocimiento que «respira».**

- **Capa de dominio**: al empezar un dominio nuevo, primero da una visión general, construye un mapa de conocimiento, te pregunta tu **objetivo de aprendizaje concreto** y planifica una ruta por "dependencias primero + importancia".
- **Capa de concepto (7 pasos Feynman)**: `fijar el objetivo → encender (preguntar → traer fuentes autorizadas de la web → primer borrador) → modelado visual (boceto) → explicar a un lego → retroceder donde te atascas → simplificar e iterar → triple verificación → guardar`.
- **Lo que se guarda**: cada concepto que dominas = una nota Markdown + una imagen final animada (HTML) + entrada en el grafo de conocimiento / hoja de ruta / sitio de documentos.
- **Ciclo de objetivos**: define un objetivo concreto (p. ej. "postular a ingeniero de aplicaciones de IA", "CET-4"), y el agente de IA calcula tu coincidencia y tus brechas frente a los requisitos reales y planifica el siguiente paso; al cumplir un objetivo, el conocimiento correspondiente empieza a "respirar".

Creencia central: **la salida fuerza la entrada — solo lo entiendes si puedes explicarlo con claridad.**

---

## Inicio rápido

Dile a tu asistente de IA (cualquiera de estas frases lo activa):

- "Aprende **IA** con Gewu"
- "Enséñame **Token** con el método Feynman"
- "Estoy empezando con el **lenguaje C** — planifícame una ruta de aprendizaje"
- "¿Qué debería aprender ahora / dónde voy?"
- "Mi objetivo es **conseguir trabajo como ingeniero de IA** — analiza la brecha entre yo y ese objetivo"

El asistente conduce tu aprendizaje con los 7 pasos de `SKILL.md` y actualiza el sitio de conocimiento cada vez que dominas un concepto. Para actualizar manualmente:

```bash
python scripts/build_graph.py                   # actualiza el grafo de conocimiento
python scripts/plan_path.py --goal entrevista   # actualiza el sitio de conocimiento (--goal opcional)
```

Abre `知识库/<categoría>/<categoría>-路线图.html` en tu navegador para explorar (claro por defecto; alterna entre los temas **claro / oscuro / papel Xuan / tinta nocturna** arriba a la derecha — los dos últimos son un estilo de tinta china).

---

## Instalación

Gewu sigue el estándar abierto Agent Skills (un único `SKILL.md` en la raíz) y funciona en cualquier agente compatible con skills.

### Requisitos

```bash
python --version
```

- Muestra `Python 3.x` → salta a "Instalación" más abajo.
- Comando no encontrado → instálalo:
  - **Windows** → [python.org/downloads](https://www.python.org/downloads/), marca *Add Python to PATH* durante la instalación
  - **macOS** → `brew install python` o desde python.org
  - **Linux** → `sudo apt install python3`

### Opción 1: en un clic (recomendada, multi-agente)

Solo dile al agente que estés usando:

```
Instálame este skill: https://github.com/YuhangZho/gewu-skill
```

O ejecuta desde la línea de comandos:

```bash
npx skills add YuhangZho/gewu-skill
```

### Opción 2: instalación manual (clonar en el directorio correcto)

<details><summary>Desplegar: directorio de skills por agente</summary>

| Agente | directorio de skills (global) |
|---|---|
| Claude Code | `~/.claude/skills/gewu/` |
| Claude escritorio / Cowork | **Ajustes → Capabilities**, añade la carpeta `gewu-skill`, o guarda el `gewu-skill.skill` incluido |
| Codex | `~/.codex/skills/gewu/` |
| Cursor | `~/.cursor/skills/gewu/` |
| OpenClaw | `~/.openclaw/skills/gewu/` |
| Qoder | `~/.qoder/skills/gewu/` |
| Kimi Code CLI | `~/.config/agents/skills/gewu/` |
| Otros 50+ agentes | las rutas varían, consulta la [tabla de soporte de vercel-labs/skills](https://github.com/vercel-labs/skills#supported-agents) |


</details>

---

## Personalización

### Interruptor de apariencia/comportamiento → `config.json`

¿Solo quieres cambiar el color de acento o el modo claro/oscuro por defecto, sin tocar código? Copia la plantilla a `知识库/_system/config.json`, **pon `enabled` en `true`** y cambia los parámetros (mientras esté apagado, todo usa los valores por defecto):

```jsonc
// 知识库/_system/config.json   (plantilla: templates/config.example.json)
{
  "enabled": true,                  // ← interruptor maestro, por defecto false
  "theme_default": "dark",          // light / dark / ink (papel Xuan) / inkdark (tinta nocturna)
  "accent": { "light": "#34c759", "dark": "#30d158" }  // acento: botones / enlaces / tarjeta activa
}
```

Vuelve a ejecutar `python scripts/plan_path.py` — el sitio de conocimiento ahora usa oscuro por defecto con acento verde.

`enabled: false` (por defecto) ignora lo anterior y usa el claro + azul incorporados.

---

## Estructura

```
gewu-skill/
  SKILL.md                      archivo principal del skill (flujo + disparadores + spec visual)
  README.md                     este archivo
  templates/concept-template.md plantilla de nota de concepto
  scripts/build_graph.py        escanea notas → grafo de conocimiento HTML (dirigido por fuerzas, flechas de dependencia, "respiración" de objetivos)
  scripts/plan_path.py          → sitio de conocimiento de una página (hoja de ruta / docs de conceptos / planificación de objetivos / grafo embebido)
  assets/hero.svg               animación promocional
```

Generado en tu directorio de aprendizaje tras una ejecución (ejemplo):

```
知识库/
  知识图谱.html               visión general global
  AI/                         una categoría
    概念.md                   una nota por concepto
    _viz/概念.html            imagen final animada
    AI-知识图谱.html          grafo de esta categoría
    AI-路线图.html            sitio de conocimiento de una página (entrada; hoja de ruta / grafo / objetivos / docs)
  _system/                    datos de máquina (graph_data / roadmap_data / domains / goals.json)
```



## Créditos
El borrador de la animación promocional se hizo con el skill [huashu-design](https://github.com/alchaincyf/huashu-design).

## Licencia
**MIT** © 2026 宇航 ([@YuhangZho](https://github.com/YuhangZho)) — consulta [`LICENSE`](./LICENSE). Libre para usar, modificar, distribuir y uso comercial, siempre que se conserven el aviso de copyright y la licencia.
