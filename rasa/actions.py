# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/
import datetime
import json
import os
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
        print(datetime.datetime.now())
        print(providerNumber)
        print("Getting active assignments for provider: "+providerNumber)
        dispatcher.utter_message("Fetching your assignments")

        timeEntryHost = os.getenv('TIMEENTRY_HOST', "http://localhost:8089");
        url = '{}/getProviderInfo?providerNumber={}'.format(timeEntryHost,providerNumber)

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
        return ["dayOfWeek", "start", "end", "worksite", "assignment"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
        return {
            "worksite": self.from_entity(entity="worksite", intent=["timeEntryInfo"]),
            "start": self.from_entity(entity="start", intent=["timeEntryInfo"]),
            "end": self.from_entity(entity="end", intent=["timeEntryInfo"]),
            "dayOfWeek": self.from_entity(entity="dayOfWeek", intent=["timeEntryInfo"]),
            "assignment": self.from_entity(entity="assignment", intent=["timeEntryInfo"])
        };

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:

        dispatcher.utter_message("Processing time request")
        worksite = tracker.get_slot('worksite');
        start = tracker.get_slot('start');
        end = tracker.get_slot('end');
        dayOfWeek = tracker.get_slot('dayOfWeek');
        assignment = tracker.get_slot('assignment');
        print("worksite: " + worksite)
        print("start: " + start)
        print("end: " + end)
        print("assignment: " + assignment)
        print("dayOfWeek: " + dayOfWeek)

        if all(x is not None for x in [assignment, start, end, worksite, dayOfWeek]):
            dispatcher.utter_message("Submitting time")
            dispatcher.utter_message(template="utter_time_entry_summary")
        else:
            dispatcher.utter_message("Something went wrong, please try again later")

        return []

class ActionClearSlots(Action):
    def name(self) -> Text:
        return "action_clear_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("Clearing all slots")
        return [AllSlotsReset()]
