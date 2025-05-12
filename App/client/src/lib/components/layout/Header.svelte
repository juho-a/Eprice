<script>
  let { user } = $props();
</script>

<header class="flex items-center justify-between bg-black p-4 mb-6 border-b-1">
<!--<header class="flex items-center bg-primary-300 p-4 mb-6">-->
  <h1 class="text-2xl text-white">Electricity prices</h1>
    <nav>
      <ul class="ml-4 flex space-x-4 text-white">
        <li>
          <a href="/" class="">Home</a>
        </li>
        {#if user}
        <li>
          <p>Placeholder</p>
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
    {#if user}
      <div class="ml-auto">
        <a href="/logout"  data-sveltekit-reload data-sveltekit-preload-data="false" 
        class="btn bg-primary-300 hover:bg-primary-500 text-white">Logout</a>
      </div>
    {/if}
</header>