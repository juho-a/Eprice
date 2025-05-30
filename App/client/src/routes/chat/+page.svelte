<script>
    import ChatView1 from "$lib/components/ChatView1.svelte";
    import ChatView2 from "$lib/components/ChatView2.svelte";
    import Tabs from "$lib/components/Tabs.svelte";

    let activeTabValue = $state(1);

    let items = [
        { label: "Chat 1",
            value: 1,
            component: ChatView1
            },
        { label: "Chat 2",
            value: 2,
            component: ChatView2
            },
    ];
</script>


<Tabs items={items} activeTabValue={activeTabValue} on:change={e => activeTabValue = e.detail} />