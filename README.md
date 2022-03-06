# Python client for Scratch Cloud Variables

### Install
```sh
pip install scratchcloudclient
```

### Scratch CloudUtils library

scratchcloudclient.CloudUtils provides functions to decode and encode strings
into 2-digit decimal encoding, which can be used to transfer text in cloud
variables. 

This project includes all the CloudUtils functions
[Scratch CloudUtils library](https://scratch.mit.edu/projects/655013932/)

### Example
```py
from scratchcloudclient import ScratchSession

session = ScratchSession('username', 'password')
# session = ScratchSession('username') # Prompts for password
connection = session.create_cloud_connection('654864684') # project id
print(connection.variables) # Dictionary of cloud variables


# Event function, gets called when cloud variables change
# (Note: Setting cloud variables to the same value will trigger the event
#        though this is not possible to detect in Scratch Project         )
def on_cloud_update(connection):
	print(connection.variables)

# Launches a thread which will run in background
connection.on_cloud_update(on_cloud_update)

# Set CLOUD_1 to 0
connection.set_variable('CLOUD_1', '0')
```

For more examples see [/examples](./examples/)

Some of the code is taken from [scratchclient](https://github.com/cubeythecube/scratchclient)