The workflow v0.2 is

fill_mtags -> make_side_header.py & make_top_header.py -> map_by_tag.py

output example:
[['', 'singular', 'singular', 'singular', 'singular', 'plural', 'plural'],
 ['', 'masculine', 'masculine', 'feminine', 'neuter', 'virile', 'nonvirile'],
 ['', 'animate', 'inanimate', '', '', '', ''],
 ['nominative', 'duży', 'duży', 'duża', 'duże', 'duzi', 'duże'],
 ['genitive', 'dużego', 'dużego', 'dużej', 'dużego', 'dużych', 'dużych'],
 ['dative', 'dużemu', 'dużemu', 'dużej', 'dużemu', 'dużym', 'dużym'],
 ['accusative', 'dużego', 'duży', 'dużą', 'duże', 'dużych', 'duże'],
 ['instrumental', 'dużym', 'dużym', 'dużą', 'dużym', 'dużymi', 'dużymi'],
 ['locative', 'dużym', 'dużym', 'dużej', 'dużym', 'dużych', 'dużych'],
 ['vocative', 'duży', 'duży', 'duża', 'duże', 'duzi', 'duże']]
The workflow v0.1 is

fill_mtags -> nest_tags

output example:
{'vocative': {'singular': {'masculine': 'duży', 'neuter': 'duże', 'feminine': 'duża'}, 'plural': {'virile': 'duzi', 'nonvirile': 'duże'}}, 'nominative': {'singular': {'masculine': 'duży', 'neuter': 'duże', 'feminine': 'duża'}, 'plural': {'virile': 'duzi', 'nonvirile': 'duże'}}, 'genitive': {'singular': {'neuter': 'dużego', 'masculine': 'dużego', 'feminine': 'dużej'}, 'plural': 'dużych'}, 'dative': {'singular': {'neuter': 'dużemu', 'masculine': 'dużemu', 'feminine': 'dużej'}, 'plural': 'dużym'}, 'accusative': {'singular': {'masculine': {'animate': 'dużego', 'inanimate': 'duży'}, 'neuter': 'duże', 'feminine': 'dużą'}, 'plural': {'virile': 'dużych', 'nonvirile': 'duże'}}, 'instrumental': {'singular': {'neuter': 'dużym', 'masculine': 'dużym', 'feminine': 'dużą'}, 'plural': 'dużymi'}, 'locative': {'singular': {'neuter': 'dużym', 'masculine': 'dużym', 'feminine': 'dużej'}, 'plural': 'dużych'}}