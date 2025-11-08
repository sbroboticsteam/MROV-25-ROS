from setuptools import setup
import os
from glob import glob

package_name = 'widget_test'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name + '/resource', glob('resource/*.xml')), 
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Tyerone Chen',
    maintainer_email='user@example.com',
    description='A collection of custom ROS 2 widgets for rqt testing.',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_simpub = widget_test.simple_simpub:main',
        ],
        'rqt_gui_py.plugins': [
            'WidgetTemplate = widget_test.widget_template:WidgetTemplate',
        ],
    },
)
