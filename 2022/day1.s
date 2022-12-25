.section ".text"
.global _start

SYS_close =6
SYS_exit =1
SYS_open =5
SYS_read =3
SYS_write =4
STDOUT =1
O_RDONLY =0

_start:
    save %sp, -64, %sp

    ! open file fname
    mov SYS_open, %g1
    set .fname, %o0
    mov O_RDONLY, %o1
    ta 8

    ! store file descriptor
    set .filedesc, %l0
    st %o0, [%l0]

    ! read from file, up to 64 kb
    mov SYS_read, %g1
    set .filedesc, %g2
    ld [%g2], %o0
    set .buf, %o1
    set 65536, %o2
    ta 8

    ! append an extra newline and a zero terminator
    set .buf, %o1
    add %o1, %o0, %o1
    mov 0x0a00, %g1
    sth %g1, [%o1]

    ! close input file
    mov SYS_close, %g1
    set .filedesc, %g2
    ld [%g2], %o0
    ta 8

    ! main loop setup
    set .buf, %l0
    set 0, %g1
    mov 0, %g2     ! current number
    mov 0, %g3     ! sum of group
    mov 0, %g4     ! double newline
    mov 0, %g5     ! biggest group so far
    mov 0, %g6     ! second biggest group
    mov 0, %g7     ! third biggest group
.loop_chars:
    ldsb [%l0], %g1  ! load next char from .buf
    cmp %g1, 0     ! is zero terminator?
    be .finish
    inc %l0

    cmp %g1, 0xa   ! is newline?
    be .endline
    nop

    ! not a double newline
    mov 0, %g4

    ! g2 = 10 * g2 + (ord(g1)-ord('0'))
    sub %g1, 48, %g1
    umul %g2, 10, %g2
    b .loop_chars
    add %g2, %g1, %g2

.endline:
    cmp %g4, 1
    be .double_newline
    nop

    mov 1, %g4     ! next newline will be a double newline
    ! add current number to the sum of the current group
    add %g3, %g2, %g3
    b .loop_chars  ! continue
    mov 0, %g2     ! reset current number

.double_newline:
    ! update best group
    cmp %g3, %g5
    ble .compare_second_best
    nop
    ! swap current group and biggest group
    xor %g3, %g5, %g5
    xor %g3, %g5, %g3
    xor %g3, %g5, %g5
.compare_second_best:
    cmp %g3, %g6
    ble .compare_third_best
    nop
    ! swap current group and second biggest
    xor %g3, %g6, %g6
    xor %g3, %g6, %g3
    xor %g3, %g6, %g6
.compare_third_best:
    cmp %g3, %g7
    ble .comparison_done
    nop
    ! move current group into third biggest
    mov %g3, %g7
.comparison_done:
    b .loop_chars   ! continue with next group
    mov 0, %g3      ! clear current group sum

.finish:
    ! save both solutions
    set .solution_part1, %l0
    st %g5, [%l0]
    set .solution_part2, %l0
    add %g5, %g6, %g5
    add %g5, %g7, %g5
    st %g5, [%l0]

    ! print part 1 solution
    set .solution_part1, %l0
    ld [%l0], %o0
    call _write_number, 1
    nop

    ! print part 2 solution
    set .msg, %l0
    mov 50, %g1
    stsb %g1, [%l0 + 5]  ! overwrite "Part 1" to "Part 2"

    set .solution_part2, %l0
    ld [%l0], %o0
    call _write_number, 1
    nop

    ! exit with success
    mov SYS_exit, %g1
    clr %o0
    ta 8
    ! --- end ---

_write_number:
    save %sp, -64, %sp
    set .msg, %g1
    add %g1, 13, %g1   ! position of last digit in .msg
    mov 6, %g2         ! repeat for 6 digits

.next_digit:
    udiv %i0, 10, %i1
    umul %i1, 10, %i2
    sub %i0, %i2, %i2  ! i2 = i0 mod 10
    mov %i1, %i0       ! i0 = i0 // 10
    mov 32, %i3        ! ascii space
    orcc %i2, %i0, %i1 ! if there are no more digits to print, keep the space
    skipz
    add %i2, 48, %i3   ! make the ascii digit by adding value of '0'
    stub %i3, [%g1]
    deccc %g2
    bnz .next_digit
    dec %g1

    ! write solution to stdout
    mov SYS_write, %g1
    mov STDOUT, %o0
    set .msg, %o1
    mov msglen, %o2
    ta 8

    ret
    restore
    .type _write_number,#function
    .size _write_number,(.-_write_number)

!---------------------

.section ".data1"
.align 4
.msg:
    .asciz "Part 1: ......\n"
    msglen = . - .msg

.fname:
    .asciz "input.txt"
    fnamelen = . - .fname

.align 4
.filedesc:
    .word 0
    .size .filedesc,4
    .type .filedesc,#object

.solution_part1:
    .word 0
    .size .solution_part1,4
    .type .solution_part1,#object

.solution_part2:
    .word 0
    .size .solution_part2,4
    .type .solution_part2,#object

!------------
.section ".bss"
.align 4

.buf:
    .size .buf,65536

