import pprint
all_tags = {'case':('nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative', 'vocative'),
                'tense': ('present', 'past', 'future', 'conditional', 'imperative'),
                'person': ('first-person', 'second-person', 'third-person', 'impersonal'),
                'number': ('singular', 'plural'),
                'gender': ('masculine', 'feminine', 'neuter'),
                'virility':('virile', 'nonvirile'),
                'animacy':('animate', 'inanimate')}

global_tags_noun = {'case':('nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative', 'vocative'),
                'tense': (),
                'person': ('first-person', 'second-person', 'third-person', 'impersonal'),
                'number': ('singular','plural'),
                'gender': ('masculine','feminine', 'neuter'),
                'virility':(),
                'animacy':('animate', 'inanimate')}

global_tags_verb = {'case':(),
                'tense': ('present', 'past', 'future', 'conditional', 'imperative'),
                'person': ('first-person', 'second-person', 'third-person', 'impersonal'),
                'number': ('singular','plural'),
                'gender': ('masculine','feminine', 'neuter'),
                'virility':(),
                'animacy':('animate', 'inanimate')}



def determine_vertical_positions(global_tags):
    if bool(global_tags['case']) and not bool(global_tags['tense']): # determine if declension or conjugation
        vertical_positions = {tag: index for index, tag in enumerate(global_tags['case'])}
    else:
        vertical_positions = {'infinitive':0,
                                'present':{'first-person':1,'second-person':2,'third-person':3, 'impersonal':4},
                                'past':{'first-person':5,'second-person':6,'third-person':7, 'impersonal':8},
                                'future':{'first-person':9,'second-person':10,'third-person':11, 'impersonal':12},
                                'conditional':{'first-person':13,'second-person':14,'third-person':15, 'impersonal':16},
                                'imperative':{'first-person':17,'second-person':18,'third-person':19}
                                }
    
    # processed_tags = []
    # vertical_positions, processed_tags = process_person(vertical_positions, processed_tags, global_tags)
    # vertical_positions, processed_tags = process_animacy(vertical_positions, processed_tags, global_tags)
    # vertical_positions, processed_tags = process_gender(vertical_positions, processed_tags, global_tags)
    # vertical_positions, processed_tags = process_singular(vertical_positions, processed_tags, global_tags)
    # vertical_positions, processed_tags = process_virility(vertical_positions, processed_tags, global_tags)
    # vertical_positions, processed_tags = process_plural(vertical_positions, processed_tags, global_tags)

    return vertical_positions

def define_2d_vertical_header(global_tags, vertical_positions):
    if bool(global_tags['case']) and not bool(global_tags['tense']): # determine if declension or conjugation
        vertical_positions
        output_grid = \
        [[''] for _ in vertical_positions]
        for tag in global_tags['case']:
            output_grid[vertical_positions[tag]][0] = tag

    else: # conjugation
        # Check the depth of the dictionary
        depth = 1 if all(not isinstance(v, dict) for v in vertical_positions.values()) else 2

        # Initialize the 2D list with empty strings
        num_rows = sum(len(v) if isinstance(v, dict) else 1 for v in vertical_positions.values())
        output_grid = [['', ''] for _ in range(num_rows)] if depth == 2 else [[''] for _ in range(num_rows)]

        # Populate the 2D list
        if depth == 1:
            for key, row in vertical_positions.items():
                output_grid[row][0] = key
        else:
            row_index = 0
            for key, subdict in vertical_positions.items():
                if isinstance(subdict, dict):
                    for subkey, subrow in subdict.items():
                        output_grid[subrow][0] = key
                        output_grid[subrow][1] = subkey
                else:
                    output_grid[row_index][0] = key
                    output_grid[row_index][1] = key
                    row_index += 1

        pass

    return output_grid

def main():
    global_tags = global_tags_verb

    # print(determine_vertical_positions(global_tags))
    define_2d_vertical_header(global_tags, determine_vertical_positions(global_tags))
