from setuptools import find_packages, setup
from typing import List

Hypen_dot = "-e ."
def get_requirements(file_path:str)->List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements= file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

    if Hypen_dot in requirements:
        requirements.remove(Hypen_dot)

    return requirements


setup(
    name= "five in a row",
    version = "1.0.0",
    author="group 6",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)