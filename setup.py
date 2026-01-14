from setuptools import setup, Extension
import pybind11

# Define the C++ extension
ext_modules = [
    Extension(
        "fast_cpp",                # The name of the module python will import
        ["src/optimized.cpp"],     # Source files
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['-std=c++17'], # Ensure modern C++ features
    ),
]

setup(
    name="my_python_pkg",
    version="0.1",
    packages=["my_python_pkg"],    # Includes your Python folder
    ext_modules=ext_modules,       # Includes your C++ extension
    zip_safe=False, install_requires=[
    'pybind11', 'pyautogui', 'numpy', 'opencv-python', 'mediapipe']
)