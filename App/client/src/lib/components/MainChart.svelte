<script>
    import chartjs from 'chart.js/auto';
    import { onMount } from 'svelte';
    import { usePricesState } from '$lib/states/usePricesState.svelte';

    let { chartType } = $props();
    let currentChart = chartType || 'bar'; // Default to 'bar' if no chart type is provided

    let prices = usePricesState();
    let ctx;
    let chartCanvas;

    let cheapestPrice = $state(null);
	let cheapestTime = $state("");

    // Function to calculate the average price for the day
    const averageDayPrice = array => array.reduce((a, b) => a + b) / array.length;

    // Function to format date to UTC+0
    function formatDateToUTC(date) {
        return new Date(date).toISOString().split('T')[0];
    }

    // Function to format time for display
    function formatTime(date) {
        return new Date(date).toLocaleString('fi-FI', {
            timeZone: 'Europe/Helsinki',
            day: '2-digit',
            month: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }   

   
   onMount(async () => {
    // Get the raw API data (array of objects)
    await prices.load();
    if (!prices.data || prices.data.length === 0) {
        console.error('No price data available');
        return;
    }
    // Ensure prices.data is an array
    const priceData = prices.data;

    // Find the most recent startDate
    const mostRecent = priceData.reduce((latest, item) =>
        new Date(item.startDate) > new Date(latest.startDate) ? item : latest
    , priceData[0]);

    // Filter data to include only entries up to the most recent hour
    const filteredData = priceData.filter(item =>
        new Date(item.startDate) <= new Date(mostRecent.startDate)
    );

    // Sort by startDate ascending (optional, for chart order)
    filteredData.sort((a, b) => new Date(a.startDate) - new Date(b.startDate));


// 🔍 Find the cheapest price
    if (filteredData.length > 0) {
        const minEntry = filteredData.reduce((min, item) =>
            item.price < min.price ? item : min
        );

        cheapestPrice = minEntry.price.toFixed(3);
        cheapestTime = new Date(minEntry.startDate).toLocaleString('fi-FI', {
            timeZone: 'Europe/Helsinki',
            day: '2-digit',
            month: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    // Transform data for the chart
    const chartLabels = filteredData.map(item => {
        const date = new Date(item.startDate);
        const hour = String(date.getUTCHours()).padStart(2, '0');
        const minute = String(date.getUTCMinutes()).padStart(2, '0');
        return `${hour}:${minute}`;
    });
    // Get the price values for the chart
    const chartValues = filteredData.map(item => item.price);

    ctx = chartCanvas.getContext('2d');
    new chartjs(ctx, {
        type: currentChart,
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Sähkön hinta UTC(+0)',
                backgroundColor: 'rgb(70, 50, 255)',
                borderColor: 'rgb(255, 255, 255)',
                borderWidth: 1,
                barThickness: 10,
                minBarLength: 5,
                data: chartValues,     
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                x: {
                    ticks: {
                        maxRotation: 60,
                        minRotation: 60
                    }
                },
            },

			plugins: {
        	tooltip: {
            callbacks: {
                title: function(context) {
                    const idx = context[0].dataIndex;
                    const item = filteredData[idx];
                    const date = new Date(item.startDate);
                    const day = String(date.getUTCDate()).padStart(2, '0');
                    const month = String(date.getUTCMonth() + 1).padStart(2, '0');
                    const year = date.getUTCFullYear();
                    const hour = String(date.getUTCHours()).padStart(2, '0');
                    const minute = String(date.getUTCMinutes()).padStart(2, '0');
                    return `${day}.${month}.${year} ${hour}:${minute}`;
                }
            }
        }
    }
        },

    });
});
</script>
<div class="w-full flex flex-col justify-center mx-auto p-4">
    {#if cheapestPrice}
        <p class="text-md text-green-400 font-semibold mt-4 mb-2 text-center">
            Halvin hinta kaaviossa: {cheapestPrice} €/kWh ({cheapestTime})
        </p>
    {/if}
    <div class="relative w-full" style="min-height:300px; max-width: 600px;">
        <canvas bind:this={chartCanvas} id="myChart"
            class="m-auto rounded"
            style="display: block; height: 500px; background-color: #1e1e2f;"
        ></canvas>
    </div>
    
</div>

