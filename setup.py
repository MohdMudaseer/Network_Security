'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''

from setuptools import setup,find_packages
from typing import List


def get_requirements()->List[str]:
    '''
    This function will return list of requirements
    '''
    requirements:List[str]=[]
    try:
        with open('requirements.txt','r') as file_obj:
            #Read lines from the file
            lines=file_obj.readlines()
            ## Process each line
            for line in lines:
                requirement=line.strip()
                ## ignore empty lines and -e .
                if requirement and requirement!= '-e .':
                    requirements.append(requirement)

    except FileNotFoundError:
        print("No such file found")

    return requirements


setup(
    name="Network_Security_Project",
    version="0.0.1",
    author="Mohd Mudaseer Mazharuddin",
    author_email="mudaseer2753@gmail.com",
     packages=find_packages(),
    install_requires=get_requirements()
)