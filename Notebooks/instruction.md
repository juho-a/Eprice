# Helper for making UML diagrams

## dependencies

Python dependencies: `gradio` and nothing else.

To render plantuml graphs, install following system dependencies:

- `sudo apt-get install default-jre`
- `wget -O ~/plantuml.jar https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar`

you may also need to install **`graphviz`** (available on most linux systems as a package).

## Running the UML dashboard

with wither using system python (assuming gradio is installed in it), or with appropriate venv active, run:

```bash
python uml_app.py
```

## Usage

You can use standard plantUML syntax. No need to pre-/append `@startuml` and `@endtuml` tags. Write your diagrams source code and submit, and the diagram get's generated. Or, if you have syntax errors, the errors will be displayed.
