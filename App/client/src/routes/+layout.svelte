<script>
    import "../app.css";
    import bg from "$lib/assets/image.png";
    import { useUserState } from "$lib/states/userState.svelte.js";
    import Header from "$lib/components/layout/Header.svelte";
    import Footer from "$lib/components/layout/Footer.svelte";
    import ChatBot from "$lib/components/ChatBot.svelte";

    
    let { children, data } = $props();
    const userState = useUserState();
    if (data.user) {
      userState.user = data.user;
    }

  </script>

<div class="flex flex-col h-full">
  
  
  <Header user={data.user} />

  {#if data.user?.email}
    <p class="">
      Logged in as: <b>{data.user?.email}</b>
    </p>

    <!-- <ChatBot user={data.user} /> -->
  {/if}
  
  <main class="container mx-auto max-w-2xl grow">
    {@render children()}
  </main>

  <Footer />
  
</div>

<!--
<style>
  :global(body){
  background-image: url("https://images.pexels.com/photos/956981/milky-way-starry-sky-night-sky-star-956981.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260");
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-position: center;
  font-family: 'Poppins', sans-serif;
  font-size: 1.2rem
  }
</style>
-->