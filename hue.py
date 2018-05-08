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
        return Presence(bridge, sensordata, **kwargs)
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
        self.rw_attributes=['name']
        self.ro_attributes=['uniqueid']

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

class Presence(Sensor): #ZLLPresence
    def fill_rw(self, **kwargs):
        super(self.__class__, self).fill_rw(**kwargs)
        for key in ['sensitivity','ledindication','usertest']:
            self.kwargs[key]=self._raw_attrs['config'][key]
            self.rw_attributes.append(key)
ZLLPresence=Presence

class LightLevel(Sensor): #ZLLLightLevel
    def fill_rw(self, **kwargs):
        super(self.__class__, self).fill_rw(**kwargs)
        for key in ['on','tholddark','tholdoffset','ledindication','usertest']:
            self.kwargs[key]=self._raw_attrs['config'][key]
            self.rw_attributes.append(key)
ZLLLightLevel=LightLevel

class Temperature(Sensor):
    def fill_rw(self, **kwargs):
        super(self.__class__, self).fill_rw(**kwargs)
        for key in ['ledindication','usertest']:
            self.kwargs[key]=self._raw_attrs['config'][key]
            self.rw_attributes.append(key)
    pass
ZLLTemperature=Temperature

# CLIP (IP) sensors
class IPSensor(Sensor):
    """General IP Sensor for storing extra values"""
    def attr_filter(self):
        self.ro_attributes+=['modelid','manufacturername']

class CLIPLightlevel(IPSensor):
    pass

class CLIPGenericFlag(IPSensor):
    pass

class CLIPGenericStatus(IPSensor):
    pass

class CLIPSwitch(IPSensor):
    pass

class CLIPOpenClose(IPSensor):
    pass

class CLIPPresence(IPSensor):
    pass

class CLIPTemperature(IPSensor):
    pass

class CLIPHumidity(IPSensor):
    pass

#Pseudo sensors
class Daylight(Sensor):
    def fill_rw(self, **kwargs):
        super(self.__class__, self).fill_rw(**kwargs)
        for key in ['on','sunriseoffset','sunsetoffset']:
            self.kwargs[key]=self._raw_attrs['config'][key]
            self.rw_attributes.append(key)
        for key in ['lat','long']:
            self.kwargs[key]=''
            self.rw_attributes.append(key)

