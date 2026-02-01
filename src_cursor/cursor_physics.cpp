#include <pybind11/pybind11.h>
#include <cmath>
#include <algorithm>

namespace py = pybind11;

class CursorPhysics {
public:
    CursorPhysics(
        double force_scale,
        double damping,
        double max_speed,
        double min_speed,
        double sensitivity_exponent = 1.0,
        double reference_magnitude = 0.01
    )
        : force_scale(force_scale),
          damping(damping),
          max_speed(max_speed),
          min_speed(min_speed),
          sensitivity_exponent(sensitivity_exponent),
          reference_magnitude(reference_magnitude),
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


        // ---- Input shaping (non-linear sensitivity curve) ----
        double mag = std::sqrt(dx * dx + dy * dy);

        if (mag > 1e-9) {
            // Pivoted power curve around reference_magnitude
            double scaled_mag = reference_magnitude *
                std::pow(mag / reference_magnitude, sensitivity_exponent);

            double scale = scaled_mag / mag;

            // Optional safety clamp
            scale = std::min(scale, 5.0);

            dx *= scale;
            dy *= scale;
        }

        mag = std::sqrt(dx * dx + dy * dy);

        if (mag < 0.002) {
            return py::make_tuple(pos_x, pos_y);
        }



        double ax = dx * force_scale;
        double ay = dy * force_scale;

        //euler
        vel_x += ax * dt;
        vel_y += ay * dt;

        vel_x *= damping;
        vel_y *= damping;

        // Clamp to max speed
        double speed = std::sqrt(vel_x * vel_x + vel_y * vel_y);
        if (speed > max_speed) {
            vel_x = (vel_x / speed) * max_speed;
            vel_y = (vel_y / speed) * max_speed;
        }

        if (speed < min_speed) {
            vel_x = vel_y = 0.0;
            return py::make_tuple(pos_x, pos_y);
        }


        // Update position
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
    double min_speed;
    double sensitivity_exponent;
    double reference_magnitude;

    double pos_x, pos_y;
    double vel_x, vel_y;
    bool clutched;
    bool input_active;
    bool initialized;
};

PYBIND11_MODULE(cursor_cpp, m) {
    py::class_<CursorPhysics>(m, "CursorPhysics")
        .def(py::init<double, double, double, double, double>(),
             py::arg("force_scale") = 300.0,
             py::arg("damping") = 0.85,
             py::arg("max_speed") = 4000.0,
             py::arg("min_speed") = 150.0,
             py::arg("sensitivity_exponent") = 1.6,
             py::arg("reference_magnitude") = 0.012)
        .def("update", &CursorPhysics::update)
        .def("clutch", &CursorPhysics::clutch)
        .def("unclutch", &CursorPhysics::unclutch)
        .def("reset", &CursorPhysics::reset);
}
