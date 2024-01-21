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
            let development_address = `http://localhost:8000/api/v1/words/suggestions/?user_input=${encodeURIComponent(query)}&skip=0&limit=1`
            let production_address = `https://zenon-backend.fly.dev/api/v1/words/suggestions/?user_input=${encodeURIComponent(query)}&skip=0&limit=1`
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

<input type="text" placeholder="Type your query..." bind:value={$userInput}>

{#if $isLoading}
    <div>Loading...</div>
{:else}
    <div id="suggestions">
        {#each $suggestions as suggestion}
            <a href="/{suggestion.id}">{suggestion.original_form} {suggestion.pos}</a>
        {/each}
    </div>
{/if}
