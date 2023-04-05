# Personal Project 5: Text Encryptor
#### Warning: Security Unproved Algorithm
----------------
I don't know how much it is secure, as I'm new to Cryptography.
I made it just for fun and curiosity, combining the concepts of Caesar cipher and hash function.
Please feel free to tell me your opinion when you:
-   are knowledgeable about security (I would like to know how secure this algorithm is)
-   know this algorithm is already exists
-   find any errors or ways to improve it
-   have any other feedback
    
#### Brief
------------------
encrypt unicode string in text file using the FNV hash function with a password.
support encoding: utf-8
simplified explanation: to be added someday

#### features
---------------
- Remains language type when encrypted (currently support only Digits, Basic symbols, English, Korean)
    * Ascii Codes including number, English, basic symbols(abcd -> 3a>$)
    * Hangul Syllables (가나다 -> 왢킘뎝)
    * Hangul Compatability Jamo (ㄱㄴㄷ -> ㆌㄱㅶ)
    * other letters: ignore
- Provides options on letters to encrypt or not to encrypt (currently support only whitespace, horizontal tab) 