<script>
  import { page } from '$app/stores';
  let { user } = $props();
</script>

<header class="flex items-center justify-between bg-black/20 drop-shadow-xl backdrop-blur-lg p-4 mb-2">
<!--<header class="flex items-center bg-primary-300 p-4 mb-6">-->
  <h1 class="text-2xl text-white">Electricity prices</h1>
    <nav>
      <ul class="ml-4 flex space-x-4 text-white">
        <li>
          <a href="/" class="">Home</a>
        </li>
        {#if user}
        <li>
          <a href="/hintatiedot" class="">Hintatiedot</a>
        </li>
        {:else}
            <li>
              <a href="/auth/login" class="">Login</a>
            </li>
            <li>
              <a href="/auth/register" class="">Register</a>
          </li>
        {/if}
      </ul>
    </nav>
    {#if user?.role === 'admin'}
        <a href="/chat" class="text-white ml-4">Developer Chat</a>
    {/if}
    {#if user && $page.url.pathname !== '/logout'}
      <div class="ml-auto">
        <a href="/logout" class="underline text-white">Logout</a>
      </div>
    {:else if $page.url.pathname === '/logout'}
      <div class="ml-auto">
        <!--This is a hack to force the placement of other elements-->
      </div>
    {/if}
</header>