from rasa_sdk import Action
from typing import Any, Dict, List, Text
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import datetime, timedelta
from cron import text_to_cron
from rasa_sdk.events import EventType
from typing import List, Dict, Text, Any
import ast


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
                text=f"An unexpected error occurred!!!!!!!!!: {str(e)}")

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
            list_all_zones_url = "http://localhost:8080/api/zones/list"

            try:
                response = requests.get(list_all_zones_url)

                if response.status_code == 200:
                    zones = response.json()
                    print(zones)

                    if isinstance(zones, list):
                        zone_list = "\n".join(
                            [zone['name'] for zone in zones if 'name' in zone])
                        dispatcher.utter_message(
                            text=f"Please specify a valid Zone Name. Here are the available zones:\n{zones}"
                        )
                    else:
                        dispatcher.utter_message(
                            text="Error: Zone data is not in the expected format."
                        )

                else:
                    dispatcher.utter_message(
                        text="Failed to fetch the list of zones.")

            except requests.exceptions.ConnectionError:
                dispatcher.utter_message(
                    text="Error: Unable to connect to the zone list API.")
            except Exception as e:
                dispatcher.utter_message(
                    text=f"An unexpected error occurred: {str(e)}")

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
            list_all_zones_url = "http://localhost:8080/api/zones/list"

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
                    dispatcher.utter_message(
                        text="Failed to fetch the list of zones.")

            except requests.exceptions.ConnectionError:
                dispatcher.utter_message(
                    text="Error: Unable to connect to the zone list API.")
            except Exception as e:
                dispatcher.utter_message(
                    text=f"An unexpected error occurred: {str(e)}")

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
        priority = tracker.get_slot("priority")

        print(zone_name, light_state, brightness_level,
              start_time, end_time, rule, end_year)
        print(schedule_name, tag, light_state_end)
        print(priority)

        if priority is None:
            priority = 1

        if priority == "high":
            priority = 1
        if priority == "medium":
            priority = 2
        if priority == "low":
            priority = 3

        if zone_name is None or schedule_name is None:
            dispatcher.utter_message(text="Please specify valid details.")
            return []

        if light_state == "on" or light_state == "ON" or light_state == "activate" or light_state == "Activate":
            light_state = "ON"

        if light_state == "off" or light_state == "OFF" or light_state == "deactivate" or light_state == "Deactivate":
            light_state = "OFF"
        if light_state_end == "on" or light_state_end == "ON" or light_state_end == "activate" or light_state_end == "Activate" or light_state_end == "turn them on":
            light_state_end = "ON"

        if light_state_end == "off" or light_state_end == "OFF" or light_state_end == "deactivate" or light_state_end == "Deactivate" or light_state_end == "turn them off":
            light_state_end = "OFF"
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
                parsed_start_time = parsed_start_time.replace(
                    year=current_time.year, month=current_time.month, day=current_time.day)
            else:
                parsed_start_time = datetime.strptime(
                    start_time, "%Y-%m-%d %H:%M")
        except ValueError as e:
            dispatcher.utter_message(
                text=f"Error parsing start time: {str(e)}")
            return []

        start_time_millis = int(parsed_start_time.timestamp() * 1000)
        print(f"Start time in milliseconds: {start_time_millis}")

        if end_year is None:
            end_year_time = parsed_start_time + timedelta(days=365)
            end_year_millis = int(end_year_time.timestamp() * 1000)
            print(f"End year {end_year_millis}")
        else:
            try:
                parsed_end_year = datetime.strptime(end_year, "%m/%d/%Y")
                end_year_time = parsed_end_year.replace(
                    hour=0, minute=0, second=0)
                end_year_millis = int(end_year_time.timestamp() * 1000)
                print(f"End year in milliseconds: {end_year_millis}")
            except ValueError as e:
                dispatcher.utter_message(
                    text=f"Error parsing end year: {str(e)}")
                return []

        if end_time is not None:
            try:
                parsed_end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
            except ValueError:
                try:
                    parsed_end_time = datetime.strptime(end_time, "%I %p")
                    parsed_end_time = parsed_end_time.replace(
                        year=current_time.year, month=current_time.month, day=current_time.day)
                except ValueError as e:
                    dispatcher.utter_message(
                        text=f"Error parsing end time: {str(e)}")
                    return []

            end_time_millis = int(parsed_end_time.timestamp() * 1000)
            print(f"End time in milliseconds: {end_time_millis}")
        else:
            dispatcher.utter_message(text="Please provide an end time.")
            return []

        zoneidbyname = f"http://localhost:8080/api/zones/byName/{zone_name}"

        try:
            status_response = requests.get(zoneidbyname)

            if status_response.status_code == 200:
                zoneId_response = status_response.json()
                print(zoneId_response)

                if isinstance(zoneId_response, dict):
                    zoneId = zoneId_response.get("zoneid")
                    if zoneId is None:
                        dispatcher.utter_message(
                            text="Error: Zone ID not found in the response.")
                        return []
                elif isinstance(zoneId_response, int):
                    zoneId = zoneId_response
                else:
                    dispatcher.utter_message(
                        text="Error: Unexpected response format.")
                    return []

            else:
                dispatcher.utter_message(
                    text=f"Error: Received unexpected status code {status_response.status_code}.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the zone list API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")
            return []

        schedule_payload = {
            "priority": priority,
            "lightstate": light_state_end,
            "lightlevel": brightness_level,
            "starttime": start_time_millis,
            "endtime": end_time_millis,
            "recurrenceRule": text_to_cron(rule),
            "startdate": start_time_millis,
            "enddate": end_year_millis,
            "schedulename": schedule_name,
            "zone": {
                "zoneid": zoneId
            }
        }

        change_state_url = "http://localhost:8080/api/schedules/save"

        try:
            change_response = requests.post(
                change_state_url, json=schedule_payload)

            if change_response.status_code == 200:
                dispatcher.utter_message(text="Schedules have been added.")
            elif change_response.status_code == 208:
                dispatcher.utter_message(text="Schedules already exist.")
            else:
                dispatcher.utter_message(text="Failed to save schedules.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the schedules control API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred 222: {str(e)}")

        return [
            SlotSet("zone_name", None),
            SlotSet("light_state", None),
            SlotSet("brightness_level", None),
            SlotSet("start_time", None),
            SlotSet("end_time", None),
            SlotSet("rule", None),
            SlotSet("end_year", None),
            SlotSet("schedule_name", None),
            SlotSet("tag", None),
            SlotSet("light_state_end", None),
        ]


