#include <iostream>
#include <fstream>
#include <math.h>

#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
#include <boost/python/def.hpp>
#include <boost/python/module.hpp>
#include <Python.h>

using namespace boost::python;
namespace np = boost::python::numpy;


class AFMWave
{
public:
    float pi = M_PI;

    AFMWave(float carrier_frequency, float amplitude, int buffer_size)
    {
        this->carrier_frequency = carrier_frequency;
        this->amplitude = amplitude;
        this->buffer_size = buffer_size;
    }
    /// Setter methods
    void setCarrierFrequency(float frequency) {this->carrier_frequency = frequency;}
    void setAmplitude(float amplitude) {this->amplitude = amplitude;}
    void setAMFrequency(float frequency) {this->am_frequency = frequency;}
    void setFMFrequency(float frequency) {this->fm_frequency = frequency;}
    void setAMDepth(float depth) {this->am_depth = depth;}
    void setFMDepth(float depth) {this->fm_depth = depth;}
    void setFS(float fs) {this->fs = fs;}
    void setBufferSize(int buffer_size) {this->buffer_size = buffer_size;}
    /// Getter methods
    float getCarrierFrequency() {return this->carrier_frequency;}
    float getAmplitude() {return this->amplitude;}
    float getAMFrequency() {return this->am_frequency;}
    float getFMFrequency() {return this->fm_frequency;}
    float getAMDepth() {return this->am_depth;}
    float getFMDepth() {return this->fm_depth;}
    float getFS() {return this->fs;}
    int getBufferSize() {return this->buffer_size;}
    /// Utilities methods
    np::ndarray getAMWave()
    {
        /// This method creates an AM wave according to the parameters
        /// and stores it into the wave numpy ndarray

        boost::python::tuple shape = boost::python::make_tuple(buffer_size, 1);
        np::dtype dtype = np::dtype::get_builtin<float>();

        np::ndarray wave = np::zeros(shape, dtype);
        float s;

        for(int i = 0; i < buffer_size; i++) // calculates the AM wave's value and stores it into wave
        {
            s = amplitude * (1 + am_depth * sin(2 * pi * am_frequency / fs * i));
            float aux = 2 * pi * carrier_frequency / fs * i;
            s = s * sin(aux);
            aux = 1 + pow(am_depth, 2) / 2;
            aux = sqrt(aux);
            s /= aux;
            wave[i] = s;
        }
        return wave;
    }

    np::ndarray getFMWave()
    {
        /// This method creates an FM wave according to the parameters
        /// and stores it into the wave numpy ndarray

        boost::python::tuple shape = boost::python::make_tuple(buffer_size, 1);
        np::dtype dtype = np::dtype::get_builtin<float>();

        np::ndarray wave = np::zeros(shape, dtype);
        float s;

        for(int i = 0; i < buffer_size; i++) // calculates the AM wave's value and stores it into wave
        {
            float aux = 2 * pi * carrier_frequency / fs * i;
            aux += (fm_depth * carrier_frequency) / (2 * fm_frequency) * sin(2 * pi * fm_frequency / fs * i);
            s = amplitude * sin(aux);
            wave[i] = s;
        }
        return wave;
    }

    np::ndarray getAFMWave()
    {
        /// This method creates an AM combined with an FM wave according to the parameters
        /// and stores it into the wave numpy ndarray

        boost::python::tuple shape = boost::python::make_tuple(buffer_size, 1);
        np::dtype dtype = np::dtype::get_builtin<float>();

        np::ndarray wave = np::zeros(shape, dtype);
        float s;

        for(int i = 0; i < buffer_size; i++) // calculates the AM wave's value and stores it into wave
        {
            s = amplitude * (1 + am_depth * sin(2 * pi * am_frequency / fs * i));
            float aux = 2 * pi * carrier_frequency / fs * i;
            aux += (fm_depth * carrier_frequency) / (2 * fm_frequency) * sin(2 * pi * fm_frequency / fs * i);
            s *= sin(aux);
            aux = 1 + pow(am_depth, 2) / 2;
            aux = sqrt(aux);
            s /= aux;

            wave[i] = s;
        }
        return wave;
    }

private:
    float carrier_frequency;
    float amplitude;
    float am_frequency;
    float fm_frequency;
    float am_depth;
    float fm_depth;
    float fs;
    int buffer_size;
};

/// Python wraper
BOOST_PYTHON_MODULE(PyAFM)
{
    Py_Initialize();
    np::initialize();

    class_<AFMWave>("AFMWave", init<float, float, int>())
        .def("setCarrierFrequency", &AFMWave::setCarrierFrequency, arg("frequency"))
        .def("setAmplitude", &AFMWave::setAmplitude, arg("amplitude"))
        .def("setAMFrequency", &AFMWave::setAMFrequency, arg("frequency"))
        .def("setFMFrequency", &AFMWave::setFMFrequency, arg("frequency"))
        .def("setAMDepth", &AFMWave::setAMDepth, arg("depth"))
        .def("setFMDepth", &AFMWave::setFMDepth, arg("depth"))
        .def("setFS", &AFMWave::setFS, arg("fs"))
        .def("setBufferSize", &AFMWave::setBufferSize, arg("buffer_size"))
        .def("getCarrierFrequency", &AFMWave::getCarrierFrequency)
        .def("getAmplitude", &AFMWave::getAmplitude)
        .def("getAMFrequency", &AFMWave::getAMFrequency)
        .def("getFMFrequency", &AFMWave::getFMFrequency)
        .def("getAMDepth", &AFMWave::getAMDepth)
        .def("getFMDepth", &AFMWave::getFMDepth)
        .def("getFS", &AFMWave::getFS)
        .def("getBufferSize", &AFMWave::getBufferSize)
        .def("getAMWave", &AFMWave::getAMWave)
        .def("getFMWave", &AFMWave::getFMWave)
        .def("getAFMWave", &AFMWave::getAFMWave);
}
