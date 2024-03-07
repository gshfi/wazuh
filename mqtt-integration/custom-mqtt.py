#!/var/ossec/framework/python/bin/python3
import json
import paho.mqtt.client as paho
import sys
import time

# Updated MQTT Broker Settings
broker = "brokerIP"
port = 1883
base_topic = "AnyTopicHere"
username = "MqttPublisherUsername"
password = "PublisherPassword"

# Function to generate a detailed message from an alert
def generate_msg(alert):
    Alert = alert['rule']['description']
    try: agentlabel = alert['agent']['labels']['labelname1']
    except KeyError: agentlabel = 'N/A'
    try: agentlabel2 = alert['agent']['labels']['labelname2']
    except KeyError: agentlabel2 = 'N/A'
    level = alert['rule']['level']
    agentname = alert['agent']['name']
    t = time.strptime(alert['timestamp'].split('.')[0], '%Y-%m-%dT%H:%M:%S')
    timestamp = time.strftime('%c', t)
    ID = alert['rule']['id']
    try: dstuser = alert['data']['win']['eventdata']['targetUserName']
    except KeyError: dstuser = 'N/A'
    try: filepath = alert['data']['win']['eventdata']['fullFilePath']
    except KeyError: filepath = 'N/A'
    try: usersid = alert['data']['win']['eventdata']['targetUser']
    except KeyError: usersid = 'N/A'
    try: user = alert['data']['win']['eventdata']['user']
    except KeyError: user = 'N/A'
    try: description = alert['data']['win']['eventdata']['description']
    except KeyError: description = 'N/A'
    try: commandline = alert['data']['win']['eventdata']['commandLine']
    except KeyError: commandline = 'N/A'
    try: fullfilepath = alert['data']['win']['ruleAndFileData']['fullFilePath']
    except KeyError: fullfilepath = 'N/A'
    try: winmessage = alert['data']['win']['system']['message']
    except KeyError: winmessage = 'N/A'

    message_elements = [
        f"Datum = {timestamp}",
        f"Alert = {Alert}",
        f"Server = {agentname}",
        f"Severity = {level}",
        f"RuleID = {ID}"
    ]

    if agentlabel != 'N/A': message_elements.append(f"Agentlabel = {agentlabel}")
    if agentlabel2 != 'N/A': message_elements.append(f"Agentlabel = {agentlabel2}")
    if dstuser != 'N/A': message_elements.append(f"Gebruiker = {dstuser}")
    if filepath != 'N/A': message_elements.append(f"Filepath = {filepath}")
    if usersid != 'N/A': message_elements.append(f"Usersid = {usersid}")
    if user != 'N/A': message_elements.append(f"Eventuser = {user}")
    if description != 'N/A': message_elements.append(f"Description = {description}")
    if commandline != 'N/A': message_elements.append(f"Commandline = {commandline}")
    if fullfilepath != 'N/A': message_elements.append(f"FullFilePath = {fullfilepath}")
    if winmessage != 'N/A': message_elements.append(f"WinMessage = {winmessage}")

    # Construct the full message
    message = '\n'.join(message_elements)

    return message

    # Callback function for publish event
def on_publish(client, userdata, result):
    print("Data published\n")

# Create MQTT client and setup
client = paho.Client("control1")
client.username_pw_set(username, password)
client.on_publish = on_publish

try:
    client.connect(broker, port)
    print(f"Connected to MQTT broker at {broker}:{port}")
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")
    sys.exit(1)

def publish_alert_message(alert_file_path):
    with open(alert_file_path, 'r') as alert_file:
        alert = json.load(alert_file)

    msg = generate_msg(alert)
    
    # Determine the topic based on the agent's label
    topic_suffix = ""
    if "labelname1" in alert.get('agent', {}).get('labels', {}):
        topic_suffix = "labelname1"
    elif "labelname2" in alert.get('agent', {}).get('labels', {}):
        topic_suffix = "labelname2"
    
    # Construct the full topic if a suffix was found
    if topic_suffix:
        full_topic = f"{base_topic}/{topic_suffix}"
    else:
        full_topic = base_topic + "/test"  # Fallback topic

    ret = client.publish(full_topic, msg)
    print(f"Published to {full_topic} with return: {ret}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python custom-mqtt.py <alert_file_path>")
        sys.exit(1)

    alert_file_path = sys.argv[1]
    publish_alert_message(alert_file_path)
