#include <pybind11/pybind11.h>
#include <cmath>

namespace py = pybind11;

class CursorPhysics {
public:
    CursorPhysics(
        double force_scale = 300.0,
        double damping = 0.85,
        double max_speed = 4000.0
    )
        : force_scale(force_scale),
          damping(damping),
          max_speed(max_speed),
          pos_x(0), pos_y(0),
          vel_x(0), vel_y(0),
          initialized(false) {}

    py::tuple update(double dx, double dy, double dt) {
        if (!initialized) {
            initialized = true;
            return py::make_tuple(pos_x, pos_y);
        }

        // Treat finger movement as force
        double ax = dx * force_scale;
        double ay = dy * force_scale;

        // Euler integration
        vel_x += ax * dt;
        vel_y += ay * dt;

        // Damping
        vel_x *= damping;
        vel_y *= damping;

        // Clamp velocity
        double speed = std::sqrt(vel_x * vel_x + vel_y * vel_y);
        if (speed > max_speed) {
            vel_x = (vel_x / speed) * max_speed;
            vel_y = (vel_y / speed) * max_speed;
        }

        // Integrate position
        pos_x += vel_x * dt;
        pos_y += vel_y * dt;

        return py::make_tuple(pos_x, pos_y);
    }

    void reset(double x, double y) {
        pos_x = x;
        pos_y = y;
        vel_x = vel_y = 0.0;
        initialized = true;
    }

private:
    double force_scale;
    double damping;
    double max_speed;

    double pos_x, pos_y;
    double vel_x, vel_y;
    bool initialized;
};

PYBIND11_MODULE(cursor_cpp, m) {
    py::class_<CursorPhysics>(m, "CursorPhysics")
        .def(py::init<double, double, double>(),
             py::arg("force_scale") = 300.0,
             py::arg("damping") = 0.85,
             py::arg("max_speed") = 4000.0)
        .def("update", &CursorPhysics::update)
        .def("reset", &CursorPhysics::reset);
}
