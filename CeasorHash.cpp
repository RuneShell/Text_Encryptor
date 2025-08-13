#include <iostream>
#include <chrono>

#include <vector>
#include <string>
#include <cstdint>
#include <algorithm>
#include <functional>
#include <stdexcept>

#include "utf8unicode_.hh"
#include "unicode_info.hh"

/*
# Python 바인딩일 때만 정의
pybind11_add_module(mymodule src/mymodule.cpp)
target_compile_definitions(mymodule PRIVATE BUILDING_PYTHON_MODULE)
*/
#ifdef BUILDING_PYTHON_MODULE
#define BUILD_ENVIRONMENT 1
#else
#define BUILD_ENVIRONMENT 0
#endif

#define dataN uint32_t
#define maskN uint32_t
#define rangeN uint32_t


class WaterHash{
    const uint64_t seed = 0xdab89f1c5e236771ULL; // A random number

    /*
    Waterhash takes (optimally) 32-bit inputs and produces a 32-bit hash as its result.
    It is an edited version of wyhash that uses at most 64-bit math instead of 128-bit.
    It is meant to use very similar code to Wheathash, which produces a 64-bit hash.
    Original Author: Wang Yi <godspeed_china@yeah.net>
    Waterhash Variant Author: Tommy Ettinger <tommy.ettinger@gmail.com>
    */
    const uint64_t _waterp0 = 0xa0761d65ull, _waterp1 = 0xe7037ed1ull, _waterp2 = 0x8ebc6af1ull;
    const uint64_t _waterp3 = 0x589965cdull, _waterp4 = 0x1d8e4e27ull, _waterp5 = 0xeb44accbull;

    uint64_t _watermum(const uint64_t A, const uint64_t B) {
        uint64_t r = A * B;
        return r - (r >> 32);
    }

    uint64_t _waterr08(const uint8_t *p){ uint8_t  v; memcpy(&v, p, 1); return v; }
    uint64_t _waterr16(const uint8_t *p){ uint16_t v; memcpy(&v, p, 2); return v; }
    uint64_t _waterr32(const uint8_t *p){ uint32_t v; memcpy(&v, p, 4); return v; }
    uint32_t waterhash(const void* key, uint32_t len, uint64_t seed){
        const uint8_t *p = (const uint8_t*)key;
        uint32_t i;
        for (i = 0; i + 16 <= len; i += 16, p += 16) {
            seed = _watermum(
                _watermum(_waterr32(p) ^ _waterp1, _waterr32(p + 4) ^ _waterp2) + seed,
                _watermum(_waterr32(p + 8) ^ _waterp3, _waterr32(p + 12) ^ _waterp4));
        }
        seed += _waterp5;
        switch (len & 15) {
        case 1:  seed = _watermum(_waterp2 ^ seed, _waterr08(p) ^ _waterp1); break;
        case 2:  seed = _watermum(_waterp3 ^ seed, _waterr16(p) ^ _waterp4); break;
        case 3:  seed = _watermum(_waterr16(p) ^ seed, _waterr08(p + 2) ^ _waterp2); break;
        case 4:  seed = _watermum(_waterr16(p) ^ seed, _waterr16(p + 2) ^ _waterp3); break;
        case 5:  seed = _watermum(_waterr32(p) ^ seed, _waterr08(p + 4) ^ _waterp1); break;
        case 6:  seed = _watermum(_waterr32(p) ^ seed, _waterr16(p + 4) ^ _waterp1); break;
        case 7:  seed = _watermum(_waterr32(p) ^ seed, (_waterr16(p + 4) << 8 | _waterr08(p + 6)) ^ _waterp1); break;
        case 8:  seed = _watermum(_waterr32(p) ^ seed, _waterr32(p + 4) ^ _waterp0); break;
        case 9:  seed = _watermum(_waterr32(p) ^ seed, _waterr32(p + 4) ^ _waterp2) ^ _watermum(seed ^ _waterp4, _waterr08(p + 8) ^ _waterp3); break;
        case 10: seed = _watermum(_waterr32(p) ^ seed, _waterr32(p + 4) ^ _waterp2) ^ _watermum(seed, _waterr16(p + 8) ^ _waterp3); break;
        case 11: seed = _watermum(_waterr32(p) ^ seed, _waterr32(p + 4) ^ _waterp2) ^ _watermum(seed, ((_waterr16(p + 8) << 8) | _waterr08(p + 10)) ^ _waterp3); break;
        case 12: seed = _watermum(_waterr32(p) ^ seed, _waterr32(p + 4) ^ _waterp2) ^ _watermum(seed ^ _waterr32(p + 8), _waterp4); break;
        case 13: seed = _watermum(_waterr32(p) ^ seed, _waterr32(p + 4) ^ _waterp2) ^ _watermum(seed ^ _waterr32(p + 8), (_waterr08(p + 12)) ^ _waterp4); break;
        case 14: seed = _watermum(_waterr32(p) ^ seed, _waterr32(p + 4) ^ _waterp2) ^ _watermum(seed ^ _waterr32(p + 8), (_waterr16(p + 12)) ^ _waterp4); break;
        case 15: seed = _watermum(_waterr32(p) ^ seed, _waterr32(p + 4) ^ _waterp2) ^ _watermum(seed ^ _waterr32(p + 8), (_waterr16(p + 12) << 8 | _waterr08(p + 14)) ^ _waterp4); break;
        }
        seed = (seed ^ seed << 16) * (len ^ _waterp0);
        return (uint32_t)(seed - (seed >> 32));
    }
    // waterHash code end.



public:
    std::vector<uint32_t> GetHashSeq(const dataN* keyI, const int keySize, const int maskSize){
        std::vector<uint32_t> mask(maskSize, 0);

        int counter = 0;
        for(int i = 0; i < maskSize; i++){
            mask[i] = waterhash(keyI, keySize, seed ^ (counter+i));
        }

        return mask;
    }
};



