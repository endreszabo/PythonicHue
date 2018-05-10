from general import GeneralHueObject, ObjectList, MultiRowList
from metaobjects import *
from huedatatypes import *

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
        #self.resolve_hue_id_fields=[
        #    ('lights','light', False)
        #]
        #super.config(self, hue_id, json)
    def fill_rw(self, **kwargs):
        super(Group, self).fill_rw(**kwargs)
        lights=self.kwargs['lights']
        #"self.kwargs['lights']=ObjectList(self.kwargs['lights'])
        lights=[]
        for light in self._raw_attrs['lights']:
            lights.append(self.bridge.generate_object_reference_by_id('light', light, bridge_reference=False))
        print('lights',self.hue_id,lights)
        self.rw_attrs.add_attribute([
            Attribute('name', HueString(self._raw_attrs['name'], 1, 32), helptext='A unique, editable name given to the group.'),
            Attribute('lights', MultiRowList(lights), helptext='The unique names of the lights that are in the group.'),
        ])
        #self.ro_attrs.add_attribute([
        #    Attribute('serial', HueString('EDITME', 6, 6), optional=True, helptext='6-characters serial number printed on light used for (re)adopting lights (optional)'),
        #    Attribute('uniqueid', HueString(self._raw_attrs['uniqueid'], 6, 32), helptext='Unique id of the device. The MAC address of the device with a unique endpoint id in the form: AA:BB:CC:DD:EE:FF:00:11-XX'),
        #])
    pass

class Light(GeneralHueObject):
    #def attr_filter(self):
    #    self.rw_attributes.append('serial')
    def fill_rw(self, **kwargs):
        super(Light, self).fill_rw(**kwargs)
        self.rw_attrs.add_attribute(
            Attribute('name', HueString(kwargs['name'], 1, 32), helptext='A unique, editable name given to the light.'),
        )
        self.ro_attrs.add_attribute([
            Attribute('serial', HueString('EDITME', 6, 6), optional=True, helptext='6-characters serial number printed on light used for (re)adopting lights (optional)'),
            Attribute('uniqueid', HueString(self._raw_attrs['uniqueid'], 6, 32), helptext='Unique id of the device. The MAC address of the device with a unique endpoint id in the form: AA:BB:CC:DD:EE:FF:00:11-XX'),
        ])
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
    def fill_rw(self, **kwargs):
        super(Sensor, self).fill_rw(**kwargs)
        self.rw_attrs.add_attribute(
            Attribute('name', HueString(kwargs['name'], 1, 32), helptext='The human readable name of the sensor. Is not allowed to be empty. (String, len: 1..32)'),
        )
        if 'uniqueid' in self._raw_attrs: #Not all sensor has a uniqueid attrube
            print(self._raw_attrs['name'], self._raw_attrs['uniqueid'])
            print('but this one has: ',self._raw_attrs['uniqueid'])
            self.ro_attrs.add_attribute(
                Attribute('uniqueid', HueString(self._raw_attrs['uniqueid'], 6, 32), helptext='Unique id of the sensor. Should be the MAC address of the device. (String, len 6..32)'),
            )

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
        super(Sensor, self).attr_filter()
        self.buttonOn=DimmerButton()
        self.buttonDimUp=DimmerButton()
        self.buttonDimDown=DimmerButton()
        self.buttonOff=DimmerButton()
ZLLSwitch=Dimmer

class Presence(Sensor): #ZLLPresence
    def fill_rw(self, **kwargs):
        super(self.__class__, self).fill_rw(**kwargs)
        print(self._raw_attrs['config'])
        self.rw_attrs.add_attribute([
            Attribute('sensitivity',   HueInteger(self._raw_attrs['config']['sensitivity'], 0, self._raw_attrs['config']['sensitivitymax']), helptext='Sensitivity of the sensor. Value in the range 0..%s' % self._raw_attrs['config']['sensitivitymax']),
            Attribute('ledindication', HueBoolean(self._raw_attrs['config']['ledindication']), helptext='Turns device LED during normal operation on or off.  Devices might still indicate exceptional operation (Reset, SW Update, Battery Low)'),
            Attribute('usertest',      HueBoolean(self._raw_attrs['config']['usertest']), helptext='Activates or extends user usertest mode of device for 120 seconds. False deactivates usertest mode. In usertest mode, sensors report changes in state faster and indicate state changes on device LE.D'),
        ])
        for key in ['sensitivity','ledindication','usertest']:
            self.kwargs[key]=self._raw_attrs['config'][key]
            self.rw_attributes.append(key)
ZLLPresence=Presence

