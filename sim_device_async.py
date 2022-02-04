# Licensed under the MIT license.
# Created based on example provided here
# https://github.com/MicrosoftLearning/AZ-220-Microsoft-Azure-IoT-Developer.git

import os
import asyncio
import random
import datetime
import sys
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

# The device connection authenticates your device to your IoT hub.
# The connection string for a device should never be stored in code.
# For the sake of simplicity we're using an environment
# variable here. If you created the environment variable with the IDE running,
# stop and restart the IDE to pick up the environment variable.
# If no environment variable is created, program
# will prompt you to provide the connection string.
#
# You can use the Azure CLI to find the connection string:
#     az iot hub device-identity connection-string show
#                               --hub-name {YourIoTHubName}
#                               --device-id MyNodeDevice
#                               --output table

CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

if CONNECTION_STRING is None:
    CONNECTION_STRING = input("Please provide the connection string: ")


# This class represents a sensor
# real-world sensors would contain code to initialize
# the device or devices and maintain internal state
class EnvironmentSensor:
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


# This function creates the payload to be sent to IoT Hub
def create_payload(sensor):
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


# This function sends the telemetry to IoT Hub in the loop
# time interval is specified in telemetry_delay (in seconds)
async def send_device_to_coud_messages_async(client,
                                             number_of_messages,
                                             telemetry_delay):
    i = 0
    print("IoT Hub device sending periodic messages")

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


def main():
    number_of_messages = 0
    telemetry_delay = 1

    print("IoT Hub Quickstart #1 - Simulated device")
    number_of_messages_prompt = input("Please provide the number of messages "
                                      "to send (0 or Enter for unlimited): ")

    if number_of_messages_prompt.isdigit():
        number_of_messages = int(number_of_messages_prompt)
    elif len(number_of_messages_prompt) == 0:
        number_of_messages = 0
    else:
        print(f"{number_of_messages_prompt} is not a number")
        sys.exit(1)

    telemetry_delay_prompt = input("Please provide time interval for "
                                   "telemetry messages (default 2): ")

    if telemetry_delay_prompt.isdigit():
        telemetry_delay = int(telemetry_delay_prompt)
    elif len(telemetry_delay_prompt) == 0:
        telemetry_delay = 2
    else:
        print(f"{telemetry_delay_prompt} is not a number")
        sys.exit(1)

    device_client = IoTHubDeviceClient.create_from_connection_string(
                                                            CONNECTION_STRING)

    loop = asyncio.get_event_loop()

    try:
        # Run the sample in the event loop
        loop.run_until_complete(
                send_device_to_coud_messages_async(device_client,
                                                   number_of_messages,
                                                   telemetry_delay))
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped by user")
    finally:
        # Upon application exit, shut down the client
        print("Shutting down IoTHubClient")
        loop.run_until_complete(device_client.shutdown())
        loop.close()


if __name__ == '__main__':
    main()
