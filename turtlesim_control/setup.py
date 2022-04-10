import os
from glob import glob
from setuptools import setup

package_name = 'turtlesim_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share',package_name),glob('launch/*launch.py')),
        (os.path.join('share',package_name),glob('launch/*launch.xml'))

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Pi Thanacha Choopojcharoen',
    maintainer_email='tchoopojcharoen@gmail.com',
    description='This package consists of node that continuously control Turtlesim as well as launch file for running necessary nodes.',
    license='GPLv2',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'controller = turtlesim_control.controller:main',
            'scheduler = turtlesim_control.scheduler:main'
        ],
    },
)
