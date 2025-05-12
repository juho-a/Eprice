<script lang="ts">
    let { heading } = $props();  
</script>

<div class="flex flex-col justify-center items-center rounded-full bg-blue-500 w-50 h-50">
    <p class="font-bold">{heading}</p>
    <span>(hinta tähän)</span>
</div>