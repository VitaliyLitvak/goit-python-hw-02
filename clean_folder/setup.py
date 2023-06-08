from setuptools import setup, find_namespace_packages

setup(name='clean-folder',
      version='1',
      description='File sorter',
      url='https://github.com/maxafanasiev/homework_2',
      author='Litvak Vitaliy',
      author_email='afanasievmaksym2@gmail.com',
      packages=find_namespace_packages(),
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:sorter']})

