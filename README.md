## Eprice app template

The python-server and Svelte client have registering and login implemented, and authentication using JWT. Otherwise everything is left open. 

In the client, there are some minimal components, mostly to serve as examples: `ChatBot.Svelte` (requires ollama to work, I'll add those later), `ChartExample.Svelte` (1,2 and 3) to show a couple of basic ways to get data to browser, both from protected and unprotected endpoints, using serverside api calls and browser api calls. 

In the client, there are some small examples on how to structure the client side code (api's, state management etc.).

There is also some example plots, using ChartJS, that fetch data using different mechanisms.
