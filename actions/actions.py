from typing import Any, Dict, Text
from rasa_sdk import Action
from typing import Any, Dict, List, Text
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset
from datetime import datetime, timedelta
from cron import text_to_cron
from rasa_sdk.events import EventType
from typing import List, Dict, Text, Any
import ast
from rasa_sdk import Tracker, FormValidationAction
from datetime import datetime
from timeToMillis import extract_start_time_millis


class ActionTurnOnLight(Action):
    def name(self) -> str:
        return "action_turn_on_light"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        light_id = tracker.get_slot("light_id")

        if light_id is None:
            dispatcher.utter_message(text="Please specify a valid light ID.")
            return [AllSlotsReset()]

        change_state_url = f"http://localhost:8080/api/lights/change/{light_id}"

        try:
            change_response = requests.put(change_state_url, json={"lightstate": "ON"})

            if change_response.status_code == 200:
                dispatcher.utter_message(text=f"Light {light_id} has been turned on 💡.")
            elif change_response.status_code == 208:
                dispatcher.utter_message(text=f"Light {light_id} is already on 💡.")
            else:
                dispatcher.utter_message(text="Failed to turn on the light 💡.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(text="Error: Unable to connect \nto the light control API.")
        except Exception as e:
            dispatcher.utter_message(text=f"An unexpected error occurred: {str(e)}")

        return [AllSlotsReset()]



class ActionTurnOffLight(Action):

    def name(self) -> str:
        return "action_turn_off_light"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        light_id = tracker.get_slot("light_id")

        if light_id is None:
            dispatcher.utter_message(text="Please specify a valid light ID.")
            return [AllSlotsReset()]

        change_state_url = f"http://localhost:8080/api/lights/change/{light_id}"

        try:
            change_response = requests.put(change_state_url, json={"lightstate": "OFF"})

            if change_response.status_code == 200:
                dispatcher.utter_message(text=f"Light {light_id} has been turned off 💡.")
            elif change_response.status_code == 208:
                dispatcher.utter_message(text=f"Light {light_id} is already off 💡.")
            else:
                dispatcher.utter_message(text="Failed to turn off the light 💡.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(text="Error: Unable to connect \nto the light control API.")
        except Exception as e:
            dispatcher.utter_message(text=f"An unexpected error occurred: {str(e)}")

        return [AllSlotsReset()]


# For Zone ON


class ActionZoneOnLight(Action):

    def name(self) -> str:
        return "action_zone_on_lights"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        zone_name = tracker.get_slot("zone_name")

        if zone_name is None:
            dispatcher.utter_message(text="Please specify a valid Zone Name.")
            return [AllSlotsReset()]
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
                            text=f"Please specify a valid Zone Name. \nHere are the available zones:\n{zones}"
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
                    text="Error: Unable to connect \nto the zone list API.")
            except Exception as e:
                dispatcher.utter_message(
                    text=f"An unexpected error occurred: {str(e)}")

            return [AllSlotsReset()]

        zone_name_parts = zone_name.split()
        if len(zone_name_parts) >= 2:
            zone_name_parts[1] = zone_name_parts[1].upper()

        updated_zone_name = ' '.join(zone_name_parts)
        print(updated_zone_name)
        change_state_url = f"http://localhost:8080/api/lights/update/state/{updated_zone_name}"

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
                text="Error: Unable to connect \nto the light control API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return [AllSlotsReset()]

# For Zone OFF


class ActionZoneOffLight(Action):

    def name(self) -> str:
        return "action_zone_off_lights"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        zone_name = tracker.get_slot("zone_name")

        print(zone_name)
        if zone_name is None:
            dispatcher.utter_message(text="Please specify a valid Zone Name.")
            return [AllSlotsReset()]
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
                            text=f"Please specify a valid Zone Name. \nHere are the available zones:\n{zone_string}"
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
                    text="Error: Unable to connect \nto the zone list API.")
            except Exception as e:
                dispatcher.utter_message(
                    text=f"An unexpected error occurred: {str(e)}")

            return [AllSlotsReset()]

        zone_name_parts = zone_name.split()
        if len(zone_name_parts) >= 2:
            zone_name_parts[1] = zone_name_parts[1].upper()

        updated_zone_name = ' '.join(zone_name_parts)
        print(updated_zone_name)
        change_state_url = f"http://localhost:8080/api/lights/update/state/{updated_zone_name}"

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
                text="Error: Unable to connect \nto the light control API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return [AllSlotsReset()]


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
            return [AllSlotsReset()]

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
            return [AllSlotsReset()]

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
                return [AllSlotsReset()]

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
                    return [AllSlotsReset()]

            end_time_millis = int(parsed_end_time.timestamp() * 1000)
            print(f"End time in milliseconds: {end_time_millis}")
        else:
            dispatcher.utter_message(text="Please provide an end time.")
            return [AllSlotsReset()]

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
                        return [AllSlotsReset()]
                elif isinstance(zoneId_response, int):
                    zoneId = zoneId_response
                else:
                    dispatcher.utter_message(
                        text="Error: Unexpected response format.")
                    return [AllSlotsReset()]

            else:
                dispatcher.utter_message(
                    text=f"Error: Received unexpected status code {status_response.status_code}.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the zone list API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")
            return [AllSlotsReset()]

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

        return [AllSlotsReset()]


