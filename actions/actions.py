import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import datetime, timedelta


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
                    dispatcher.utter_message(
                        text=f"Light {light_id} is already on 💡.")
                    return [SlotSet("light_id", None)]
                else:
                    change_response = requests.put(
                        change_state_url, json={"lightstate": "ON"})

                    if change_response.status_code == 200:
                        dispatcher.utter_message(
                            text=f"Light {light_id} has been turned on 💡.")
                    else:
                        dispatcher.utter_message(
                            text="Failed to turn on the light 💡.")
            else:
                dispatcher.utter_message(
                    text="Error: Unable to retrieve the light status 💡.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the light control API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

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
                    dispatcher.utter_message(
                        text=f"Light {light_id} is already off 💡.")
                    return [SlotSet("light_id", None)]
                else:
                    change_response = requests.put(
                        change_state_url, json={"lightstate": "OFF"})

                    if change_response.status_code == 200:
                        dispatcher.utter_message(
                            text=f"Light {light_id} has been turned off 💡.")
                    else:
                        dispatcher.utter_message(
                            text="Failed to turn off the light 💡.")
            else:
                dispatcher.utter_message(
                    text="Error: Unable to retrieve the light status 💡.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the light control API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return [SlotSet("light_id", None)]
    
# For Zone ON
class ActionZoneOnLight(Action):
        
    def name(self) -> str:
        return "action_zone_on_lights"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        zone_name = tracker.get_slot("zone_name")

        if zone_name is None:
            dispatcher.utter_message(text="Please specify a valid Zone Name.")
            return []
        if len(zone_name.split()) < 2: 
            list_all_zones_url = "http://localhost:8080/api/zones/AllZone"

            try:
                response = requests.get(list_all_zones_url)

                if response.status_code == 200:
                    zones = response.json()
                    print(zones)

                    if isinstance(zones, list):
                            zone_list = "\n".join([zone['name'] for zone in zones if 'name' in zone])
                            dispatcher.utter_message(
                                text=f"Please specify a valid Zone Name. Here are the available zones:\n{zones}"
                            )
                    else:
                            dispatcher.utter_message(
                                text="Error: Zone data is not in the expected format."
                            )

                else:
                    dispatcher.utter_message(text="Failed to fetch the list of zones.")
            
            except requests.exceptions.ConnectionError:
                dispatcher.utter_message(text="Error: Unable to connect to the zone list API.")
            except Exception as e:
                dispatcher.utter_message(text=f"An unexpected error occurred: {str(e)}")

            return []


        zone_name_parts = zone_name.split()
        if len(zone_name_parts) >= 2:
            zone_name_parts[1] = zone_name_parts[1].upper()  

        updated_zone_name = ' '.join(zone_name_parts)
        print(updated_zone_name)
        change_state_url = f"http://localhost:8080/api/lights/update-state/{updated_zone_name}"

        try:
            change_response = requests.put(
                change_state_url, json={"lightstate": "ON"})

            if change_response.status_code == 200:
                dispatcher.utter_message(
                    text=f"{zone_name} lights have been turned on 💡.")
            elif change_response.status_code == 208:  
                dispatcher.utter_message(
                    text=f"{zone_name} lights are already on 💡.")
            else:
                dispatcher.utter_message(
                    text=f"Failed to turn on the lights in {zone_name} 💡.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the light control API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return [SlotSet("zone_name", None)]  

# For Zone OFF
class ActionZoneOffLight(Action):
        
    def name(self) -> str:
        return "action_zone_off_lights"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        zone_name = tracker.get_slot("zone_name")

        print(zone_name)
        if zone_name is None:
            dispatcher.utter_message(text="Please specify a valid Zone Name.")
            return []
        if len(zone_name.split()) < 2: 
            list_all_zones_url = "http://localhost:8080/api/zones/AllZone"

            try:
                response = requests.get(list_all_zones_url)

                if response.status_code == 200:
                    zones = response.json()

                    if isinstance(zones, list):
                            zone_string = "\n".join(zones)
                            print(zone_string)
                            dispatcher.utter_message(
                                text=f"Please specify a valid Zone Name. Here are the available zones:\n{zone_string}"
                            )
                    else:
                            dispatcher.utter_message(
                                text="Error: Zone data is not in the expected format."
                            )

                else:
                    dispatcher.utter_message(text="Failed to fetch the list of zones.")
            
            except requests.exceptions.ConnectionError:
                dispatcher.utter_message(text="Error: Unable to connect to the zone list API.")
            except Exception as e:
                dispatcher.utter_message(text=f"An unexpected error occurred: {str(e)}")

            return []
        
        zone_name_parts = zone_name.split()
        if len(zone_name_parts) >= 2:
            zone_name_parts[1] = zone_name_parts[1].upper()  

        updated_zone_name = ' '.join(zone_name_parts)
        print(updated_zone_name)
        change_state_url = f"http://localhost:8080/api/lights/update-state/{updated_zone_name}"

        try:
            change_response = requests.put(
                change_state_url, json={"lightstate": "OFF"})

            if change_response.status_code == 200:
                dispatcher.utter_message(
                    text=f"{zone_name} lights have been turned off 💡.")
            elif change_response.status_code == 208:  
                dispatcher.utter_message(
                    text=f"{zone_name} lights are already off 💡.")
            else:
                dispatcher.utter_message(
                    text=f"Failed to turn off the lights in {zone_name} 💡.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the light control API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return [SlotSet("zone_name", None)]  


class ActionSchedulesLight(Action):
    
    def name(self) -> str:
        return "action_schedules"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        zone_name = tracker.get_slot("zone_name")
        light_state = tracker.get_slot("light_state")
        brightness_level = tracker.get_slot("brightness_level")
        start_time = tracker.get_slot("start_time")
        end_time = tracker.get_slot("end_time")
        rule = tracker.get_slot("rule")
        end_year = tracker.get_slot("end_year")
        schedule_name = tracker.get_slot("schedule_name")
        tag = tracker.get_slot("tag")
        light_state_end = tracker.get_slot("light_state_end")

        print(zone_name, light_state, brightness_level, start_time, end_time, rule, end_year)
        print(schedule_name, tag, light_state_end)

        if zone_name is None or schedule_name is None:
            dispatcher.utter_message(text="Please specify valid details.")
            return []

        if brightness_level is None:
            brightness_level = 100
        current_time = datetime.now()
        if start_time is None:
            current_time = datetime.now()
            start_time = current_time.strftime("%Y-%m-%d %H:%M")
            print(f"Default start time set to: {start_time}")

        try:
            if "PM" in start_time or "AM" in start_time:
                parsed_start_time = datetime.strptime(start_time, "%I %p")  
                parsed_start_time = parsed_start_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
            else:
                parsed_start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        except ValueError as e:
            dispatcher.utter_message(text=f"Error parsing start time: {str(e)}")
            return []

        start_time_millis = int(parsed_start_time.timestamp() * 1000)
        print(f"Start time in milliseconds: {start_time_millis}")

        # Handle end_year
        if end_year is None:
            end_year_time = parsed_start_time + timedelta(days=365)
            end_year_millis = int(end_year_time.timestamp() * 1000)
            print(f"End year {end_year_millis}")
        else:
            try:
                parsed_end_year = datetime.strptime(end_year, "%m/%d/%Y")
                end_year_time = parsed_end_year.replace(hour=0, minute=0, second=0)
                end_year_millis = int(end_year_time.timestamp() * 1000)
                print(f"End year in milliseconds: {end_year_millis}")
            except ValueError as e:
                dispatcher.utter_message(text=f"Error parsing end year: {str(e)}")
                return []

        if end_time is not None:
            try:
                parsed_end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
            except ValueError:
                try:
                    parsed_end_time = datetime.strptime(end_time, "%I %p")
                    parsed_end_time = parsed_end_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
                except ValueError as e:
                    dispatcher.utter_message(text=f"Error parsing end time: {str(e)}")
                    return []

            end_time_millis = int(parsed_end_time.timestamp() * 1000)
            print(f"End time in milliseconds: {end_time_millis}")
        else:
            dispatcher.utter_message(text="Please provide an end time.")
            return []


        schedule_payload = {  
            "priority": 1,  
            "lightstate": light_state_end,
            "lightlevel": brightness_level,
            "starttime": start_time_millis,  
            "endtime": end_time_millis,       
            "recurrenceRule": rule,
            "startdate": start_time_millis,
            "enddate": end_year_millis,
            "schedulename": schedule_name,
            "zone": {
                "zoneid": 1
            }
        }

        change_state_url = "http://localhost:8080/api/schedules/save"

        try:
            change_response = requests.post(change_state_url, json=schedule_payload)

            if change_response.status_code == 200:
                dispatcher.utter_message(text="Schedules have been added.")
            elif change_response.status_code == 208:  
                dispatcher.utter_message(text="Schedules already exist.")
            else:
                dispatcher.utter_message(text="Failed to save schedules.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(text="Error: Unable to connect to the schedules control API.")
        except Exception as e:
            dispatcher.utter_message(text=f"An unexpected error occurred: {str(e)}")

        return [SlotSet("zone_name", None)]
