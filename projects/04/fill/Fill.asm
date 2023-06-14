// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// Screen: 256 rows, 512 pixels/row
// Starts at RAM address 16384 (symbol SCREEN)
// Each row is 32 consecutive 16-bit words.
// Pixel at row `r` from top and column `c` from left is at c%16 bit (from LSB to MSB) of the word at
// RAM[16384 + r*32 + c/16]
// 1 = black; 0 = white
// KBD @ 24576
//
//        i = 0
//        col = 1
//
//        while True: // infinite loop
//            
//            while col <= 16:
//
//            pixel = 1 if KBD else 0
//                
//                SCREEN + i = SCREEN + i OR (col * pixel)
//
//                col += col
//
//            i++
//            col = 1
//
//            if i >= SCREEN + (256 * 32):
//                i = 0
//

(RESET)             // Jump here every time I need to reinitialize `i`
@SCREEN
D=A
@i
M=D                 // initialize `i` to first screen address

(MAINLOOP)

@bitsplace          // variable to increment from 1, 2, 4, 8, 16, 32, 1 ...
M=1                 // set bitsplace=1
@j                  // variable to increment through 16-bits of word
M=0                 // set j=0

(WORDLOOP)

@KBD                // get keyboard status and jump
D=M                 
@ISKEYUP
D;JEQ
@ISKEYDOWN
D;JGT

(ISKEYUP)           // if key is up
@bitsplace
D=!M                // negate `bitsplace`...
@i
A=M
M=M&D               // ... and AND it with current value @i
@ENDIF
0;JMP

(ISKEYDOWN)         // if key is pressed
@bitsplace
D=M
@i
A=M
M=M|D               // OR `bitsplace` with current value @i
@ENDIF
0;JMP
(ENDIF)

@bitsplace
D=M
@bitsplace          // double `bitsplace
MD=D+M
@j
MD=M+1              // increment `j`
@16
D=D-A               // D = `j` - 16
@WORDLOOP
D;JLT               // while `j` - 16 < 0, keep looping through word at @i

@i
MD=M+1              // increment `i` for subsequent screen address 

@24575              // if i - 24575 > 0, then we've exceeded screen addresses; 
D=D-A
@RESET
D;JGT

@MAINLOOP           
0;JMP               // infinite loop
