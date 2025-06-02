<script>
    import chartjs from 'chart.js/auto';
    import { onMount } from "svelte";
    import { usePricesState } from "$lib/states/usePricesState.svelte";
    import PriceCards from '$lib/components/PriceCards.svelte';

    let priceCanvas;
    let priceChart;

    // Local reactive prices array
    let prices = [];

    // Helper: get today's date in Helsinki
    function isTodayHelsinki(dateStr) {
        const d = new Date(dateStr);
        const today = new Date().toLocaleDateString('fi-FI', { timeZone: 'Europe/Helsinki' });
        const dDate = d.toLocaleDateString('fi-FI', { timeZone: 'Europe/Helsinki' });
        return dDate === today;
    }

    // Fetch prices on mount and after login/redirect
    async function fetchPrices() {
        const { data, update } = usePricesState();
        await update(); // Always fetch fresh data
        prices = data;
    }

    onMount(fetchPrices);

    // Also fetch prices if the page becomes visible again (e.g. after login)
    if (typeof window !== "undefined") {
        window.addEventListener("visibilitychange", () => {
            if (document.visibilityState === "visible") fetchPrices();
        });
    }

    // Reactive: today's prices and chart
    let todayPrices = [];
    let todayValues = [];
    let labels = [];

    $: {
        todayPrices = prices.filter(p => isTodayHelsinki(p.startDate));
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
                        backgroundColor: 'rgba(0, 200, 255, 0.6)',
                        borderColor: 'rgb(0, 200, 255)',
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
    }
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