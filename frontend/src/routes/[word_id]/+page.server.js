import { error } from '@sveltejs/kit';

export async function load({ params }) {

// write the function that uses params.root_form
// and GET API
    let development_address = `http://localhost:8000/api/v1/words/wordinfo/?user_input=${encodeURIComponent(parseInt(params.word_id, 10))}`
    let production_address = `https://zenon-backend.fly.dev/api/v1/words/wordinfo/?user_input=${encodeURIComponent(parseInt(params.word_id, 10))}`

    let word = null
    const response = await fetch(production_address);
    if (!response.ok) {
        error(404, {
            message: 'Not found'
        })
    }
    word = await response.json();

    if (!word) {
        error(404, {
            message: 'json conversion failed'
        })
    }

    if (!word[0].forms_json === undefined || word[0].forms_json === null, word[0].forms_json === "null") {
        error(404, {
            message: 'forms_json is not ready for this word'
        })
    }

    return {
        word
    }

}