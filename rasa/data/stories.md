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

## time entry form
* start
    - time_entry_form                   <!--Run the time_entry_form action-->
    - form{"name": "time_entry_form"}   <!--Activate the form-->
    - form{"name": null}                <!--Deactivate the form-->
    - utter_time_entry_summary
    - action_clear_slots