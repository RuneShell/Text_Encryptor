#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

//#include "C:\Users\Computer\AppData\Local\Programs\Python\Python310\Lib\site-packages\pybind11\include\pybind11\pybind11.h"
//#include "C:\Users\Computer\AppData\Local\Programs\Python\Python310\Lib\site-packages\pybind11\include\pybind11\stl.h"

#include "encrypt_with_fnv.hh"

namespace py = pybind11;

PYBIND11_MODULE(CeasorHash, m){
    m.doc() = "made by RuneShell";

    py::class_<EncryptWithFNV1A>(m, "EncryptWithFNV1A")
        .def(py::init<>())

        .def("EncryptUTF8Data", 
            [](EncryptWithFNV1A &self, std::vector<unsigned char> data, std::string key="", bool mode=true){ self.EncryptUTF8Data(data, key, mode); return data; },
            py::arg("data: std::vector<unsigned char>&"), py::arg("key: std::string")="", py::arg("encrypt_mode: bool")=1, 
            "Encrypt/Decrypt byte sequence with options(1: Encrypt, 0: Decrypt). Default key=\"\", mode=1");
        
}