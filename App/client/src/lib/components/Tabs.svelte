<script>
  import { createEventDispatcher } from 'svelte';
  
  let { activeTabValue, items } = $props();

  const dispatch = createEventDispatcher();

  const handleClick = tabValue => () => dispatch('change', tabValue);
  let size=$state("");

  $effect(() => {
    //This is really hacky, but it works for now
    const activeItem = items.find(item => item.value === activeTabValue);
    if (activeItem && activeItem.label === "Wide") {
      size = "max-w-5xl";
    } else {
      size = "max-w-3xl";
    }
  });
</script>

<div class="p-8 mx-auto {size}">
    <ul>
    {#each items as item}
        <li class={activeTabValue === item.value ? 'active' : ''}>
            <button type="button" onclick={handleClick(item.value)} class="tab-btn">{item.label}</button>
        </li>
    {/each}
    </ul>
    {#each items as item}
        {#if activeTabValue == item.value}
        <div class="box bg-primary-50">
            <item.component />
        </div>
        {/if}
    {/each}
</div>


<style>
	.box {
		margin-bottom: 10px;
		padding: 40px;
		border: 1px solid #dee2e6;
    border-radius: 0 0 .5rem .5rem;
    border-top: 0;
    background-image: url('$lib/assets/image13.jpeg'); /* <-- Add this line */
    background-size: cover;               /* Optional: cover the box */
    background-repeat: no-repeat;         /* Optional: no repeat */
    background-position: center;
	}
  ul {
    display: flex;
    flex-wrap: wrap;
    padding-left: 0;
    margin-bottom: 0;
    list-style: none;
    border-bottom: 1px solid #dee2e6;
  }
	li {
		margin-bottom: -1px;
	}

  .tab-btn {
    border: 1px solid transparent;
    border-top-left-radius: 0.25rem;
    border-top-right-radius: 0.25rem;
    display: block;
    padding: 0.5rem 1rem;
    cursor: pointer;
    background: none;
    color: inherit;
    font: inherit;
    outline: none;
  }

  .tab-btn:hover {
    border-color: #e9ecef #e9ecef #dee2e6;
  }

  li.active > .tab-btn {
    color: #495057;
    background-color: #fff;
    border-color: #dee2e6 #dee2e6 #fff;
  }
</style>
