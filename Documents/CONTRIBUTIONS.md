# Contributions



├── LICENSE
├── README.md
├── App
│   ├── README.md
│   ├── compose.yaml (anything with containers, Paavo)
│   ├── project.env (anything with project and container level configurations, Paavo)
│   │
│   ├── backend-tests (Setup, Paavo)
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   └── tests
│   │       ├── test_auth_controller.py (Juho & Paavo)
│   │       └── test_data_controller.py (Juho)
│   │
│   ├── chat-engine (Paavo)
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   ├── _compose.yaml
│   │   ├── agent_app.py
│   │   ├── agent_manager.py
│   │   ├── app.py
│   │   ├── autoloading_uml.py
│   │   ├── chat_app.py
│   │   ├── chat_manager_with_tools.py
│   │   ├── file_app.py
│   │   ├── diagrams
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── db_calls.py
│   │       ├── helpers.py
│   │       └── tools.py
│   │
│   ├── client (Paavo)
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   ├── docker
│   │   ├── src
│   │   │   ├── app.css
│   │   │   ├── app.html
│   │   │   ├── hooks.server.js
│   │   │   ├── lib
│   │   │   │   ├── apis
│   │   │   │   │   └── data-api.js
│   │   │   │   ├── assets
│   │   │   │   │   ├── image12.jpg
│   │   │   │   │   └── image3.png
│   │   │   │   ├── components
│   │   │   │   │   ├── ChatBot.svelte
│   │   │   │   │   ├── ChatView1.svelte
│   │   │   │   │   ├── ChatView2.svelte
│   │   │   │   │   ├── ChatView3.svelte
│   │   │   │   │   ├── ChatView4.svelte
│   │   │   │   │   ├── PriceCards.svelte
│   │   │   │   │   ├── Tabs.svelte
│   │   │   │   │   └── layout
│   │   │   │   │       ├── Clock.svelte
│   │   │   │   │       ├── Footer.svelte
│   │   │   │   │       ├── Header.svelte
│   │   │   │   │       └── User.svelte
│   │   │   │   ├── states
│   │   │   │   │   ├── usePricesState.svelte.js
│   │   │   │   │   └── userState.svelte.js
│   │   │   │   └── utils
│   │   │   │       ├── clock.js
│   │   │   │       ├── date-helpers.js
│   │   │   │       └── stats-helpers.js
│   │   │   └── routes
│   │   │       ├── +layout.js
│   │   │       ├── +layout.server.js
│   │   │       ├── +layout.svelte
│   │   │       ├── +page.svelte
│   │   │       ├── api
│   │   │       │   └── devchat
│   │   │       │       └── +server.js
│   │   │       ├── auth
│   │   │       │   └── [action]
│   │   │       │       ├── +page.js
│   │   │       │       ├── +page.server.js
│   │   │       │       └── +page.svelte
│   │   │       ├── chat
│   │   │       │   └── +page.svelte
│   │   │       ├── epc
│   │   │       │   ├── +page.server.js
│   │   │       │   └── +page.svelte
│   │   │       ├── logout
│   │   │       │   ├── +page.js
│   │   │       │   ├── +page.server.js
│   │   │       │   └── +page.svelte
│   │   │       ├── price
│   │   │       │   ├── +page.server.js
│   │   │       │   └── +page.svelte
│   │   │       └── send
│   │   │           ├── +page.server.js
│   │   │           └── +page.svelte
│   │   └── static
│   │       └── favicon.png
│   │
│   ├── data-preparation (Paavo)
│   │   ├── README.md
│   │   └── scripts
│   │       ├── Dockerfile
│   │       ├── README.md
│   │       ├── clean_porssisahko.py
│   │       ├── populate_porssisahko.py
│   │       └── retrieve_porssisahko_update.sh
│   │
│   ├── database-migrations (Paavo)
│   │   ├── V1__users.sql
│   │   ├── V2__porssisahko.sql
│   │   ├── V3__timezone.sql
│   │   ├── V4__users_add_role.sql
│   │   ├── V5__porssisahko_load_entries.sql
│   │   ├── V6__users_add_isverified.sql
│   │   │   None (bad version naming -- accidentally missed V7)
│   │   ├── V8__extension_vector.sql
│   │   └── V9__code.sql
│   │   ├── V10__code_constraint.sql
│   │   ├── V11__documents.sql
│   │   ├── V12__files.sql
│   │
│   ├── e2e-tests (Setup, Paavo)
│   │   ├── Dockerfile
│   │   └── tests
│   │       └── frontend.spec.js
│   │
│   ├── python-server (Juho & Paavo)
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   ├── main.py (Juho & Paavo)
│   │   ├── requirements.txt
│   │   ├── config
│   │   │   ├── __init__.py
│   │   │   └── secrets.py
│   │   ├── controllers
│   │   │   ├── auth_controller.py (Juho & Paavo)
│   │   │   └── data_controller.py (Juho)
│   │   ├── ext_apis
│   │   │   └── ext_apis.py (Juho)
│   │   ├── models
│   │   │   ├── custom_exception.py (Juho)
│   │   │   ├── data_model.py (Juho)
│   │   │   └── user_model.py (Paavo)
│   │   ├── repositories
│   │   │   ├── porssisahko_repository.py (Paavo)
│   │   │   └── user_repository.py (Paavo)
│   │   ├── scheduled_tasks
│   │   │   └── porssisahko_scheduler.py (Paavo)
│   │   ├── services
│   │   │   ├── auth_service.py (Paavo)
│   │   │   └── data_service.py (Juho)
│   │   └── utils
│   │       ├── email_tools.py (Paavo)
│   │       ├── porssisahko_service_tools.py (Juho)
│   │       └── porssisahko_tools.py (Paavo)
│   │
│   └── user-chat (Setup, Paavo)
│       ├── Dockerfile
│       ├── README
│       ├── gradio_dashboard.py
│       └── run.sh
│
└── Documents
    ├── README.md
    ├── backend_design.md
    ├── openapi_endpoint_descriptions.md
    ├── project_description.md
    ├── project_directory_structure.txt
    ├── api_definitions
        ├── openapi.json
        ├── README.md
    └── diagrams
        └── sources
            ├── authentication_call_sequence_diagram.wsd
            ├── authentication_class_diagram.wsd
            ├── authentication_use_case.wsd
            ├── data_access_call_sequence_diagram.wsd
            ├── llm_retrieval.wsd
            ├── services_diagram.wsd
            ├── tool_calling.wsd
            └── use_case.wsd


