# AzureIoTSamples
This project help me to be with preparartion to AZ-220 exam.
You can also use all it if you wish ;)

I will continiusly add next features. Let's get started ;)

## Prerequisites
To have it working the following requirements should be met:
1. Installed Azure Iot SDK for Python (https://github.com/Azure/azure-iot-sdk-python)
2. Active Acure subscription [Azure Portal](https://portal.azure.com)

## Azure IoT resources
When you have alredy active the Azure subcriprion, you need to create at least below Azure IoT resources [in square brackets I will give the numbers of programs that will require the given object]:

1. IoTHub ```[1]```
2. IoTDevice ```[1]```

> **TIP**: If you are not yet familiar with Azure IoT I would recommend to the exercises from [Microsoft Learning GitHub](https://github.com/MicrosoftLearning/AZ-220-Microsoft-Azure-IoT-Developer)

## 1. Sending message to IoT hub asynchronously (sim_device_async.py)
This program sends messages with the following payload uctire to the IoTHub:
```cmd/sh
"payload": {
            "temperature": 28.03118331388056,
            "humidity": 70.70824441850742,
            "pressure": 1019.6749466511045,
            "location": {
                "latitude": 52.49183891046268,
                "longitude": 21.256189610462688
            }
```

The connection string to the IoT device is required. You can find it in Azure portal or you can use below PowerShell command:

```cmd/sh
az iot hub device-identity connection-string show --hub-name {IoTHubName} --device-id {IoTDeviceName} --output table
```

For security reasons it is not recommended to write the connection string directly to the program file. You can export it to the environment variable using following command"
```cmd/sh
export IOTHUB_DEVICE_CONNECTION_STRING={YourConnectiionString}
```

If you don't do it, you will be prompted by the program to provide it.
Additionally the program will prompt you to provide number of messages to send and time interval between messages. If you provide number of messages as 0 or blank, the program will send it continiusly until press Ctrl+C. The default message interval is 1s.

To see if messages are flowing to the IoTHub successfully, you can use below PowerShell command:
```cmd/sh
az iot hub monitor-events --hub-name {IoTHubName} --device-id {IoTDeviceName}
```
> **NOTE**: If you have configured message routing to send all messages to the endpoint, the above command will not show any messages. 