class ActionZoneBrightness(Action):

    def name(self) -> str:
        return "action_brightness"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        zone_name = tracker.get_slot("zone_name")
        brightness_level = tracker.get_slot("brightness_level")

        if zone_name is None:
            dispatcher.utter_message(text="Please specify a Zone Name.")
            return []
        if brightness_level is None:
            dispatcher.utter_message(text="Please specify a Brightness level.")
            return []

        change_state_url = f"http://localhost:8080/api/lights/update-brightness/{zone_name}?brightnessLevel={brightness_level}"

        try:
            change_response = requests.put(change_state_url)

            if change_response.status_code == 200:
                dispatcher.utter_message(
                    text=f"The brightness for zone '{zone_name}' has been updated to {brightness_level}.")
            else:
                dispatcher.utter_message(
                    text="Failed to update the brightness. Please try again later.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the light control API. Please check the connection.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return [SlotSet("zone_name", None), SlotSet("brightness_level", None)]


class ActionLightBrightness(Action):

    def name(self) -> str:
        return "action_brightness_light"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        zone_name = tracker.get_slot("zone_name")
        brightness_level = tracker.get_slot("brightness_level")
        light_id = tracker.get_slot("light_id")

        if zone_name is None:
            dispatcher.utter_message(text="Please specify a Zone Name.")
            return []
        if brightness_level is None:
            dispatcher.utter_message(text="Please specify a Brightness level.")
            return []
        if light_id is None:
            dispatcher.utter_message(text="Please specify a Light Id.")
            return []

        change_state_url = f"http://localhost:8080/api/lights/brightness/update/zone/light/{zone_name}?lightid={light_id}&brightnessLevel={brightness_level}"

        try:
            change_response = requests.put(change_state_url)

            if change_response.status_code == 200:
                dispatcher.utter_message(
                    text=f"The brightness for zone '{zone_name}' has been updated to {brightness_level} for the light Id {light_id}.")
            else:
                dispatcher.utter_message(
                    text="Failed to update the brightness. Please try again later.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the light control API. Please check the connection.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return [SlotSet("zone_name", None), SlotSet("brightness_level", None), SlotSet("light_id", None)]


class ActionListZone(Action):

    def name(self) -> str:
        return "action_list_zone"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        list_all_zones_url = "http://localhost:8080/api/zones/list"

        try:
            response = requests.get(list_all_zones_url)

            if response.status_code == 200:
                zones = response.json()

                if isinstance(zones, list):
                    table_header = "Zone Name | Address\n" + "-"*30
                    table_rows = [
                        f"{zone.get('name', 'Unnamed Zone')} | {zone.get('address', 'No Address')}"
                        for zone in zones
                    ]
                    zone_table = table_header + "\n" + "\n".join(table_rows)

                    dispatcher.utter_message(
                        text=f"Here are the available zones:\n{zone_table}"
                    )
                else:
                    dispatcher.utter_message(
                        text="Error: Zone data is not in the expected format."
                    )
            else:
                dispatcher.utter_message(
                    text="Failed to fetch the list of zones.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the zone list API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return []


class ActionListZoneLights(Action):

    def name(self) -> str:
        return "action_list_zone_light"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        zone_name = tracker.get_slot("zone_name")
        list_all_zones_url = f"http://localhost:8080/api/lights/zone/light/{zone_name}"
        if zone_name is None:
            dispatcher.utter_message(text="Please specify a Zone Name.")
            return []
        try:
            response = requests.get(list_all_zones_url)

            if response.status_code == 200:
                zones = response.json()

                if isinstance(zones, list):
                    table_header = "Light Id | Lightstate | Brightness\n" + "-"*30
                    table_rows = [
                        f" {zone.get('lightid', 'Unnamed lightid')} | {zone.get('lightstate', 'Unnamed lightstate')} | {zone.get('lightlevel', 'No lightlevel')}"
                        for zone in zones
                    ]
                    zone_table = table_header + "\n" + "\n".join(table_rows)

                    dispatcher.utter_message(
                        text=f"Here are the available {zone_name}:\n{zone_table}"
                    )
                else:
                    dispatcher.utter_message(
                        text="Error: Zone data is not in the expected format."
                    )
            else:
                dispatcher.utter_message(
                    text="Failed to fetch the list of zones.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the zone list API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return [SlotSet("zone_name", None)]


class ActionLightsStatus(Action):

    def name(self) -> str:
        return "action_check_light_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        light_id = tracker.get_slot("light_id")
        light_status_url = f"http://localhost:8080/api/lights/list/{light_id}"

        if light_id is None:
            dispatcher.utter_message(text="Please specify a Light Id.")
            return []

        try:
            response = requests.get(light_status_url)

            if response.status_code == 200:
                light = response.json()

                if isinstance(light, dict) and "lightid" in light:
                    light_details = (
                        f"Light Id: {light.get('lightid', 'N/A')}\n"
                        f"Serial Number: {light.get('serialNumber', 'N/A')}\n"
                        f"Model: {light.get('model', 'N/A')}\n"
                        f"Light Level: {light.get('lightlevel', 'N/A')}\n"
                        f"Light State: {light.get('lightstate', 'N/A')}\n"
                        f"Zone: {light.get('zone', {}).get('name', 'N/A')}, "
                        f"{light.get('zone', {}).get('address', 'N/A')}"
                    )

                    dispatcher.utter_message(
                        text=f"Here is the status for light {light_id}:\n{light_details}"
                    )
                else:
                    dispatcher.utter_message(
                        text="Error: Unexpected response format from the API."
                    )
            else:
                dispatcher.utter_message(
                    text=f"Failed to fetch the status for light {light_id}. Please try again later."
                )

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the light status API."
            )
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}"
            )

        return [SlotSet("light_id", None)]


class ActionZoneLightStatus(Action):

    def name(self) -> str:
        return "action_check_zone_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        zone_name = tracker.get_slot("zone_name")
        zone_light_state_url = f"http://localhost:8080/api/lights/lights-state/zone/{zone_name}"
        light_brightness_url = f"http://localhost:8080/api/lights/zone/lightslevel/{zone_name}"

        if not zone_name:
            dispatcher.utter_message(text="Please specify a zone name.")
            return []

        try:
            state_response = requests.get(zone_light_state_url)
            brightness_response = requests.get(light_brightness_url)

            if state_response.status_code == 200 and brightness_response.status_code == 200:
                zonelightstatus = state_response.text
                zonelightbrightness = brightness_response.text

                print("Light Status:", zonelightstatus)
                print("Brightness:", zonelightbrightness)

                try:
                    zonelightstatus = ast.literal_eval(
                        zonelightstatus)
                    zonelightbrightness = ast.literal_eval(zonelightbrightness)

                    if isinstance(zonelightstatus, list) and isinstance(zonelightbrightness, list):
                        response_text = f"Zone: {zone_name}\n"

                        light_state = zonelightstatus[0] if zonelightstatus else "N/A"
                        brightness = zonelightbrightness[0] if zonelightbrightness else "N/A"
                        
                        response_text += f"Light State: {light_state}, \nBrightness: {brightness}\n"

                        dispatcher.utter_message(text=response_text)


                    else:
                        dispatcher.utter_message(
                            text="Error: The data returned from the API is not in the expected list format."
                        )

                except Exception as e:
                    dispatcher.utter_message(
                        text=f"Error parsing data: {str(e)}"
                    )
            else:
                dispatcher.utter_message(
                    text=f"Failed to fetch data for zone '{zone_name}'. Please try again later."
                )

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the zone light state or brightness API."
            )
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}"
            )

        return [SlotSet("zone_name", None)]




