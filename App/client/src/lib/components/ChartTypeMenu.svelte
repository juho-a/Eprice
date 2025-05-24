<script>
    let { chartType } = $props();
</script>
<div class="mb-4 w-full max-w-xs">
	<label for="taulukko" class="block mb-1 text-sm text-white">Valitse kaaviotyyppi</label>
	<select
		id="taulukko"
		bind:value={chartType}
		class="w-full px-3 py-2 rounded bg-gray-800 text-white border border-gray-600 text-sm"
	>
		<option value="bar">Bar</option>
		<option value="line">Line</option>
		<option value="pie">Pie</option>
		<option value="doughnut">Doughnut</option>
		<option value="radar">Radar</option>
		<option value="polarArea">Polar Area</option>
	</select>
</div>