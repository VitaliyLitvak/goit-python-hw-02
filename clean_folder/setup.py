from setuptools import setup, find_namespace_packages

setup(name='clean-folder',
      version='1',
      description='File sorter',
      url='https://github.com/VitaliyLitvak/goit-python-hw-02',
      author='Litvak Vitaliy',
      author_email='vitaliy.litvak@gmail.com',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:sorter']})