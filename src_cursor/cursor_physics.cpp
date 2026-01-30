#include <pybind11/pybind11.h>
#include <cmath>

namespace py = pybind11;

class CursorPhysics {
public:
    CursorPhysics(
        double force_scale,
        double damping,
        double max_speed
    )
        : force_scale(force_scale),
          damping(damping),
          max_speed(max_speed),
          pos_x(0), pos_y(0),
          vel_x(0), vel_y(0),
          clutched(false),
          input_active(false),
          initialized(false) {}

    py::tuple update(double dx, double dy, double dt) {
        if (!initialized) {
            return py::make_tuple(pos_x, pos_y);
        }

        if (clutched) {
            return py::make_tuple(pos_x, pos_y);
        }

        if (!input_active) {
            input_active = true;
            vel_x = vel_y = 0.0;
            return py::make_tuple(pos_x, pos_y);
        }


        double ax = dx * force_scale;
        double ay = dy * force_scale;

        vel_x += ax * dt;
        vel_y += ay * dt;

        vel_x *= damping;
        vel_y *= damping;

        double speed = std::sqrt(vel_x * vel_x + vel_y * vel_y);
        if (speed > max_speed) {
            vel_x = (vel_x / speed) * max_speed;
            vel_y = (vel_y / speed) * max_speed;
        }

        pos_x += vel_x * dt;
        pos_y += vel_y * dt;

        return py::make_tuple(pos_x, pos_y);
    }

    void clutch() {
        clutched = true;
        vel_x = vel_y = 0.0;
    }

    void unclutch() {
        clutched = false;
        input_active = false;
    }


    void reset(double x, double y) {
        pos_x = x;
        pos_y = y;
        vel_x = vel_y = 0.0;
        input_active = false;
        initialized = true;
    }



private:
    double force_scale;
    double damping;
    double max_speed;

    double pos_x, pos_y;
    double vel_x, vel_y;
    bool clutched;
    bool input_active;
    bool initialized;
};

PYBIND11_MODULE(cursor_cpp, m) {
    py::class_<CursorPhysics>(m, "CursorPhysics")
        .def(py::init<double, double, double>(),
             py::arg("force_scale") = 300.0,
             py::arg("damping") = 0.85,
             py::arg("max_speed") = 4000.0)
        .def("update", &CursorPhysics::update)
        .def("clutch", &CursorPhysics::clutch)
        .def("unclutch", &CursorPhysics::unclutch)
        .def("reset", &CursorPhysics::reset);
}
