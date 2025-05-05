<script>
    import ChartExample from "$lib/components/ChartExample.svelte";
    //let { data, form } = $props();
    
</script>

<h1 id="mainheading" class="text-center">
    Welcome!<br>
    <span class="text-2xl">Market Electricity Prices<br> {new Date().toLocaleDateString()}</span>
    <br>
</h1>

<ChartExample />