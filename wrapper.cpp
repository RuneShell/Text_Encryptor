#include <cstdint>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

//#include "C:\Users\Computer\AppData\Local\Programs\Python\Python310\Lib\site-packages\pybind11\include\pybind11\pybind11.h"
//#include "C:\Users\Computer\AppData\Local\Programs\Python\Python310\Lib\site-packages\pybind11\include\pybind11\stl.h"

#include "CeasorHash.cpp"

namespace py = pybind11;

PYBIND11_MODULE(CeasorHash, m){
    m.doc() = "made by RuneShell";

    py::class_<CeasorHash>(m, "CeasorHash")
        .def(py::init<>())

        .def("EncryptWithCeasorHash", 
            // Python: list(int) -> Cpp: std::vector<uint32_t>
            [](CeasorHash &self, std::vector<uint32_t> data, std::vector<uint32_t> key={}, const bool mode=true, const int dataType=1){ 
                self.EncryptWithCeasorHash(data, key, mode, dataType); return data; },
                py::arg("data: std::vector<uint32_t>&"), 
                py::arg("key: std::vector<uint32_t>")="", 
                py::arg("encrypt_mode: const bool")=true, 
                py::arg("data_type: const int")=1,
                "Encrypt/Decrypt byte sequence with options:\n \
                mode: (True: Encrypt, False: Decrypt)\n \
                dataType: (1: UTF-8, 2: Unicode Point) (both 'data' and 'key')\n"
        );
        
}