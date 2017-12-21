import xlrd

class Celda:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
class ProcesaExcel:

    def __init__(self, path, celda_cabecera_izq, celda_cabecera_der):
        if celda_cabecera_izq.row != celda_cabecera_der.row:
            raise ValueError("The row of both header cells must be equal!")
        elif celda_cabecera_izq.col >= celda_cabecera_der.col:
            raise ValueError("The left row cel must be lower than right row cel!")

        self.path = path
        self.celda_cabecera_izq = celda_cabecera_izq
        self.celda_cabecera_der = celda_cabecera_der

        wb = xlrd.open_workbook(self.path)
        # By default I work on first sheet
        ws = wb.sheet_by_index(0)
        
        self.headers = []
        for col in range(self.celda_cabecera_izq.col, self.celda_cabecera_der.col + 1):
            self.headers.append( ws.cell(self.celda_cabecera_izq.row, col).value )

    def get_excel_headers(self):
        return self.headers
        
    def get_excel_data(self):
        wb = xlrd.open_workbook(self.path)
        # By default I work on first sheet
        ws = wb.sheet_by_index(0)

        import ipdb; ipdb.set_trace(context=21)
        res = []
        row = self.celda_cabecera_izq.row + 1
        while row < ws.nrows:
            obj = dict()
            for col in range(self.celda_cabecera_izq.col, self.celda_cabecera_der.col + 1):
                obj[ ws.cell(self.celda_cabecera_izq.row, col).value ] = ws.cell(row, col)

            res.append(obj)
            row += 1

        return res

