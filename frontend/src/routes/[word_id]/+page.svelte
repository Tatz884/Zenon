<script>
    // This 'data' contains 2 things:
    // 1. data.summaries inhereted from ./+layout.server.js
    // 2. data.word inherited from +page.server.js
    export let data;

    // Reactive declaration for forms and headerSizesParsed
    $: forms = data.word[0].forms_json ? JSON.parse(data.word[0].forms_json) : [];
    $: headerSizesParsed = data.word[0].header_sizes ? JSON.parse(data.word[0].header_sizes) : { top: { width: 1, height: 1}, side: { width: 1, height: 1 } };

    $: processedForms = processForms(forms, headerSizesParsed);

    function processForms(forms, headerSizes) {
        // Initialize an array to keep track of processed cells for rowspan
        const processedCells = forms.map(row => row.map(() => false));

        return forms.map((row, rowIndex) => {
            return row.map((cell, colIndex) => {
                // Skip this cell if it has been processed in a previous rowspan
                if (processedCells[rowIndex][colIndex]) return null;

                let rowspan = 1;
                let colspan = 1;

                // Check for horizontal span (colspan)
                while (colIndex + colspan < row.length && cell === row[colIndex + colspan]) {
                    colspan++;
                }

                // Check for vertical span (rowspan)
                while (
                    rowIndex + rowspan < forms.length &&
                    forms[rowIndex + rowspan][colIndex] === cell &&
                    allEqual(forms, rowIndex, rowspan, colIndex, colspan)
                ) {
                    rowspan++;
                }

                // Mark cells as processed for rowspan
                for (let i = rowIndex; i < rowIndex + rowspan; i++) {
                    for (let j = colIndex; j < colIndex + colspan; j++) {
                        processedCells[i][j] = true;
                    }
                }

                // Insert ' / ' after '{@html '<br>'}' in cell.value
                if (typeof cell === 'string' && cell.includes(' / ')) {
                    cell = cell.split(' / ').join(' /<br>');
                }

                const isTopHeader = rowIndex < headerSizes.top.height;
                const isSideHeader = (colIndex < headerSizes.side.width) && (rowIndex >= headerSizes.top.height);
                return { value: cell, rowspan, colspan, isTopHeader, isSideHeader };
            });
        }).filter(row => row.some(cell => cell !== null)); // Filter out rows that are completely processed
    }

    // Helper function to check if all cells in the span are equal
    function allEqual(forms, rowIndex, rowspan, colIndex, colspan) {
        for (let i = rowIndex; i < rowIndex + rowspan; i++) {
            for (let j = colIndex; j < colIndex + colspan; j++) {
                if (forms[i][j] !== forms[rowIndex][colIndex]) {
                    return false;
                }
            }
        }
        return true;
    }
</script>

<table>
    {#each processedForms as row}
        <tr>
            {#each row as cell}
                {#if cell}
                    <!-- Use <th> for header cells and <td> for others -->
                    {#if cell.isTopHeader || cell.isSideHeader}
                        <th rowspan={cell.rowspan} colspan={cell.colspan}>
                            {@html cell.value}
                        </th>
                    {:else}
                        <td rowspan={cell.rowspan} colspan={cell.colspan}>
                            {@html cell.value}
                        </td>
                    {/if}
                {/if}
            {/each}
        </tr>
    {/each}
</table>

<style>
    table {
        border-collapse: collapse; /* Ensures that borders are neat */
    }
    th, td {
        border: 1px solid black; /* Sets a black border for each cell */
        padding: 5px; /* Optional: Adds some padding inside cells */
        text-align: center; /* Optional: Centers text in cells */
    }
</style>