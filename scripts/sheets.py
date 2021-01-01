import os, xlrd

class Minput:
    def __init__(self):
        self.key = None
        self.filename = None
        self.rotation = None
        self.mirrored = None
        self.weight = None

class Tempo:
    def __init__(self):
        self.times = []
        self.beats = []

class Sheets:
    def read_minputs(self, wb):
        self.minputs = {}
        sheet = wb.sheet_by_name('minputs')
        keys = [sheet.cell_value(0, c) for c in range(sheet.ncols)]
        for r in range(1, sheet.nrows):
            minput = Minput()
            values = [sheet.cell_value(r, c) for c in range(sheet.ncols)]
            for key, value in zip(keys, values):
                if key == 'mirrored':
                    minput.mirrored = bool(value)
                elif key == 'weight':
                    minput.weight = float(value)
                else:
                    setattr(minput, key, value)
            minput.key = os.path.splitext(minput.filename)[0]
            self.minputs[minput.key] = minput
    def read_tempo(self, wb):
        sheet = wb.sheet_by_name('tempo')
        self.tempo = Tempo()
        self.tempo.times = [int(sheet.cell_value(r, 2))/48000 for r in range(1, sheet.nrows)]
        self.tempo.beats = [float(int(sheet.cell_value(r, 0))*4+int(sheet.cell_value(r, 1))-1) for r in range(1, sheet.nrows)]
    def __init__(self):
        wb = xlrd.open_workbook('xmas.xlsx')
        try:
            self.read_minputs(wb)
            self.read_tempo(wb)
        finally:
            wb.release_resources()
            
sheets = Sheets()
minputs = sheets.minputs
tempo = sheets.tempo