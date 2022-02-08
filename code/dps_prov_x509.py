# Licensed under the MIT license.
# Created based on example provided here
# https://github.com/MicrosoftLearning/AZ-220-Microsoft-Azure-IoT-Developer.git

import os
import asyncio
from azure.iot.device import X509
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient
import azure_iot_samples

# Azure IoTHub hostname
HOSTNAME = "global.azure-devices-provisioning.net"

# Azure Device Provisioning Service (DPS) ID Scope
DPS_ID_SCOPE = os.getenv("DPS_SCOPE_ID")

# Certificate (cert.pem) File Name
CERT_FILENAME = os.getenv("X509_CERT_FILE")

# Key (key.pem) File Name
KEY_FILENAME = os.getenv("X509_KEY_FILE")

# Certificate pass phrase
PASS_PHRASE = os.getenv("X509_PASS_PHRASE")


async def register_device(provisioning_device):
    registration_effect = await provisioning_device.register()
    return registration_effect


def main():
    loop = asyncio.get_event_loop()

    # Device ID
    device_id = "sensor-thl-2005"

    x509 = X509(CERT_FILENAME, KEY_FILENAME, PASS_PHRASE)

    provisioning_device_client = ProvisioningDeviceClient \
        .create_from_x509_certificate(
            provisioning_host=HOSTNAME,
            registration_id=device_id,
            id_scope=DPS_ID_SCOPE,
            x509=x509,
        )

    registration_result = asyncio.run(register_device(
                                        provisioning_device_client))

    if registration_result.status == "assigned":
        IoTHubID = registration_result.registration_state.assigned_hub
        deviceID = registration_result.registration_state.device_id

        device_client = IoTHubDeviceClient.create_from_x509_certificate(
            x509=x509,
            hostname=IoTHubID,
            device_id=deviceID,
        )

        print(f'Device ID: {deviceID}')
        print(f'IoT Hub: {IoTHubID}')

        parameters = azure_iot_samples.initial_parameters()

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


if __name__ == "__main__":
    main()
