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

/*
        i = 0
        col = 1

        while True: // infinite loop
            
            while col <= 16:

            pixel = 1 if KBD else 0
                
                SCREEN + i = SCREEN + i OR (col * pixel)

                col += col

            i++
            col = 1

            if i >= SCREEN + (256 * 32):
                i = 0

*/

@i              
//MD=0            //  set cur pixel i = 0
M=0
(LOOP)
//@SCREEN
//A=A+D           // set A = screen + i
@KBD
D=M             // get keypress status
@KEYUP
D;JEQ
@KEYDOWN
D;JGT
(KEYUP)         // if key up
@i
D=M
@SCREEN
A=A+D
M=0
@ENDIF
0;JMP
(KEYDOWN)       // else if key down
@i
D=M
@SCREEN
A=A+D
M=!M            // set M = !M (the entire word of pixels becomes black)
@ENDIF
0;JMP
(ENDIF)
@i
M=M+1          // ++i
@LOOP           
0;JMP           // infinite loop
