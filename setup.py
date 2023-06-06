from typing import List
from setuptools import(
    find_packages,
    setup
)


def get_requirements(file_path:str)->List[str]:

    requirements=[]
    HYPHEN_DOT='-e .'

    with open(file_path) as file_obj:
        
        requirements=file_obj.readlines()
        requirements=[reqs.replace("\n"," ") for reqs in requirements]


        if HYPHEN_DOT in requirements:
            requirements.remove(HYPHEN_DOT)


    return requirements




setup(
    name="Students ML Project",
    version='5.2.1',
    author='Ahmad Mponda',
    author_email='ahmadmponda@gmail.com',
    description='This Project uses Machine Learning to predict Students Performance',
    packages=find_packages(),
    install_reqs=get_requirements('requirements.txt')
)
