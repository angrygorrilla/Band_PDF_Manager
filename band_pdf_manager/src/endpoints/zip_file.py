import os
import zipfile
import time
toDirectory = ".\\Py\Backup"
fileName = int(time.time())


#zip all files in a given folder into a given zip file
#currently includes a second zipped folder, but this works for now
def zipdir(src,dest_name):
    zipf = zipfile.ZipFile(dest_name, 'w', zipfile.ZIP_DEFLATED)
    # ziph is zipfile handle
    for root, dirs, files in os.walk(src):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()

if __name__=="__main__":
    zipdir('tst','zipfile.zip')
