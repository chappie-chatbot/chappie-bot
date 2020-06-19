## fallback
- utter_default

## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## list capabilities
* capabilities
  - utter_capabilities

## thanks
* thank
  - utter_welcome

## timeEntryRequest
* timeEntryRequest
    - action_get_active_assignments
    - utter_ask_time_entry_details

## timeEntryInfo
* timeEntryInfo
    - submit_time_entry_info
    - form{"name": "submit_time_entry_info"}
    - slot{"requested_slot": "dayOfWeek"}
    - slot{"requested_slot": "start"}
    - slot{"requested_slot": "end"}
    - slot{"requested_slot": "worksite"}
    - slot{"requested_slot": "assignment"}
    - form{"name": null}
* thank
  - utter_welcome