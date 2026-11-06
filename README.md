# T3 Study

Una skill de estudio para [T3 Code](https://github.com/pingdotgg/t3code), inspirada en [amosblomqvist/learn](https://github.com/amosblomqvist/learn). Sirve para ramos universitarios y temas independientes: diagnóstico → plan aprobado → enseñanza por conceptos, con quizzes y apuntes opcionales.

**El modo de estudio se activa solo cuando lo invocas.** Abrir un ramo, preguntar una duda, trabajar en código o decir “continuar” fuera de una lección no crea apuntes ni inicia un diagnóstico.

```text
Codex: $t3-study estudiar cc, mínimos cuadrados
Claude: /t3-study tema independiente: transformers
```

En otros proveedores de T3 que lean `AGENTS.md`, pide explícitamente: `Usa la skill t3-study de skills/t3-study/SKILL.md para estudiar cc`. La compatibilidad de herramientas depende del proveedor; el flujo dispone de una alternativa sin subagentes.

## Empezar

1. Clona el repo y abre su carpeta en T3 como proyecto:

   ```text
   git clone https://github.com/AndrewwAM/t3-study.git
   ```

2. Selecciona el proveedor/modelo que hará de profesor en el hilo. El framework no cambia esa elección ni tus preferencias globales.
3. Opcionalmente, copia `perfil.example.md` a `perfil.md` y completa idioma, nombre y preferencias. Sin perfil, el agente usa español y te trata de “tú”.
4. Agrega material en `ramos/<sigla>/material/` y pide `$t3-study configurar ramo <sigla>` (o `/t3-study ...` en Claude). Para un tema independiente puedes saltar este paso.
5. Invoca la skill para estudiar. La primera vez en un workspace/equipo sin perfil de modelos, te propondrá una configuración disponible en tu T3 y esperará tu elección.

Los adaptadores para Codex y Claude ya vienen en el repositorio como archivos normales; no necesitas enlaces simbólicos, instalar una skill global ni permisos de administrador. Puedes abrir una subcarpeta de ramo: las instrucciones resuelven las rutas desde la ubicación real de la skill. Si el cliente no descubre skills de carpetas superiores, abre el proyecto raíz o indica el archivo compartido explícitamente.

Después de actualizar instrucciones o cambiar de versión, abre un hilo nuevo: una conversación existente puede conservar reglas anteriores.

## Uso

Los ejemplos usan Codex; en Claude reemplaza `$t3-study` por `/t3-study`.

```text
$t3-study estudiar cc para el C2
$t3-study practicar cc C2
$t3-study seguir cc
$t3-study tema independiente: redes neuronales
$t3-study estudiar cc, interpolación, sin guardar apuntes
$t3-study configurar modelos
$t3-study configurar ramo cc
```

Dentro de una lección activa puedes responder quizzes y decir `continuar` sin invocar otra vez la skill. `Salir del modo estudio` o cambiar a una tarea corriente termina ese flujo. Configurar cursos o modelos es mantenimiento: no inicia una clase ni exige aprobar un plan pedagógico.

El diagnóstico localiza lo que ya entiendes y lo que aún no. Luego el agente presenta el plan y espera tu aprobación antes de enseñar. Responde los quizzes en chat: `2`, `1 y 3`, `no sé` o tu desarrollo. Las soluciones no se guardan en archivos antes de que respondas.

## Modelos de los subagentes

El profesor conserva el modelo del hilo. Hay tres roles opcionales: investigación, diagramas Mermaid y gráficos/geometría. El agente puede ejecutarlos por sí mismo o delegarlos con T3.

En la primera configuración, la skill:

1. Consulta la identidad del entorno y los proveedores/modelos reportados por `orchestrator_capabilities`.
2. Excluye proveedores deshabilitados y comprueba las opciones que admite cada modelo.
3. Sugiere una combinación razonada para los roles y pregunta si aceptas, personalizas o prefieres trabajar sin subagentes.
4. Guarda la elección solo después de tu respuesta en `study-models.json`, separado por `environmentId` del equipo.

No se distribuyen proveedores personales, nombres de modelos fijos ni una configuración de otro usuario. Los perfiles existentes se reutilizan; no hay sustituciones silenciosas. Cuando el catálogo es parcial, un modelo ausente se trata como no verificado y se busca antes de descartarlo. Las sugerencias no son un benchmark ni una garantía de precio o cuota.

Puedes mezclar proveedores si T3 lo permite: por ejemplo, un profesor de Claude con un investigador de otro proveedor. La autenticación y los límites reales se comprueban al ejecutar una tarea necesaria, no lanzando agentes de prueba durante la configuración.

Para cambiar el perfil, invoca `configurar modelos` o edita `study-models.json`. El [esquema y procedimiento](skills/t3-study/references/models.md) describen las opciones. El helper portable usa únicamente Python estándar:

```text
python scripts/study_models.py show
python scripts/study_models.py check --environment ID --catalog /ruta/catalogo.json
python scripts/study_models.py set --environment ID --catalog /ruta/catalogo.json --profile /ruta/perfil.json
```

Usa `python3` o `py` si ese es tu comando de Python. `check` y `set` reciben una instantánea real del catálogo de T3; no consultan proveedores ni inician clases. Desde otra carpeta, ejecuta el script por su ruta absoluta y usa `--workspace /ruta/t3-study`.

Sin herramientas de descubrimiento de T3, el agente explica la limitación y ofrece estudiar sin subagentes. Si falta Python, puede revisar la configuración contra el catálogo sin afirmar que ejecutó el validador.

## Material y notas

```text
ramos/<sigla>/
├── curso.md                 # programa, evaluaciones, unidades y mapa de fuentes
├── material/                # material actual: programa, diapositivas, guías, notebooks
└── material-adicional/      # fuentes adicionales y evaluaciones de otros semestres

notas/
├── index.md
├── <sigla>/<tema>/
│   ├── _state.md
│   ├── sessions/FECHA-tema.md
│   └── viz/
└── independiente/<tema>/
    ├── _state.md
    └── sessions/FECHA-tema.md
```

El material actual determina el alcance de las evaluaciones. El adicional sirve para practicar; el agente debe señalar diferencias de notación, alcance o teoría. Los archivos fuente se preservan. Cada pregunta usa un conjunto acotado de archivos, no una lectura completa del ramo.

Con una lección activa, **guardar apuntes es el comportamiento predeterminado**: el agente registra progreso real, fuentes y quizzes ya corregidos, usando `templates/`. Puedes abrir `notas/` en Obsidian, pero no es obligatorio. Puedes retomar con otro proveedor leyendo el mismo estado.

Si pides **“sin guardar apuntes”**, no se crean ni actualizan notas, índices, estados o figuras persistentes. El agente usa archivos temporales solo para cálculos/gráficos necesarios. Una selección de modelos puede mantenerse solo en la conversación; guardar configuración requiere tu elección separada. Retomar sin apuntes depende del historial del chat.

El repo no incluye servidor de pizarra ni transcripción automática. Los quizzes son por chat y el agente escribe los apuntes; no tienes que copiarlos tú. Por defecto, las fórmulas del chat usan Unicode y las notas usan LaTeX. Puedes cambiar la preferencia si tu cliente renderiza LaTeX.

Tus notas, cursos personales, `perfil.md` y `study-models.json` están ignorados por Git. Respáldalos aparte; no se suben automáticamente ni se incluyen en los cambios del framework.

## Dependencias opcionales

La lección en chat no necesita un servidor ni una base de datos. Para el validador de modelos usa Python 3.11 o posterior. Para cálculos y figuras, instala NumPy/SciPy/matplotlib en el entorno Python que uses; para PDFs sin lector nativo, Poppler aporta `pdftotext`. Obsidian es opcional.

Puedes preparar un entorno Python aislado:

```text
python -m venv .venv
```

Linux/macOS:

```text
.venv/bin/python -m pip install numpy scipy matplotlib
```

Windows:

```text
.venv\Scripts\python.exe -m pip install numpy scipy matplotlib
```

Indica al agente ese Python si no está activo en su terminal. Si una dependencia falta, debe explicar qué comprobación no pudo hacer y ofrecer una alternativa; no afirmar que verificó un cálculo o una imagen que no pudo revisar.

## Actualizar desde la versión anterior

```text
git pull --ff-only
```

Si tienes cambios propios en archivos del framework, revísalos antes de actualizar y resuelve cualquier conflicto conservando tu trabajo. El refactor mantiene `ramos/`, `notas/`, `perfil.md` y las plantillas: no hay migración destructiva de material o sesiones.

Los antiguos `.agents/skills/study-*` pasan a ser referencias internas. La única entrada de estudio es `t3-study`. `AGENTS.md` deja de cargar el método pedagógico por defecto y `CLAUDE.md` importa solo las reglas generales.

Abre un hilo nuevo y usa `$t3-study seguir <ramo>` o `/t3-study seguir <ramo>`. Decir solamente `estudiar` ya no activa el sistema. Si habías instalado copias globales de las skills antiguas por tu cuenta, revisa esas copias: actualizar este repo no las elimina.

## Desarrollo y límites de verificación

```text
python -B -m unittest discover -s tests -v
git diff --check
```

Las pruebas usan workspaces, perfiles y catálogos ficticios en directorios temporales. Comprueban la configuración inicial, validación de opciones/proveedores, conservación de otros perfiles y funcionamiento desde subcarpetas. No hacen llamadas a modelos ni escriben apuntes personales. CI ejecuta el helper en Linux, macOS y Windows; eso no certifica todas las combinaciones de proveedor/modelo ni una lección completa.

El modelo puede equivocarse y las reglas de activación son instrucciones del agente, no un aislamiento de permisos. Verifica fuentes y resultados relevantes. El contenido de una skill ya usada puede permanecer en el contexto de un hilo; utiliza otro hilo si necesitas una separación completa entre estudio y trabajo.

## Estructura del framework

```text
AGENTS.md                         # límites generales, sin enseñanza automática
CLAUDE.md                         # importa esos límites
.agents/skills/t3-study/           # entrada explícita de Codex
.claude/skills/t3-study/            # entrada explícita de Claude
skills/t3-study/SKILL.md           # flujo compartido
skills/t3-study/references/        # módulos internos y configuración de modelos
scripts/study_models.py            # validador portable, sin dependencias externas
templates/                        # notas, estado, curso e índice
ramos/_ejemplo/                    # estructura de muestra
perfil.example.md                 # preferencias opcionales del estudiante
tests/                            # pruebas aisladas
```

Edita la skill compartida o sus referencias para cambiar el método. Mantén las instrucciones pedagógicas fuera de `AGENTS.md` para que no afecten tareas normales.
