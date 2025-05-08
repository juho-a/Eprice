
## Eprice app template

Set up: run `deno install --allow-scripts` in client folder. Create `.env.local` in client folder -- same in the python-server folder -- these should not go into git. Ask values in Discord. Let's keep the `node_modules/` (as with .env.local files) out of git. But for now, you should have these locally on client even if you run with docker (they get copied into container).

Run containers: `docker compose up --build` or `docker compose up -d <service>` if you only want to run specific service (all services in `compose.yaml` file). You can stop the containers with control-C or `docker compose down`.

The python-server and Svelte client have registering and login implemented, and authentication using JWT. Otherwise everything is left open. 

In the client, there are some minimal components, mostly to serve as examples: `ChatBot.Svelte` (requires ollama to work, I'll add those later), `ChartExample.Svelte` shows how to get data from unprotected endpoint. 

In the client, there are some small examples on how to structure the client side code (api's, state management etc.).

There is also some example plots, using ChartJS, that fetch data using different mechanisms.

The links in the client header panel are defined in `client/src/lib/components/layout/`.