class ActionZoneBrightness(Action):

    def name(self) -> str:
        return "action_brightness"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        zone_name = tracker.get_slot("zone_name")
        brightness_level = tracker.get_slot("brightness_level")

        if zone_name is None:
            dispatcher.utter_message(text="Please specify a Zone Name.")
            return [AllSlotsReset()]
        if brightness_level is None:
            dispatcher.utter_message(text="Please specify a Brightness level.")
            return [AllSlotsReset()]

        change_state_url = f"http://localhost:8080/api/lights/update-brightness/{zone_name}?brightnessLevel={brightness_level}"

        try:
            change_response = requests.put(change_state_url)

            if change_response.status_code == 200:
                dispatcher.utter_message(
                    text=f"The brightness for zone '{zone_name}' \nhas been updated to {brightness_level}.")
            else:
                dispatcher.utter_message(
                    text="Failed to update the brightness. Please try again later.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the light control API. Please check the connection.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return [AllSlotsReset()]


class ActionLightBrightness(Action):

    def name(self) -> str:
        return "action_brightness_light"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        zone_name = tracker.get_slot("zone_name")
        brightness_level = tracker.get_slot("brightness_level")
        light_id = tracker.get_slot("light_id")
        brightness_level = int(brightness_level)
        if brightness_level is None and light_id:
            dispatcher.utter_message(text="Please specify a Valid Details.")
        elif brightness_level is None and light_id is None:
            dispatcher.utter_message(
                text="Please specify a Brightness \nname and light id.")
            return [AllSlotsReset()]
        if brightness_level is None:
            dispatcher.utter_message(text="Please specify a Brightness level.")
            return [AllSlotsReset()]
        if light_id is None:
            dispatcher.utter_message(text="Please specify a Light Id.")
            return [AllSlotsReset()]
        if brightness_level < 0:
            dispatcher.utter_message(text="Specify a brightness between 0-100.")
            return [AllSlotsReset()]
        elif brightness_level > 100:
            dispatcher.utter_message(text="Specify a brightness between 0-100.")
            return [AllSlotsReset()]


        change_state_url = f"http://localhost:8080/api/lights/brightness/update/{light_id}?brightnessLevel={brightness_level}"

        try:
            change_response = requests.put(change_state_url)

            if change_response.status_code == 200:
                dispatcher.utter_message(
                    text=f"The brightness has been updated to {brightness_level} \n for the light Id {light_id}.")
            else:
                dispatcher.utter_message(
                    text="Failed to update the brightness. \nPlease try again later.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the light \ncontrol API. Please check the connection.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return [AllSlotsReset()]


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
                        text="Error: Zone data is not \nin the expected format."
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

        return [AllSlotsReset()]


class ActionListZoneLights(Action):

    def name(self) -> str:
        return "action_list_zone_light"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        zone_name = tracker.get_slot("zone_name")
        list_all_zones_url = f"http://localhost:8080/api/lights/zone/light/{zone_name}"
        if zone_name is None:
            dispatcher.utter_message(text="Please specify a Zone Name.")
            return [AllSlotsReset()]
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
                        text="Error: Zone data is not \nin the expected format."
                    )
            else:
                dispatcher.utter_message(
                    text="Failed to fetch the list of zones.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to \nconnect to the zone list API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return [AllSlotsReset()]


class ActionLightsStatus(Action):

    def name(self) -> str:
        return "action_check_light_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        light_id = tracker.get_slot("light_id")
        light_status_url = f"http://localhost:8080/api/lights/list/{light_id}"

        if light_id is None:
            dispatcher.utter_message(text="Please specify a Light Id.")
            return [AllSlotsReset()]

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
                    text=f"Failed to fetch the status for \nlight {light_id}. Please try again later."
                )

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to \nthe light status API."
            )
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}"
            )

        return [AllSlotsReset()]


