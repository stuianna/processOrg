'''
Class ProccessOrg - Module for organising multiple external processes.
Created April 2019
Stuart Ianna
'''
import subprocess
import os
import signal
import logging

class ProcessOrg():

    def __init__(self):
        self.children = []

    '''
    Create a new process to be exectuded. Provies functionallity to handle error
    should the process not be found.
    Appends the process to the global children list

    Returns the process for later handing
    '''
    def create(self,process,name,blocking=False,printOutput=False):

        p = None

        try:
            if printOutput:
                p = subprocess.Popen(process)
            else:
                p = subprocess.Popen(process,stdout=subprocess.PIPE)

            self.children.append({"process":p,"name":name,"blocking":blocking,"printOutput":printOutput})
            if blocking:
                p.wait()
        except IOError as e:

            ## Handle error for non existent process name here
            logging.error('Starting process: "{}" with command: "{}". Error code: {}'.format(name,process,e))
            pass
        return p

    '''
    Kill a given process. If the process doesn't exist try to remove it from
    the child list.

    Returns output if killed or None if the process didn't exist
    '''
    def destroy(self,name):

        child = self.getChildFromName(name)
        output = None

        if child is None:
            logging.warning('Cannot kill process named {}, does not exist'.format(name))
            return None

        p = child['process']
        status = p.poll()

        if status is None:
            ## Process is still running, kill it
            p.terminate()
            p.wait()
            output = p.communicate()[0]
            self.children.remove(child)

        else:
            ## Process has already finished, but still exists on the list
            ## Remove it from the list

            ## Try to read some output, continue if already read.
            try:
                output = p.communicate()[0]
            except:
                pass
            self.children.remove(child)
            return output

        return output


    '''
    Determine if a process is still running, return true if still running
    '''
    def isRunning(self,name):

        child = self.getChildFromName(name)

        if child is None:

            logging.warning('Cannot get status, process named {} does not exist'.format(name))
            return False

        p = child["process"]
        status = p.poll()

        if status == None:
            return True

        return False

    '''
    Get the output of a completed process, returns none if the process is still running
    or the process doesn't exist
    '''
    def getOutput(self,name):

        child = self.getChildFromName(name)

        if child is None:

            logging.warning('Cannot get output, process named {} does not exist'.format(name))
            return None

        p = child["process"]
        status = p.poll()

        ## Check if the process is still running
        if status is None:

            ##Process is still running
            logging.warning('Cannot get output, process named {} is still running'.format(name))
            return None

        ## Get the output
        stdout = p.communicate()[0]
        return stdout.decode('utf-8')

    '''
    Get all the children spawned
    '''
    def getChildren(self):

        return [child['name'] for child in self.children]

    '''
    Kill all the children 
    '''
    def killAll(self):

        for child in self.children:
            os.kill(child['process'].pid,signal.SIGINT)

    '''
    Get the pid of a child using its name
    '''
    def getPid(self,name):

        child = self.getChildFromName(name)
        if child == None:

            logging.warning('Cannot get pid, process named {} does not exist'.format(name))
            return None

        return child['process'].pid

    '''
    Get the process object from the name of the process
    '''
    def getChildFromName(self,name):

        for child in self.children:
            if child["name"] == name:
                return child

        return None
