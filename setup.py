from setuptools import find_packages

from distutils.core import setup


version = '0.1'

setup(
    name = "django-file-sharing",
    version = version,
    author = "vahid chakoshy",
    author_email = "vchakoshy@gmail.com",
    description = "file sharing application",
    url = "https://github.com/karoon/django-file-sharing",
    packages=find_packages(),
    include_package_data = True,
    zip_safe=False,
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        
    ]
)
