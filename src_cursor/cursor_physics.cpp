#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // Include this if you want to use std::vector -> python list

namespace py = pybind11;

// 1. A heavy function you want to speed up
double heavy_computation(int n) {
    double result = 0;
    for (int i = 0; i < n; i++) {
        result += i * 0.5; // Simulate work
    }
    return result;
}

// 2. Define the module
PYBIND11_MODULE(fast_cpp, m) {
    m.doc() = "Optimized C++ routines for my project";
    m.def("heavy_computation", &heavy_computation, "A function that runs fast");
}