class ActionScheduleLight(Action):

    def name(self) -> Text:
        return "action_schedule_light"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if not tracker.get_slot("zone_name"):
            dispatcher.utter_message(text="For which zone would you like to schedule the light? (e.g)., For Zone A")
            return []

        if not tracker.get_slot("light_state"):
            dispatcher.utter_message(text="What should be the light state (on/off)? (e.g., Turn ON)")
            return []

        if not tracker.get_slot("brightness_level"):
            dispatcher.utter_message(text="What should be the light level (0-100)? (e.g., 90%)")
            return []

        if not tracker.get_slot("rule"):
            dispatcher.utter_message(text="Please specify the recurrence rule (e.g., 6 pm every Sunday).")
            return []

        if not tracker.get_slot("end_time"):
            dispatcher.utter_message(text="When should this schedule end? (e.g., End by 6 am)")
            return []

        if not tracker.get_slot("schedule_name"):
            dispatcher.utter_message(text="Please provide a name for this schedule.(e.g., Evening Lights)")
            return []

        if not tracker.get_slot("priority"):
            dispatcher.utter_message(text="Please specify the priority level for this schedule.(e.g., Make it 1)")
            return []

        zone_name = tracker.get_slot("zone_name")
        light_state = tracker.get_slot("light_state")
        light_level = tracker.get_slot("brightness_level")
        recurrence_rule = tracker.get_slot("rule")
        end_time = tracker.get_slot("end_time")
        schedule_name = tracker.get_slot("schedule_name")
        schedule_priority = tracker.get_slot("priority")

        confirmation_message = (
            f"Please confirm the following details:\n"
            f"- Zone: {zone_name}\n"
            f"- Light State: {light_state}\n"
            f"- Light Level: {light_level}\n"
            f"- Recurrence Rule: {recurrence_rule}\n"
            f"- End Time: {end_time}\n"
            f"- Schedule Name: {schedule_name}\n"
            f"- Schedule Priority: {schedule_priority}\n\n"
            "Do you confirm this schedule?"
        )
        
        dispatcher.utter_message(text=confirmation_message)
        return [SlotSet("confirmation", None)]  

