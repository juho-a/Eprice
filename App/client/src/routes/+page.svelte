<script>
    import ChartExample3 from "$lib/components/ChartExample3.svelte";
    //let { data, form } = $props();
    
</script>

<h1 id="mainheading" class="text-center">
    Welcome!<br>
    <span class="text-2xl">Market Electricity Prices<br> {new Date().toLocaleDateString()}</span>
    <br>
</h1>

<ChartExample3 />