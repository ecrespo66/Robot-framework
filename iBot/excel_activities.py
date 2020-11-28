import os, sys, subprocess
from openpyxl import load_workbook, Workbook

# Renaming functions
OpenExcelWorkbook = load_workbook

# Renaming classes
NewExcelWorkbook = Workbook


class Excel:
    
    def __init__(self, path):
        self.path = path
        
        if not os.path.exists(self.path):
            Workbook().save(self.path)
        
        return
    
    def open(self):

        if os.path.exists(self.path):
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, path])

        elif not os.self.path.exists(self.path):
            ExcelCreateWorkbook(self.path)
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, self.path])

    def save(self, new_path=None):

        workbook = load_workbook(self.path)
        if not new_path:
            workbook.save(self.path)
        elif not os.path.isfile(new_path):
            workbook.save(new_path)

    def addSheet(self, sheet_name=None):

        workbook = load_workbook(self.path)
        
        if sheet_name not in workbook.sheetnames:
            workbook.create_sheet(title=sheet_name)
            workbook.save(self.path)

        elif not sheet_name:
            workbook.create_sheet()
            workbook.save(self.path)
            
    def removeSheet(self, sheet_name):
        
        workbook = load_workbook(self.path)
        
        if sheet_name in workbook.sheetnames:
            del workbook[sheet_name]
            workbook.save(self.path)
        else:
            pass
            
    def renameSheet(self, oldName, newName):
        workbook = load_workbook(self.path)
        if oldName in workbook.sheetnames:
            workbook[oldName].title = newName
            workbook.save(self.path)
        else:
            print("sheet doesn't exist")
        
    def getSheets(self):
    
        workbook = load_workbook(self.path)
        return workbook.sheetnames

    def readCell(self, cell="A1", sheet=None):
   
        workbook = load_workbook(self.path)

        if sheet:
            worksheet = workbook[sheet]
        else:
            worksheet = workbook.active

        return worksheet[cell].value


    def readRowCol(self, r=1, c=1, sheet=None):
   
        workbook = load_workbook(self.path)
        if sheet:
            worksheet = workbook[sheet]
        else:
            worksheet = workbook.active
        return worksheet.cell(row=r, column=c).value


    def writeCell(self, sheet=None, cell="A1", value=None):
    
        workbook = load_workbook(self.path)
        if sheet:
            worksheet = workbook[sheet]
        else:
            worksheet = workbook.active

        worksheet[cell] = value
        workbook.save(self.path)
        


    def writeRowCol(self, sheet=None, r=1, c=1, write_value='Value'):
   
        workbook = load_workbook(self.path)
        if sheet:
            worksheet = workbook[sheet]
        else:
            worksheet = workbook.active
            worksheet.cell(row=r, column=c).value = write_value
            workbook.save(self.path)
            return

    def rowInList(self, start_cell, end_cell, sheet=None):

        workbook = load_workbook(self.path)
        if sheet:
            worksheet = workbook[sheet]
        else:
            worksheet = workbook.active

        values = []
        for rowobj in worksheet[start_cell:end_cell][0]:
            values.append(rowobj.value)

        return values

    def columnInList(self, start_cell, end_cell, sheet=None):

        workbook = load_workbook(self.path)
        if sheet:
            worksheet = workbook[sheet]
        else:
            worksheet = workbook.active

            values = []
        for colobj in worksheet[start_cell:end_cell]:
            values.append(colobj[0].value)

        return values


    def selectionInMatrix(self, upper_left_cell, bottom_right_cell, sheet=None):

        workbook = load_workbook(self.path)
        if sheet:
            worksheet = workbook.get_sheet_by_name(sheet)
        else:
            worksheet = workbook.active

        matrix = []
        for rowobj in worksheet[upper_left_cell:bottom_right_cell]:
            next_row = []
            for cellobj in rowobj:
                next_row.append(cellobj.value)
            matrix.append(next_row)

        return matrix
        
        

'''

def ExcelCreateWorkbook(path):
    
    if not os.path.exists(path):
        Workbook().save(path)
    return


def ExcelOpenWorkbook(path):
   
    if os.path.exists(path):
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, path])

    elif not os.path.exists(path):
        ExcelCreateWorkbook(path)
        opener ="open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, path])
    return


def ExcelSaveExistingWorkbook(path, new_path=None):

    workbook = load_workbook(path)
    if not new_path:
        workbook.save(path)
    elif not os.path.isfile(new_path):
        workbook.save(new_path)
    return


def ExcelCreateWorkSheet(path, sheet_name=None):
    
    workbook = load_workbook(path)
    if sheet_name and sheet_name not in workbook.get_sheet_names():
        workbook.create_sheet(title=sheet_name)
    elif not sheet_name:
        workbook.create_sheet()
    workbook.save(path)
    return


def ExcelGetSheets(path):
    
    workbook = load_workbook(path)
    return workbook.get_sheet_names()


def ExcelReadCell(path, cell="A1", sheet=None):
   
    workbook = load_workbook(path)
    if sheet:
        worksheet = workbook.get_sheet_by_name(sheet)
    else:
        worksheet = workbook.active

    return worksheet[cell].value


def ExcelReadRowCol(path, r=1, c=1, sheet=None):
   
    workbook = load_workbook(path)
    if sheet:
        worksheet = workbook.get_sheet_by_name(sheet)
    else:
        worksheet = workbook.active

    return worksheet.cell(row=r, column=c).value


def ExcelWriteRowCol(path, sheet=None, r=1, c=1, write_value='Value'):
   
    workbook = load_workbook(path)
    if sheet:
        worksheet = workbook.get_sheet_by_name(sheet)
    else:
        worksheet = workbook.active
    worksheet.cell(row=r, column=c).value = write_value
    workbook.save(path)
    return


def ExcelWriteCell(path, sheet=None, cell="A1", write_value='Value'):
    
    workbook = load_workbook(path)
    if sheet:
        worksheet = workbook.get_sheet_by_name(sheet)
    else:
        worksheet = workbook.active

    worksheet[cell] = write_value
    workbook.save(path)
    return


def ExcelPutRowInList(path, start_cell, end_cell, sheet=None):

    workbook = load_workbook(path)
    if sheet:
        worksheet = workbook.get_sheet_by_name(sheet)
    else:
        worksheet = workbook.active

    values = []
    for rowobj in worksheet[start_cell:end_cell][0]:
        values.append(rowobj.value)

    return values


def ExcelPutColumnInList(path, start_cell, end_cell, sheet=None):

    workbook = load_workbook(path)
    if sheet:
        worksheet = workbook.get_sheet_by_name(sheet)
    else:
        worksheet = workbook.active

    values = []
    for colobj in worksheet[start_cell:end_cell]:
        values.append(colobj[0].value)

    return values

def ExcelPutSelectionInMatrix(path, upper_left_cell, bottom_right_cell, sheet=None):

    workbook = load_workbook(path)
    if sheet:
        worksheet = workbook.get_sheet_by_name(sheet)
    else:
        worksheet = workbook.active

    matrix = []
    for rowobj in worksheet[upper_left_cell:bottom_right_cell]:
        next_row = []
        for cellobj in rowobj:
            next_row.append(cellobj.value)
        matrix.append(next_row)

    return matrix

'''    