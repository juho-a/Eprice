<script>
    import chartjs from 'chart.js/auto';
    import { enhance } from '$app/forms';
    import { onMount } from 'svelte';

    let selection = $state("all");
    let { form } = $props();
    let startTime = $state("");
    let endTime = $state("");

    let productionValues = [];
	let productionLabels = [];
	let productionCtx;
	let productionCanvas;

    let consumptionValues = [];
    let consumptionLabels = [];
    let consumptionCtx;
    let consumptionCanvas;

    onMount(() => {
        productionCtx = productionCanvas.getContext('2d');
        var productionChart = new chartjs(productionCtx, {
            type: 'line',
            data: {
                labels: productionLabels,
                datasets: [{
                        label: 'Production',
                        backgroundColor: 'rgb(255, 99, 132)',
                        borderColor: 'rgb(255, 99, 132)',
                        data: productionValues
                }]
            }
    });
    $effect(() => {
        if (form?.productionLabels && form?.productionValues) {
            productionValues = form.productionValues;
            productionLabels = form.productionLabels;
            productionChart.data.labels = productionLabels;
            productionChart.data.datasets[0].data = productionValues;
            productionChart.update();
            startTime = form.startTime || "";
            endTime = form.endTime || "";
        }
    });

    onMount(() => {
        consumptionCtx = consumptionCanvas.getContext('2d');
        var consumptionChart = new chartjs(consumptionCtx, {
            type: 'line',
            data: {
                labels: consumptionLabels,
                datasets: [{
                        label: 'Consumption',
                        backgroundColor: 'rgb(54, 162, 235)',
                        borderColor: 'rgb(54, 162, 235)',
                        data: consumptionValues
                }]
            }
        });
        $effect(() => {
            if (form?.consumptionLabels && form?.consumptionValues) {
                consumptionValues = form.consumptionValues;
                consumptionLabels = form.consumptionLabels;
                consumptionChart.data.labels = consumptionLabels;
                consumptionChart.data.datasets[0].data = consumptionValues;
                consumptionChart.update();
            }
        });
    });

	});

</script>


<h1 id="minorheading">Production Data</h1>

<canvas bind:this={productionCanvas} id="myChart"></canvas>


<form method="POST" use:enhance action="?/getProductionRange" class="mx-auto w-full max-w-md space-y-4">
  <div class="flex items-center justify-between">
    <label class="label">
        <span class="label-text">Date</span>
        <input class="input" name="startTime" id="startTime" type="date" />
    </label>
    <label class="label">
        <span class="label-text">Date</span>
        <input class="input" name="endTime" id="endTime" type="date" />
    </label>
    <label class="label">
        <span class="label-text">Select Option</span>
        <select class="select" bind:value={selection} id="selection">
            <option value="all">All</option>
            <option value="0">Mondays</option>
            <option value="1">Tuesdays</option>
            <option value="2">Wednesdays</option>
            <option value="3">Thursdays</option>
            <option value="4">Fridays</option>
            <option value="5">Saturdays</option>
            <option value="6">Sundays</option>
            <option value="weekdays">Weekdays</option>
            <option value="weekends">Weekends</option>
        </select>
    </label>
  </div>
    <button class="w-full btn preset-filled-primary-500" type="submit">
        Retrieve  data
    </button>
</form>

{#if form?.error}
  <div class="alert alert-error">
    {form.error}
  </div>
{/if}


<h1 id="minorheading">Consumption Data</h1>

<canvas bind:this={consumptionCanvas} id="myChart"></canvas>


<form method="POST" use:enhance action="?/getConsumptionRange" class="mx-auto w-full max-w-md space-y-4">
  <div class="flex items-center justify-between">
    <label class="label">
        <span class="label-text">Date</span>
        <input class="input" name="startTime" id="startTime" type="date" bind:value={startTime} />
    </label>
    <label class="label">
        <span class="label-text">Date</span>
        <input class="input" name="endTime" id="endTime" type="date" bind:value={endTime} />
    </label>
    <label class="label">
        <span class="label-text">Select Option</span>
        <select class="select" bind:value={selection} id="selection">
            <option value="all">All</option>
            <option value="0">Mondays</option>
            <option value="1">Tuesdays</option>
            <option value="2">Wednesdays</option>
            <option value="3">Thursdays</option>
            <option value="4">Fridays</option>
            <option value="5">Saturdays</option>
            <option value="6">Sundays</option>
            <option value="weekdays">Weekdays</option>
            <option value="weekends">Weekends</option>
        </select>
    </label>
  </div>
    <button class="w-full btn preset-filled-primary-500" type="submit">
        Retrieve  data
    </button>
</form>


{#if form?.error}
  <div class="alert alert-error">
    {form.error}
  </div>
{/if}