## Notebooks

Additionally, the project/developer chat's retrieval mechanism requires some amount of parsing/cleaning/loading (all project code and documents), which is done offline using scripts and `document_loading.ipynb` inside `Eprice/Notebooks/`. These are at least in some parts based on Paavo's (heh, me in 3rd person...) other previous and contemporary projects/works. Not everything is included in this repo, but will be later made available in `https://github.com/PaavoReinikka`. 

To aid in the documentation of the project, there is also a UML diagram generator dashboard in `Eprice/Notebooks/` (using PlantUML syntax). It was written with Python (see Notebooks README for details and instructions).

## User Chat

User chat is based on Ollama served Llama 3.2 model, which is fully open-source and free. The chat is pretty much just a template / placeholder, to demonstrate it is also possible to include an open-source llm in a containerized app. However, to get good performance from the model, it does require fine-tuning, and/or (ideally) a slightly bigger model -- cuda capable gpu is not mandatory, unless training, and the smaller models run fine on modern cpu's. In the time constraints of this project, it was not feasible to fine-tune the model (within a timeframe of roughly 4-6 weeks). Acquiring and preparing data for fine-tuning is also very time consuming.

## Developer chat

The developer chat is based on OpenAI's gtp-4o-mini, which is basically free for research (and such) purposes. There are also a lot of open-source generative text models (chat and completion) in HF, and also good datasets for fine-tuning. Some of the experiments, with various open models, during this project will eventually be published in `https://github.com/PaavoReinikka`.

The embedding model used here, is open-source from HuggingFace. There are many good models available at HF, and a there is a leader board for embedding models, which is a good place to start looking (`https://huggingface.co/spaces/mteb/leaderboard`).

## Documentation

Most of the documentation was written by Paavo Reinikka, with some help from Juho Ahopelto, and with a lot of help from Copilot.

