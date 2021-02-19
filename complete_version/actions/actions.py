# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
import os
import re

def google_translate(word):
    from google_trans_new import google_translator
    translator = google_translator()
    return translator.translate(word, lang_src='de', lang_tgt='en')

class ActionLanguageSearch(Action):

    def name(self) -> Text:
        return "action_lang_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "languages.csv")
        wals_data = pd.read_csv(data_path)
        entities = list(tracker.get_latest_entity_values("language"))
        print(entities)

        if len(entities) > 0:
            query_lang = entities.pop()
            query_lang = str(google_translate(query_lang))
            query_lang = query_lang.lower().capitalize()
            query_lang = query_lang.strip()
            print(query_lang)
            print("____")
            print(wals_data["Name"] == query_lang)
            out_row = wals_data[wals_data["Name"] == query_lang].to_dict("records")
            print(out_row)

            if len(out_row) > 0:
                out_row = out_row[0]
                out_text = "Die Sprache %s gehört zur Familie %s\n mit Gattung als  %s\n und hat ISO-Code %s" % (out_row["Name"], out_row["Family"], out_row["Genus"], out_row["ISO_codes"])
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "Es tut uns leid! Wir haben keine Aufzeichnungen für die Sprache%s" % query_lang)

        return []



class ActionCountrySearch(Action):    
    def name(self) -> Text:
        return "country_lang_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # change the data path according to where you are fetching the data from 
        data_path = os.path.join("data", "cldf-datasets-wals-014143f", "cldf", "country.csv") 
        wals_data = pd.read_csv(data_path)
        country_entitiy = list(tracker.get_latest_entity_values("Land")) # assuming that the entity name is country

        if len(country_entitiy) > 0:
            country_name = country_name_gi = country_entitiy.pop()
            country_name = translator.translate(country_name, dest='en').text
            country_name = country_name.strip()

            out_row = wals_data[wals_data["Land"] == country_name]

            if len(out_row) > 0:
                language_name = out_row['Offizielle Sprache'].values[0]
                out_text = "Die Sprache %s wird gesprochen %s" % (language_name,country_name_gi)
                dispatcher.utter_message(text = out_text)
            else:
                dispatcher.utter_message(text = "Keine Datensätze gefunden für %s" % country_name_gi)

        return []
