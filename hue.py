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

#Sensors
def SensorFactory(bridge, sensordata, **kwargs):
    if kwargs['type']=='ZLLSwitch':
        return Dimmer(bridge, sensordata, **kwargs)
    elif kwargs['type']=='Daylight':
        return Daylight(bridge, sensordata, **kwargs)
    elif kwargs['type']=='ZGPSwitch':
        return Tap(bridge, sensordata, **kwargs)
    elif kwargs['type']=='ZLLPresence':
        return Motion(bridge, sensordata, **kwargs)
    elif kwargs['type']=='ZLLTemperature':
        return Temperature(bridge, sensordata, **kwargs)
    elif kwargs['type']=='ZLLLightLevel':
        return LightLevel(bridge, sensordata, **kwargs)
    elif kwargs['type']=='CLIPSwitch':
        return CLIPSwitch(bridge, sensordata, **kwargs)
    elif kwargs['type']=='CLIPOpenClose':
        return CLIPOpenClose(bridge, sensordata, **kwargs)
    elif kwargs['type']=='CLIPPresence':
        return CLIPPresence(bridge, sensordata, **kwargs)
    elif kwargs['type']=='CLIPTemperature':
        return CLIPTemperature(bridge, sensordata, **kwargs)
    elif kwargs['type']=='CLIPHumidity':
        return CLIPHumidity(bridge, sensordata, **kwargs)
    elif kwargs['type']=='CLIPDaylight':
        return CLIPDaylight(bridge, sensordata, **kwargs)
    elif kwargs['type']=='CLIPGenericFlag':
        return CLIPGenericFlag(bridge, sensordata, **kwargs)
    elif kwargs['type']=='CLIPGenericStatus':
        return CLIPGenericStatus(bridge, sensordata, **kwargs)
    elif kwargs['type']=='CLIPZLLLightLevel':
        return CLIPZLLLightLevel(bridge, sensordata, **kwargs)
    raise NotImplementedError('Sensor type of "%s" is unsupported' % kwargs['type'])

class Sensor(GeneralHueObject):
    def attr_filter(self):
        self.rw_attributes=['name','config','recycle']
        self.ro_attributes=['type','modelid','manufacturername','uniqueid']

# ZigBee native sensors
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

class Motion(Sensor): #ZLLPresence
    def attr_filter(self):
        self.rw_attributes.append('sensitivity')
        self.ro_attributes.append('sensitivitymax')
        self.buttonOn=DimmerButton()
        self.buttonDimUp=DimmerButton()
        self.buttonDimDown=DimmerButton()
        self.buttonOff=DimmerButton()
ZLLPresence=Motion

class LightLevel(Sensor): #ZLLLightLevel
    def attr_filter(self):
        self.rw_attributes.append('tholddark')
        self.rw_attributes.append('tholdoffset')
ZLLLightLevel=LightLevel

class Temperature(Sensor):
    pass

# CLIP (IP) sensors
class CLIPLightlevel(LightLevel):
    pass

class CLIPGenericFlag(Sensor):
    pass

class CLIPGenericStatus(Sensor):
    pass

class CLIPSwitch(Sensor):
    pass

class CLIPOpenClose(Sensor):
    pass

class CLIPPresence(Sensor):
    pass

class CLIPTemperature(Sensor):
    pass

class CLIPHumidity(Sensor):
    pass

#Pseudo sensors
class Daylight(Sensor):
    def attr_filter(self):
        self.rw_attributes.append('lat')
        self.rw_attributes.append('long')
        self.rw_attributes.append('sunriseoffset')
        self.rw_attributes.append('sunsetoffset')
 
