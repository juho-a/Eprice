<script>
    import chartjs from 'chart.js/auto';
    import { onMount } from 'svelte';
    import { usePricesState } from '$lib/states/usePricesState.svelte';

    let { chartType } = $props();
    let currentChart = chartType || 'bar'; // Default to 'bar' if no chart type is provided

    let prices = usePricesState();
    let ctx;
    let chartCanvas;

   
   onMount(async () => {
    // Get the raw API data (array of objects)
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
<canvas bind:this={chartCanvas} id="myChart" class="
    w-full
    bottom-10
    top-10
    m-auto
    rounded"
    style="width: 100%; background-color: #1e1e2f;"
></canvas>


