.data
    time: .word 0x3F9409
    tmps: .word 0,1, 2,3
    LED0: .word 0x00000000,0x00800001,0x00C00003,0x00E00007,0x00F0000F,0x00F8001F,0x00FC003F,0x00FE007F,0x00FF00FF,0x00FF81FF,0x00FFC3FF,0x00FFE7FF,0xFFFFFF,0x00FFE7FF,0x00FFC3FF,0x00FF81FF,0x00FF00FF,0x00FE007F,0x00FC003F,0x00F8001F,0x00F0000F,0x00E00007,0x00C00003,0x00800001 #两边到中间
    LED1: .word 0xFFFFFF,0x00FFE7FF,0x00FFC3FF,0x00FF81FF,0x00FF00FF,0x00FE007F,0x00FC003F,0x00F8001F,0x00F0000F,0x00E00007,0x00C00003,0x00800001,0x00000000,0xFFFFFF,0x00FFE7FF,0x00FFC3FF,0x00FF81FF,0x00FF00FF,0x00FE007F,0x00FC003F,0x00F8001F,0x00F0000F,0x00E00007,0x00C00003,0x00800001,0x00000000 #中间到两边
    light_high_2: .word 0x0000,0x0000,0x0080,0x00A0,0x00A8,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00AA,0x00A8,0x00A0,0x0080,0x0000,0x0000 # jzl2
    light_low_2:  .word 0x0000,0x0000,0x0001,0x0005,0x0015,0x0055,0x0155,0x0555,0x1555,0x5555,0x7D55,0xFF55,0xFF55,0xFFFF,0xFF55,0xFF55,0x7D55,0x5555,0x1555,0x0555,0x0155,0x0055,0x0015,0x0005,0x0001,0x0000,0x0000 # jzl2
    light_high_3: .word 0x0000,0x0000,0x0000,0x0040,0x0050,0x0054,0x0055,0x0055,0x0055,0x0055,0x0055,0x0055,0x0055,0x0055,0x0055,0x0055,0x0055,0x0055,0x0055,0x0055,0x0055,0x0055,0x0054,0x0050,0x0040,0x0000,0x0000 # jzl3
    light_low_3:  .word 0x0000,0x0000,0x0000,0x0002,0x000A,0x002A,0x00AA,0x02AA,0x0AAA,0x2AAA,0xAAAA,0xEAAA,0xFAAA,0xFAAA,0xFAAA,0xFAAA,0xEAAA,0xAAAA,0x2AAA,0x0AAA,0x02AA,0x00AA,0x002A,0x000A,0x0020,0x0000,0x0000 # jzl3
    LED4: .word 0xFFFFFF,0x00FFC3FF,0x00FF00FF,0x00FC003F,0x00F0000F,0x00C00003,0x00000000,0x00FFE7FF,0x00FF81FF,0x00FE007F,0x00F8001F,0x00E00007,0x00800001, 0xFFFFFF,0x00FFC3FF,0x00FF00FF,0x00FC003F,0x00F0000F,0x00C00003,0x00000000,0x00FFE7FF,0x00FF81FF,0x00FE007F,0x00F8001F,0x00E00007,0x00800001
.text
start:
        lui $28, 0xFFFF
        ori $28, $28, 0xF000
        andi $s1, $zero,0 #默认全灭
        andi $s2, $zero,0
        andi $s5, $zero,0 #数组下标
        ori $s6, $zero,96 # 24种模式
        ori $t0, $zero,0
        ori $t1, $zero,1
        ori $t2, $zero,2
        ori $t3, $zero,3
		ori $t4, $zero,4
        # ori $t4, $zero,8 # debug
switch:
	lw $s7, 0xc70($28) # switch 输入
	# lw $s7, tmps($t4) # debug
	beq $s7,$t0, blink0
	beq $s7,$t1,blink1
	beq $s7,$t2,blink2
	beq $s7,$t3,blink3
	beq $s7,$t4,blink4

blink0:
        lw $s1, LED0($s5) #低位亮
        lw $s2, LED0($s5) # 高位亮
        SRL $s2, $s2, 16
        sw $s1,0xC60 ($28) #输出
        sw $s2,0xC62 ($28)
        addi $s5,$s5, 4 #数组下标指向下一个

        andi $s3,$zero, 0 #清零，准备进入循环
        lw  $s4, time($zero) #0x3F9409次
	jal lop
        bne $s5, $s6, switch #没有做完24种模式

        andi $s5, $zero,0
        j switch

blink1:
        lw $s1, LED1($s5)
        lw $s2, LED1($s5)
        SRL $s2, $s2, 16
        sw $s1,0xC60 ($28)
        sw $s2,0xC62 ($28)
        addi $s5,$s5, 4 #加1

        andi $s3,$zero, 0 #清零
        lw  $s4, time($zero) #0x3F9409次
	jal lop
        bne $s5, $s6, switch

        andi $s5, $zero,0
        j switch

blink2:
        lw $s1, light_low_2($s5)
        lw $s2, light_high_2($s5)
        #  SRL $s2, $s2, 16
        sw $s1,0xC60 ($28)
        sw $s2,0xC62 ($28)
        addi $s5,$s5, 4 #加1

        andi $s3,$zero, 0 #清零
        lw  $s4, time($zero) #0x3F9409次
	jal lop
        bne $s5, $s6, switch

        andi $s5, $zero,0
        j switch
 blink3:
        lw $s1, light_low_3($s5)
        lw $s2, light_high_3($s5)
        # SRL $s2, $s2, 16
        sw $s1,0xC60 ($28)
        sw $s2,0xC62 ($28)
        addi $s5,$s5, 4 #加1

        andi $s3,$zero, 0 #清零
        lw  $s4, time($zero) #0x3F9409次
	jal lop
        bne $s5, $s6, switch

        andi $s5, $zero,0
        j switch

blink4:
        lw $s1, LED4($s5)
        lw $s2, LED4($s5)
        SRL $s2, $s2, 16
        sw $s1,0xC60 ($28)
        sw $s2,0xC62 ($28)
        addi $s5,$s5, 4 #加1

        andi $s3,$zero, 0 #清零
        lw  $s4, time($zero) #0x3F9409次
	jal lop
        bne $s5, $s6, switch

        andi $s5, $zero,0
        j switch

lop:    addi $s3,$s3, 1 #加1
        bne $s3, $s4, lop
        jr $ra