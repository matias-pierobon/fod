from struct import Struct

types = {
    'integer': 'i',
    'string': 'c'*255,
    'char': 'c',
    'boolean': '?',
    'long': 'l',
    'float': 'f',
    'double': 'd',
    'real': 'd'
}

class StructuredFile():

    def __init__(self, filename, structure, mode='rb'):
        self.struct = Struct("x".join([ types[t] for t in structure ]))
        self.filename = filename
        self.file = open(filename, mode)
    
    def normalize(self, data):
        return self.struct.pack(*data)

    def denormalize(self, buffer):
        return self.struct.unpack(buffer)

    def write(self, tuple):
        self.file.write(self.normalize(tuple))
    
    def read(self):
        return self.denormalize(self.file.read(self.size()))
    
    def size(self):
        return self.struct.size

    def seek(self, position, from_what=0):
        if (not isinstance(position, int)):
            raise TypeError()
        if((0 <= position < len(self)) and from_what == 0):
            #(x, 0)
            pass
        elif((0 <= self.tell() + position < len(self)) and from_what == 1):
            #(x, 1)
            pass
        elif((-len(self) < position <= 0) and from_what == 2):
            #(x, 2)
            pass
        elif( position < 0 and from_what == 0):
            #(-x, 0)
            return self.tail(-position)
        else:
            raise IndexError()
        
        return self.file.seek(position * self.size(), from_what)

    def forward(self, position):
        return self.seek(position, 1)

    def backward(self, position):
        return self.forward(-position)

    def tail(self, position=0):
        return self.seek(-position, 2)

    def tell(self):
        return self.file.tell() // self.size()

    def eof(self):
        return self.tell() == len(self)

    def close(self):
        self.file.close()

    def __iter__(self):
        try:
            while True:
                yield self.read()
        except:
            return

    def __repr__(self):
        return f"<StructuredFile filename={self.filename} struct={self.struct}>"

    def __str__(self):
        return self.filename

    def __len__(self):
        pos = self.file.tell()
        size = self.file.seek(0, 2)
        self.file.seek(pos)
        return size // self.size()
    
    def __length_hint__(self):
        return len(self)

    def __getitem__(self, position):
        if isinstance(position, slice):
            return [self[p] for p in range(*position.indices(len(self)))]

        self.seek(position)
        return self.read()

    def __missing__(self, position):
        return position < len(self)
    
    def __setitem__(self, position, data):
        if isinstance(position, slice):
            for p in range(*position.indices(len(self))):
                self[p] = data
            return

        self.seek(position)
        self.write(data)
    
    def __contains__(self, item):
        p = self.tell()
        self.seek(0)
        for i in self:
            if i == item:
                return True
        self.seek(p)
        return False

    def __enter__(self):
        self.seek(0)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

if(__name__ == '__main__'):
    file = StructuredFile('turnos.dat', ('char', 'integer'), 'rb+')
    print(file[1:3])