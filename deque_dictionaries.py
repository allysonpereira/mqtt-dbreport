from collections import deque
import time
import random
 
# Initialize an empty dictionary to hold the deques
deques_dict = {}
 
# List of possible keys
keys = ["pod1", "pod2", "pod3", "pod4"]
 
# Start the infinite loop
while True:
    # Choose a key at random
    chosen_key = random.choice(keys)
 
    # If the deque for the chosen key doesn't exist, initialize it
    if chosen_key not in deques_dict:
        deques_dict[chosen_key] = deque(maxlen=5)
 
    # Append a random number to the deque associated with the chosen key
    deques_dict[chosen_key].append(random.randint(1, 100))  # Append a random number for variety
 
    # Print the current state of the dictionary
    for key, d in deques_dict.items():
        print(f"{key}: {list(d)}")
 
    # Wait for 1 second before the next iteration
    time.sleep(1)