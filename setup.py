from setuptools import setup, find_packages

setup(
    name='file_watcher',
    version='0.0.1',
    description='A script that performs an action on file changes',
    url='https://github.com/karatekid/?',
    author='Michael Christen',
    author_email='mchristen96@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'file-watcher=file_watcher.file_watcher:main',
        ],
    }
)

