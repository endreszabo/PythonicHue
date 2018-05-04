from general import GeneralHueObject, ObjectList

class Schedule(GeneralHueObject):
    def attr_filter(self):
        self.rw_attributes=['name','description','command','localtime','status','autodelete']
        self.ro_attributes=[]
    def configure(self):
        if 'command' in self.kwargs:
            #self.kwargs['command']['XXX']=122
            self.kwargs['command']=self.action(self.kwargs['command'])

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
        self.kwargs['lights']=ObjectList(self.kwargs['lights'])
    pass

class Light(GeneralHueObject):
    #def attr_filter(self):
    #    self.rw_attributes.append('serial')
    def to_python(self, objtype):
        return super(Light, self).to_python(objtype, suffix=["\t## 6-characters serial number printed on light (optional)","\tserial = None"])
    pass
