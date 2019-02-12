"""

"""


class CreateSingleton(type):
    singleton_instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.singleton_instances:
            cls.singleton_instances[cls] = super(CreateSingleton, cls).__call__(*args, **kwargs)
        return cls.singleton_instances[cls]

    def __del__(cls):
        # loop=asyncio.get_event_loop()
        # loop.create_task(cls.singleton_instances[cls].close())
        cls.singleton_instances[cls].close()

    @staticmethod
    def __clean_all__():
        for _instance in CreateSingleton.singleton_instances:
            _instance.__del__()
