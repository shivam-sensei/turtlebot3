import os

from setuptools import find_packages, setup

package_name = 'custom_launchfile'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['custom_launchfile/nav2_bringup.launch.py']),
        ('share/' + package_name + '/maps', ['maps/map.yaml', 'maps/map.pgm']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dream-hell',
    maintainer_email='shivgupta751157@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [ 
        ],
    },
)
