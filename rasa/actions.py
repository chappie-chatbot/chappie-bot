# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
import json
from typing import Any, Text, Dict, List, Union

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset

# This is a simple example for a custom action which utters "Hello World!"

#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionGetActiveAssignmetns(Action):

    def name(self) -> Text:
        print("Get assignments")
        return "action_get_active_assignments"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:

        providerNumber = tracker.sender_id;
        print(providerNumber)
        print("Getting active assignments for provider: "+providerNumber)
        dispatcher.utter_message("Fetching your assignments")

        url = 'http://host.docker.internal:8089/getProviderInfo?providerNumber={providerNumber}'.format(providerNumber=providerNumber)

        response = requests.get(url).text
        assignments = json.loads(response)['assignments']

        assignmentsStr = ""
        for assignment in assignments:
            assignmentsStr = assignmentsStr+assignment['assignmentName'] + ","

        dispatcher.utter_message(assignmentsStr)
        return []

class SubmitTimeEntryInfo(FormAction):

    def name(self):
        return "submit_time_entry_info"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["start", "end", "worksite"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "worksite": self.from_entity(entity="worksite", intent=["timeEntryInfo"]),
            "start": self.from_entity(entity="start", intent=["timeEntryInfo"]),
            "end": self.from_entity(entity="end", intent=["timeEntryInfo"])
        };

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        worksite = tracker.get_slot('worksite');
        start = tracker.get_slot('start');
        end = tracker.get_slot('end');
        print(worksite)
        print(start)
        print(end)

        dispatcher.utter_message("Submitting time")
        dispatcher.utter_message(template="utter_time_entry_summary")
        return []

class ActionClearSlots(Action):
    def name(self) -> Text:
        return "action_clear_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Clearing all slots")
        return [AllSlotsReset()]
