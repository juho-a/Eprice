<script>
    import chartjs from 'chart.js/auto';
    import { onMount } from "svelte";
    import { usePricesState } from "$lib/states/usePricesState.svelte";
    import { isTodayHelsinki } from '$lib/utils/date-helpers';
    import PriceCards from '$lib/components/PriceCards.svelte';

    // TODO: switch to stateful variables
    let priceCanvas;
    let priceChart;
    let prices = [];

    // Fetch prices on mount and after login/redirect
    const fetchPrices = async () => {
        const { data, update } = usePricesState();
        await update(); // Always fetch fresh data
        prices = data;
    }

    // Also fetch prices if the page becomes visible again (e.g. after login)
    if (typeof window !== "undefined") {
        window.addEventListener("visibilitychange", () => {
            if (document.visibilityState === "visible") fetchPrices();
        });
    }

    // TODO: switch to stateful variables
    let todayPrices = [];
    let todayValues = [];
    let labels = [];

    onMount(async () => {
        await fetchPrices();
        prices.sort((a, b) => new Date(a.startDate) - new Date(b.startDate));
        // todayPrices = prices.filter(p => isTodayHelsinki(p.startDate));
        // keep the first 24 hours of prices (Fix for Juho's issue)
        todayPrices = prices.slice(0, 24);
        todayValues = todayPrices.map(p => p.price);
        labels = todayPrices.map(p =>
            new Date(p.startDate).toLocaleTimeString('fi-FI', {
                timeZone: 'Europe/Helsinki',
                hour: '2-digit',
                minute: '2-digit'
            })
        );

        // Draw or update chart
        if (priceCanvas && labels.length) {
            if (priceChart) priceChart.destroy();
            priceChart = new chartjs(priceCanvas.getContext('2d'), {
                type: "bar",
                data: {
                    labels,
                    datasets: [{
                        label: 'Price (c/kWh)',
                        backgroundColor: 'rgba(10, 200, 245, 0.6)',
                        borderColor: 'rgb(10, 200, 245)',
                        data: todayValues
                    }]
                },
                options: {
                    responsive: true,
                    interaction: { mode: 'index', intersect: false },
                    plugins: { title: { display: false } },
                }
            });
        }
    });
</script>

<div class="max-w-3xl mx-auto mt-16">
    <h1 class="text-center text-3xl font-extrabold mb-8">
        Market Electricity Prices Today<br>
        <span class="text-xl">{new Date().toLocaleDateString('fi-FI', { timeZone: 'Europe/Helsinki' })}</span>
    </h1>
    <div class="shadow-lg p-4 border-1 border-primary-100 rounded-xl bg-white dark:bg-gray-800">
        <canvas bind:this={priceCanvas} id="priceChart" style="width:100%;height:400px;"></canvas>
    </div>
    <div class="py-8">
        <PriceCards values={todayValues} kind="price" unit="c/kWh"/>
    </div>
    <div class="text-center">
        <p class="text-lg">
            Want to see more features and get the full functionality of the app?
            <br />
            <a href="http://localhost:5173/auth/register" class="inline-block mt-6 px-4 py-2 bg-primary-500 text-white font-bold rounded hover:bg-primary-600 transition">
                Register for free
            </a>
        </p>
    </div>
</div>