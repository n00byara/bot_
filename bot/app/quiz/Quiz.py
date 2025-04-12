class Quiz:
    _state = False
    _id = 0

    @classmethod
    def id(cls):
        return cls._id

    @classmethod
    def state(cls):
        return cls._state
    
    @classmethod
    def start(cls, id):
        cls._state = True
        cls._id = id

    @classmethod
    def stop(cls):
        cls._state = False
        cls._id = 0

    @classmethod
    def state(cls):
        return cls._state