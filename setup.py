from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    this function for get independecy line by line from
    file requirements.txt return into list

    return : list of indepedency
    """

    requirement_list:List[str] = []
    try :
        with open('requirements.txt', 'r') as file:
            #Read line from the file
            lines = file.readlines()
            #Process each line
            for line in lines:
                requirement = line.strip()
                #ignore '-e .'
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    
    except FileNotFoundError:
        print('requirements.txt is not found')

    return requirement_list

#Set Setup
setup(
    name="NetworkSecurity",
    version='0.0.1',
    author='I Gusti Ayu Meliniarayani',
    author_email='igamelinia13@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)

