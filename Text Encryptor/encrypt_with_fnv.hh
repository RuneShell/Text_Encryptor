/*
* File: encrypt_with_fnv.hh
* Author: HleeJ 
*       dlhj09@naver.com
*       https://github.com/HleeJ 
* Locate: in Personal-Project 5: Text Encryptor
* 2023-04
* ----------------------------------
* Brief: Encrypt/Decrypt vector<unsigned int> using fnv1a hash function with a password provided as a string.
*/

#include <string>
#include <vector>
#include <stdint.h>

#include "unicode_info.hh"


class EncryptWithFNV1A {
private:
    /*=== fnv-1a Mask Genereator ===*/

    // FNV-1a hash function for 32-bit integers.
    uint32_t fnv1a_32(std::string key) {
        const uint32_t FNV_offset_basis = 2166136261; // fixed
        const uint32_t FNV_prime = 16777619; // fixed
        uint32_t hash_val = FNV_offset_basis;

        for (char c : key) {
            hash_val ^= static_cast<uint32_t>(c);
            hash_val *= FNV_prime; //automatically truncate to 32bits when exceeds 32bits
        }
        return hash_val;
    }

    // PCG random number generator for 32-bit integers
    class PCG {
    private:
        uint64_t state;
        const uint64_t inc = 0x14057b7ef767814fULL; // increment / not fixed, recommended
    public:
        PCG(uint32_t seed) : state(seed) {}
        uint32_t operator()() {
            uint64_t oldstate = state;
            state = oldstate * 6364136223846793005ULL + inc;
            uint32_t xorshifted = static_cast<uint32_t>(((oldstate >> 18u) ^ oldstate) >> 27u);
            uint32_t rot = static_cast<uint32_t>(oldstate >> 59u);
            return (xorshifted >> (-(int32_t)rot)) | (xorshifted << (32u + rot));
        }
    };

    // Generate pseudo-random list of integers // 160ms per 2000000 data
    std::vector<uint32_t> generate_mask(std::string key, int length) {
        /* color value 0~255 */
        const int modulo = 1000007;
        std::vector<uint32_t> result;
        int i;

        uint32_t seed = fnv1a_32(key);
        PCG rng(seed);

        rng();
        for (i = 0; i < length; i++) {
            result.push_back(rng() % modulo);
        }

        return result;
    }


    /*-----------------------------------------------------------------------------*/
    /*=== Encrypt / Decrypt Options ===*/

    /* Option 2: Encrypt/Decrypt with custom range (a~b) */ //How about access with pointer?
    static inline unsigned int Encrypt_range(unsigned int x, uint32_t n, int a, int b) {
        return (x - a + n) % (b - a + 1) + a;
    }
    static inline unsigned int Decrypt_range(unsigned int y, uint32_t n, int a, int b) {
        unsigned int c = b - a + 1;
        int t = y - a - n; //cannot use 'unsigned' (negative value)
        if (t < 0) {
            t += ((unsigned int)((c - 1 - t) / c)) * c;
        }
        return t + a;
    }


    /*------------------------------------------------------------------------------*/
public:
    /* Encrypt/Decrypt Data with options */
    bool EncryptData(std::vector<unsigned int>& data, std::string key, bool encrypt_mode) {
        unsigned int data_length = data.size();
        static unsigned int (* Task)(unsigned int, uint32_t, int a, int b) = nullptr;
        int i;

        std::vector<uint32_t> mask = generate_mask(key, data_length);

        if (encrypt_mode) {
            Task = &Encrypt_range;
        }
        else {
            Task = &Decrypt_range;
        }

        /* Do Encrypt/Decrypt */
        for (i = 0; i < data_length; i++) {
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

        return true;
    }
};


