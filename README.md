# MQTT broker deployment implementing EOD database reports

## These are practice scripts for a MQTT broker setting that is to be deployed into kubernetes and have additional features added to it.

### Current version
- The previous version of these scrips were dealing with multiple pods subscribing to the same topic.
- The idea now is to update the scripts in order to make all the existing pods subscribe into a different and unique topic. 
- One topic is assigned to each pod.
- The scripts add the message received from the pod into the database.
- A new consumer script must be created where a dictionary is created with the key being the topic and the value will be a deque (this requires the implementation of 2 python features 
from the python collection (deque , queue, and dictionaries).

### What is the final goal of this project?

- The first step here is to have both consumer and producer scripts working and sendind messages to the database (MySQL Workbench) where each pod is assigned to a unique topic which is already
implemented at this point.
- Next, the MQTT scripts would be used to implement data structures to store an amount of data (last 10 or 100 days).
- The end goal would be to have a daily EOD automated report from a database generating hyteresis based on the set thresholds.


