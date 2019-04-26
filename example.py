'''
Example usage for Class ProcessOrg.py
Created April 2019
Stuart Ianna
'''

import time
import sys
import signal
from ProcessOrg import ProcessOrg

children = ProcessOrg()

'''
kill_handler gets called when the main program receives a SIGINT signal. This is
the signal which corresponds with ctrl+c being pressed.
'''
def kill_handler(sig,frame):

    # Kill all the processes spawned 
    children.killAll()

    ## Other things can be done here before the program is shutdown

    ## Kill the program
    sys.exit()

if __name__ == '__main__':

    '''
    Assign a function callback to the SIGINT (ctrl+c) command
    This way, all running processes can be killed before termination
    '''
    signal.signal(signal.SIGINT,kill_handler)
    
    '''
    Create a subproccess to be executed
        Arg1 - The command to be exectuted
        Arg2 - The name to be given to the process
        Arg3 - Make the process blocking? (optional, default = False)
        Arg4 - Print process output to stdout (optional, default = False)

    Returns the process object created or None if command passed doesn't exist.
    '''
    list_child = children.create(['ls'],'list',False,False)

    #Create another process, this one doesn't terminate automatically
    ping_child = children.create(['ping','www.google.com'],'ping')

    '''
    Get a list of all processes created, by name.
    Note processes which have finished remain on list until killed
    '''
    allProcesses = children.getChildren()
    print('Created processes:',allProcesses)

    '''
    Get the pid of a single process by name
    '''
    processPid = children.getPid('list')
    print('PID:',processPid)

    #Sleep here so the process has some time to finish
    time.sleep(3)

    '''
    Get the output of a completed process by name
    '''
    processOutput = children.getOutput('list')
    print('List output:',processOutput)

    '''
    Kill a given process
    This will also remove a completed process from the process list.
    '''
    children.destroy('list')
    allProcesses = children.getChildren()
    print('Created processes:',allProcesses)

    '''
    Check if a process is still running
    ''' 

    ping_running = children.isRunning('ping')
    print('Ping running?:',ping_running)

    '''
    Kill an infinite process and get its output
    '''
    output = children.destroy('ping')
    print(output)

    ping_running = children.isRunning('ping')
    print('Ping running?:',ping_running)

    '''
    Kill all the processes spawned by the module
    '''
    children.killAll()
