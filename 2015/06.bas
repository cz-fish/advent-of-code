Option _Explicit

Const TURN_ON = 1
Const TURN_OFF = -1
Const TOGGLE = 2

' one instruction line parsed from the input file
Type InstrType
    As Integer cmd, minx, miny, maxx, maxy
End Type

Dim line$, drawCommand As InstrType
Dim hori(0 To 599)
Dim vert(0 To 599)
Dim instructions(0 To 299) As InstrType
Dim counter%, instr_counter%

Open "input06.txt" For Input As #1
counter% = 0
instr_counter% = 0
Do Until EOF(1)
    If counter% >= 600 Then
        ' our hori and vert arrays only have space for 300*2 coordinates
        Error 2
    End If

    Line Input #1, line$
    Call parseLine(line$, drawCommand)
    ' collect all horizontal coordinates hori and vertical ones into vert
    hori(counter%) = drawCommand.minx
    hori(counter% + 1) = drawCommand.maxx + 1
    vert(counter%) = drawCommand.miny
    vert(counter% + 1) = drawCommand.maxy + 1
    counter% = counter% + 2
    instructions(instr_counter%) = drawCommand
    instr_counter% = instr_counter% + 1
Loop
Close #1

'If counter% < 600 Then
'    ' we were expecting 300*2 values. If there is fewer then we might have garbage in the hori and vert arrays
'    Error 3
'End If

' sort hori and vert
Call mergeSort(hori())
Call mergeSort(vert())

Dim horiCount%, vertCount%

horiCount% = makeUnique(hori())
vertCount% = makeUnique(vert())

'Print "hori count " + Str$(horiCount%)
'Print "vert count " + Str$(vertCount%)

Dim xi%, yi%, i%
Dim p1_tot_br& ' total brightness according to part 1 interpretation
Dim p2_tot_br& ' total brightness according to part 2 interpretation
Dim p1_rec_br& ' brightness of a rectangle according to part 1 interpretation
Dim p2_rec_br& ' brightness of a rectangle according to part 2 interpretation
Dim rec_size& ' current rectangle size
Dim ins As InstrType

p1_tot_br& = 0
p2_tot_br& = 0

If 0 Then
    ' Use example instead of real input
    instr_counter% = 3
    instructions(0).cmd = TURN_ON
    instructions(0).minx = 0
    instructions(0).maxx = 999
    instructions(0).miny = 0
    instructions(0).maxy = 999
    instructions(1).cmd = TOGGLE
    instructions(1).minx = 0
    instructions(1).maxx = 999
    instructions(1).miny = 0
    instructions(1).maxy = 0
    instructions(2).cmd = TURN_OFF
    instructions(2).minx = 499
    instructions(2).maxx = 500
    instructions(2).miny = 499
    instructions(2).maxy = 500
    horiCount% = 4
    hori(0) = 0
    hori(1) = 499
    hori(2) = 501
    hori(3) = 1000
    vertCount% = 5
    vert(0) = 0
    vert(1) = 1
    vert(2) = 499
    vert(3) = 501
    vert(4) = 1000
End If

' for each rectangle formed by 2 consecutive horizontal and 2 consecutive vertical coordinates
For xi% = 0 To horiCount% - 2
    For yi% = 0 To vertCount% - 2
        rec_size& = (hori(xi% + 1) - hori(xi%)) * (vert(yi% + 1) - vert(yi%))
        p1_rec_br& = 0
        p2_rec_br& = 0
        ' for each input instruction
        For i% = 0 To instr_counter% - 1
            ins = instructions(i%)
            ' if this instruction intersects the rectangle
            If ins.minx < hori(xi% + 1) And ins.maxx >= hori(xi%) And ins.miny < vert(yi% + 1) And ins.maxy >= vert(yi%) Then
                ' apply the brightness change of the instruction on the whole rectangle

                ' Part 1 interpretation:
                If ins.cmd = TURN_ON Then
                    p1_rec_br& = 1
                ElseIf ins.cmd = TURN_OFF Then
                    p1_rec_br& = 0
                ElseIf ins.cmd = TOGGLE Then
                    p1_rec_br& = -p1_rec_br& + 1
                End If

                ' Part 2 interpretation:
                p2_rec_br& = p2_rec_br& + ins.cmd
                ' prevent underflow of 0
                If p2_rec_br& < 0 Then
                    p2_rec_br& = 0
                End If

            End If
        Next i%
        ' accumulate total brightness of the rectangle
        p1_tot_br& = p1_tot_br& + p1_rec_br& * rec_size&
        p2_tot_br& = p2_tot_br& + p2_rec_br& * rec_size&
    Next yi%
Next xi%

Print "Part 1 total brightness: " + Str$(p1_tot_br&)
Print "Part 2 total brightness: " + Str$(p2_tot_br&)

End

' Parse one line of input into the instruction structure
Sub parseLine (line$, result As InstrType)
    Dim words$(0 To 4), i%, n%, c%
    Do
        n% = InStr(i% + 1, line$, " ")
        If n% <> 0 Then
            words$(c%) = Mid$(line$, i% + 1, n% - i% - 1)
            c% = c% + 1
        Else
            words$(c%) = Mid$(line$, i% + 1)
        End If
        i% = n%
    Loop Until n% = 0
    If words$(0) = "toggle" Then
        c% = 1
        result.cmd = TOGGLE
    Else
        c% = 2
        If words$(1) = "on" Then
            result.cmd = TURN_ON
        Else
            result.cmd = TURN_OFF
        End If
    End If
    Call parseCoords(words$(c%), result.minx, result.miny)
    Call parseCoords(words$(c% + 2), result.maxx, result.maxy)
End Sub

' Parse corrds from string "xxx,yyy"
Sub parseCoords (word$, x%, y%)
    Dim n%
    n% = InStr(1, word$, ",")
    If n% = 0 Then
        Print "cannot parse coords '" + word$ + "'"
        End 1
    End If
    x% = Val(Mid$(word$, 1, n%))
    y% = Val(Mid$(word$, n% + 1))
End Sub

' Given a sorted array, compact all unique (non-duplicate) values, and return the
' new size of the compacted array. Contents of the rest of the original array, past
' the compacted size, is undefined
Function makeUnique (arr())
    Dim size%
    size% = UBound(arr) - LBound(arr) + 1
    If size% < 2 Then
        makeUnique = size%
        Exit Function
    End If

    Dim newSize%, currIndex%
    newSize% = LBound(arr) + 1
    For currIndex% = LBound(arr) + 1 To UBound(arr)
        If arr(currIndex%) <> arr(currIndex% - 1) Then
            If newSize% < currIndex% Then
                arr(newSize%) = arr(currIndex%)
            End If
            newSize% = newSize% + 1
        End If
    Next
    makeUnique = newSize%
End Function

'$INCLUDE:'lib/mergesort.bm'

