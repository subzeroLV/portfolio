'''
This project was created to monitor the output of spoolfiles from an AS400 system
that creates PDF's instead of physically printing.
'''
# import libraries/packages
from pathlib import Path
from datetime import datetime
import os 
from collections import namedtuple
import pandas as pd 

# named tuples are iterable
File = namedtuple('File', 'name path size_kb modified_date')

# create empty list for the files
files = []

# declare the path to browse. In this case, it's a directory for print jobs converted to PDF
p = Path(r'Z:\RPA9')
#p = Path(r'Z:\RST8')

def endPrint():
    '''
    Sets up the printing for the results at the end of the script
    '''
    print(df, '\n')
    print(f"Number of files in {path}: {len(files)}")
    print(f'Total combined size of files is: {columnRounded} Mb')
    print('End of Report\n')

# use glob to get specific files/file extensions
for item in p.glob('**/*'):
    if item.suffix in (['.PDF', '.pdf']):
        name = item.name
        path = Path.resolve(item).parent
        size = item.stat().st_size / 1024   # convert bytes to kilobytes
        rounded = round(size, 2)            # round to 2 decimal places
        modified = datetime.fromtimestamp(item.stat().st_mtime)

        files.append(File(name, path, rounded, modified))

# convert list of files to dataframe
df = pd.DataFrame(files)

# total the file sizes, convert to megabytes, and round to 2 decimal places
columnName = 'size_kb'
columnSum = df[columnName].sum() / 1024
columnRounded = round(columnSum, 2)

endPrint()
