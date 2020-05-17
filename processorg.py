"""
ProccessOrg: Single class module for organising multiple external processes.
"""
import subprocess
import os
import signal
import logging

log = logging.getLogger(__name__)


class ProcessOrg():
    """Class for organising multiple subprocesses.

    The logging module is used to log errors and warnings.

    Typical Usage:
    >>>    children = ProcessOrg()

    # Create a new non-blocking process 'list' to list all files in a directory
    >>> children.create(['ls'], 'list')

    # Get the output of the process
    >>> children.get_output('list')
    'your_directory_contents''

    # Kill the process (remove it from spawed process list)
    >>> children.destroy('list')

    Attributes:
    children:list
        A list of dictionaries corresponing to all spawned processes.
        - Keys:
            - process:subprocess - The subprocess object relating to the process.
            - name:str - The name given to  the process.
            - blocking:Boolean - Set true if the process is blocking (not run in background)
            - printOutput:Boolen - Set true if output is printed directly to stdout. If
                false, output is stored and can be retreived with method get_output.
    """
    def __init__(self):
        self.children = []

    def create(self, process, name, blocking=False, print_output=False):
        """Create a new process to be exectuded.

        A new process, when created is executed immedietaly.

        Example:,
        Create a new process which blockes main thread execution and
        printes all directory contents to stdout.

        create([ls,-l], list, True, True)

        Each time a new process is created it is added to the children list.
        The process can be killed and removed from this list using the destroy
        method.

        A logging.error is generated if the process called doesn't exist.

        Parameters:
            - process:list - A list containing the process name and arguments.
            - name:str - The name given to the process. This name is used
                to access the process at a later time.
            - blocking:Boolean - If set to true, main thread excecution will
                halt until the process has finished. If set false, the
                process runs in the background.
            - print_output:Boolean - If true, process output is printed
                to stdout. If false the process output is stored and can
                be retreived once the process has finished. Use 'get_output'
                to retreive.

        Returns:
            - p:subproccess.Popen - Object of created subprocess.
        """
        p = None

        try:
            # Output is printed to the connected stdout.
            if print_output:
                p = subprocess.Popen(process)
            # Need to setup a stdout pipe if output is not being immedietly displayed.
            else:
                p = subprocess.Popen(process, stdout=subprocess.PIPE)

            # Add the process to the list so it can be queried or destroyed by name at a later time.
            self.children.append({"process": p, "name": name, "blocking": blocking, "print_output": print_output})
            if blocking:
                p.wait()
        except IOError as e:
            # Handle error for non existent process name here
            log.error('Starting process: "{}" with command: "{}". Exception: {}'.format(name, process, e))
            return None
        return p

    def destroy(self, name):
        """
        Kill a given process. If the process doesn't exist try to remove it from the child list.

        Generates a logging.warning if the process doesn't exist.

        Parameters:
            - name:str - The name of the process to destroy

        Returns:
            - If the process existed, the output of the process is returned. (If
                print_output = False when the process was created). If the process
                didn't exist, then None is returned.
        """
        child = self.get_child_from_name(name)
        output = None

        if child is None:
            log.warning('Cannot kill process named {}, does not exist'.format(name))
            return None

        p = child['process']
        status = p.poll()

        if status is None:
            # Process is still running, kill it
            p.terminate()
            p.wait()
            output = p.communicate()[0]
            self.children.remove(child)
        else:
            # Process has already finished, but still exists on the list, remove it.

            # Try to read some output, continue if already read.
            try:
                output = p.communicate()[0]
            except Exception as e:
                log.debug("Trying to read output of a process which has none. Exception {}".format(e))
                return None
            self.children.remove(child)
        return output.decode('utf-8')

    def is_running(self, name):
        """
        Determine if a process is still running.

        Parameters:
            - name:str - The name of the process to query.

        Returns:
            - True if the process is running.
        """
        child = self.get_child_from_name(name)

        if child is None:
            log.warning('Cannot get status, process named {} does not exist'.format(name))
            return False

        p = child["process"]
        status = p.poll()

        if status is None:
            return True
        return False

    def get_output(self, name):
        '''
        Get the output of a completed process.

        Generates logging.warning if the process doesn't exist or the
        process is still running..

        Parameters:
            - name:str - The name of the process to query.

        Return:
            - The output of the process which was sent to stdout while
                the process was running. Returns None if the process
                doesn't exist or the porcess is still running.
        '''

        child = self.get_child_from_name(name)

        if child is None:

            log.warning('Cannot get output, process named {} does not exist'.format(name))
            return None

        p = child["process"]
        status = p.poll()

        # Check if the process is still running
        if status is None:
            # Process is still running
            log.warning('Cannot get output, process named {} is still running'.format(name))
            return None

        # Get the output
        stdout = p.communicate()[0]
        return stdout.decode('utf-8')

    def get_children(self):
        '''
        Get a list of names for all spawned processses.

        Returns:
            - A list of the names of all generated processes
        '''
        return [child['name'] for child in self.children]

    def kill_all(self):
        """
        Kill all processes created and remove them from the
        process list.

        Returns
            - None
        """
        for child in self.children:
            os.kill(child['process'].pid, signal.SIGINT)

    def get_pid(self, name):
        """
        Get the PID of a process from its name.

        Generates a logging.warning if the process doesn't exist.

        Parameters:
            - name:str - The name of the process to get PID from.

        Return:
            - The PID of the process.
        """
        child = self.get_child_from_name(name)
        if child is None:
            log.warning('Cannot get pid, process named {} does not exist'.format(name))
            return None
        return child['process'].pid

    def get_child_from_name(self, name):
        """
        Get the process submodule object from the name of the process.

        Parameters:
            name:str - The name of the process to query.

        Returns:
            p:subprocess.popen - Object corresponding to process name.
            Returns None if the process doesn't exist.
        """
        for child in self.children:
            if child["name"] == name:
                return child
        return None
