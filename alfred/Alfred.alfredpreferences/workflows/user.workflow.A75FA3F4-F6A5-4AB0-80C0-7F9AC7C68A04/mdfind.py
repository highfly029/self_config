# coding: utf-8

from workflow import Workflow3
import os
import sys
import subprocess
import re

def generate_feedback_results(wf,judge_code,fileName,result):
    if(judge_code == 1):
        kwargs = {
                    'title': fileName,
                    'subtitle': result,
                    "valid": True,
                    'arg': result
                }
    else:
        kwargs = {
                    'title': result,
                    'subtitle': '' ,
                    'valid': False
                }
    wf.add_item(**kwargs)

def main(wf):
    searchName = sys.argv[1]
    rootPath = sys.argv[2]

    for root,dirs,files in os.walk(rootPath):
        for file in files:
            filePath = os.path.join(root,file)
            if os.path.isfile(filePath):
                dir,fileName=os.path.split(filePath)
                # if fileName.lower().startswith(searchName.lower()) and fileName.endswith(".csv"):
                if searchName.lower() in fileName.lower():
                    generate_feedback_results(wf,1,fileName, filePath)
    
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow3()
    main(wf)