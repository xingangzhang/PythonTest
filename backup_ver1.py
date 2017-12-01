import os
import time

source = ['F:\\OneDrive']
target_dir='F:\\back up'
if not os.path.exists(target_dir):
    os.mkdir(target_dir) # 创建目录
    print('Successfully created directory', target_dir)

today = target_dir + os.sep + time.strftime('%Y%m%d')
if not os.path.exists(today):
    os.mkdir(today)
    print('Successfully created directory', today)

comment = input('Enter a comment --> ')
if len(comment) == 0:
    target = '"' + today + os.sep + time.strftime('%H%M%S') + '.zip' + '"'
else:
    target = '"' + today + os.sep + time.strftime('%H%M%S') + '_' + comment.replace(' ','_') + '.zip' + '"'


zip_command = 'zip -r {0} {1}'.format(target, ' '.join(source))

print('Zip command is:')
print(zip_command)
print('Running:')
if os.system(zip_command) == 0:
    print('Successful backup to', target)
else:
    print('Backup FAILED')