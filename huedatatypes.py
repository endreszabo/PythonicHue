class HueString(str):
    def __new__(cls, value, *args, **kwargs):
        return str.__new__(cls, value)
    def __init__(self, value, minlen, maxlen):
        if (len(value)>maxlen):
            raise ValueError('String allowed length exceeded')
        if (len(value)<minlen):
            raise ValueError('String shorter than allowed')
class HueASCIIString(HueString):
    def __new__(cls, value, *args, **kwargs):
        return str.__new__(cls, value)
    def __init__(self, value, minlen, maxlen):
        super(HueString, self.__class__).__init__(self, value, minlen, maxlen)
        if (value[0]=='k'):
            raise ValueError(self.__class__.__name__)
        if (len(value)>16):
            raise ValueError('String allowed length exceeded')


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
        if(self.helptext):
            s+=' # '+self.helptext
        return s

class AttributeGroup:
    def __init__(self, heading=None, attributes=[]):
        assert type(heading) is str
        self.heading=heading
        self.attributes=attributes
    def add_attribute(self, attribute):
        self.attributes.append(attribute)
    def to_python(self, indent=1):
        s=[("\t"*indent)+'## '+self.heading]
        for attribute in self.attributes:
            s.append(("\t"*indent)+str(attribute))
        return s
        #return "\n".join(s)
    pass

if __name__ == "__main__":
    a=AttributeGroup('read only stuffs', [
        Attribute('foo',HueASCIIString('ktest value', 0, 16), helptext='hint for foo attribute'),
        Attribute('bar',HueASCIIString('test string', 0, 16), helptext='hint again, but now for bar attribute'),
        ]
    )
    print(a.to_python())
