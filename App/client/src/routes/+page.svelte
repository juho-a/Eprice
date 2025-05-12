<script>
    import PriceBall from "$lib/components/layout/PriceBall.svelte";
    import ChartExample from "$lib/components/ChartExample.svelte";
    import { onMount } from "svelte";
    import { usePricesState } from "$lib/states/usePricesState.svelte";

    const hour = new Date().getHours();
    const averageDayPrice = array => array.reduce((a, b) => a + b) / array.length;

    let prices = null; // Store the fetched prices
    let loading = true; // Loading state
    let error = null; // Error state
    let dailyAverage = null; // Store the calculated daily average

    onMount(async () => {
        // Fetch data from the API
        try {
            const response = await usePricesState();
            prices = response.data;

            if (prices?.chartValues) {
                dailyAverage = averageDayPrice(prices.chartValues);
            }
        } catch (err) {
            error = "Failed to fetch electricity prices.";
            console.error("Error fetching data:", err);
        }
    });
    //let { data, form } = $props();
</script>

<h1 id="mainheading" class="text-center">
    Welcome!<br>
    <span class="text-2xl">Market Electricity Prices<br> {new Date().toLocaleDateString()}</span>
    <br>
</h1>
<main class="flex gap-20">
    <div class="text-center gap-5 flex flex-col">
       <PriceBall heading="Sähkönhinta NYT" price={prices?.chartValues[hour]}/>
       <PriceBall heading="Sähkö 24h" price={Math.round(dailyAverage * 100) / 100}/>
       <PriceBall heading="Sähkö viikko" />
        
    </div>
    <ChartExample />   
</main>