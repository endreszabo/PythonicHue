class HueString(str):
    def __new__(cls, value, *args, **kwargs):
        return str.__new__(cls, value)
    def __init__(self, value, minlen, maxlen):
        if (len(value)>maxlen):
            raise ValueError('String allowed length exceeded')
        if (len(value)<minlen):
            raise ValueError('String shorter than allowed')

class HueInteger(int):
    def __new__(cls, value, *args, **kwargs):
        return int.__new__(cls, value)
    def __init__(self, value, minlen, maxlen):
        if (value>maxlen):
            raise ValueError('Value larger than allowed')
        if (value<minlen):
            raise ValueError('Value smaller than allowed')

class HueUInt16(HueInteger):
    def __init__(self, value):
        if (value>2**16-1):
            raise ValueError('Value larger than allowed')
        if (value<0):
            raise ValueError('Value smaller than allowed')
    #def __init__(self, value):
    #    super(HueInteger, self.__class__).__init__(self, value, 0, 2**16-1)

HueBoolean=bool #one can not simply subclass 'bool'


class HueASCIIString(HueString):
    def __new__(cls, value, *args, **kwargs):
        return str.__new__(cls, value)
    def __init__(self, value, minlen, maxlen):
        super(HueString, self.__class__).__init__(self, value, minlen, maxlen)
        if (value[0]=='k'):
            raise ValueError(self.__class__.__name__)
        if (len(value)>16):
            raise ValueError('String allowed length exceeded')

class HueArray(list):
    pass
        #assert len(value) > 0

class Attribute:
    def __init__(self, name, obj, optional=False, helptext=''):
        self.attribute=obj
        self.name=name
        self.helptext=helptext
        self.obj=obj
        self.optional=optional
    def __str__(self):
        s=''
        if(self.optional):
            s+'#'
        s+=self.name
        s+=' = '
        s+=repr(self.obj)
        s+=','
        if(self.helptext):
            s+=' # '+self.helptext
        return s
    #@property
    #def name(self):
    #    return self.name

class AttributeGroup:
    def __init__(self, heading=None, attributes=[]):
        assert type(heading) is str
        self.heading=heading
        self.attributes=dict()
        for attribute in attributes:
            self.attributes[attribute.name]=attribute
    def add_attribute(self, attributes):
        if (type(attributes) is list):
            for attribute in attributes:
                self.attributes[attribute.name]=attribute
        else:
            self.attributes[attributes.name]=attributes
    def to_python(self, indent=1):
        if self.attributes:
            s=[("\t"*indent)+'## '+self.heading]
            for attribute in self.attributes:
                s.append(("\t"*indent)+str(self.attributes[attribute]))
            return s
        return []
        #return "\n".join(s)

if __name__ == "__main__":
    a=AttributeGroup('read only stuffs', [
        Attribute('foo',HueASCIIString('ktest value', 0, 16), helptext='hint for foo attribute'),
        Attribute('bar',HueASCIIString('test string', 0, 16), helptext='hint again, but now for bar attribute'),
        ]
    )
    print(a.to_python())
