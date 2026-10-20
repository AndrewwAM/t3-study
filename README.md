# T3 Study

Un entorno de estudio para [T3 Code](https://github.com/pingdotgg/t3code). Abres un hilo, escribes `estudiar cc para el C2` y el agente actúa como profesor particular:

1. **Diagnóstico.** Quizzes cortos para ver qué sabes.
2. **Plan.** Te muestra un plan y espera tu aprobación.
3. **Clases.** Enseña paso a paso.

Usa tu material del ramo como fuente y guarda notas de cada sesión para retomar donde quedaste.

- **Cualquier ramo:** cada uno tiene su carpeta con su material.
- **Cualquier proveedor de T3:** Antigravity (Gemini), Claude, Cursor, Codex u otro que lea `AGENTS.md`.
- **Linux, macOS y Windows.**

Está inspirado en [amosblomqvist/learn](https://github.com/amosblomqvist/learn).

---

## 1. Requisitos

| Qué | Para qué | Obligatorio |
|---|---|---|
| [T3 Code](https://github.com/pingdotgg/t3code) | La app donde conversas con el agente | Sí |
| Al menos un proveedor configurado en T3 | El modelo que hace de profesor (ver [§3](#3-elegir-proveedor-y-modelo)) | Sí |
| Git | Descargar y actualizar T3 Study | Sí |
| Python 3 con `numpy`, `scipy`, `matplotlib` | El agente verifica cálculos y hace gráficos | Muy recomendado en ramos con cálculo |
| Poppler (`pdftotext`) | Leer PDFs de forma confiable | Recomendado |
| [Obsidian](https://obsidian.md) | Ver las notas con fórmulas y diagramas | Opcional |

### Linux

```bash
# Ubuntu / Debian
sudo apt install git python3-pip poppler-utils
# Fedora
sudo dnf install git python3-pip poppler-utils
# Arch
sudo pacman -S git python-pip poppler

python3 -m pip install --user numpy scipy matplotlib
```

Si `pip` reclama un «externally managed environment», instala los paquetes de tu distribución (`python3-numpy python3-scipy python3-matplotlib`) o usa `pipx`/un entorno virtual.

### Windows (PowerShell)

```powershell
winget install --id Git.Git -e
winget install --id Python.Python.3.12 -e
winget install --id oschwartz10612.Poppler -e
py -m pip install numpy scipy matplotlib
```

Después **cierra y vuelve a abrir T3 Code** (y la terminal) para que vea los programas nuevos. Comprueba con:

```powershell
git --version; py --version; pdftotext -v
```

Si `pdftotext` no aparece, agrega la carpeta `bin` de Poppler al `PATH` (*Configuración → Sistema → Acerca de → Configuración avanzada del sistema → Variables de entorno*).

### macOS

```bash
brew install git python poppler
python3 -m pip install numpy scipy matplotlib
```

## 2. Instalación

Linux / macOS:

```bash
git clone https://github.com/AndrewwAM/t3-study.git
cd t3-study
cp perfil.example.md perfil.md
```

Windows (PowerShell):

```powershell
git clone https://github.com/AndrewwAM/t3-study.git
cd t3-study
Copy-Item perfil.example.md perfil.md
```

Completa `perfil.md` con tu nombre, carrera y preferencias. Es opcional, pero el agente lo usa.

> Mientras el repo sea privado, primero acepta la invitación de colaborador que llega a tu correo de GitHub. Al clonar, Git te pedirá iniciar sesión.

## 3. Elegir proveedor y modelo

T3 Study no depende de un proveedor: las instrucciones están en `AGENTS.md` y las skills en `.agents/skills/`. Para Claude hay además un `CLAUDE.md`. Elige en T3 el proveedor que tengas:

| Proveedor en T3 | Modelo sugerido para estudiar | Estado |
|---|---|---|
| Antigravity (Google AI Pro) | Gemini 3.8 Flash (High) | Probado |
| Claude | Claude Sonnet 5.5 (Opus para demostraciones difíciles) | Probado |
| Cursor | Un modelo fuerte (Claude, Gemini o GPT) en lugar de los rápidos | Probado |
| Codex | GPT-6.1 Sol, esfuerzo `high` | Compatible (versión anterior probada) |
| OpenCode, Pi u otros | Cualquiera que lea `AGENTS.md` | Sin probar |

Prefiere un modelo con razonamiento alto: el profesor tiene que verificar y planificar, no solo responder rápido.

## 4. Configurar T3 Code

1. **Proveedor:** en la configuración de T3, en la sección de proveedores, activa el tuyo e inicia sesión (cuenta de Google para Antigravity, de Anthropic para Claude, etc.).
2. **Proyecto:** agrega un proyecto y elige la carpeta `t3-study` **raíz**, la que contiene `AGENTS.md`. Si eliges una carpeta superior o inferior, el agente no carga las instrucciones.
3. **Modelo:** en el selector del hilo, elige proveedor y modelo (ver la tabla). Puedes dejarlo como predeterminado del proyecto.
4. **Permisos:** el agente necesita crear y editar archivos en `notas/` y ejecutar comandos (Python, `pdftotext`). Usa el modo de acceso completo o uno que acepte ediciones automáticamente. Si no, T3 te pedirá aprobar cada paso.

## 5. Agregar un ramo

Cada ramo vive en `ramos/<sigla-corta>/`, por ejemplo `ramos/cc/`:

```
ramos/cc/
├── material/                 ← TU material de este semestre: programa, ppts, guías, rúbricas, notebooks
└── material-adicional/       ← material de otra persona o de semestres anteriores
    └── 2026.1-lucas/         ← p. ej. una carpeta que te pasaron, tal cual
```

- `material/` es **lo oficial**: fechas, alcance de cada evaluación y notación salen de aquí. Pon el programa del ramo (syllabus o planificación): es lo primero que lee el agente.
- `material-adicional/` sirve para practicar: certámenes anteriores, rúbricas y apuntes. Si contradice tu material actual, el agente te avisa y usa el actual.

Luego, en un hilo nuevo:

```
configurar ramo cc
```

El agente lee el programa, arma `ramos/cc/curso.md` con evaluaciones, fechas, unidades y qué archivo corresponde a cada unidad, y te pide que lo revises. Repítelo cuando agregues material nuevo.

## 6. Estudiar

En un hilo nuevo del proyecto:

| Escribes | Qué pasa |
|---|---|
| `estudiar cc para el C2` | Diagnóstico de lo que entra en el C2 → plan → clases por pasos |
| `estudiar cc, mínimos cuadrados` | Lo mismo, acotado a un tema |
| `practicar cc C2` | Diagnóstico corto y luego ejercicios tipo certamen, corregidos con criterio de rúbrica |
| `seguir cc` | Retoma donde quedaste |
| `tema independiente: transformers` | Un tema fuera de los ramos |

**Cómo funciona una sesión:**

1. **Diagnóstico.** Quizzes para encontrar dónde termina lo que sabes. Equivocarse aquí es útil.
2. **Plan.** Te muestra el enfoque y un mapa de dependencias. **No empieza a enseñar hasta que lo apruebes** (`dale`) o pidas cambios.
3. **Clases.** Un concepto a la vez: por qué importa, de dónde sale y cómo se conecta con lo anterior. Cada uno termina con un quiz y, en ramos de cálculo o programación, con un ejercicio tipo certamen.

**Responder quizzes:** escribe el número (`3`), varios si corresponde (`1 y 3`), o `0` / `no sé`. «No sé» no cuenta como error: le muestra al agente dónde está tu límite. Si prefieres opciones clicables, pídelo (`hazme los quizzes con opciones clicables`).

**Consejos:**

- Usa **un hilo nuevo por sesión** y empieza con `seguir <ramo>`: los hilos muy largos empeoran al modelo.
- Si algo te parece mal, dilo. El agente debe verificar en tu material o con Python, y corregir.
- Para cortar a mitad de una sesión, escribe `paremos aquí`: el agente deja las notas listas para retomar.
- Puedes cambiar de proveedor entre sesiones: las notas son archivos Markdown y cualquier modelo las retoma.

## 7. Dónde queda todo

```
notas/
├── index.md                              ← temas activos
└── cc/minimos-cuadrados/
    ├── _state.md                         ← qué sabes, plan, siguiente paso (para retomar)
    ├── sessions/2026-10-19-…md           ← la clase: quizzes, plan, conceptos, fuentes
    └── viz/                              ← gráficos generados
```

Puedes abrir `notas/` como bóveda de Obsidian.

**Tus notas, tu material y `perfil.md` no se suben a Git** (están en `.gitignore`). Respáldalos por tu cuenta, por ejemplo con una carpeta sincronizada (Drive, OneDrive, MEGA) o un repo privado propio.

## 8. Actualizar

```bash
git pull
```

Tus archivos están ignorados por Git, así que actualizar no los toca.

## 9. Limitaciones

- **No hay registro automático de la conversación.** El agente escribe la nota mientras avanza; si falta algo, pídele `actualiza las notas`.
- **La respuesta de cada quiz vive solo en la memoria del modelo** hasta que respondes. No se muestra ni se guarda en archivos, pero tampoco está protegida técnicamente.
- **El modelo puede equivocarse,** sobre todo con PDFs escaneados o manuscritos. Si algo no cuadra, pide `verifícalo en el material` o `verifícalo con Python`. Como referencia: Gemini 3.8 Flash (High) resolvió bien, con verificación numérica, una pregunta de 50 puntos de un certamen de Computación Científica.
- **El chat de T3 no muestra fórmulas LaTeX** (`$x^2$` aparece tal cual). Por eso el agente escribe las fórmulas del chat con símbolos (`Aᵀr = 0`, `x ∈ ℝⁿ`, `‖r‖₂`) y usa LaTeX solo en las notas, que Obsidian sí muestra. Si algún día tu cliente muestra LaTeX, pon `Fórmulas en el chat: latex` en `perfil.md`.
- Las instrucciones del agente están en inglés a propósito, porque los modelos las siguen mejor. Todo lo que tú ves sale en español.

## 10. Estructura

```
AGENTS.md                      ← instrucciones (las leen Antigravity, Codex, Cursor, OpenCode…)
CLAUDE.md                      ← redirige a AGENTS.md para Claude
.agents/skills/
├── study-teach/               ← método: diagnóstico → plan → clases
├── study-research/            ← verificar en el material antes de afirmar
├── study-quiz/                ← cómo construir y corregir quizzes
├── study-visualize/           ← diagramas Mermaid y gráficos con Python
└── study-course-setup/        ← configurar un ramo
templates/                     ← plantillas de notas, estado y perfil de ramo
ramos/_ejemplo/                ← estructura de muestra
perfil.example.md              ← copia a perfil.md
```

Para cambiar el comportamiento, edita `AGENTS.md` o las skills.
