from collections import deque
import time
 
# Initialize the deque with a maximum length of 5
d = deque(maxlen=5)
 
# Start adding numbers to the deque
for i in range(1, 11):  # Let's add numbers from 1 to 10 as an example
    d.append(i)  # Add a new number to the deque
    print("Current deque:", list(d))  # Print the current state of the deque
    time.sleep(1)  # Wait for 1 second before adding the next number