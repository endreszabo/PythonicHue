import qhue
from general import GeneralHueObject, ObjectGroup, indenter
from hue import *

def format_dict(kwargs, indent=1, char='\t'):
    return [(char*indent)+'{0} = {1!r},'.format(k, v) for k, v in kwargs.items()]

class Bridge:
    qhue=None
    rw_attributes=['name','zigbeechannel','dhcp','ipaddress','netmask','gateway','proxyaddress','proxyport','timezone','portalservices']
    ro_attributes=['bridgeid']
    kwargs={}
    rokwargs={}

    def __init__(self, api_key='', **kwargs):
        self.qhue=qhue.Bridge(kwargs['ipaddress'], api_key)
        self.api_key=api_key
        self.object_groups={
            'actual': ObjectGroup(self,'actual'),
            'desired': ObjectGroup(self,'desired')
        }
        self.current_object_group='actual'

        self.config = self.raw_get_config()
        self.name = self.config['name']
        self.populate_actual()
        self.changes=[]
        for attr in self.rw_attributes:
            if attr in self.config:
                self.kwargs[attr]=self.config[attr]
        for attr in self.ro_attributes:
            if attr in self.config:
                self.rokwargs[attr]=self.config[attr]
        self.current_object_group='desired'
    def add_change(self, method='PUT', body={}):
        print('would change:', body)
        pass
    def commit(self):
        #self.object_groups['actual'].diff(self.object_groups['desired'])
        self.object_groups['desired'].diff(self.object_groups['actual'])
    def populate_actual(self):
        jsonlights=self.raw_get_lights()
        for light in jsonlights:
            foo=jsonlights[light]
            foo['serial']='fixme'
            #self.add_actual('lights',Light(self, light, **foo))
            #self.actual.add_light(light, Light(self, light, **foo))
            self.add_light(Light(self, light, **foo))
        jsongroups=self.raw_get_groups()
        for group in jsongroups:
            foo=jsongroups[group]
            self.add_group(Group(self, group, **foo))
        jsonsensors=self.raw_get_sensors()
        for sensor in jsonsensors:
            foo=jsonsensors[sensor]
            self.add_sensor(SensorFactory(self, sensor, **foo))
        jsonschedules=self.raw_get_schedules()
        for schedule in jsonschedules:
            foo=jsonschedules[schedule]
            self.add_schedule(Schedule(self, schedule, **foo))
        jsonscenes=self.raw_get_scenes()
        for scene in jsonscenes:
            foo=jsonscenes[scene]
            self.add_scene(Scene(self, scene, **foo))
        jsonrules=self.raw_get_rules()
        for rule in jsonrules:
            foo=jsonrules[rule]
            self.add_rule(Rule(self, rule, **foo))
    def raw_get_lights(self):
        return self.qhue.lights()
    def raw_get_groups(self):
        return self.qhue.groups()
    def raw_get_sensors(self):
        return self.qhue.sensors()
    def raw_get_config(self):
        return self.qhue.config()
    def raw_get_schedules(self):
        return self.qhue.schedules()
    def raw_get_scenes(self):
        return self.qhue.scenes()
    def raw_get_rules(self):
        return self.qhue.rules()
    def add_actual(self, objtype, obj):
        return self.current_object_group.add_object(objtype, obj)
    def add_desured(self, objtype, obj):
        return self.current_object_group.add_object(objtype, obj)
    def add_normalize(self, objtype, obj):
        if not obj.hue_id:
            if not obj.name not in self.object_groups['actual'].objects_by_name:
                crate_object(objtype, obj)
            else:
                if obj.kwargs['name'] not in self.object_groups['actual'].objects_by_name[objtype]:
                    self.create_object(objtype, obj)#light)
                obj.hue_id=self.object_groups['actual'].objects_by_name[objtype][obj.kwargs['name']].hue_id
                obj.hue_id=self.object_groups['actual'].objects_by_name[objtype][obj.kwargs['name']].hue_id
    def create_light(light_wanted=None):
        raise NotImplementedError
    def create_object(self, objtype, obj):
        if objtype=='light':
            self.create_lights(obj)
        raise NotImplementedError('Object creation of type %s not yet supported' % objtype)
    def add_light(self, light):
        self.add_normalize('light', light)
        return self.object_groups[self.current_object_group].add_object('light',light)
    def add_group(self, group):
        self.add_normalize('group', group)
        return self.object_groups[self.current_object_group].add_object('group',group)
    def add_sensor(self, sensor):
        self.add_normalize('sensor', sensor)
        return self.object_groups[self.current_object_group].add_object('sensor',sensor)
    def add_schedule(self, schedule):
        self.add_normalize('schedule', schedule)
        return self.object_groups[self.current_object_group].add_object('schedule',schedule)
    def add_scene(self, scene):
        self.add_normalize('scene', scene)
        return self.object_groups[self.current_object_group].add_object('scene',scene)
    def add_rule(self, rule):
        self.add_normalize('rule',rule)
        return self.object_groups[self.current_object_group].add_object('rule',rule)
    def lights(self):
        return self.actual.get_lights()
    def groups(self):
        return self.actual.get_groups()
    def sensors(self):
        return self.actual.get_sensors()
    def schedules(self):
        return self.actual.get_schedules()
    def get_light_by_id(self, hue_id):
        if hue_id in self.actual.objects_by_hue_id['light']:
            return self.actual.objects_by_hue_id['light'][hue_id]
        return None
    def get_object_by_id(self, obj, hue_id):
        return self.actual.get_object_by_id(obj, hue_id)
    def get_object_by_hue_id(self, obj, hue_id):
        return self.object_groups['actual'].get_object_by_hue_id(obj, hue_id)
    def generate_object_reference_by_id(self, obj, hue_id, bridge_reference=True):
        #if bridge_reference:
        #    return 'bridge.get_%s("%s")' % (obj, self.object_groups[self.current_object_group].get_object_by_id(obj, hue_id).kwargs['name'])
        #return '%s' % (self.object_groups[self.current_object_group].get_object_by_id(obj, hue_id).kwargs['name'])
        obj = self.object_groups[self.current_object_group].get_object_by_id(obj, hue_id)
        if bridge_reference:
            return 'bridge.get_%s("%s")' % (obj, obj.name)
        return '%s' % (obj.name)
    def to_python(self):
        s=['bridge = %s(' % self.__class__.__name__,
            '\tapi_key="%s",' % self.api_key,
            '\t## Read-write attributes']
        s+=format_dict(self.kwargs)
        s.append('\t## Read-only attributes')
        s+=format_dict(self.rokwargs)
        s.append('\t## Lamp serial numbers (optional)')
        s.append('\tlamp_serials=[]')
        s+=[')','']
        s+=self.object_groups['actual'].to_python()
        return "\n".join(s)
##    def __repr__(self):
##        s=[]
##        s.append(indenter([
##            'bridges["%s"] = %s(api_key="%s"' % (self.name, self.__class__.__name__, self.api_key),
##            '## Read-write attributes',
##            ['{0}={1!r}'.format(k, v) for k, v in self.kwargs.items()],
##            '## Read-only attributes',
##            ['{0}={1!r}'.format(k, v) for k, v in self.rokwargs.items()], 
##            ')'
##            ],suffix=',',
##        ))
##
##        s.append('bridges["%s"] = %s(api_key="%s",\n\t## Read-write attributes\n\t%s,\n\t## Read-only attributes\n\t%s\n)' % (
##            self.name, self.__class__.__name__, self.api_key,
##            ',\n\t'.join(['{0}={1!r}'.format(k, v) for k, v in self.kwargs.items()]),
##            ',\n\t'.join(['{0}={1!r}'.format(k, v) for k, v in self.rokwargs.items()])
##        ))
##        s.append('light={}')
##        for light in self.actual.objects['lights']:
##            print(light)
##            print('lights["%s"] = bridges["%s"].add_light(%s)' % (
##                light.kwargs['name'],
##                self.name,
##                light.__repr__()
##            ))
##        return "\n".join(s)
