### Containerized Eprice app template

**Install docker and docker compose**. Maybe easiest to just install docker desktop, especially on windows.

**Postgres is not needed on local machine** (unless you want to run outside containers).

**Install Deno** (see client folder).

The compose.yaml and the individual Dockerfiles are sufficient to run the App. Docker does the installing for the containers. But you can still run `deno install --allow-scripts`, if you want to run on local host. On windows, after running deno install, `node_modules/` that are loaded into client should not be copied into the container -- the container is using arch-linux as base image. You can either remove those, or add your own `.dockerignore` file.

Run using docker compose:

`docker compose up --build` (no need to build everytime)

You can also simply `ctrl+C` to shut down the containers, or

`docker compose down` to tear down.


#### Run the Playwright e2e tests

When the containers are up and running, in another terminal run:

`docker compose run --rm --entrypoint=npx e2e-tests playwright test`

We can also eventually modify the compose.yaml so that the tests are automatically run when the app is launched.


#### Running without Docker

Can be done, but needlessly cumbersome. Ask Paavo for the how.
