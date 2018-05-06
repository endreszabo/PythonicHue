from general import GeneralHueObject, ObjectList
from metaobjects import *

class Schedule(GeneralHueObject):
    def attr_filter(self):
        self.rw_attributes=['name','description','command','localtime','status','autodelete']
        self.ro_attributes=[]
    def configure(self):
        if 'command' in self.kwargs:
            #self.kwargs['command']['XXX']=122
            self.kwargs['command']=self.action(self.kwargs['command'])

class Scene(GeneralHueObject):
    def attr_filter(self):
        self.rw_attributes=['name','lights','recycle', 'locked','appdata', 'picture', 'lightstates']
        self.ro_attributes=[]
        self.resolve_hue_id_fields=[
            ('lights','light', False),
            ('lightstates','light', False)
        ]
    def fill_rw(self, **kwargs):
        super(self.__class__, self).fill_rw(**kwargs)
        # known API quirk: get per scene lightstates attribute that was not received when asked for all the scenes
        self.kwargs['lightstates']=self.bridge.qhue.scenes[self.hue_id]()['lightstates']

class Rule(GeneralHueObject):
    def attr_filter(self):
        self.rw_attributes=['name','conditions','actions']
        self.ro_attributes=[]
    def fill_rw(self, **kwargs):
        super(self.__class__, self).fill_rw(**kwargs)
        # known API quirk: get per scene lightstates attribute that was not received when asked for all the scenes
        #self.kwargs['lightstates']=self.bridge.qhue.scenes[self.hue_id]()['lightstates']

def SensorFactory(bridge, sensordata, **kwargs):
    if kwargs['type']=='ZLLSwitch':
        return Dimmer(bridge, sensordata, **kwargs)
    return Sensor(bridge, sensordata, **kwargs)

class Sensor(GeneralHueObject):
    def attr_filter(self):
        self.rw_attributes=['name','config','recycle']
        self.ro_attributes=['type','modelid','manufacturername','uniqueid']

class Group(GeneralHueObject):
    def attr_filter(self):
        self.rw_attributes=['name','lights','groupclass',('type','hue_type'),('class','hue_class')]
        self.ro_attributes=[]
        self.resolve_hue_id_fields=[
            ('lights','light', False)
        ]
        #super.config(self, hue_id, json)
    def fill_rw(self, **kwargs):
        super(Group, self).fill_rw(**kwargs)
        lights=self.kwargs['lights']
        #"self.kwargs['lights']=ObjectList(self.kwargs['lights'])
    pass

class Light(GeneralHueObject):
    #def attr_filter(self):
    #    self.rw_attributes.append('serial')
    def to_python(self, objtype):
        return super(Light, self).to_python(objtype, suffix=["\t## 6-characters serial number printed on light (optional)","\tserial = None"])
    pass

class Tap(Sensor): #ZLLSwitch
    def attr_filter(self):
        self.Button1=Button()
        self.Button2=Button()
        self.Button3=Button()
        self.Button4=Button()
ZGPSwitch=Tap

class Dimmer(Sensor): #ZLLSwitch
    def attr_filter(self):
        self.buttonOn=DimmerButton()
        self.buttonDimUp=DimmerButton()
        self.buttonDimDown=DimmerButton()
        self.buttonOff=DimmerButton()
ZLLSwitch=Dimmer

class CLIPGenericStatus(Sensor): #Z
    pass

