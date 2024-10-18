import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionTurnOnLight(Action):
    
    def name(self) -> str:
        return "action_turn_on_light"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        light_id = tracker.get_slot("light_id") 
        
        if light_id is None:
            dispatcher.utter_message(text="Please specify a valid light ID.")
            return []

        check_status_url = f"http://localhost:8080/api/lights/list/{light_id}"
        change_state_url = f"http://localhost:8080/api/lights/change/{light_id}"
        
        try:
            status_response = requests.get(check_status_url)
            
            if status_response.status_code == 200:
                current_status = status_response.json().get("lightstate", "OFF")
                
                if current_status == "ON":
                    dispatcher.utter_message(text=f"Light {light_id} is already on.")
                    return [SlotSet("light_id", None)]
                else:
                    change_response = requests.put(change_state_url, json={"lightstate": "ON"})
                    
                    if change_response.status_code == 200:
                        dispatcher.utter_message(text=f"Light {light_id} has been turned on.")
                    else:
                        dispatcher.utter_message(text="Failed to turn on the light.")
            else:
                dispatcher.utter_message(text="Error: Unable to retrieve the light status.")
        
        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(text="Error: Unable to connect to the light control API.")
        except Exception as e:
            dispatcher.utter_message(text=f"An unexpected error occurred: {str(e)}")
        
        return [SlotSet("light_id", None)]


class ActionTurnOffLight(Action):
    
    def name(self) -> str:
        return "action_turn_off_light"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        light_id = tracker.get_slot("light_id") 
        
        if light_id is None:
            dispatcher.utter_message(text="Please specify a valid light ID.")
            return []

        check_status_url = f"http://localhost:8080/api/lights/list/{light_id}"
        change_state_url = f"http://localhost:8080/api/lights/change/{light_id}"
        
        try:
            status_response = requests.get(check_status_url)
            
            if status_response.status_code == 200:
                current_status = status_response.json().get("lightstate", "ON")
                
                if current_status == "OFF":
                    dispatcher.utter_message(text=f"Light {light_id} is already off.")
                    return [SlotSet("light_id", None)]
                else:
                    change_response = requests.put(change_state_url, json={"lightstate": "OFF"})
                    
                    if change_response.status_code == 200:
                        dispatcher.utter_message(text=f"Light {light_id} has been turned off.")
                    else:
                        dispatcher.utter_message(text="Failed to turn off the light.")
            else:
                dispatcher.utter_message(text="Error: Unable to retrieve the light status.")
        
        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(text="Error: Unable to connect to the light control API.")
        except Exception as e:
            dispatcher.utter_message(text=f"An unexpected error occurred: {str(e)}")
        
        return [SlotSet("light_id", None)]