class LightLevel(Sensor): #ZLLLightLevel
    def fill_rw(self, **kwargs):
        super(self.__class__, self).fill_rw(**kwargs)
        self.rw_attrs.add_attribute([
            Attribute('on',               HueBoolean(self._raw_attrs['config']['on']), helptext='Turns the sensor on/off. When off, state changes of the sensor are not reflected in the sensor resource. Default is “true”'),
            Attribute('threshold_dark',   HueUInt16(self._raw_attrs['config']['tholddark']), helptext='Threshold the user configured to be used in rules to determine insufficient lightlevel (ie below threshold). Default value 16000'),
            Attribute('threshold_offset', HueUInt16(self._raw_attrs['config']['tholdoffset']), helptext='Threshold the user configured to be used in rules to determine sufficient lightlevel (ie above threshold). Specified as relative offset to the “dark” threshold. Shall be >=1. Default value 7000'),
            Attribute('ledindication', HueBoolean(self._raw_attrs['config']['ledindication']), helptext='Turns device LED during normal operation on or off.  Devices might still indicate exceptional operation (Reset, SW Update, Battery Low)'),
            Attribute('usertest',      HueBoolean(self._raw_attrs['config']['usertest']), helptext='Activates or extends user usertest mode of device for 120 seconds. False deactivates usertest mode. In usertest mode, sensors report changes in state faster and indicate state changes on device LE.D'),
        ])
        for key in ['on','tholddark','tholdoffset','ledindication','usertest']:
            self.kwargs[key]=self._raw_attrs['config'][key]
            self.rw_attributes.append(key)
ZLLLightLevel=LightLevel

class Temperature(Sensor):
    def fill_rw(self, **kwargs):
        super(self.__class__, self).fill_rw(**kwargs)
        self.rw_attrs.add_attribute([
            Attribute('ledindication', HueBoolean(self._raw_attrs['config']['ledindication']), helptext='Turns device LED during normal operation on or off.  Devices might still indicate exceptional operation (Reset, SW Update, Battery Low)'),
            Attribute('usertest',      HueBoolean(self._raw_attrs['config']['usertest']), helptext='Activates or extends user usertest mode of device for 120 seconds. False deactivates usertest mode. In usertest mode, sensors report changes in state faster and indicate state changes on device LE.D'),
        ])
        for key in ['ledindication','usertest']:
            self.kwargs[key]=self._raw_attrs['config'][key]
            self.rw_attributes.append(key)
ZLLTemperature=Temperature

# CLIP (IP) sensors
class IPSensor(Sensor):
    """General IP Sensor for storing extra values"""
    def attr_filter(self):
        self.ro_attributes+=['modelid','manufacturername']
    def fill_rw(self, **kwargs):
        super(IPSensor, self).fill_rw(**kwargs)
        self.ro_attrs.add_attribute([
            Attribute('modelid', HueString(kwargs['modelid'], 6, 32), helptext='This parameter uniquely identifies the hardware model of the device for the given manufacturer.'),
            Attribute('manufacturername', HueString(kwargs['manufacturername'], 6, 32), helptext='The name of the device manufacturer (Zigbee sensor manufacturer name, resp. IP device manufacturer)'),
        ])

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

    def fill_rw(self, **kwargs):
        super(Daylight, self).fill_rw(**kwargs)
        self.rw_attrs.add_attribute([
            Attribute('on',               HueBoolean(self._raw_attrs['config']['on']), helptext='Turns the sensor on/off. When off, state changes of the sensor are not reflected in the sensor resource. Default is “true”'),
            Attribute('sunrise_offset',   HueInteger(self._raw_attrs['config']['sunriseoffset'], -120, 120), helptext='Timeoffset in minutes to sunrise. Daylight changes to true sunriseoffset minutes after sunrise. Values: -120..120min, default 30min. In case this cause overlap with sunset, daylight will be constantly: true if next sunrise is moved before sunset false if next sunrise is moved after sunset'),
            Attribute('sunset_offset',    HueInteger(self._raw_attrs['config']['sunsetoffset'], -120, 120), helptext='Timeoffset in minutes to sunset.  Daylight changes to true sunsetoffset minutes after sunset. Values: -120..120min, default -30min. . In case this cause overlap with sunset, daylight will be constantly: false if next sunset is moved before sunrise true if next sunset is moved after sunrise'),
        ])
        self.ro_attrs.add_attribute([
            Attribute('long', HueString('DDD.DDDDN', 9, 9), optional=True, helptext='GPS coordinate longitude in decimal degrees DDD.DDDD{W|E} with leading zeros required ending with W or E e.g. 000.3295W “none” .  In future versions this may change to null.'),
            Attribute('lat',  HueString('DDD.DDDDN', 9, 9), optional=True, helptext='GPS coordinate latitude in decimal degrees DDD.DDDD{N|S} with leading zeros required e.g. 010.5186N ending with N or S “none”.In future versions this may change to null.'),
        ])