class CeasorHash{
private:
    // [Lambda Methods] (inline)
    std::function<void(dataN&, dataN&, dataN&, dataN&)> quarter_round = [](dataN& a, dataN& b, dataN& c, dataN& d){ // Fiestel-like round 
        a += b; d ^= a; d = (d << 16) | (d >> 16); // uint32_t -> overflow: positive
        c += d; b ^= c; b = (b << 12) | (b >> 20);
        a += b; d ^= a; d = (d << 8) | (d >> 24);
        c += d; b ^= c; b = (b << 7) | (b >> 25);
    };
    
    std::function<uint32_t(std::vector<dataN>::const_iterator, std::vector<dataN>::const_iterator)> GetXOR = \
    [](std::vector<dataN>::const_iterator vb, std::vector<dataN>::const_iterator ve){
        uint32_t GETXOR_IV = 0b101010000001100001001001011101; // Initialization Vector (random int)
        for(; vb != ve; vb++){
            GETXOR_IV ^= *vb;
        }
        return GETXOR_IV;
    };

    std::function<dataN(dataN, maskN, rangeN, rangeN)> EncryptRange = [](dataN x, maskN n, rangeN a, rangeN b){ return (x - a + n) % (b - a + 1) + a; };
    std::function<dataN(dataN, maskN, rangeN, rangeN)> DecryptRange = [](dataN y, maskN n, rangeN a, rangeN b){
        uint32_t range = b + 1 - a; // [a, b] -> [a, b+1) range
        int32_t t = y - a - (n % range); // negative -> 'signed' int
        if(t < 0) t += range;
        return a + t;
    };


