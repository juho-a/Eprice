### Client/front template for Eprice app

You need to have deno installed: https://docs.deno.com/runtime/

* missing project.env -- ask Paavo for this.

* run this with docker compose.

* first run `deno install --allow-scripts` in `client/` and `e2e-tests/` directories. This is likely to change in the future, but for now the denoland's alpine base image does not allow installing with optional flags.

**CHANGE**: Running deno install locally is now optional. 

---

# Eprice Frontend

This is the frontend for the Eprice application, built with Svelte. It displays real-time and historical electricity prices for users in a clear and interactive way.

## Features

- **Current Price Display:** Shows the current hour’s electricity price.
- **Daily & Weekly Averages:** Calculates and displays average prices for today and the past week.
- **Interactive Chart:** Visualizes price data over time.
- **Responsive UI:** Built with Svelte components for a modern, mobile-friendly experience.
- **User Authentication:** Register, login, verify, and remove accounts.
- **Production/Consumption Comparison:** View and compare electricity production and consumption data.
- **Theme Switching:** Change the UI theme from the footer.

## Main Components

- src/routes/**+page.svelte**  
  The main landing page. Fetches price data, calculates averages, and renders:
  - `MainChart` for visualizing daily price.

- src/routes/price/**+page.svelte**  
  A page for selecting a custom date range and viewing a table and chart of prices.

- src/routes/epc/**+page.svelte**  
  Shows production, consumption, and price data with interactive charts and filters.

- src/components/layout/**Header.svelte**  
  Navigation bar with links that adapt based on authentication state and user role.

- src/components/layout/**Footer.svelte**  
  Footer with theme-switching buttons.

- src/components/layout/**User.svelte**  
  Displays the currently logged-in user's email.

- src/components/layout/**Clock.svelte**  
  Shows the current time, updating every second.

## Authentication

- Users can register, login, verify their email, and remove their account via forms in the `/auth/[action]` route.
- Authentication state is reflected in the header and enables additional features.

## Theming

- Users can switch between several color themes using buttons in the footer. The selected theme is applied to the whole app.

## Testing

- **Playwright** is used for end-to-end testing.  
  Test files are located in `../../e2e-tests/tests/`.

## Tech Stack

- [Svelte](https://svelte.dev/)
- [Vite](https://vitejs.dev/) (for development/build)
- Fetch API for data requests
- Playwright for end-to-end testing
- Docker (for development and deployment)


