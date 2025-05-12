<script>
    import PriceBall from "$lib/components/layout/PriceBall.svelte";
    import ChartExample from "$lib/components/ChartExample.svelte";
    //let { data, form } = $props();
</script>

<h1 id="mainheading" class="text-center">
    Welcome!<br>
    <span class="text-2xl">Market Electricity Prices<br> {new Date().toLocaleDateString()}</span>
    <br>
</h1>
<main class="flex gap-20">
    <div class="text-center gap-5 flex flex-col">
       <PriceBall heading="Sähkönhinta NYT" />
       <PriceBall heading="Sähkö 24h" />
       <PriceBall heading="Sähkö viikko" />
        
    </div>
    <ChartExample />   
</main>