<script>
    import { readPriceRange } from '$lib/apis/data-api.js';
    import { onMount } from 'svelte';
    
    let data = $state(null); // Store the fetched prices

    const start = new Date();
    start.setUTCHours(0, 0, 0, 0); // Set to midnight UTC

    const end = new Date(start);
    end.setUTCDate(end.getUTCDate() + 2); // Add 2 days

    function toZeroSecondsISOString(date) {
        const d = new Date(date);
        d.setUTCSeconds(0, 0);
        return d.toISOString().split('.')[0] + 'Z';
    }

    let dateRange = $state({
        startDate: toZeroSecondsISOString(start),
        endDate: toZeroSecondsISOString(end)
    });

    async function fetchPrices() {
        try {
            const response = await readPriceRange(dateRange.startDate, dateRange.endDate);
            data = response;
        } catch (error) {
            console.error('Error fetching prices:', error);
        }
}


    onMount(fetchPrices);
    // Function to calculate the average price for the day
</script>


<h1>Hintateedot</h1>
<input type="date" bind:value={dateRange.startDate} placeholder="YYYY-MM-DDTHH:mm:ssZ" />
<input type="date" bind:value={dateRange.endDate} placeholder="YYYY-MM-DDTHH:mm:ssZ" />
<button onclick={() => fetchPrices()}>Hae hinnat</button>

{#if data && data.length > 0}
	<h2 class="text-xl font-semibold mb-4">Hintatiedot</h2>
	<div class="overflow-x-auto">
		<table class="min-w-full bg-white border border-gray-200 rounded-md shadow-sm">
			<thead class="bg-gray-100">
				<tr>
					<th class="text-left px-4 py-2 border-b text-primary-100-900">Päivämäärä ja aika</th>
					<th class="text-left px-4 py-2 border-b">Hinta (€/kWh)</th>
				</tr>
			</thead>
			<tbody>
				{#each data as { startDate, price }}
					<tr class="hover:bg-gray-50">
						<td class="px-4 py-2 border-b text-sm text-gray-700">
							{new Date(startDate).toLocaleString('fi-FI', {
								day: '2-digit',
								month: '2-digit',
								hour: '2-digit',
								minute: '2-digit'
							})}
						</td>
						<td class="px-4 py-2 border-b text-sm text-gray-700">{price.toFixed(3)}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
{:else}
	<p class="text-gray-600">No data fetched yet.</p>
{/if}

