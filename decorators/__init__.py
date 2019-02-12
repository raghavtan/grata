"""

"""
import time

# This logs the name of the method whose execution time exceeds the given threshold.
TIME_THRESHOLD = 0.001

# This will store average measurements for each method name.
# { method_name: [ call_count, average_time ] }
measurements = {}


def time_cast(method):
    """

    :param method:
    :return:
    """

    async def wrapper(*args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        method_name = f"{method.__module__}.{method.__name__}()"

        # Get the measurements.
        time_start = time.time()
        result = await method(*args, **kwargs)
        time_taken = time.time() - time_start

        # Log the warning if the execution took a lot of time.
        if time_taken >= TIME_THRESHOLD:
            print(f"{method_name} took {time_taken}s to execute")

        # Update the measurements.
        count, average = measurements.get(method_name, [0, 0])
        average = (average * count + time_taken) / (count + 1)
        count += 1
        measurements[method_name] = [count, average]

        return result

    return wrapper


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed
