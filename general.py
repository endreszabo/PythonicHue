
def indenter(items, indent=1, char='\t', suffix=''):
    for i in range(len(items)):
        #print(type(items[i]))
        if type(items[i]) == list:
            #items[i]=char+indenter(items[i], indent=indent+1, char=char, suffix=suffix)
            items[i]=char+indenter(items[i], indent=indent+1, char=char, suffix=suffix)
        if items[i][0]!='#' and items[i][-1]!=suffix:
            items[i]+=suffix
    return ('\n'+(char*indent)).join(items)

class ObjectList(list):
    def __repr__(self):
        return("[\n\t\t"+',\n\t\t'.join([str(x) for x in self])+"\n\t]")

class ObjectGroup:
    def __init__(self,bridge=None,name='(no name)'):
        self.objects=dict()
        self.objects_by_name=dict()
        self.objects_by_hue_id=dict()
        self.bridge=bridge
        self.name=name
        for objtype in ['light', 'group', 'sensor', 'schedule', 'scene']:
            self.objects[objtype]=list()
            self.objects_by_name[objtype]=dict()
            self.objects_by_hue_id[objtype]=dict()
    def add_object(self,objtype,obj):
        #if objtype not in self.objects:
        #    self.objects[objtype]=list()
        #    self.objects_by_name[objtype]=dict()
        #    self.objects_by_hue_id[objtype]=dict()
        if objtype not in self.objects:
            raise ValueError('Object class "%s" storage not defined in ObjectGroup' % objtype)
        self.objects[objtype].append(obj)
        if obj.hue_id:
            print('og name %s adding obytype %s with id %s' % (self.name, objtype, obj.hue_id))
            self.objects_by_hue_id[objtype][obj.hue_id]=obj
        if 'name' in obj.kwargs:
            self.objects_by_name[objtype][obj.kwargs['name']]=obj
        #self.objects[obj.__class__.__name__.lower()][obj.hue_id]=obj
        return obj
    def add_light(self, hue_id, light):
        return self.add_object('light',light)
    def add_group(self, hue_id, group):
        return self.add_object('group',group)
    def add_sensor(self, hue_id, sensor):
        return self.add_object('sensor',sensor)
    def add_schedule(self, hue_id, schedule):
        return self.add_object('schedule',schedule)
    def get_lights(self):
        return repr(self.objects['light'])
    def get_groups(self):
        return repr(self.groups)
    def get_sensors(self):
        return repr(self.sensors)
    def get_schedules(self):
        return repr(self.schedules)
    def get_object_by_id(self, obj, hue_id):
        return self.objects_by_hue_id[obj][hue_id]
    def get_object_by_hue_id(self, obj, hue_id):
        #return list(filter(lambda x: x.kwargs['hue_id']==hue_id, self.objects[obj]))
#        matched_object_key=list(
#            filter(
#                lambda x: self.objects[obj][x].hue_id==hue_id,
#                list(self.objects[obj].keys())
#            )
#        )
        if hue_id in self.objects_by_hue_id[obj]:
            return self.objects_by_hue_id[obj][hue_id]
        return None
    def to_python(self, prefix=[], suffix=[]):
        s=[]
        for obj in self.objects:
            s+=[
                '#'*(len(obj)+12),
                '# %s objects #' % obj,
                '#'*(len(obj)+12),
                ''
            ]
            #s+=prefix
            for item in self.objects[obj]:
                s+=item.to_python(obj)
                s.append('')
        #if suffix:
        #    s+=suffix
        return s

##        for light in self.objects['light']:
##            #print(light)
##            print('lights["%s"] = bridges["%s"].add_light(%s)' % (
##                light.kwargs['name'],
##                self.name,
##                light.__repr__()
##            ))
    def diff(self, other):
        print('2 actual has:', repr(self.objects_by_hue_id))
        print('2 desired has: ', repr(other.objects_by_hue_id))
        print('3 actual has:', repr([[x, id(x)] for x in self.objects['light']]))
        print('3 desired has:', repr([[x, id(x)] for x in other.objects['light']]))
        print('===self===')
        print('objects ',repr(self.objects))
        print('objects_by_id ',repr(self.objects_by_hue_id))
        print('objects_by_name ',repr(self.objects_by_name))
        print('===other===')
        print('objects ',repr(other.objects))
        print('objects_by_id ',repr(other.objects_by_hue_id))
        print('objects_by_name ',repr(other.objects_by_name))
        print(repr(other.objects_by_hue_id))
        for objtype in other.objects_by_hue_id:
            print('processing objtype: "%s"'%objtype)
            print('self',self.objects_by_hue_id[objtype])
            print('other',other.objects_by_hue_id[objtype])
            for obj in list(other.objects_by_hue_id[objtype].keys()):
                print(self.objects_by_hue_id[objtype][obj].diff(other.objects_by_hue_id[objtype][obj]))
                if obj not in self.objects_by_hue_id[objtype]:
                    print('nincs')
                    self.bridge.add_change('POST',{'obj':obj})
                else:
                    print('van')
        print(self, other)

    def __repr__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.name)

class GeneralHueObject:
    def attr_filter(self):
        pass

    def configure(self):
        pass

    def fill_rw(self, **kwargs):
        for attr in self.rw_attributes:
            if type(attr) == tuple:
                if attr[0] in kwargs:
                    self.kwargs[attr[1]]=kwargs[attr[0]]
            if attr in kwargs:
                self.kwargs[attr]=kwargs[attr]

    def fill_ro(self, **kwargs):
        for attr in self.ro_attributes:
            if attr in kwargs:
                self.rokwargs[attr]=kwargs[attr]
    def reference(self):
        return 'bridges["%s"].get_light_by_name("%s")' % (self.bridge.name, self.name())

    def name(self):
        return self.kwargs['name']
        if self.kwargs.has_key('name'):
            return self.kwargs['name']
        return self.hue_id

    def __init__(self, bridge=None, hue_id=None, **kwargs):
        self.bridge=bridge
        self.kwargs=dict()
        self.rokwargs={}
        self.rw_attributes=['name']
        self.ro_attributes=['uniqueid']
        self.resolve_hue_id_fields=[]
        #kwargs=kwargs.copy()
        self.hue_id=hue_id
        self.properties = kwargs
        self.attr_filter()
        self.fill_rw(**kwargs)
        self.fill_ro(**kwargs)
        #print(self.__repr__())
        #reprs.append(self.__repr__())
        self.configure()
##    def __repr__(self):
##        s=[]
##        s.append('%s(hue_id=%r,\n\t## Read-write attributes\n\t%s,\n\t## Read-only attributes\n\t%s\n)' % (
##            self.__class__.__name__, self.hue_id,
##            ',\n\t'.join(['{0}={1!r}'.format(k, v) for k, v in self.kwargs.items()]),
##            ',\n\t'.join(['{0}={1!r}'.format(k, v) for k, v in self.rokwargs.items()])
##        ))
##        return "\n".join(s)
    def diff(self, other):
        u=[]
        for arg in list(set(list(self.kwargs.keys())+list(other.kwargs.keys()))):
            if arg not in list(self.kwargs.keys()):
                u.append(('POST', { arg: other.kwargs }))
            elif self.kwargs[arg] != other.kwargs[arg]:
                u.append(('PUT', { arg: other.kwargs }))
        return u
    def action(self, action):
        if action:
            addrparts=action['address'].split('/')
            #print(addrparts)
            #`print(self.bridge.actual.objects['sensors'])
            addrparts[3]=addrparts[3][:-1]
            unit=self.bridge.get_object_by_hue_id(addrparts[3], addrparts[4])
            #print(unit)
            if unit:
                action=unit.render_action(addrparts[5:], action)
    def render_action(self, addrparts, action):
        return {'foo':'bar'}
    def to_python(self, objtype, prefix=[], suffix=[]):
        print(self.__class__.__name__,repr(self.kwargs))
        if self.resolve_hue_id_fields:
            for field in self.resolve_hue_id_fields:
                print("Type of field",type(self.kwargs[field[0]]))
                if type(self.kwargs[field[0]]) == list:
                    for i in range(len(self.kwargs[field[0]])):
                        self.kwargs[field[0]][i]=self.bridge.generate_object_reference_by_id(field[1], self.kwargs[field[0]][i], field[2])
                elif type(self.kwargs[field[0]]) == dict:
                    the_dict=self.kwargs[field[0]]
                    for i in list(the_dict.keys()):
                        the_dict[self.bridge.generate_object_reference_by_id(field[1], i, field[2])]=the_dict[i]
                        the_dict.pop(i)
                    #raise NotImplementedError('Dict reference generation not supported')
        s=['bridge.add_%s(%s(' % (objtype, self.__class__.__name__)]
        s+=prefix
        s.append('\t## Read-write attributes')
        s+=['\t{0}={1!r},'.format(k, v) for k, v in self.kwargs.items()]
        s.append('\t## Read-only attributes')
        s+=['\t{0}={1!r},'.format(k, v) for k, v in self.rokwargs.items()]
        s+=suffix
        s.append('))')
        return s
    def get_name(self):
        if 'name' in self.kwargs:
            return self.kwargs['name']
        else:
            raise ValueError('object "%s" has no name' % self.__class__.__name__)
    def __repr__(self):
        return '<%s "%s">' % (self.__class__.__name__, self.kwargs['name'])

