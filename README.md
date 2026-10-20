# estudio-agente

Un entorno de estudio para T3 Code: abres un hilo, escribes `estudiar cc para el C2` y el agente actúa como profesor particular. Primero diagnostica lo que sabes con quizzes, después propone un plan y espera tu aprobación, y luego enseña paso a paso. Usa como fuente tu propio material del ramo y guarda notas de cada sesión para retomar donde quedaste.

Sirve para cualquier ramo: cada uno tiene su carpeta con su material. Está pensado para **Antigravity (Gemini)**, pero también funciona con Codex o Claude.

Está inspirado en [amosblomqvist/learn](https://github.com/amosblomqvist/learn).

---

## 1. Requisitos

| Qué | Para qué | Obligatorio |
|---|---|---|
| [T3 Code](https://github.com/pingdotgg/t3code) | La app donde se conversa con el agente | Sí |
| Cuenta de Google con Antigravity (p. ej. Google AI Pro) | Los modelos Gemini | Sí (o Codex/Claude) |
| `git` | Clonar y actualizar el framework | Sí |
| Python 3 con `numpy`, `scipy`, `matplotlib` | El agente verifica cálculos y hace gráficos | Muy recomendado en ramos numéricos |
| `pdftotext` (paquete `poppler-utils` / `poppler`) | Leer PDFs de forma confiable | Recomendado |
| [Obsidian](https://obsidian.md) | Ver las notas con fórmulas y diagramas | Opcional |

```bash
# Ubuntu/Debian
sudo apt install git poppler-utils python3-pip && pip install numpy scipy matplotlib
# Fedora
sudo dnf install git poppler-utils python3-pip && pip install numpy scipy matplotlib
# macOS (Homebrew)
brew install git poppler python && pip3 install numpy scipy matplotlib
```

## 2. Instalación

```bash
git clone git@github.com:AndrewwAM/estudio-agente.git
cd estudio-agente
cp perfil.example.md perfil.md   # y complétalo: nombre, carrera, preferencias
```

> El repo es privado: primero acepta la invitación de colaborador que llega a tu correo de GitHub.

## 3. Configurar T3 Code

1. **Activar Antigravity:** en la configuración de T3, en la sección de proveedores, activa **Antigravity** e inicia sesión con tu cuenta de Google.
2. **Agregar el proyecto:** *Add project* → elige la carpeta `estudio-agente` **raíz** (la que contiene `AGENTS.md`). Si abres una carpeta superior o inferior, el agente no carga las instrucciones.
3. **Elegir modelo:** en el selector de modelo del hilo, elige **Antigravity → Gemini 3.8 Flash (High)**. Puedes dejarlo como modelo por defecto del proyecto.
4. **Permisos:** el agente tiene que poder crear y editar archivos en `notas/` y ejecutar comandos (Python, `pdftotext`). Usa el modo de acceso completo o uno que acepte ediciones automáticamente. De lo contrario, T3 te pedirá aprobar cada paso.

## 4. Agregar un ramo

Cada ramo vive en `ramos/<sigla-corta>/` (por ejemplo `ramos/cc/`):

```
ramos/cc/
├── material/                 ← TU material de este semestre: programa, ppts, guías, rúbricas, notebooks
└── material-adicional/       ← material de otra persona o de semestres anteriores
    └── 2026.1-lucas/         ← p. ej. la carpeta que te pasó Lucas, tal cual
```

- `material/` es **lo oficial**: fechas, alcance de cada certamen y notación salen de aquí.
- `material-adicional/` sirve para practicar: certámenes anteriores, rúbricas y apuntes. Si contradice tu material actual, el agente te lo avisa y usa el actual.
- Pon el programa del ramo (syllabus/planificación) en `material/`: es lo primero que lee.

Luego, en un hilo nuevo:

```
configurar ramo cc
```

El agente lee el programa, arma `ramos/cc/curso.md` con evaluaciones, fechas, unidades y qué archivo corresponde a cada unidad, y te pide que lo revises. Cuando agregues material nuevo, repite `configurar ramo cc`.

## 5. Estudiar

Escribe en un hilo nuevo del proyecto:

| Escribes | Qué pasa |
|---|---|
| `estudiar cc para el C2` | Diagnóstico de lo que entra en el C2 → plan → clases por pasos |
| `estudiar cc, mínimos cuadrados con QR` | Lo mismo, acotado a un tema |
| `practicar cc C2` | Diagnóstico corto y luego ejercicios tipo certamen, corregidos con criterio de rúbrica |
| `seguir cc` | Retoma donde quedaste (lee las notas de la última sesión) |
| `tema independiente: transformers` | Un tema fuera de los ramos |

**Cómo funciona una sesión:**

1. **Diagnóstico.** Quizzes cortos para encontrar dónde termina lo que sabes. No es una nota: equivocarse aquí es útil.
2. **Plan.** Te muestra el enfoque y un mapa de dependencias (qué va primero y por qué). **No empieza a enseñar hasta que digas que sí** (`dale`, `ok`, o pide cambios).
3. **Clases.** Un concepto a la vez: por qué importa, de dónde sale y cómo se conecta con lo anterior. Termina cada uno con un quiz; en ramos de cálculo o programación, también con un ejercicio tipo certamen.

**Responder quizzes:** escribe el número (`3`), varios si corresponde (`1 y 3`), o `0` / `no sé`. «No sé» no cuenta como error: le dice al agente dónde está tu límite. Si prefieres opciones clicables, pídelo (`hazme los quizzes con opciones clicables`).

**Consejos:**

- Usa **un hilo nuevo por sesión** y empieza con `seguir <ramo>`: los hilos muy largos degradan al modelo.
- Si algo te parece mal, dilo: el agente debe verificar en tu material o con Python, y corregir.
- Para cortar a mitad de una sesión, escribe `paremos aquí`: el agente actualiza las notas para retomar después.

## 6. Dónde queda todo

```
notas/
├── index.md                              ← temas activos
└── cc/minimos-cuadrados-qr/
    ├── _state.md                         ← qué sabes, plan, siguiente paso (para retomar)
    ├── sessions/2026-10-19-…md           ← la clase: quizzes, plan, conceptos, fuentes
    └── viz/                              ← gráficos generados
```

Puedes abrir `notas/` como bóveda en Obsidian para ver fórmulas y diagramas.

**Tus notas, tu material y `perfil.md` no se suben al repo** (están en `.gitignore`). Respáldalos por tu cuenta, por ejemplo con una carpeta sincronizada o un repo privado propio.

## 7. Actualizar el framework

```bash
git pull
```

Como tus archivos están ignorados por git, actualizar no los toca.

## 8. Limitaciones conocidas

- **No hay registro automático de la conversación.** El agente escribe la nota de la sesión mientras avanza; si algo falta, pídele `actualiza las notas`.
- **La respuesta de cada quiz vive solo en la memoria del modelo** hasta que respondes: no se muestra ni se guarda en archivos, pero tampoco está protegida técnicamente.
- **Gemini 3.8 Flash (High)** resolvió correctamente, con verificación numérica, una pregunta de 50 puntos de un C3 de Computación Científica. Aun así puede equivocarse, sobre todo con PDFs escaneados o manuscritos. Si algo no cuadra, pide `verifícalo en el material` o `verifícalo con Python`.
- Las instrucciones para el agente están en inglés a propósito (los modelos las siguen mejor). Todo lo que tú ves sale en español.

## 9. Estructura del framework

```
AGENTS.md                      ← instrucciones que el agente carga automáticamente
.agents/skills/
├── study-teach/               ← método: diagnóstico → plan → clases
├── study-research/            ← verificar en el material antes de afirmar
├── study-quiz/                ← cómo construir y corregir quizzes
├── study-visualize/           ← diagramas Mermaid y gráficos con Python
└── study-course-setup/        ← configurar un ramo nuevo
templates/                     ← plantillas de notas, estado y perfil de ramo
ramos/_ejemplo/                ← estructura de muestra
perfil.example.md              ← copia a perfil.md
```

Para cambiar el comportamiento, edita `AGENTS.md` o las skills.
