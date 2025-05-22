<script>
    import chartjs from 'chart.js/auto';
    import { onMount } from 'svelte';
    import { usePricesState } from '$lib/states/usePricesState.svelte';

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
    const chartLabels = filteredData.map(item =>
        new Date(item.startDate).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false })
    );
    const chartValues = filteredData.map(item => item.price);

    ctx = chartCanvas.getContext('2d');
    new chartjs(ctx, {
        type: 'line',
        data: {
            labels: chartLabels,
            datasets: [{
                label: 'Sähkön hinta',
                backgroundColor: 'rgb(70, 50, 255)',
                borderColor: 'rgb(255, 255, 255)',
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
                }
            },

			plugins: {
        	tooltip: {
            callbacks: {
                title: function(context) {
                    // Get the index of the hovered item
                    const idx = context[0].dataIndex;
                    const item = filteredData[idx];
                    const date = new Date(item.startDate);
                    // Format: "21.05.2025 21:00"
                    const day = String(date.getDate()).padStart(2, '0');
					const month = String(date.getMonth() + 1).padStart(2, '0');
					const year = date.getFullYear();
					const time = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
					return `${day}.${month}.${year} ${time}`;
                }
            }
        }
    }
        },

    });
});
</script>

<canvas bind:this={chartCanvas} id="myChart" class="
	bottom-10
	top-10
	m-auto
	rounded"
 style="width: 100%;background-color: #1e1e2f;"
></canvas>