class ActionConfirmSchedule(Action):

    def name(self) -> Text:
        return "action_confirm_schedule"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        confirmation = tracker.get_slot("confirmation")
        zone_name = tracker.get_slot("zone_name")
        light_state = tracker.get_slot("light_state")
        light_level = tracker.get_slot("brightness_level")
        recurrence_rule = tracker.get_slot("rule")
        end_time = tracker.get_slot("end_time")
        schedule_name = tracker.get_slot("schedule_name")
        schedule_priority = tracker.get_slot("priority")

        if light_state == "ON" or light_state == "on" or light_state == "On" or light_state == "oN":
            light_state = "ON"
        if light_state == "OFF" or light_state == "off" or light_state == "OFf" or light_state == "oFF" or light_state=="Off":
            light_state = "OFF"
        
        if confirmation == "yes":
            
            zoneidbyname = f"http://localhost:8080/api/zones/byName/{zone_name}"

            try:
                status_response = requests.get(zoneidbyname)

                if status_response.status_code == 200:
                    zoneId_response = status_response.json()
                    print(zoneId_response)

                    if isinstance(zoneId_response, dict):
                        zoneId = zoneId_response.get("zoneid")
                        if zoneId is None:
                            dispatcher.utter_message(
                                text="Error: Zone ID not found in the response.")
                            return []
                    elif isinstance(zoneId_response, int):
                        zoneId = zoneId_response
                    else:
                        dispatcher.utter_message(
                            text="Error: Unexpected response format.")
                        return []

                else:
                    dispatcher.utter_message(
                        text=f"Error: Received unexpected status code {status_response.status_code}.")

            except requests.exceptions.ConnectionError:
                dispatcher.utter_message(
                    text="Error: Unable to connect to the zone list API.")
            except Exception as e:
                dispatcher.utter_message(
                    text=f"An unexpected error occurred: {str(e)}")
                return []

            schedule_payload = {
                "priority": schedule_priority,
                "lightstate": light_state,
                "lightlevel": light_level,
                "starttime": light_level,
                "endtime": light_level,
                "recurrenceRule": recurrence_rule,
                "startdate": light_level,
                "enddate": light_level,
                "schedulename": schedule_name,
                "zone": {
                    "zoneid": zoneId
                }
            }

            change_state_url = "http://localhost:8080/api/schedules/save"

            try:
                change_response = requests.post(
                    change_state_url, json=schedule_payload)

                if change_response.status_code == 200:
                    dispatcher.utter_message(text="Schedule added successfully!")
                elif change_response.status_code == 208:
                    dispatcher.utter_message(text="Schedules already exist.")
                else:
                    dispatcher.utter_message(text="Failed to save schedules.")

            except requests.exceptions.ConnectionError:
                dispatcher.utter_message(
                    text="Error: Unable to connect to the schedules control API.")
            except Exception as e:
                dispatcher.utter_message(
                    text=f"An unexpected error occurred 222: {str(e)}")
        if confirmation == "no":
            dispatcher.utter_message(text="Schedule creation canceled.")
        
        return [SlotSet(slot, None) for slot in ["zone_name", "light_state", "brightness_level", "rule", "end_time", "schedule_name", "priority", "confirmation"]]
