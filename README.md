Python class helper for handling multiple external subprocesses.

```shell
pip install --user git+https://github.com/stuianna/processOrg --upgrade
```

Example: Create two process, one infinite and one terminating. Get the output of both.
```python
from processorg import ProcessOrg

children = ProcessOrg()

# Create a blocking process named 'list' which runs the command 'ls'
>>> children.create(['ls'], 'list')

# Create a background process named 'pinger' which pings a website.
>>> children.create(['ping', 'www.google.com'], 'pinger')

# Get the list process output
>>> list_output = children.get_output('list')

# Get the pid of pinger
>>> pid = children.get_pid('pinger')

# Check if pinger is still running
>>> children.is_running('pinger')
True

# Kill pinger and get its output
>>> ping_output = children.kill('pinger')

# Kill all processes
>>> children.kill_all()
```

It is useful to add a handler to handle shutdown events and make sure all processes are killed.
```python
import signal

children = ProcessOrg()

def kill_handler(sig, frame):
    children.kill_all()
    sys.exit()

signal.signal(signal.SIGINT, kill_handler)

# Create processes and do other things
```

See `help(ProcessOrg)` for more detailed information.

