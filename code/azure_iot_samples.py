import sys
import random
import datetime
import asyncio
from azure.iot.device import Message


class EnvironmentSensor:
    """This class represents a sensor
       real-world sensors would contain code to initialize
       the device or devices and maintain internal state
    """
    def __init__(self):
        self.min_temperature = 20
        self.min_humidity = 60
        self.min_pressure = 1013.25
        self.min_latitude = 52.2241328
        self.min_longitude = 20.9884835
        self.random = random.random()

    def read_temperature(self):
        return self.min_temperature + self.random * 15

    def read_humidity(self):
        return self.min_humidity + self.random * 20

    def read_pressure(self):
        return self.min_pressure + self.random * 12

    def read_location(self):
        coordinates = {}    # empty dictionary
        coordinates['latitude'] = self.min_latitude + self.random * 0.5
        coordinates['longitude'] = self.min_longitude + self.random * 0.5
        return coordinates


def create_payload(sensor):
    """This function creates the payload to be sent to IoT Hub

    Args:
        sensor (EnvironmentSensor): Virtual IoT sensor

    Returns:
        Message: Formatted payload
    """
    msg_txt = '''{{"temperature":{temperature},"humidity":{humidity},''' \
              '''"pressure":{pressure},''' \
              '''"location":{{"latitude":{latitude},''' \
              '''"longitude":{longitude}}}}}'''
    msg_txt_formatted = msg_txt.format(
                            temperature=sensor.read_temperature(),
                            humidity=sensor.read_humidity(),
                            pressure=sensor.read_pressure(),
                            latitude=sensor.read_location()['latitude'],
                            longitude=sensor.read_location()['longitude'])
    message = Message(msg_txt_formatted)

    return message


async def send_device_to_coud_messages_async(client,
                                             number_of_messages,
                                             telemetry_delay):
    """This function sends the telemetry to IoT Hub in the loop
       time interval is specified in telemetry_delay

    Args:
        client (IoTHubDeviceClient): A device client that connects
                                     to an Azure IoT Hub instance
        number_of_messages (int): number of messages to be sent (0=unlimited)
        telemetry_delay (int): time interval between messages
    """
    i = 0
    print("IoT Hub device sending periodic messages")

    if not client.connected:
        await client.connect()

    while i < number_of_messages or number_of_messages == 0:
        sensor = EnvironmentSensor()
        payload = create_payload(sensor)

        payload.content_type = "application/json"
        payload.content_encoding = "utf-8"

        # Add a custom application property to the message.
        # An IoT hub can filter on these properties without access to
        # the message body.
        if sensor.read_temperature() > 30:
            payload.custom_properties["temperatureAlert"] = "true"
        else:
            payload.custom_properties["temperatureAlert"] = "false"

        # Send the message.
        now = format(datetime.datetime.now())
        await client.send_message(payload)
        print(f"{now} Sending message: {payload}")
        await asyncio.sleep(telemetry_delay)
        i += 1


def initial_parameters():
    """This function prompt user about number of messages to be send
       and telemetry delay

    Returns:
        dict: Number of messages to be sent and time interval between them
    """
    parameters = {}
    parameters['number_of_messages'] = 0
    parameters['telemetry_delay'] = 1

    number_of_messages_prompt = input("Please provide the number of messages "
                                      "to send (0 or Enter for unlimited): ")

    if number_of_messages_prompt.isdigit():
        parameters['number_of_messages'] = int(number_of_messages_prompt)
    elif len(number_of_messages_prompt) == 0:
        parameters['number_of_messages'] = 0
    else:
        print(f"{number_of_messages_prompt} is not a number")
        sys.exit(1)

    telemetry_delay_prompt = input("Please provide time interval for "
                                   "telemetry messages (default 2): ")

    if telemetry_delay_prompt.isdigit():
        parameters['telemetry_delay'] = int(telemetry_delay_prompt)
    elif len(telemetry_delay_prompt) == 0:
        parameters['telemetry_delay'] = 2
    else:
        print(f"{telemetry_delay_prompt} is not a number")
        sys.exit(1)

    return parameters
