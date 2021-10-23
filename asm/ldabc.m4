; Example of using m4 as an Assembly macro processor: main program


; On Linux assemble with:
;
;   cat ldabc.m4 | m4 | asm80 - -o ldabc.com
;
; To view the Assembly source generated by m4:
;
;   cat ldabc.m4 | m4

            include(`ldabcmac.m4')      ; Include macro definition file

            ldabc(data1, data2, data3)  ; Call macro

data1:      db      1
data2:      db      2
data3:      db      3