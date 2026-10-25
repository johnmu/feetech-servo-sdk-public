from setuptools import setup

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setup(
    name='feetech-servo-sdk',
    version='1.0.0+johnmu.1',
    packages=['scservo_sdk'],
    url='https://github.com/johnmu/feetech-servo-sdk-public',
    license='UNLICENSE',
    author='vertigra',
    author_email='a@nesterof.com',
    description='This is source code from official feetech repository',
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=['pyserial'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Operating System :: POSIX :: Other',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Hardware :: Universal Serial Bus (USB) :: Communications Device Class (CDC)'
    ]
)
