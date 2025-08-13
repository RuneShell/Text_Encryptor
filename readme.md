

# Personal Project 5: Text Encryptor
<strong> Warning: Experimental Algorithm</strong>

I made it just for fun and curiosity, combining the concepts of Caesar cipher, hash function and a few of cryptography.

    
## Brief
Encrypt string using the confused WaterHash sequences with a password.
Support encoding: utf-8, unicode code points

Blueprint:
![blueprint.jpg]()

## Features
- Preserves character type after encrpytion. (currently support only Digits, Basic symbols, English, Korean)
    * Ascii Codes including number, English, basic symbols(abcd -> x%V8)
    * Hangul Syllables (가나다 -> 듌빾켰)
    * Hangul Compatability Jamo (ㄱㄴㄷ -> ㅩㅪㅗ)
    * other letters: ignored
- Maintains original string length after encryption.
	* You can encrypt multiple times for increased obfuscation.
- Provides options to selectively encrypt certain characters. (currently supports only whitespace, horizontal tab) 

## Samples
Default GUI
![sample_1_default.gif]()

Encrypt
![sample_2_encrypt.gif]()

Decrypt
![smaple_3_decrypt.gif]()