    // [Sub Methods]
    void CeasorHashRound(std::vector<maskN>::iterator partialMask, const int shuffle1Count, const int shuffle2Count, const int shuffle3Count, const int shuffle4Count){
        for(int i = 0; i < shuffle1Count; i++){ // shuffle 1 (vertical)
            quarter_round(partialMask[0], partialMask[4], partialMask[8], partialMask[12]);
            quarter_round(partialMask[1], partialMask[5], partialMask[9], partialMask[13]);
            quarter_round(partialMask[2], partialMask[6], partialMask[10], partialMask[14]);
            quarter_round(partialMask[3], partialMask[7], partialMask[11], partialMask[15]);
        }
        for(int i = 0; i < shuffle2Count; i++){ // shuffle 2 (left-up diagonal)
            quarter_round(partialMask[0], partialMask[5], partialMask[10], partialMask[15]);
            quarter_round(partialMask[4], partialMask[9], partialMask[14], partialMask[3]);
            quarter_round(partialMask[8], partialMask[13], partialMask[2], partialMask[7]);
            quarter_round(partialMask[12], partialMask[1], partialMask[6], partialMask[11]);
        }
        for(int i = 0; i < shuffle3Count; i++){ // shuffle 3 (right-up diagonal)
            quarter_round(partialMask[12], partialMask[9], partialMask[6], partialMask[3]);
            quarter_round(partialMask[13], partialMask[10], partialMask[7], partialMask[0]);
            quarter_round(partialMask[14], partialMask[11], partialMask[4], partialMask[1]);
            quarter_round(partialMask[15], partialMask[8], partialMask[5], partialMask[2]);
        }
        for(int i = 0; i < shuffle4Count; i++){ // shuffle 4 (horizontal)
            quarter_round(partialMask[0], partialMask[1], partialMask[2], partialMask[3]);
            quarter_round(partialMask[4], partialMask[5], partialMask[6], partialMask[7]);
            quarter_round(partialMask[8], partialMask[9], partialMask[10], partialMask[11]);
            quarter_round(partialMask[12], partialMask[13], partialMask[14], partialMask[15]);
        }
        //special shuffle needed
    }


    // [Core Methods]
    // 1. Generate Mask
    //std::vector<maskN> GenerateMask(const std::vector<dataN>& data, const std::vector<dataN>::iterator& keyBegin, const std::vector<dataN>::iterator& keyEnd, int maskSize){
    // If first parameter 'data' effect on mask, cannot find the same pattern in encrypted text. => disabled
    std::vector<maskN> GenerateMask(const std::vector<dataN>::iterator& keyBegin, const std::vector<dataN>::iterator& keyEnd, int maskSize){
        maskSize += (16 - maskSize%16) % 16; // For round system, maskSize must devided into 16.

        uint32_t keyXOR = GetXOR(keyBegin, keyEnd); // Get XOR with key
        WaterHash waterHash{};
        std::vector<maskN> mask = waterHash.GetHashSeq(&(*keyBegin), std::distance(keyBegin, keyEnd), maskSize); // generate wyHash sequence with key

        std::for_each(mask.begin(), mask.end(), [keyXOR](maskN& m){return m ^= keyXOR;}); // apply mask element-wise XOR with keyXOR

        uint32_t dataXOR;
        std::vector<maskN>::iterator partialMaskbegin = mask.begin(); // !!! NOT using [data], data is different when enc and dec => mask only depend on password. => mask can be predictable
        
        for(int i = 0; i < maskSize/16; i++){ // Feistel-like shuffle
            dataXOR = GetXOR(partialMaskbegin, partialMaskbegin+16);
            CeasorHashRound(partialMaskbegin, ((dataXOR>>6) & 0b11) + 5, ((dataXOR>>4) & 0b11) + 5, (dataXOR>>2) & 0b11, dataXOR & 0b11);
            partialMaskbegin += 16;
        }

        return mask;
    }

    // 2. Modulus Diffused data
    void ModulusData(std::vector<uint32_t>& data, const std::vector<uint32_t>& mask, const int encMode){
        int data_size = data.size();

        std::function<dataN(dataN, maskN, rangeN, rangeN)> Task;
        Task = encMode ? EncryptRange : DecryptRange;

        /* Do Encrypt/Decrypt */
        for (int i = 0; i < data_size; i++) {
            /* Byte 1 data */
            if (IS_ENC_HTAB && ((BYTE1_START <= data[i] && data[i] <= BYTE1_END) || data[i] == HORIZONTAL_TAB)) {
                if (data[i] == HORIZONTAL_TAB) data[i] = BYTE1_START - 1;
                data[i] = Task(data[i], mask[i], BYTE1_START - 1, BYTE1_END); //-1: horizontal tab
                if (data[i] == BYTE1_START - 1) data[i] = HORIZONTAL_TAB;
            }
            else if ((!IS_ENC_HTAB) && (BYTE1_START <= data[i] && data[i] <= BYTE1_END)) {
                data[i] = Task(data[i], mask[i], BYTE1_START, BYTE1_END);
            }
            /* Byte 2 data */
            //there is no letter to encrypt in Byte 2
            /* Byte 3 data */
            else if (KOR_COMP_JAMO_START <= data[i] && data[i] <= KOR_COMP_JAMO_END) { // U+12,592~12,687
                data[i] = Task(data[i], mask[i], KOR_COMP_JAMO_START, KOR_COMP_JAMO_END);
            }
            else if (KOR_SYLL_START <= data[i] && data[i] <= KOR_SYLL_END) {
                data[i] = Task(data[i], mask[i], KOR_SYLL_START, KOR_SYLL_END);
            }
        }

    }




