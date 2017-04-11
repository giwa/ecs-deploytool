import sys
from subprocess import Popen, PIPE


class Command:
    """
    Command wraps the system call
    """

    @staticmethod
    def run(command):
        """
        Run command in shell
        """
        process = Popen(command,
                        stdout=sys.stdout,
                        stderr=sys.stderr,
                        shell=True)
        process.communicate()
