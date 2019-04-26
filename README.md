# ProcessOrg

Python class helper for handling multiple external subprocesses.

Example: Create two process, one infinite and one terminating. Get the output of both.

```
from ProcessOrg import ProcessOrg

# Class object
children = ProcessOrg()

# Create a process name 'list' which runs the command 'ls'
child = children.create(['ls'],'list')

# Create a process name 'pinger' which pings a website (Infinite command)
child = children.create(['ping','www.google.com'],'pinger')

# Get the list process output
list_output = children.getOutput('list')

# Kill pinger and get its output
ping_output = children.kill('pinger')

# Kill all processes
children.killAll()


```

See `example.py` for more detailed example.

