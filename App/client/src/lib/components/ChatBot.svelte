<script>
    let chatOnState = $state(false);
    //let data = $props(); WE CAN GET THE USER INFO THIS WAY
    const toggleChat = () => {
        chatOnState = !chatOnState;
    };
    let user = $props();
</script>

<!-- Styles like chat-toggle are in app.css (mix with tailwind) -->
<button
    class="text-white font-bold py-2 px-8 rounded chat-toggle {chatOnState ? '' : 'hidden'}"
    onclick={toggleChat}>
    {chatOnState ? 'Hide Chat' : 'Open Chat'}
</button>

{#if chatOnState}
    <div class="gradio-embed" style="position: fixed; bottom: 0; right: 0; width: 400px; height: 800px; z-index: 9999;">
        <iframe title="Gradio App"
            src="http://localhost:7860/"
            width="100%"
            height="100%"
            frameborder="20"
            allowfullscreen
            name="gradio-iframe"
            sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
        ></iframe>
    </div>
{/if}
