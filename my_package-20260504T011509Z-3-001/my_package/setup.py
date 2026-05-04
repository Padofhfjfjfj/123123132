from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1.0',
    description='A simple example package',
    author='Your Name',
    author_email='you@example.com',
    packages=find_packages(),          # 自動找出所有 package
    install_requires=[                 # 依賴套件
        # 'requests>=2.20.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',           # Python 最低版本需求
)
