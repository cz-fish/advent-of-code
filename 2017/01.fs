namespace AoC2017

open System.IO

module Day01 = 

    let rec countSame (head:int) rest =
        match rest with
            | [] -> 0
            | x :: xs ->
                if head = x then
                    head + countSame x xs
                else
                    countSame x xs

    let loadFile() =
        List.map (fun c -> int c - int '0') (File.ReadLines("input01.txt") |> Seq.head |> Seq.toList)

    let partA() =
        let text = loadFile()
        let last = text |> List.last
        printfn "Part 01a result: %d" (countSame last text)
        0

    let partB() =
        let input = loadFile()
        let length = input |> List.length
        let period = length / 2
        printfn "Part 01b result: %d" (
            [ for i in 0 .. length - 1
                ->  if input.[i] = input.[(i + period) % length] then
                        input.[i]
                    else
                        0
            ] |> List.sum
        )
        0