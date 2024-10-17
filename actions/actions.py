# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
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


import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionTurnOnLight(Action):

    def name(self) -> str:
        return "action_turn_on_light"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Fetch the light_id from the slot
        light_id = tracker.get_slot("light_id") 
        
        if light_id is None:
            dispatcher.utter_message(text="Please specify a valid light ID.")
            return []

        url = f"http://localhost:8080/api/lights/change/{light_id}"
        
        try:
            # Send a request to update the light state to "ON"
            response = requests.put(url, json={"lightstate": "ON"})
            
            if response.status_code == 200:
                dispatcher.utter_message(text=f"Light {light_id} has been turned on.")
            else:
                dispatcher.utter_message(text="Failed to turn on the light.")
        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(text="Error: Unable to connect to the light control API.")
        except Exception as e:
            dispatcher.utter_message(text=f"An unexpected error occurred: {str(e)}")

        return []

class ActionTurnOffLight(Action):

    def name(self) -> str:
        return "action_turn_off_light"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Fetch the light_id from the slot
        light_id = tracker.get_slot("light_id") 
        
        if light_id is None:
            dispatcher.utter_message(text="Please specify a valid light ID.")
            return []

        url = f"http://localhost:8080/api/lights/change/{light_id}"
        
        try:
            # Send a request to update the light state to "OFF"
            response = requests.put(url, json={"lightstate": "OFF"})
            
            if response.status_code == 200:
                dispatcher.utter_message(text=f"Light {light_id} has been turned off.")
            else:
                dispatcher.utter_message(text="Failed to turn off the light.")
        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(text="Error: Unable to connect to the light control API.")
        except Exception as e:
            dispatcher.utter_message(text=f"An unexpected error occurred: {str(e)}")

        return []
