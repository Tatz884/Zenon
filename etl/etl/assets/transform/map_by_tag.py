try: # execute from dagster
    from etl.assets.transform.make_top_header import make_top_header, fill_empty_strings_top
    from etl.assets.transform.make_side_header import make_side_header, fill_empty_strings_side
    from etl.assets.transform.add_all_missing_tags import process_entries
except ImportError: # in case you want to execute the script directly
    from make_top_header import make_top_header, fill_empty_strings_top
    from make_side_header import make_side_header, fill_empty_strings_side
    from add_all_missing_tags import process_entries
import pprint
import traceback
import pandas as pd
from dagster import (
    asset,
    AssetExecutionContext,
    get_dagster_logger,
    MetadataValue
)

det = [{'form': '', 'source': 'declension', 'tags': ['table-tags']}, {'form': 'pl-decl-numeral', 'source': 'declension', 'tags': ['inflection-template']}, {'form': 'kilkunastu', 'tags': ['nominative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['nominative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['genitive', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['dative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['accusative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['accusative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastoma', 'tags': ['instrumental', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['locative', 'plural'], 'source': 'declension'}, {'form': 'kilkunastu', 'tags': ['plural', 'virile', 'vocative'], 'source': 'declension'}, {'form': 'kilkanaście', 'tags': ['plural', 'vocative'], 'source': 'declension'}]
adj1 = [{'form': 'większy', 'tags': ['comparative']}, {'form': 'największy', 'tags': ['superlative']}, {'form': 'dużo', 'tags': ['adverb']}, {'form': 'duższy', 'tags': ['Middle', 'Polish', 'comparative']}, {'form': 'naduższy', 'tags': ['Middle', 'Polish', 'superlative']}, {'form': 'najduższy', 'tags': ['Middle', 'Polish', 'superlative']}, {'form': '', 'source': 'declension', 'tags': ['table-tags']}, {'form': 'pl-decl-adj-auto', 'source': 'declension', 'tags': ['inflection-template']}, {'form': 'duży', 'tags': ['masculine', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duże', 'tags': ['neuter', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duża', 'tags': ['feminine', 'nominative', 'singular', 'vocative'], 'source': 'declension'}, {'form': 'duzi', 'tags': ['nominative', 'plural', 'virile', 'vocative'], 'source': 'declension'}, {'form': 'duże', 'tags': ['nominative', 'nonvirile', 'plural', 'vocative'], 'source': 'declension'}, {'form': 'dużego', 'tags': ['genitive', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['feminine', 'genitive', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['genitive', 'plural'], 'source': 'declension'}, {'form': 'dużemu', 'tags': ['dative', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['dative', 'feminine', 'singular'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['dative', 'plural'], 'source': 'declension'}, {'form': 'dużego', 'tags': ['accusative', 'animate', 'masculine', 'singular'], 'source': 'declension'}, {'form': 'duży', 'tags': ['accusative', 'inanimate', 'masculine', 'singular'], 'source': 'declension'}, {'form': 'duże', 'tags': ['accusative', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużą', 'tags': ['accusative', 'feminine', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['accusative', 'plural', 'virile'], 'source': 'declension'}, {'form': 'duże', 'tags': ['accusative', 'nonvirile', 'plural'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['instrumental', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużą', 'tags': ['feminine', 'instrumental', 'singular'], 'source': 'declension'}, {'form': 'dużymi', 'tags': ['instrumental', 'plural'], 'source': 'declension'}, {'form': 'dużym', 'tags': ['locative', 'masculine', 'neuter', 'singular'], 'source': 'declension'}, {'form': 'dużej', 'tags': ['feminine', 'locative', 'singular'], 'source': 'declension'}, {'form': 'dużych', 'tags': ['locative', 'plural'], 'source': 'declension'}]

verb2 = [{'form': 'zmoczyć', 'tags': ['perfective']}, {'form': 'zamoczyć', 'tags': ['perfective']}, {'form': 'imperfective', 'source': 'conjugation', 'tags': ['table-tags']}, {'form': 'pl-conj-ai-yć', 'source': 'conjugation', 'tags': ['inflection-template']}, {'form': 'moczyć', 'tags': ['infinitive'], 'source': 'conjugation'}, {'form': 'moczę', 'tags': ['present', 'singular'], 'source': 'conjugation'}, {'form': 'moczymy', 'tags': ['plural', 'present'], 'source': 'conjugation'}, {'form': 'moczysz', 'tags': ['present', 'singular'], 'source': 'conjugation'}, {'form': 'moczycie', 'tags': ['plural', 'present'], 'source': 'conjugation'}, {'form': 'moczy', 'tags': ['present', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczą', 'tags': ['plural', 'present', 'third-person'], 'source': 'conjugation'}, {'form': 'moczy się', 'tags': ['impersonal', 'present'], 'source': 'conjugation'}, {'form': 'moczyłem', 'tags': ['masculine', 'past', 'singular'], 'source': 'conjugation'}, {'form': '-(e)m moczył', 'tags': ['masculine', 'past', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłam', 'tags': ['feminine', 'past', 'singular'], 'source': 'conjugation'}, {'form': '-(e)m moczyła', 'tags': ['feminine', 'past', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłom', 'tags': ['neuter', 'past', 'singular'], 'source': 'conjugation'}, {'form': '-(e)m moczyło', 'tags': ['neuter', 'past', 'singular'], 'source': 'conjugation'}, {'form': 'moczyliśmy', 'tags': ['past', 'plural', 'virile'], 'source': 'conjugation'}, {'form': '-(e)śmy moczyli', 'tags': ['past', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczyłyśmy', 'tags': ['nonvirile', 'past', 'plural'], 'source': 'conjugation'}, {'form': '-(e)śmy moczyły', 'tags': ['nonvirile', 'past', 'plural'], 'source': 'conjugation'}, {'form': 'moczyłeś', 'tags': ['masculine', 'past', 'singular'], 'source': 'conjugation'}, {'form': '-(e)ś moczył', 'tags': ['masculine', 'past', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłaś', 'tags': ['feminine', 'past', 'singular'], 'source': 'conjugation'}, {'form': '-(e)ś moczyła', 'tags': ['feminine', 'past', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłoś', 'tags': ['neuter', 'past', 'singular'], 'source': 'conjugation'}, {'form': '-(e)ś moczyło', 'tags': ['neuter', 'past', 'singular'], 'source': 'conjugation'}, {'form': 'moczyliście', 'tags': ['past', 'plural', 'virile'], 'source': 'conjugation'}, {'form': '-(e)ście moczyli', 'tags': ['past', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczyłyście', 'tags': ['nonvirile', 'past', 'plural'], 'source': 'conjugation'}, {'form': '-(e)ście moczyły', 'tags': ['nonvirile', 'past', 'plural'], 'source': 'conjugation'}, {'form': 'moczył', 'tags': ['masculine', 'past', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyła', 'tags': ['feminine', 'past', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyło', 'tags': ['neuter', 'past', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyli', 'tags': ['past', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'moczyły', 'tags': ['nonvirile', 'past', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'moczono', 'tags': ['impersonal', 'past'], 'source': 'conjugation'}, {'form': 'będę moczył', 'tags': ['future', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'będę moczyć', 'tags': ['future', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'będę moczyła', 'tags': ['feminine', 'future', 'singular'], 'source': 'conjugation'}, {'form': 'będę moczyć', 'tags': ['feminine', 'future', 'singular'], 'source': 'conjugation'}, {'form': 'będę moczyło', 'tags': ['future', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'będę moczyć', 'tags': ['future', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'będziemy moczyli', 'tags': ['future', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'będziemy moczyć', 'tags': ['future', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'będziemy moczyły', 'tags': ['future', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'będziemy moczyć', 'tags': ['future', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'będziesz moczył', 'tags': ['future', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'będziesz moczyć', 'tags': ['future', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'będziesz moczyła', 'tags': ['feminine', 'future', 'singular'], 'source': 'conjugation'}, {'form': 'będziesz moczyć', 'tags': ['feminine', 'future', 'singular'], 'source': 'conjugation'}, {'form': 'będziesz moczyło', 'tags': ['future', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'będziesz moczyć', 'tags': ['future', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'będziecie moczyli', 'tags': ['future', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'będziecie moczyć', 'tags': ['future', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'będziecie moczyły', 'tags': ['future', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'będziecie moczyć', 'tags': ['future', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'będzie moczył', 'tags': ['future', 'masculine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyć', 'tags': ['future', 'masculine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyła', 'tags': ['feminine', 'future', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyć', 'tags': ['feminine', 'future', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyło', 'tags': ['future', 'neuter', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyć', 'tags': ['future', 'neuter', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będą moczyli', 'tags': ['future', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'będą moczyć', 'tags': ['future', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'będą moczyły', 'tags': ['future', 'nonvirile', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'będą moczyć', 'tags': ['future', 'nonvirile', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie moczyć się', 'tags': ['future', 'impersonal'], 'source': 'conjugation'}, {'form': 'moczyłbym', 'tags': ['conditional', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'bym moczył', 'tags': ['conditional', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłabym', 'tags': ['conditional', 'feminine', 'singular'], 'source': 'conjugation'}, {'form': 'bym moczyła', 'tags': ['conditional', 'feminine', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłobym', 'tags': ['conditional', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'bym moczyło', 'tags': ['conditional', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'moczylibyśmy', 'tags': ['conditional', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'byśmy moczyli', 'tags': ['conditional', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczyłybyśmy', 'tags': ['conditional', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'byśmy moczyły', 'tags': ['conditional', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'moczyłbyś', 'tags': ['conditional', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'byś moczył', 'tags': ['conditional', 'masculine', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłabyś', 'tags': ['conditional', 'feminine', 'singular'], 'source': 'conjugation'}, {'form': 'byś moczyła', 'tags': ['conditional', 'feminine', 'singular'], 'source': 'conjugation'}, {'form': 'moczyłobyś', 'tags': ['conditional', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'byś moczyło', 'tags': ['conditional', 'neuter', 'singular'], 'source': 'conjugation'}, {'form': 'moczylibyście', 'tags': ['conditional', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'byście moczyli', 'tags': ['conditional', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczyłybyście', 'tags': ['conditional', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'byście moczyły', 'tags': ['conditional', 'nonvirile', 'plural'], 'source': 'conjugation'}, {'form': 'moczyłby', 'tags': ['conditional', 'masculine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'by moczył', 'tags': ['conditional', 'masculine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyłaby', 'tags': ['conditional', 'feminine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'by moczyła', 'tags': ['conditional', 'feminine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyłoby', 'tags': ['conditional', 'neuter', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'by moczyło', 'tags': ['conditional', 'neuter', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'moczyliby', 'tags': ['conditional', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'by moczyli', 'tags': ['conditional', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'moczyłyby', 'tags': ['conditional', 'nonvirile', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'by moczyły', 'tags': ['conditional', 'nonvirile', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'moczono by', 'tags': ['conditional', 'impersonal'], 'source': 'conjugation'}, {'form': 'niech moczę', 'tags': ['imperative', 'singular'], 'source': 'conjugation'}, {'form': 'moczmy', 'tags': ['imperative', 'plural'], 'source': 'conjugation'}, {'form': 'mocz', 'tags': ['imperative', 'singular'], 'source': 'conjugation'}, {'form': 'moczcie', 'tags': ['imperative', 'plural'], 'source': 'conjugation'}, {'form': 'niech moczy', 'tags': ['imperative', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'niech moczą', 'tags': ['imperative', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'moczący', 'tags': ['active', 'adjectival', 'masculine', 'participle', 'singular'], 'source': 'conjugation'}, {'form': 'mocząca', 'tags': ['active', 'adjectival', 'feminine', 'participle', 'singular'], 'source': 'conjugation'}, {'form': 'moczące', 'tags': ['active', 'adjectival', 'neuter', 'participle', 'singular'], 'source': 'conjugation'}, {'form': 'moczący', 'tags': ['active', 'adjectival', 'participle', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczące', 'tags': ['active', 'adjectival', 'nonvirile', 'participle', 'plural'], 'source': 'conjugation'}, {'form': 'moczony', 'tags': ['adjectival', 'masculine', 'participle', 'passive', 'singular'], 'source': 'conjugation'}, {'form': 'moczona', 'tags': ['adjectival', 'feminine', 'participle', 'passive', 'singular'], 'source': 'conjugation'}, {'form': 'moczone', 'tags': ['adjectival', 'neuter', 'participle', 'passive', 'singular'], 'source': 'conjugation'}, {'form': 'moczeni', 'tags': ['adjectival', 'participle', 'passive', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'moczone', 'tags': ['adjectival', 'nonvirile', 'participle', 'passive', 'plural'], 'source': 'conjugation'}, {'form': 'mocząc', 'tags': ['adjectival', 'contemporary', 'participle'], 'source': 'conjugation'}, {'form': 'moczenie', 'tags': ['noun-from-verb'], 'source': 'conjugation'}]

verb3 = [{'form': 'pieprzyć', 'tags': ['infinitive'], 'source': 'conjugation'}, {'form': 'pieprzę', 'tags': ['present', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzymy', 'tags': ['plural', 'present', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzysz', 'tags': ['present', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzycie', 'tags': ['plural', 'present', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzy', 'tags': ['present', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'pieprzą', 'tags': ['plural', 'present', 'third-person'], 'source': 'conjugation'}, {'form': 'pieprzy się', 'tags': ['impersonal', 'present'], 'source': 'conjugation'}, {'form': 'pieprzyłem', 'tags': ['masculine', 'past', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': '-(e)m pieprzył', 'tags': ['masculine', 'past', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzyłam', 'tags': ['feminine', 'past', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': '-(e)m pieprzyła', 'tags': ['feminine', 'past', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzyłom', 'tags': ['neuter', 'past', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': '-(e)m pieprzyło', 'tags': ['neuter', 'past', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzyliśmy', 'tags': ['past', 'plural', 'virile', 'first-person'], 'source': 'conjugation'}, {'form': '-(e)śmy pieprzyli', 'tags': ['past', 'plural', 'virile', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzyłyśmy', 'tags': ['nonvirile', 'past', 'plural', 'first-person'], 'source': 'conjugation'}, {'form': '-(e)śmy pieprzyły', 'tags': ['nonvirile', 'past', 'plural', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzyłeś', 'tags': ['masculine', 'past', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': '-(e)ś pieprzył', 'tags': ['masculine', 'past', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzyłaś', 'tags': ['feminine', 'past', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': '-(e)ś pieprzyła', 'tags': ['feminine', 'past', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzyłoś', 'tags': ['neuter', 'past', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': '-(e)ś pieprzyło', 'tags': ['neuter', 'past', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzyliście', 'tags': ['past', 'plural', 'virile', 'second-person'], 'source': 'conjugation'}, {'form': '-(e)ście pieprzyli', 'tags': ['past', 'plural', 'virile', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzyłyście', 'tags': ['nonvirile', 'past', 'plural', 'second-person'], 'source': 'conjugation'}, {'form': '-(e)ście pieprzyły', 'tags': ['nonvirile', 'past', 'plural', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzył', 'tags': ['masculine', 'past', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'pieprzyła', 'tags': ['feminine', 'past', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'pieprzyło', 'tags': ['neuter', 'past', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'pieprzyli', 'tags': ['past', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'pieprzyły', 'tags': ['nonvirile', 'past', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'pieprzono', 'tags': ['impersonal', 'past'], 'source': 'conjugation'}, {'form': 'będę pieprzył', 'tags': ['future', 'masculine', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'będę pieprzyć', 'tags': ['future', 'masculine', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'będę pieprzyła', 'tags': ['feminine', 'future', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'będę pieprzyć', 'tags': ['feminine', 'future', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'będę pieprzyło', 'tags': ['future', 'neuter', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'będę pieprzyć', 'tags': ['future', 'neuter', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'będziemy pieprzyli', 'tags': ['future', 'plural', 'virile', 'first-person'], 'source': 'conjugation'}, {'form': 'będziemy pieprzyć', 'tags': ['future', 'plural', 'virile', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'będziemy pieprzyły', 'tags': ['future', 'nonvirile', 'plural', 'first-person'], 'source': 'conjugation'}, {'form': 'będziemy pieprzyć', 'tags': ['future', 'nonvirile', 'plural', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'będziesz pieprzył', 'tags': ['future', 'masculine', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'będziesz pieprzyć', 'tags': ['future', 'masculine', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'będziesz pieprzyła', 'tags': ['feminine', 'future', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'będziesz pieprzyć', 'tags': ['feminine', 'future', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'będziesz pieprzyło', 'tags': ['future', 'neuter', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'będziesz pieprzyć', 'tags': ['future', 'neuter', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'będziecie pieprzyli', 'tags': ['future', 'plural', 'virile', 'second-person'], 'source': 'conjugation'}, {'form': 'będziecie pieprzyć', 'tags': ['future', 'plural', 'virile', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'będziecie pieprzyły', 'tags': ['future', 'nonvirile', 'plural', 'second-person'], 'source': 'conjugation'}, {'form': 'będziecie pieprzyć', 'tags': ['future', 'nonvirile', 'plural', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'będzie pieprzył', 'tags': ['future', 'masculine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie pieprzyć', 'tags': ['future', 'masculine', 'singular', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'będzie pieprzyła', 'tags': ['feminine', 'future', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie pieprzyć', 'tags': ['feminine', 'future', 'singular', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'będzie pieprzyło', 'tags': ['future', 'neuter', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'będzie pieprzyć', 'tags': ['future', 'neuter', 'singular', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'będą pieprzyli', 'tags': ['future', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'będą pieprzyć', 'tags': ['future', 'plural', 'third-person', 'virile', 'derogatory'], 'source': 'conjugation'}, {'form': 'będą pieprzyły', 'tags': ['future', 'nonvirile', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'będą pieprzyć', 'tags': ['future', 'nonvirile', 'plural', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'będzie pieprzyć się', 'tags': ['future', 'impersonal'], 'source': 'conjugation'}, {'form': 'pieprzyłbym', 'tags': ['conditional', 'masculine', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'bym pieprzył', 'tags': ['conditional', 'masculine', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzyłabym', 'tags': ['conditional', 'feminine', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'bym pieprzyła', 'tags': ['conditional', 'feminine', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzyłobym', 'tags': ['conditional', 'neuter', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'bym pieprzyło', 'tags': ['conditional', 'neuter', 'singular', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzylibyśmy', 'tags': ['conditional', 'plural', 'virile', 'first-person'], 'source': 'conjugation'}, {'form': 'byśmy pieprzyli', 'tags': ['conditional', 'plural', 'virile', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzyłybyśmy', 'tags': ['conditional', 'nonvirile', 'plural', 'first-person'], 'source': 'conjugation'}, {'form': 'byśmy pieprzyły', 'tags': ['conditional', 'nonvirile', 'plural', 'derogatory', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzyłbyś', 'tags': ['conditional', 'masculine', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'byś pieprzył', 'tags': ['conditional', 'masculine', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzyłabyś', 'tags': ['conditional', 'feminine', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'byś pieprzyła', 'tags': ['conditional', 'feminine', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzyłobyś', 'tags': ['conditional', 'neuter', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'byś pieprzyło', 'tags': ['conditional', 'neuter', 'singular', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzylibyście', 'tags': ['conditional', 'plural', 'virile', 'second-person'], 'source': 'conjugation'}, {'form': 'byście pieprzyli', 'tags': ['conditional', 'plural', 'virile', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzyłybyście', 'tags': ['conditional', 'nonvirile', 'plural', 'second-person'], 'source': 'conjugation'}, {'form': 'byście pieprzyły', 'tags': ['conditional', 'nonvirile', 'plural', 'derogatory', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzyłby', 'tags': ['conditional', 'masculine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'by pieprzył', 'tags': ['conditional', 'masculine', 'singular', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'pieprzyłaby', 'tags': ['conditional', 'feminine', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'by pieprzyła', 'tags': ['conditional', 'feminine', 'singular', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'pieprzyłoby', 'tags': ['conditional', 'neuter', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'by pieprzyło', 'tags': ['conditional', 'neuter', 'singular', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'pieprzyliby', 'tags': ['conditional', 'plural', 'third-person', 'virile'], 'source': 'conjugation'}, {'form': 'by pieprzyli', 'tags': ['conditional', 'plural', 'third-person', 'virile', 'derogatory'], 'source': 'conjugation'}, {'form': 'pieprzyłyby', 'tags': ['conditional', 'nonvirile', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'by pieprzyły', 'tags': ['conditional', 'nonvirile', 'plural', 'third-person', 'derogatory'], 'source': 'conjugation'}, {'form': 'pieprzono by', 'tags': ['conditional', 'impersonal'], 'source': 'conjugation'}, {'form': 'niech pieprzę', 'tags': ['imperative', 'singular', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprzmy', 'tags': ['imperative', 'plural', 'first-person'], 'source': 'conjugation'}, {'form': 'pieprz', 'tags': ['imperative', 'singular', 'second-person'], 'source': 'conjugation'}, {'form': 'pieprzcie', 'tags': ['imperative', 'plural', 'second-person'], 'source': 'conjugation'}, {'form': 'niech pieprzy', 'tags': ['imperative', 'singular', 'third-person'], 'source': 'conjugation'}, {'form': 'niech pieprzą', 'tags': ['imperative', 'plural', 'third-person'], 'source': 'conjugation'}, {'form': 'imperfective', 'source': 'conjugation', 'tags': ['table-tags']}, {'form': 'pl-conj-ai-yć', 'source': 'conjugation', 'tags': ['inflection-template']}, {'form': 'pieprzący', 'tags': ['active', 'adjectival', 'masculine', 'participle', 'singular'], 'source': 'conjugation'}, {'form': 'pieprząca', 'tags': ['active', 'adjectival', 'feminine', 'participle', 'singular'], 'source': 'conjugation'}, {'form': 'pieprzące', 'tags': ['active', 'adjectival', 'neuter', 'participle', 'singular'], 'source': 'conjugation'}, {'form': 'pieprzący', 'tags': ['active', 'adjectival', 'participle', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'pieprzące', 'tags': ['active', 'adjectival', 'nonvirile', 'participle', 'plural'], 'source': 'conjugation'}, {'form': 'pieprzony', 'tags': ['adjectival', 'masculine', 'participle', 'passive', 'singular'], 'source': 'conjugation'}, {'form': 'pieprzona', 'tags': ['adjectival', 'feminine', 'participle', 'passive', 'singular'], 'source': 'conjugation'}, {'form': 'pieprzone', 'tags': ['adjectival', 'neuter', 'participle', 'passive', 'singular'], 'source': 'conjugation'}, {'form': 'pieprzeni', 'tags': ['adjectival', 'participle', 'passive', 'plural', 'virile'], 'source': 'conjugation'}, {'form': 'pieprzone', 'tags': ['adjectival', 'nonvirile', 'participle', 'passive', 'plural'], 'source': 'conjugation'}, {'form': 'pieprząc', 'tags': ['adjectival', 'contemporary', 'participle'], 'source': 'conjugation'}, {'form': 'pieprzenie', 'tags': ['noun-from-verb'], 'source': 'conjugation'}]

# Tag categories
CASE_TAGS =  {'nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative', 'vocative'}
TENSE_TAGS = {'infinitive', 'present', 'past', 'future', 'conditional', 'imperative'}
PERSON_TAGS = {'first-person', 'second-person', 'third-person', 'impersonal'}
NUMBER_TAGS = {'singular', 'plural'}
GENDER_TAGS = {'masculine', 'feminine', 'neuter'}
VIRILITY_TAGS = {'virile', 'nonvirile'}
ANIMACY_TAGS = {'animate', 'inanimate'}
ALL_TAGS = CASE_TAGS | TENSE_TAGS | PERSON_TAGS | NUMBER_TAGS | GENDER_TAGS | VIRILITY_TAGS | ANIMACY_TAGS | {'derogatory'}

global_tags = {'case':('nominative','genitive'),
                'tense': ('present','past'),
                'person': (),
                'number': ('singular','plural'),
                'gender': ('masculine','feminine', 'neuter'),
                'virility':(),
                'animacy':('animate', 'inanimate')}

all_tags = {'case':('nominative', 'genitive', 'dative', 'accusative', 'instrumental', 'locative', 'vocative'),
                'tense': ('infinitive','present', 'past', 'future', 'conditional', 'imperative'),
                'person': ('first-person', 'second-person', 'third-person', 'impersonal'),
                'number': ('singular', 'plural'),
                'gender': ('masculine', 'feminine', 'neuter'),
                'virility':('virile', 'nonvirile'),
                'animacy':('animate', 'inanimate')}

#####
##### turn zero: get inflection type #####
def get_inflection_from_source(data):
    """returns the first one as a string (e.g. 'pl-conj-ai').
    
    Note:it is possible that sometimes multiple inflection templates exist, but they are not very different
    e.g. if the one inflection template is pl-conj-ai, then another template is pl-conj-ai-IX,
    but not pl-decl or pl-conj-ap. Thus this function returns the string instead of the list"""
    for item in data:
        if item.get('source'):
            return item['source']
    return None  # Return None if no match found

def get_inflection_type(data):
    """
    Returns 'conj' if the output of get_inflection_type contains 'conj'.
    """
    inflection_type = get_inflection_from_source(data)
    if inflection_type and 'conjugation' in inflection_type:
        return 'conjugation'
    elif inflection_type and 'declension' in inflection_type:
        return 'declension'
    return None  # Return None if 'conj' is not found or get_inflection_type returns None



def create_integer_list(top_header):
    # The width of the 2D list is the length of the first sublist in top_header
    width = len(top_header[0])
    # Create a list of integers from 0 to width - 1
    integer_list = list(range(width))
    return integer_list

# determining horizontal_index
def find_horizontal_index(top_header, dictionary):
    # Extract the tags from the dictionary
    tags = set(dictionary['tags'])
    pivot_row = None

    # Iterate over each row in the top_header to find the pivot row
    for row in top_header:
        if any(tag in row for tag in tags):
            pivot_row = row

    # If a pivot row is found, find the positions of the tags in this row
    if pivot_row:
        positions = [i for i, element in enumerate(pivot_row) if element in tags]
        # Return the position or list of positions
        return positions

    # If no pivot row is found, return the list that spans full width of the dictionary
    full_range_int_list = create_integer_list(top_header)
    return full_range_int_list

def find_vertical_index(side_header, dictionary):
    positions = []
    tags = set(dictionary.get('tags', []))  # Extract tags from the dictionary

    for column in zip(*side_header):  # Iterate through columns
        current_positions = [i for i, cell in enumerate(column) if any(tag in cell for tag in tags)]
        if current_positions:
            if positions:
                # Keep only positions that are in both current_positions and positions
                positions = [pos for pos in positions if pos in current_positions]
            else:
                positions = current_positions
        elif not positions:
            # If positions is still empty in the first iteration, populate it
            positions = current_positions

    return positions

def create_padding_empty_lists(top_header, side_header):
    """
    Creates two new lists of lists with empty strings based on the dimensions of the input lists.

    Parameters:
    top_header (list of lists): The first input list of lists.
    side_header (list of lists): The second input list of lists.

    Returns:
    tuple: Two new lists of lists with empty strings.
    """
    # Measure the heights and widths of the input lists
    height1, width1 = len(top_header), len(top_header[0])
    height2, width2 = len(side_header), len(side_header[0])

    # Create two new lists of lists based on the dimensions of the input lists
    top_left_corner = [["" for _ in range(width2)] for _ in range(height1)]
    bottom_right_corner = [["" for _ in range(width1)] for _ in range(height2)]

    return top_left_corner, bottom_right_corner

def place_form(dictionary, horizontal_indices, vertical_indices, bottom_right_corner):
    """
    Modifies a 2D list (bottom_right_corner) by inserting a specific value from a dictionary into specified positions,
    appending to existing values if they are non-empty.

    Parameters:
    dictionary (dict): A dictionary containing at least a 'form' key.
    horizontal_indices (list of int): List of column indices for modification.
    vertical_indices (list of int): List of row indices for modification.
    bottom_right_corner (list of list of str): The 2D list to be modified.

    Returns:
    bottom_right_corner (list of list of str): The modified 2D list with the 'form' value inserted.
    """
    # Retrieve the value associated with the 'form' key in the dictionary
    form_value = dictionary.get('form', '')

    # Modify the 2D list based on the specified indices
    for v_index in vertical_indices:
        for h_index in horizontal_indices:
            # Check if indices are within bounds
            if v_index < len(bottom_right_corner) and h_index < len(bottom_right_corner[v_index]):
                # Check if the current position contains a non-empty string
                if bottom_right_corner[v_index][h_index]:
                    # Append form_value to the existing value
                    bottom_right_corner[v_index][h_index] += ' / ' + form_value
                else:
                    # Set the current position to form_value
                    bottom_right_corner[v_index][h_index] = form_value

    return bottom_right_corner

def process_dictionaries(list_of_dictionary, top_header, side_header, bottom_right_corner):
    for dictionary in list_of_dictionary:
        h_index = find_horizontal_index(top_header, dictionary)
        v_index = find_vertical_index(side_header, dictionary)
        bottom_right_corner = place_form(dictionary, h_index, v_index, bottom_right_corner)
    return bottom_right_corner

def combine_2d_lists(top_left, top_right, bottom_left, bottom_right):
    # Combine top parts
    top_combined = [tl + tr for tl, tr in zip(top_left, top_right)]

    # Combine bottom parts
    bottom_combined = [bl + br for bl, br in zip(bottom_left, bottom_right)]

    # Combine top and bottom
    combined = top_combined + bottom_combined

    return combined

def map_by_tag(data,  global_tags):
    """
    Create 2D list of list based on the forms.
    Example output:
    [['', 'plural', 'plural'],
    ['', 'virile', 'nonvirile'],
    ['nominative', 'kilkunastu', 'kilkanaście'],
    ['genitive', '', 'kilkunastu'],
    ['dative', '', 'kilkunastu'],
    ['accusative', 'kilkunastu', 'kilkanaście'],
    ['instrumental', '', 'kilkunastoma'],
    ['locative', '', 'kilkunastu'],
    ['vocative', 'kilkunastu', 'kilkanaście']]
    """
    try:
        top_header = make_top_header(global_tags)
        side_header = make_side_header(global_tags, data)

        header_sizes = {'top':{'height':len(top_header), 'width':len(top_header[0]) + len(side_header[0])}, 
                        'side':{'height':len(side_header), 'width':len(side_header[0])}}

        top_left_corner, bottom_right_corner = create_padding_empty_lists(top_header, side_header)
        modified_bottom_right_corner = process_dictionaries(data, top_header, side_header, bottom_right_corner)
        top_header = fill_empty_strings_top(top_header)
        side_header = fill_empty_strings_side(side_header)
        output_grid = combine_2d_lists(top_left_corner, top_header, side_header, modified_bottom_right_corner)
        outcome = True

        return output_grid, outcome, header_sizes
    except Exception as e:
        # if any(word_dict.get('form') == 'pieprzyłem' for word_dict in data):
        #     traceback.print_exc()
        outcome = False
        return None, outcome, None
    
def process_row(row):
    output_grid, outcome, header_sizes = map_by_tag(row['forms_with_added_tags'], row['global_tags_in_add_tags'])
    return pd.Series([output_grid, outcome, header_sizes])

@asset
def map_by_tag_apply(
    context: AssetExecutionContext,
    add_all_missing_tags_apply: pd.DataFrame
) -> pd.DataFrame:
    """
    Create the pd.Series of 2D list of list based on the forms.
    Example row in output is:
    [['', 'plural', 'plural'],
    ['', 'virile', 'nonvirile'],
    ['nominative', 'kilkunastu', 'kilkanaście'],
    ['genitive', '', 'kilkunastu'],
    ['dative', '', 'kilkunastu'],
    ['accusative', 'kilkunastu', 'kilkanaście'],
    ['instrumental', '', 'kilkunastoma'],
    ['locative', '', 'kilkunastu'],
    ['vocative', 'kilkunastu', 'kilkanaście']]

    Note: In metadata, failure_rate_percentage here is based on the number of failure in map_by_tag,
    out of the rows that succeeded in previous 'add_all_missing_tags'
    """
    log = get_dagster_logger()

    df = add_all_missing_tags_apply
    # map_by_tag_apply = pd.DataFrame()
    map_by_tag_apply = df

    # log.info(df.head(3).to_markdown())
    map_by_tag_apply[['map_by_tag', 'map_by_tag_outcome', 'header_sizes']] = \
    df.apply(process_row, axis=1)

    failure_count = int(((map_by_tag_apply['map_by_tag_outcome']== False) & (map_by_tag_apply['add_tag_processed']== True)).sum())
    total_rows_count = int((add_all_missing_tags_apply['add_tag_processed']== True).sum())
    failure_rate = failure_count / total_rows_count
    failure_rate_percentage = round(failure_rate * 100, 2)

    context.add_output_metadata(
        metadata={
            "map_by_tag_preview": MetadataValue.md(map_by_tag_apply.map_by_tag.head(3).to_markdown()),
            "failure_example": MetadataValue.md(map_by_tag_apply[(map_by_tag_apply['map_by_tag_outcome']== False) & (map_by_tag_apply['add_tag_processed']== True)].head(10).to_markdown()),
            "failure_count": MetadataValue.int(failure_count),
            "failure_percent": MetadataValue.float(failure_rate_percentage),
        }
    )
    return map_by_tag_apply[['map_by_tag', 'map_by_tag_outcome', 'header_sizes']]


if __name__ == "__main__":
    data = verb3
    processed_data, invalid_forms, global_tags, is_processed = process_entries(data)
    print(processed_data)
    print(global_tags)
    output_grid, outcome, header_sizes = map_by_tag(processed_data, global_tags)
    pprint.pprint(output_grid, width=250)
