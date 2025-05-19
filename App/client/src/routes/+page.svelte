<script>
    import PriceBall from "$lib/components/layout/PriceBall.svelte";
    import ChartExample from "$lib/components/ChartExample.svelte";

    import { onMount } from "svelte";
    import { usePricesState } from "$lib/states/usePricesState.svelte";

    const { data: pricesState, update } = usePricesState();


    const averageDayPrice = array => array.reduce((a, b) => a + b) / array.length;

    let currentPrice = null; // Default value for current price
    let prices = null; // Store the fetched prices
    let loading = true; // Loading state
    let error = null; // Error state
    let dailyAverage = null; // Store the calculated daily average

    // Calculate the current price and daily average
    $: {
        if (pricesState) {
            console.log("Chart Values:", pricesState);
            const now = new Date();
            const currentHour = now.getHours();
            const currentDate = now.toISOString().split("T")[0];

            // Find the current price
            const matchingPrice = pricesState.find(price => {
                const priceDate = new Date(price.startDate);
                return (
                    priceDate.getUTCHours() === currentHour &&
                    priceDate.toISOString().startsWith(currentDate)
                );
            });

            currentPrice = matchingPrice ? matchingPrice.price : "N/A";

            // Calculate the daily average
            dailyAverage = averageDayPrice(pricesState.map(p => p.price));
            dailyAverage = dailyAverage.toFixed(3); // Format to 2 decimal places
        }
    }

    onMount(async () => {
        // Fetch data from the API
        try {
            await update();
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
       <PriceBall heading="Sähkönhinta NYT" price={currentPrice}/>
       <PriceBall heading="Sähkö 24h" price={dailyAverage}/>
       <PriceBall heading="Sähkö viikko" />
        
    </div>
    <ChartExample />   
</main>