import { PUBLIC_INTERNAL_API_URL } from "$env/static/public";
import { redirect } from "@sveltejs/kit";
import { COOKIE_KEY } from "$env/static/private";

const apiRequest = async (url) => {
  return await fetch(`${PUBLIC_INTERNAL_API_URL}${url}`, {
    method: "GET",
  });
};

export const actions = {

  logout: async ({ cookies, locals }) => {
    const response = await apiRequest("/api/auth/logout");
    if (response.ok) {
      cookies.delete(COOKIE_KEY, { path: "/"});
      //TODO: clear locals
      // locals.user = undefined; // Clear user session in locals
      throw redirect(302, "/");
    } else {
      return { error: "Logout failed" };
    }
  }

};
