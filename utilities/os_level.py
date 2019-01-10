"""
# -------------------------------
common utils module
# -------------------------------
"""
import inspect
import subprocess
from utilities import logger


def run_shell(command,
              show_output=False,
              show_output_on_error=True,
              continue_on_error=False):
    """
    # -------------------------------
    :param command:
    :param show_output:
    :param show_output_on_error:
    :param continue_on_error:
    :return:
    # -------------------------------
    """

    # -------------------------------
    # Subprocess linux command executor
    # -------------------------------
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
    output, error = process.communicate()

    if process.returncode != 0 and not continue_on_error:
        trace = "Error in Shell Commands:\n" + output + "\n" + error
        logger.debug( trace)
        exit(-1)

    if process.returncode != 0 and show_output_on_error:
        trace = ":Error in Shell Commands:\n" + output + "\n" + error
        logger.debug( trace)

    if show_output:
        trace = output + "\n" + error
        logger.debug( trace)

    return process.returncode, output, error


def set_env_variables(env_object):
    """
    # -------------------------------
    :param env_object:
    :return:
    # -------------------------------
    """
    environment_dictonary = dict(
        (name,
         getattr(env_object, name)
         ) for name in dir(env_object) if not name.startswith('__'))
    trace = "Setting Deployment environment variables"
    logger.debug( trace)
    for env_key, env_value in environment_dictonary.iteritems():
        # os.environ[env_key] = env_value
        trace = "{KEY}={VALUE}".format(KEY=env_key, VALUE=env_value)
        logger.debug( trace)
        run_shell("export {KEY}='{VALUE}'".format(KEY=env_key, VALUE=env_value))
    return environment_dictonary
