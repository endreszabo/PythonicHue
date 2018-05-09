## Meta objects
## These objects are not valid hue data types, but kind of helpers for defining valid hue object properties
now=0

class AbstractHelper:
    pass

class Action(AbstractHelper):
    pass

class Condition(AbstractHelper):
    def __init__(self, condition):
        self.condition=condition
    def __str__(self):
        return self.condition
    pass

class Conditions(AbstractHelper):
    def __init__(self, conditions=[]):
        self.conditions=dict()
        for condition in conditions:
            self.conditions[condition['address']]=condition
    pass

class ButtonState(object):
    def __init__(self, ago=0):
        self.ago=ago
    def __str__(self):
        return("%s(%s)" % (self.__class__.__name__, self.ago))
    pass

class Button:
    class pressed(ButtonState):
        pass
TapButton=Button

class DimmerButton(Button):
    class depressed(ButtonState):
        pass
    class longPressed(ButtonState):
        pass
    class longDepressed(ButtonState):
        pass

if __name__ == "__main__":
    conditions=Conditions(
    [
  {
    "address": "/sensors/2/state/buttonevent",
    "operator": "eq",
    "value": "1000"
  },
  {
    "address": "/sensors/2/state/lastupdated",
    "operator": "dx"
  },
  ])
    button=DimmerButton()
    print(Condition(str(button.pressed(now))))

