import { error } from "@sveltejs/kit";

export const load = ({ params, url }) => {
  if (params.action !== "login" && params.action !== "register" && params.action !== "verify") {
    throw error(404, "Page not found.");
  }

  if (url.searchParams.has("registered")) {
    params.registered = true;
  }

  if (url.searchParams.has("email")) {
    params.email = url.searchParams.get("email");
  } else {
    params.email = null;
  }

  if (url.searchParams.has("code")) {
    params.code = url.searchParams.get("code");
  } else {
    params.code = null;
  }

  return params;
};