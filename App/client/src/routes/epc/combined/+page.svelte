<script>
    import chartjs from 'chart.js/auto';
    import { enhance } from '$app/forms';
    import { onMount } from 'svelte';

    let { form } = $props();
    let startTime = $state(form?.startTime || "");
    let endTime = $state(form?.endTime || "");
    let selection = $state(form?.selection || "both");

    let labels = form?.labels || [];
    let productionValues = form?.productionValues || [];
    let consumptionValues = form?.consumptionValues || [];
    let differenceValues = form?.differenceValues || [];

    let bothCanvas, diffCanvas;
    let bothChart, diffChart;
    let chartType = $state("line");

    let isLoading = $state(false);

    const toggleChartType = () => {
        chartType = chartType === "line" ? "bar" : "line";
        bothChart.config.type = chartType;
        diffChart.config.type = chartType;
        bothChart.update();
        diffChart.update();
    };


    const getBothDatasets = () => {
        return [
            {
                label: 'Production',
                backgroundColor: 'rgba(245, 39, 157, 0.2)',
                borderColor: 'rgb(245, 39, 157)',
                data: productionValues,
                yAxisID: 'y',
            },
            {
                label: 'Consumption',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgb(54, 162, 235)',
                data: consumptionValues,
                yAxisID: 'y',
            }
        ];
    }

    const getDiffDatasets = () => {
        return [
            {
                label: 'Production - Consumption',
                backgroundColor: 'rgba(157,39, 245, 1)',
                borderColor: 'rgb(157,39, 245)',
                data: differenceValues,
                yAxisID: 'y',
            }
        ];
    }

    onMount(() => {
        // Both chart
        bothChart = new chartjs(bothCanvas.getContext('2d'), {
            type: chartType,
            data: {
                labels,
                datasets: getBothDatasets()
            },
            options: {
                responsive: true,
                interaction: { mode: 'index', intersect: false },
                stacked: false,
                plugins: {
                    title: { display: false }
                },
                scales: {
                    y: { type: 'linear', display: true, position: 'left' }
                }
            }
        });
        // Difference chart
        diffChart = new chartjs(diffCanvas.getContext('2d'), {
            type: chartType,
            data: {
                labels,
                datasets: getDiffDatasets()
            },
            options: {
                responsive: true,
                interaction: { mode: 'index', intersect: false },
                stacked: false,
                plugins: {
                    title: { display: false }
                },
                scales: {
                    y: { type: 'linear', display: true, position: 'left' }
                }
            }
        });
    });

    // Update charts after form submit
    $effect(() => {
        if (form?.labels && bothChart && diffChart) {
            labels = form.labels;
            productionValues = form.productionValues || [];
            consumptionValues = form.consumptionValues || [];
            differenceValues = form.differenceValues || [];
            startTime = form.startTime || "";
            endTime = form.endTime || "";

            bothChart.data.labels = labels;
            bothChart.data.datasets = getBothDatasets();
            bothChart.update();

            diffChart.data.labels = labels;
            diffChart.data.datasets = getDiffDatasets();
            diffChart.update();
        }
    });
</script>

<h1 id="minorheading" class="text-center">Production vs. Consumption</h1>
<div class="card">
    <!-- Only one canvas is visible at a time -->
    <canvas bind:this={bothCanvas} id="bothChart" style="display: {selection === 'both' ? 'block' : 'none'}"></canvas>
    <canvas bind:this={diffCanvas} id="diffChart" style="display: {selection === 'difference' ? 'block' : 'none'}"></canvas>
</div>
<br/>
<div class="card">
    <form method="POST" use:enhance={() => {
                                isLoading = true;
                                return async ({update}) => {
                                    await update();
                                    isLoading = false;
                                }
                            }}
          action="?/getCombinedRange" class="mx-auto w-full max-w-md space-y-4">
        <div class="flex items-center justify-between">
            <label class="label">
                <span class="label-text">Start date</span>
                <input class="input" name="startTime" id="startTime" type="date" required />
            </label>
            <label class="label">
                <span class="label-text">End date</span>
                <input class="input" name="endTime" id="endTime" type="date" required />
            </label>
            <label class="label">
                <span class="label-text">Select Option</span>
                <select class="select" id="selection" name="selection" bind:value={selection}>
                    <option value="both">Both</option>
                    <option value="difference">Difference</option>
                </select>
            </label>
        </div>
        <div class="flex items-center justify-between">
            <button class="w-full btn preset-filled-primary-500"
                    type="submit"
                    disabled={isLoading}>
                {#if isLoading}
                    Loading...
                {:else}
                    Retrieve data
                {/if}
            </button>
            <button class="btn preset-filled-secondary-500"
                    type="button"
                    onclick={toggleChartType}>
                Toggle Chart Type
        </div>
    </form>
</div>

{#if form?.error}
  <div class="alert alert-error">
    {form.error}
  </div>
{/if}
