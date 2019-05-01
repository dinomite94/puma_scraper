#!/usr/local/bin/python3
from openpyxl import workbook, load_workbook
from openpyxl.drawing.image import Image

from collections import namedtuple
import os


HyperLink = namedtuple('HyperLink', ['text', 'link'])

root_dir = os.path.dirname(os.path.realpath(__file__))
template_xlsx = os.path.join(root_dir, 'templates/Auswertung Untersuchungskriterien.xlsx')
output_xlsx = os.path.join(root_dir, 'out/jobs/Auswertung Untersuchungskriterien.xlsx')


def export(data_table):
    xfile = load_workbook(template_xlsx)
    sheet = xfile.get_sheet_by_name('Sheet1')

    row_num = 5
    for row in data_table:
        column_num = 2

        for data in row:
            cell = sheet.cell(row=row_num, column=column_num)

            if isinstance(data, HyperLink):
                cell.value = data.text
                cell.hyperlink = data.link
                cell.style = 'Hyperlink'
            else:
                cell.value = data

            column_num += 1

        row_num += 1

    xfile.save(output_xlsx)



if __name__ == "__main__":    
    rows = [
        [0, 0, 0,
            HyperLink(text='Screenshot', link='jobs/r874.png'),
            HyperLink(text='Lokal', link='jobs/r874.html'),
            HyperLink(text='Online', link='https://about.puma.com/en/jobs/r874')],
        [1, 2, 3],
        [6, 5, 4],
    ]

    export(rows)
