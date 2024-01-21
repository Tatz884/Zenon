<script>
    import { writable } from 'svelte/store';

    const userInput = writable('');
    const suggestions = writable([]);
    const isLoading = writable(false);
    /**
     * @type {number | undefined}
     */
    let debounceTimeout;

    /**
     * @param {{ (query: any): Promise<void>; (arg0: any): any; }} func
     * @param {number | undefined} delay
     */
    function debounce(func, delay) {
        return (/** @type {any} */ ...args) => {
            clearTimeout(debounceTimeout);
            // @ts-ignore
            debounceTimeout = setTimeout(() => func(...args), delay);
        };
    }

    /**
     * @param {string} query
     */
    async function fetchSuggestions(query) {
        isLoading.set(true);
        try {
            let development_address = `http://localhost:8000/api/v1/words/suggestions/?user_input=${encodeURIComponent(query)}&skip=0&limit=10`
            let production_address = `https://zenon-backend.fly.dev/api/v1/words/suggestions/?user_input=${encodeURIComponent(query)}&skip=0&limit=10`
            const response = await fetch(production_address);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            console.log(data)
            suggestions.set(data);
        } catch (error) {
            console.error('Error fetching data:', error);
            // Handle errors appropriately
        } finally {
            isLoading.set(false);
        }
    }

    const debouncedFetchSuggestions = debounce(fetchSuggestions, 500); // 500 ms delay

    $: if ($userInput.length > 0) {
        debouncedFetchSuggestions($userInput);
    } else {
        suggestions.set([]);
    }
</script>

<div class="suggestions-container">
    <input type="text" placeholder="Type your query..." bind:value={$userInput}>

    {#if $isLoading}
        <div id="suggestions">Loading...</div>
    {:else}
        <div id="suggestions">
            {#each $suggestions as suggestion}
                <a href="/{suggestion.id}">{suggestion.original_form} {suggestion.pos}</a><br>
            {/each}
        </div>
    {/if}
</div>

<style>
    .suggestions-container {
        position: relative;
    }
    #suggestions {
        position: absolute;
        top: 100%; /* Position below the input field */
        left: 0;
        width: 100%; /* Match the width of the input field */
        background: white; /* Optional: for better visibility */
        z-index: 1000; /* Ensure it's above other content */
        max-height: 300px; /* Optional: limit height */
        overflow-y: auto; /* Optional: add scroll for long lists */
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1); /* Optional: add shadow for depth */
    }
</style>