    void MyErrorThrower(const std::string& s){
        //if(BUILD_ENVIRONMENT == 1) {}
        throw std::runtime_error(s);
    }



public:
    // Default Constructor

    /* EncryptWithCeasorHash(list UTF-8/Unicode data, password="", encrypt mode=1, data type=1) -> void (reference: encrypted/decryted data)
    * encMode - 1: encrypt, 0: decrypt / dataType - 1: UTF-8 data, 2: Unicode data
    * Input Adaptor Function
    */
    void EncryptWithCeasorHash(std::vector<dataN>& data, std::vector<dataN> key={}, const bool encMode=true, const int dataType=1){
        // Check data Type UTF-8/Unicode
        if(dataType == 1){ // UTF-8 -> unicode // UTF-8 is 0~255, Unicode is 0~1,114,111 
            // Convert Data
            std::vector<dataN> tempV;
            Utf8Unicode converter{};
            bool result = converter.utf8_to_unicode(data, tempV);
            if(!result) MyErrorThrower("invalid/not a UTF-8 string data");
            data = std::move(tempV);

            // Convert Key
            tempV.clear();
            result = converter.utf8_to_unicode(key, tempV);
            if(!result) MyErrorThrower("invalid/not a UTF-8 string key");
            key = std::move(tempV);
        }
        else if(dataType > 2){
            MyErrorThrower("argument dataType out of range");
            return;
        }


        // add something to key that retains in plaintext.
        // 1. Plaintext Size
        key.push_back(data.size());
        // 2. Plaintext Unicode Domain Pattern(to complete this, I should change entire structure, so later...)
        //...
        

        // Devide Key 'sentence' into words.
        std::vector<dataN>::iterator keyBegin = key.begin();
        std::vector<dataN>::iterator keyEnd = std::find(keyBegin, key.end(), 0x20);  // 0x20: whitespace in ASCII code
        std::vector<maskN> mask = GenerateMask(keyBegin, keyEnd, data.size());
        if(keyEnd != key.end()) keyBegin = keyEnd + 1;

        while(true){
            keyEnd = std::find(keyBegin, key.end(), 0x20);
            if(keyEnd == key.end()) break;

            std::vector<maskN> tempMask = GenerateMask(keyBegin, keyEnd, data.size());
            if(GetXOR(keyBegin, keyEnd) & 1){ // ADD to mask
                std::transform(mask.begin(), mask.end(), tempMask.begin(), mask.begin(), [](const int& a, const int& b){return a+b;});
            }
            else{ // XOR to mask
                std::transform(mask.begin(), mask.end(), tempMask.begin(), mask.begin(), [](const int& a, const int& b){return a^b;});
            }
            keyBegin = keyEnd + 1;
        }

        
        // unicode
        ModulusData(data, mask, encMode);


        // Return dataType unicode -> utf-8
        if(dataType == 1){
            std::vector<unsigned int> tempV;
            Utf8Unicode converter{};
            converter.unicode_to_utf8(data, tempV);
            data = std::move(tempV);
        }
    }

};

/* For test
int main() {
    std::vector<dataN> data = { 97, 115, 99 };
    std::vector<dataN> pw = { 112, 119 };
    CeasorHash c{};

    c.EncryptWithCeasorHash(data, pw, 1, 1);
    for(const auto e: data) std::cout << e << ' ';
    std::cout << '\n';

    c.EncryptWithCeasorHash(data, pw, 0, 1);
    for (const auto e : data) std::cout << e << ' ';
    std::cout << '\n';
}
*/