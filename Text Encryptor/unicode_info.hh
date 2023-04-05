/*
* File: unicode_info.hh
* Author: HleeJ
*       dlhj09@naver.com
*       https://github.com/HleeJ
* Locate: in Personal-Project 5: Text Encryptor, included in "encrypt_with_fnv.hh"
* 2023-04
* ----------------------------------
* Brief: Unicode Code Point hex data for encrypt algorithm
*/

#pragma once
/* 
======= Unicode Letters to Encrypt ======= 
	< 1 Byte > 
U+0009 : horizontal tab (optional)
U+0020 : whitespace
U+0021~U+002F : Symbols
U+0030~U+0039 : Decimals
U+003A~U+0040 : Symbols
U+0041~U+005A : English Uppercase
U+005B~U+0060 : Symbols
U+0061~U+007A : English Lowercase
U+007B~U+007E : Symbols

	< 2 Byte >

	< 3 Byte >
U+1100~U+11FF : Hangul Jamo (unsupported)
U+3130~U+318F : Hangul Compatibility Jamo
U+AC00~U+D7A3 : Hangul Syllables


======= Unicode Letters NOT to Encrypt =======
	< 1 Byte >
U+000D : Carraige Return
U+000A : Line Feed

all other letters
*/



/* options */
#define IS_ENC_HTAB false //is encrypt horizontal tab
#define IS_ENC_SPACE true //is encrypt whitespace



/* Min/Max value of first byte of Bytes */
/*--------------------------------------*/
#define BYTE1_MIN 0x00
#define BYTE1_MAX 0x7F

#define BYTE2_MIN 0xC0
#define BYTE2_MAX 0xDF

#define BYTE3_MIN 0xE0
#define BYTE3_MAX 0xEF



/* Unicode code points to Encrypt  */
/*-----------------------------------*/
/*	< Byte 1>  */
#define HORIZONTAL_TAB 0x09
#if IS_ENC_SPACE true
#define BYTE1_START 0x20
#elif
#define BYTE1_START 0x21
#endif
#define BYTE1_END 0x7E
#define KOR_COMP_JAMO_START 0x3130
#define KOR_COMP_JAMO_END 0x318F
#define KOR_SYLL_START 0xAC00
#define KOR_SYLL_END 0xD7A3


