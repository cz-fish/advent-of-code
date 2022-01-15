Option _Explicit

' Solve the problem (part 1 only) visually by actually drawing and toggling rectangles on the screen
' and then counting how many pixels are white.

' this happens to be color white
Const TURN_ON = 15
' this happens to be color black
Const TURN_OFF = 0
' this value doesn't matter
Const TOGGLE = 2

' one instruction line parsed from the input file
Type InstrType
    As Integer cmd, minx, miny, maxx, maxy
End Type

Dim line$, drawCommand As InstrType

' main buffer is what we will be drawing into
Dim Shared mainBuffer As Long
mainBuffer = _NewImage(1000, 1000, 256)
_Dest mainBuffer
Screen mainBuffer

Open "input06.txt" For Input As #1
Do Until EOF(1)
    Line Input #1, line$
    Call parseLine(line$, drawCommand)
    'Print "command " + str$(drawCommand.cmd) + ", [" + str$(drawCommand.minx) + _
    '    "," + str$(drawCommand.miny) + "] .. [" + str$(drawCommand.maxx) + _
    '    "," + str$(drawCommand.maxy) + "]"

    ' draw each command from the input into our main buffer.
    ' Turn on and turn off are straightforward, toggle is special
    If drawCommand.cmd = TURN_ON Or drawCommand.cmd = TURN_OFF Then
        Call fillRect(drawCommand)
    Else
        Call toggleRect(drawCommand)
    End If
Loop

Close #1

' Now the screen is showing the final pattern. Press any key and we'll
' count how many pixels it has lit, which will be the solution
Dim key$, dots&
key$ = Input$(1)
dots& = countDots
Screen 0
Print "Lit dots" + Str$(dots&)
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

' Fill a rectangle in the active buffer.
' Because cmd.cmd has the right value, we can use it as color
Sub fillRect (cmd As InstrType)
    Dim i%
    For i% = cmd.miny To cmd.maxy
        Line (cmd.minx, i%)-(cmd.maxx, i%), cmd.cmd
    Next i%
End Sub

' To toggle a rectangle, we first fill it with white in another buffer
' And then copy the buffer over to our designated main buffer with the XOR operation
Sub toggleRect (cmd As InstrType)
    Dim buffer As Long
    Dim img%(1000 * 1000)
    buffer = _NewImage(1000, 1000, 256)
    _Dest buffer
    cmd.cmd = TURN_ON
    Call fillRect(cmd)
    _Source buffer
    Get (0, 0)-(999, 999), img%()
    cmd.cmd = TOGGLE
    _Dest mainBuffer
    Put (0, 0), img%(), Xor
    _FreeImage (buffer)
End Sub

' Read the color of each pixel from the main buffer and count the white ones
Function countDots ()
    Dim cnt&, x%, y%
    _Source mainBuffer
    For x% = 0 To 999
        For y% = 0 To 999
            If Point(x%, y%) <> 0 Then
                cnt& = cnt& + 1
            End If
        Next y%
    Next x%
    countDots = cnt&
End Function

