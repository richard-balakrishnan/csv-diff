import os
# path - path or directory
# ext - extension of file to be found
# eg: getExtList('D:\folder','csv')
def getExtList(path, ext):
    collect = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if(file.endswith('.' + ext)):
                collect.append(os.path.join(root,file))
    return collect