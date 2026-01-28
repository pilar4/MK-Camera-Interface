from setuptools import setup, Extension
import pybind11
import os

src_dir = os.path.join(os.path.dirname(__file__), "src_cursor")

ext_modules = [
    Extension(
        "src_cursor.cursor_cpp",
        [os.path.join(src_dir, "cursor_physics.cpp")],
        include_dirs=[pybind11.get_include()],
        language="c++",
    ),
]

setup(
    name="my_python_pkg",
    version="0.1",
    ext_modules=ext_modules,
    zip_safe=False,
    install_requires=['pybind11']
)