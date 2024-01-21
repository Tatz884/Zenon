import { all_words } from './data.js';

export function load() {
	return {
		summaries: all_words.map((word) => ({
			pos: word.pos,
			root_form: word.root_form
		}))
	};
}