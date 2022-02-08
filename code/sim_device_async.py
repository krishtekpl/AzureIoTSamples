# Licensed under the MIT license.
# Created based on example provided here
# https://github.com/MicrosoftLearning/AZ-220-Microsoft-Azure-IoT-Developer.git

import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
import azure_iot_samples

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


def main():
    connection_str = CONNECTION_STRING

    if connection_str is None:
        connection_str = input("Please provide the connection string: ")

    print("IoT Hub Quickstart #1 - Simulated device")
    parameters = azure_iot_samples.initial_parameters()

    device_client = IoTHubDeviceClient.create_from_connection_string(
                                                            connection_str)

    loop = asyncio.get_event_loop()

    try:
        # Run the sample in the event loop
        loop.run_until_complete(
                azure_iot_samples.send_device_to_coud_messages_async(
                                            device_client,
                                            parameters['number_of_messages'],
                                            parameters['telemetry_delay']))
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped by user")
    finally:
        # Upon application exit, shut down the client
        print("Shutting down IoTHubClient")
        loop.run_until_complete(device_client.shutdown())
        loop.close()


if __name__ == '__main__':
    main()
