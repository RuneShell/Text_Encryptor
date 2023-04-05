/*
* File: main.cpp
* Author: HleeJ
*       dlhj09@naver.com
*       https://github.com/HleeJ
* Locate: in Personal-Project 5: Text Encryptor
* 2023-04
* ----------------------------------
* Brief: Get file path, Select txt file, Get password to Encrypt & Decrypt utf-8 data
*/

//ver. C++17

#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <filesystem> /* filesystem >= C++17 */
#include <stdint.h>

#include "encrypt_with_fnv.hh"
#include "utf8unicode.hh"


//options
#define MAX_STR 250


namespace fs = std::filesystem;

int ReadFile(std::string file_name, unsigned char** data, int* datalen);


int main() {
    //to load file list
    char path_str[MAX_STR];
    int txt_count = 0;
    std::vector<fs::path> txt_list;

    //to load several file
    int encrypt_command;
    int encrypt_mode; /* 0: Encrypt, 1: Decrypt*/
    std::string selected_name;

    //file data (utf8)
    unsigned char* temp1 = { 0 };
    unsigned char** data = &temp1;
    int temp2 = 0;
    int* datalen = &temp2;

    //Encrypt/Decrypt
    EncryptWithFNV1A encryptor = EncryptWithFNV1A();

    //file data (unicode code point)
    Utf8Unicode convert = Utf8Unicode();
    std::vector<unsigned int> unicode_data;
    std::string pw;

    //encrypted data (unicode code point)
    std::vector<uint32_t> mask;
    std::string encrypted_name;
    std::string encrypted_data;



    printf(">>> TXT ENCRYPTOR <<<\n\n");
    //Load Text List
    std::cout << ">>>Enter directory path that has txt file to encrypt: ";
    std::cin.getline(path_str, MAX_STR);
    fs::path path_dir(path_str);
    std::cout << "=== TXT file list in given directory ===" << '\n';
    for (const fs::directory_entry& entry : fs::directory_iterator(path_dir)) {
        if (entry.path().extension() == ".txt") {
            txt_list.push_back(entry.path().filename());
            txt_count++;
            std::cout << txt_count << ": " << entry.path().filename().string() << '\n';
        }
    }

    //Get File Number
    std::cout << "\n>>>Enter the number of file to encrypt/decrypt : ";
    std::cin >> encrypt_command;

    if (1 <= encrypt_command && encrypt_command <= txt_count) {
        selected_name = (path_dir / txt_list[encrypt_command - 1]).string();
        ReadFile(selected_name, data, datalen);
        convert.utf8_to_unicode(*data, *datalen, unicode_data);

        //Get Encrypt Mode
        std::cout << "\n>>>Select Mode (encrypt: 0/ decrypt: 1): ";
        std::cin >> encrypt_mode;

        //Get Password
        std::cout << "\n>>>Enter Password: ";
        std::cin >> pw;

        if (encrypt_mode == 0) {//encrypt
            encryptor.EncryptData(unicode_data, pw, true);
            encrypted_name = (path_dir / txt_list[encrypt_command - 1].stem()).string() + "_encrypted.txt";
        }
        else if (encrypt_mode == 1) {//decrypt
            encryptor.EncryptData(unicode_data, pw, false);
            encrypted_name = (path_dir / txt_list[encrypt_command - 1].stem()).string() + "_decrypted.txt";
        }

        convert.unicode_to_utf8(unicode_data, encrypted_data);

        std::ofstream out(encrypted_name);
        out << encrypted_data;
        out.close();
        std::cout << "\nSaved file as: " << fs::path(encrypted_name).filename() << '\n';
    }
    else {
        std::cout << "Number Out of Range.\n";
    }

    std::cout << "\n\nSuccess.\nProgram end.\n";
    return 0;
}


int ReadFile(std::string file_name, unsigned char** data, int* datalen) {
    std::ifstream  selected_file(file_name);
    if (selected_file) {
        selected_file.seekg(0, selected_file.end);
        int length = (int)selected_file.tellg();
        selected_file.seekg(0, selected_file.beg);

        unsigned char* buffer = (unsigned char*)malloc(length+1);

        selected_file.read((char*)buffer, length);
        selected_file.close();
        
        //correct file length when exceeds REAL length (temp) //maybe this problem(https://stackoverflow.com/questions/22984956/tellg-function-give-wrong-size-of-file)
        for (int i = length - 1; i >= 0; i--) {
            if (buffer[i] == 0xcd) length--;
            else break;
        }

        *data = buffer;
        *datalen = length;
    }
    return 0;
}