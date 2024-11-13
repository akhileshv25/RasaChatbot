import requests
import ast
from datetime import datetime, timedelta

api = "http://localhost:8080/api"

def change_light_state(light_id: str, state: str) -> str:
    """
    Function to change the state of a light.
    """
    change_state_url = f"{api}/lights/change/{light_id}"

    try:
        change_response = requests.put(change_state_url, json={"lightstate": state})

        message = change_response.content.decode('utf-8').strip()
        return f"{message} 💡"

    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to the light control API."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"



def change_zone_light_state(zone_name: str, state: str) -> str:
    """
    function to change the state of lights in a zone.
    """
    zone_name_parts = zone_name.split()
    if len(zone_name_parts) >= 2:
        zone_name_parts[1] = zone_name_parts[1].upper()

    updated_zone_name = ' '.join(zone_name_parts)

    change_state_url = f"{api}/lights/update/state/{updated_zone_name}"

    try:
        change_response = requests.put(change_state_url, json={"lightstate": state})
        message = change_response.content.decode('utf-8').strip()
        return f"{message}💡"

    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to the light control API."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def get_zone_list() -> str:
    """
    function to fetch all available zones from the API.
    """
    list_all_zones_url = f"{api}/zones/list"
    
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
                return f"Here are the available zones:\n{zone_table}"
            else:
                return "Error: Zone data is not in the expected format."
        else:
            return "Failed to fetch the list of zones."

    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to the zone list API."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def update_brightness(api_url: str, brightness_level: int, entity_name: str) -> str:
    """
     Function to update the 🔆brightness of a zone or light.
    """
    try:
        change_response = requests.put(api_url)

        if change_response.status_code == 200:
            return f"The 🔆brightness for {entity_name} \nhas been updated to {brightness_level}."
        else:
            return "Failed to update the 🔆brightness. \nPlease try again later."

    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to the light \ncontrol API. Please check the connection."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
    

def check_status_light(light_id : int) ->str:
    """
    Function for check light staus with light id
    """
    light_status_url = f"{api}/lights/list/{light_id}"

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
                        f"Zone: {light.get('zone', {}).get('name', 'N/A')}, \n"
                        f"{light.get('zone', {}).get('address', 'N/A')}"
                    )

                    return f"Here is the status for light {light_id}:\n{light_details}"
            
            else:
                return "Error: Unexpected response format from the API."
                
        else:
           
           return f"Failed to fetch the status for \nlight {light_id}. Please try again later."
            

    except requests.exceptions.ConnectionError:
           return "Error: Unable to connect to \nthe light status API."
            
    except Exception as e:
            return f"An unexpected error occurred: {str(e)}"
    

def check_zone_status(zone_name : str) -> str:
    zone_light_state_url = f"{api}/lights/lights-state/zone/{zone_name}"
    light_brightness_url = f"{api}/lights/zone/lightslevel/{zone_name}"
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

                    return response_text

                else:
                    return "Error: The data returned from the \nAPI is not in the expected list format."
                

            except Exception as e:
                return f"Error parsing data: {str(e)}"
                
        else:
            return f"Failed to fetch data for zone \n'{zone_name}'. Please try again later."
        

    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to the \nzone light state or brightness API."
        
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def get_zone_lights(zone_name: str) -> str:
    list_all_zones_url = f"{api}/lights/zone/light/{zone_name}"
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

                return f"Here are the available {zone_name}:\n{zone_table}"
                
            else:
                return "Error: Zone data is not \nin the expected format."
                
        else:
            return "Failed to fetch the list of zones."

    except requests.exceptions.ConnectionError:
        return"Error: Unable to \nconnect to the zone list API."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def delete_schedule(schedule_name : str) -> str:

    delete_schedules_url = f"{api}/schedules/remove/byname/{schedule_name}"

    try:
        response = requests.delete(delete_schedules_url)

        if response.status_code == 200:
            return "Schedule deleted successfully."
        else:
            return "schedule not found. \nPlease try again."
            

    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect \nto the zone list API."
    
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
        
def convert_millis_to_time(millis: int) -> str:
    """Converts milliseconds to a human-readable time format."""
    if millis == 0:
        return "N/A"

    seconds = millis / 1000
    time_obj = timedelta(seconds=seconds)
    
    hours, remainder = divmod(time_obj.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def list_zone_schedule(zone_name: str) -> str:
    list_all_zones_url = f"{api}/schedules/listbyzone/{zone_name}"
    print(zone_name)

    try:
        response = requests.get(list_all_zones_url)

        if response.status_code == 200:
            schedules = response.json()

            if isinstance(schedules, list):
                if schedules:
                    all_schedules = []  # Collect all schedule messages here
                    for schedule in schedules:
                        schedule_name = schedule.get("schedulename", "N/A")
                        priority = schedule.get("priority", "N/A")
                        start_time = convert_millis_to_time(schedule.get("starttime", 0))
                        end_time = convert_millis_to_time(schedule.get("endtime", 0))
                        light_state = schedule.get("lightstate", "N/A")
                        light_level = schedule.get("lightlevel", "N/A")
                        recurrence_rule = schedule.get("recurrenceRule", "N/A")
                        zone_name = schedule.get("zone", {}).get("name", "N/A")

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
                        all_schedules.append(schedule_message)

                    # Join all schedule messages into one response
                    return "\n\n".join(all_schedules)

                else:
                    return "No schedules found for this zone."

            else:
                return "Error: Response format is not as expected."
        else:
            return "Failed to fetch the list of schedules."

    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to the zone list API."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def change_light_state_using_zone_name(light_id : int , zone_name:str , light_state:str) -> str:

    url_change_light_state = f"http://localhost:8080/api/lights/toggle?zoneName={zone_name}&lightId={light_id}&newState={light_state}"
    try:
        change_response = requests.put(url_change_light_state)
        message = change_response.content.decode('utf-8').strip()
        return f"{message} 💡"
    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to the light control API."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

def update_brightness_light_using_zonename(light_id : int , zone_name:str , lightlevel:int) -> str:

    url_change_light_state = f"{api}/lights/update/brightness?zoneName={zone_name}&lightId={light_id}&brightnessLevel={lightlevel}"
    try:
        change_response = requests.put(url_change_light_state)
        message = change_response.content.decode('utf-8').strip()
        return f"{message} 💡"
    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to the light control API."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
