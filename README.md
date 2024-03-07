# Integrating MQTT client with Wazuh

This guide provides a comprehensive overview of integrating MQTT messaging with Wazuh, enabling automatic dissemination of alert contents via MQTT. This integration facilitates real-time alerting and response capabilities, enhancing the security monitoring framework.

## Overview

The setup process involves installing necessary dependencies, configuring Wazuh to trigger custom Python scripts, and ensuring that MQTT messages are correctly published and received by a subscriber.

## Setup Guide

### 1. Installing Dependencies

The integration requires the Paho MQTT library (version before 2.0.0). It must be installed under the `wazuh` user to ensure the integration script has the necessary permissions to execute properly. Use the following command:

```
/var/ossec/framework/python/bin/python3 -m pip install "paho-mqtt<2.0.0" 
```

### 2. Creating the Custom Python Script

A custom Python script is needed to publish alerts from Wazuh to an MQTT broker. A template script is available here:

```
mqtt-integration/custom-mqtt.py
```

This script listens for alerts predefined in the ossec.conf file and publishes them to an MQTT broker.

### 3. Configuring ossec.conf

Modify the ossec.conf file to specify which alerts should trigger the MQTT integration. This configuration should be placed after the block:
```
<!-- Osquery integration --> 
```
The following XML snippet enables the MQTT integration for alerts with rule ID 100002:

```
<integration>
  <name>custom-mqtt</name>
  <rule_id>100002</rule_id>
  <alert_format>json</alert_format>
</integration>
```

Adjust the rule ID as necessary to match the alerts you wish to forward.

### 4. Setting Up the Subscriber

To verify the operation of the integration and to observe the alerts, set up a subscriber script that listens for messages on the configured MQTT topics. A subscriber script can also be found in here; mqtt-integration/subscriberscript.py 
