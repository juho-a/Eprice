<script>
    import { getStats } from "$lib/utils/stats-helpers.js";
    let { values } = $props();
    let stats = $state({});
    $effect(() => {
        if (values && values.length > 0) {
            stats = getStats(values);
        } else {
            stats = undefined;
        }
    });
</script>

{#if stats}
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-label">Max</div>
            <div class="stat-value">{stats.max} c/kWh</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Min</div>
            <div class="stat-value">{stats.min} c/kWh</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Average</div>
            <div class="stat-value">{stats.mean} c/kWh</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Std.</div>
            <div class="stat-value">{stats.std} c/kWh</div>
        </div>
    </div>
{/if}

<style>
.stats-row {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
    justify-content: center;
}
.stat-card {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 1rem 2rem;
    min-width: 120px;
    text-align: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}
.stat-label {
    font-size: 1rem;
    color: #64748b;
    margin-bottom: 0.5rem;
}
.stat-value {
    font-size: 1.25rem;
    font-weight: bold;
    color: #0f172a;
}
</style>