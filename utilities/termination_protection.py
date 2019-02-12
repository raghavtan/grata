import inspect
import signal
import sys


class TerminateProtected:
    """
    # -------------------------------
    Protect a piece of code from being killed by SIGINT or SIGTERM.
    It can still be killed by a force kill.

    Example:
        with TerminateProtected():
            run_func_1()
            run_func_2()

    Both functions will be executed even if a sigterm or sigkill has been received.
    # -------------------------------
    """
    killed = False

    def _handler(self, signum, frame):
        trace = "Received SIGINT or SIGTERM! Finishing this block, then exiting."
        print(inspect.stack()[0][3], trace)

        self.killed = True

    def __enter__(self):
        self.old_sigint = signal.signal(signal.SIGINT, self._handler)
        self.old_sigterm = signal.signal(signal.SIGTERM, self._handler)

    def __exit__(self, type, value, traceback):
        if self.killed:
            sys.exit(0)
        signal.signal(signal.SIGINT, self.old_sigint)
        signal.signal(signal.SIGTERM, self.old_sigterm)
