// src/routes/protected/+page.server.js
import { redirect } from '@sveltejs/kit';
import { COOKIE_KEY } from "$env/static/private";

// This function checks if the user is authenticated by looking for a session cookie.
export async function load({ cookies }) {
	const session = cookies.get(COOKIE_KEY);

	if (!session) {
		throw redirect(302, '/auth/login');
	}

	// Optionally pass user session data to the page:
	return {
		user: { session }
	};
}
