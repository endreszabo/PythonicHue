## Meta objects
## These objects are not valid hue data types, but kind of helpers for defining valid hue object properties

class AbstractHelper:
    pass

class Action(AbstractHelper):
    pass

class Condition(AbstractHelper):
    pass

class ButtonState(object):
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