class ActionZoneLightStatus(Action):

    def name(self) -> str:
        return "action_check_zone_status"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:
        zone_name = tracker.get_slot("zone_name")
        zone_light_state_url = f"http://localhost:8080/api/lights/lights-state/zone/{zone_name}"
        light_brightness_url = f"http://localhost:8080/api/lights/zone/lightslevel/{zone_name}"

        if not zone_name:
            dispatcher.utter_message(text="Please specify a zone name.")
            return [AllSlotsReset()]

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
                            text="Error: The data returned from the \nAPI is not in the expected list format."
                        )

                except Exception as e:
                    dispatcher.utter_message(
                        text=f"Error parsing data: {str(e)}"
                    )
            else:
                dispatcher.utter_message(
                    text=f"Failed to fetch data for zone \n'{zone_name}'. Please try again later."
                )

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect to the \nzone light state or brightness API."
            )
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}"
            )

        return [AllSlotsReset()]


class ValidateScheduleLightForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_schedule_light_form"

    async def validate_light_state(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Validate the light state to ensure it's either 'on' or 'off'."""

        light_state = slot_value.strip().lower()

        if light_state in ["on", "off", "ON", "OFF", "On", "oFF", "Off"]:
            return {"light_state": light_state}
        else:
            dispatcher.utter_message(
                text="Please specify a valid light state: 'on' or 'off'.")
            return {"light_state": None}

    async def validate_brightness_level(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Validate the brightness level to ensure it's between 0 and 100."""

        try:
            brightness = int(slot_value)
        except ValueError:
            dispatcher.utter_message(
                text="Please enter a valid brightness \nlevel as a number between 0 and 100.")
            return {"brightness_level": None}

        if 0 <= brightness <= 100:
            return {"brightness_level": brightness}
        else:
            dispatcher.utter_message(
                text="Brightness level must be \nbetween 0 and 100.")
            return {"brightness_level": None}

    async def validate_priority(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Validate the priority to ensure it's 'high', 'medium', or 'low'."""

        priority = slot_value.strip().lower()

        if priority in ["high", "medium", "low"]:
            return {"priority": priority}
        else:
            dispatcher.utter_message(
                text="Please enter a valid priority \nlevel: 'high', 'medium', or 'low'."
            )
            return {"priority": None}

    async def validate_end_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        """Validate end_time to ensure it follows a recognizable time format."""

        time_input = slot_value.strip().lower()
        valid_time = None

        for time_format in ["%I %p", "%H:%M", "%I:%M %p", "%H"]:
            try:
                valid_time = datetime.strptime(time_input, time_format).time()
                break
            except ValueError:
                continue

        if valid_time:
            return {"end_time": valid_time.strftime("%H:%M")}
        else:
            dispatcher.utter_message(
                text="Please enter a valid time in formats \nlike '6 am', '18:00', or '6:30 PM'."
            )
            return {"end_time": None}


class ActionConfirmSchedule(Action):
    def name(self) -> Text:
        return "action_confirm_schedule"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> list:
        confirmation = tracker.get_slot("confirmation")
        if confirmation and confirmation.lower() in ["yes", "confirm", "sure"]:
            # Retrieve the slot values
            zone_name = tracker.get_slot("zone_name")
            light_state = tracker.get_slot("light_state")
            brightness_level = tracker.get_slot("brightness_level")
            rule = tracker.get_slot("rule")
            end_time = tracker.get_slot("end_time")
            schedule_name = tracker.get_slot("schedule_name")
            priority = tracker.get_slot("priority")

            priority_valid = priority.strip().lower()

            if priority_valid == "high":
                priority = 1
            elif priority_valid == 'low':
                priority = 3
            elif priority_valid == 'medium':
                priority = 2

            light_state_valid = light_state.strip().lower()

            if light_state_valid == "on":
                light_state = "ON"
            elif light_state_valid == "off":
                light_state = "OFF"
            elif light_state_valid == "photocell":
                light_state = "PHOTOCELL"

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
                            return [AllSlotsReset()]
                    elif isinstance(zoneId_response, int):
                        zoneId = zoneId_response
                    else:
                        dispatcher.utter_message(
                            text="Error: Unexpected response format.")
                        return [AllSlotsReset()]

                else:
                    dispatcher.utter_message(
                        text=f"Error: Received unexpected status code \n{status_response.status_code}.")

            except requests.exceptions.ConnectionError:
                dispatcher.utter_message(
                    text="Error: Unable to connect to \nthe zone list API.")
            except Exception as e:
                dispatcher.utter_message(
                    text=f"An unexpected error occurred: {str(e)}")
                return [AllSlotsReset()]

            schedule_payload = {
                "priority": priority,
                "lightstate": light_state,
                "lightlevel": brightness_level,
                "starttime": extract_start_time_millis(rule),
                "endtime": brightness_level,
                "recurrenceRule": text_to_cron(rule),
                "startdate": extract_start_time_millis(rule),
                "enddate": extract_start_time_millis(end_time),
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
                    text="Error: Unable to connect to \nthe schedules control API.")
            except Exception as e:
                dispatcher.utter_message(
                    text=f"An unexpected error occurred 222:\n {str(e)}")
                dispatcher.utter_message(text="Schedule added successfully! ✅")
            return [AllSlotsReset()]

        else:
            dispatcher.utter_message(text="Schedule canceled. ❌")
            return [AllSlotsReset()]


class ActionCancelSchedule(Action):
    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]


class ActionListZoneSchedules(Action):

    def name(self) -> str:
        return "action_list_zone_schedule"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:

        zone_name = tracker.get_slot("zone_name")
        list_all_zones_url = f"http://localhost:8080/api/schedules/listbyzone/{zone_name}"
        print(zone_name)

        try:
            response = requests.get(list_all_zones_url)

            if response.status_code == 200:
                schedules = response.json()

                if isinstance(schedules, list):

                    if schedules:
                        for schedule in schedules:
                            schedule_name = schedule.get("schedulename", "N/A")
                            priority = schedule.get("priority", "N/A")
                            start_time = self.convert_millis_to_time(
                                schedule.get("starttime", 0))
                            end_time = self.convert_millis_to_time(
                                schedule.get("endtime", 0))
                            light_state = schedule.get("lightstate", "N/A")
                            light_level = schedule.get("lightlevel", "N/A")
                            recurrence_rule = schedule.get(
                                "recurrenceRule", "N/A")
                            zone_name = schedule.get(
                                "zone", {}).get("name", "N/A")

                            print(schedule_name)
                            print(priority)
                            print(start_time)
                            print(end_time)

                            schedule_message = (
                                f"📅 Schedule: {schedule_name}\n"
                                f"🕐 Start Time: {start_time}\n"
                                f"🕒 End Time: {end_time}\n"
                                f"💡 Light State: {light_state}\n"
                                f"🌟 Brightness Level: {light_level}%\n"
                                f"🔁 Recurrence: {recurrence_rule}\n"
                                f"🌍 Zone: {zone_name}\n"
                                f"🔢 Priority: {priority}"
                            )


                            dispatcher.utter_message(text=schedule_message)

                    else:
                        dispatcher.utter_message(
                            text="No schedules found for this zone.")

                else:
                    dispatcher.utter_message(
                        text="Error: Response format \nis not as expected.")
            else:
                dispatcher.utter_message(
                    text="Failed to fetch the \nlist of schedules.")

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect \nto the zone list API.")
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}")

        return []

    def convert_millis_to_time(self, millis: int) -> str:
        """Converts milliseconds to a human-readable time format."""
        if millis == 0:
            return "N/A"

        seconds = millis / 1000
        time_obj = datetime.utcfromtimestamp(seconds)

        return time_obj.strftime("%H:%M")


class ActionListZoneSchedules(Action):

    def name(self) -> str:
        return "action_delete_scheduleby_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[EventType]:

        schedule_name = tracker.get_slot("schedule_name") 
        schedule_name = schedule_name.strip().lower()
        print(schedule_name)

        delete_schedules_url = f"http://localhost:8080/api/schedules/remove/byname/{schedule_name}"

        try:
            response = requests.delete(delete_schedules_url)

            if response.status_code == 200:
                dispatcher.utter_message(text="Schedule deleted successfully.")
            else:
                dispatcher.utter_message(
                    text="schedule not found. \nPlease try again."
                )

        except requests.exceptions.ConnectionError:
            dispatcher.utter_message(
                text="Error: Unable to connect \nto the zone list API."
            )
        except Exception as e:
            dispatcher.utter_message(
                text=f"An unexpected error occurred: {str(e)}"
            )

        return [AllSlotsReset()]
