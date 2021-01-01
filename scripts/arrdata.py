class Arrdata:
    def __init__(self, id, start, end, box):
        self.id = id
        self.start = start
        self.end = end
        self.box = box

arrdatas = {}
def add_arrdata(arrdata):
    arrdatas[arrdata.id] = arrdata

add_arrdata(Arrdata('2', 5, 24, 'kbox'))
add_arrdata(Arrdata('3', 13, 32, 'kbox'))
add_arrdata(Arrdata('11', 23, 190, 'mbox'))
add_arrdata(Arrdata('a', 136, 153, 'kbox'))
add_arrdata(Arrdata('b', 142, 160, 'kbox'))
add_arrdata(Arrdata('c', 149, 167, 'kbox'))
add_arrdata(Arrdata('d', 156, 173, 'kbox'))