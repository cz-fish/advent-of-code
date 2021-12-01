namespace AoC2021

open System.IO

module Day01 = 

    let loadFile() =
        File.ReadLines("input01.txt") |> Seq.toList |> List.map int

    let partA() =
        let numbers = loadFile()
        let res = List.zip numbers ((numbers |> List.tail ) @ [0]) |> List.map(fun (f, s) -> if s > f then 1 else 0) |> List.sum
        printfn "Part 01a result: %d" res
        0

    let partB() =
        let numbers = loadFile()
        let length = (numbers |> List.length) - 2
        let triplets = List.zip3 (numbers |> List.take length)
                                 (numbers |> List.tail |> List.take length)
                                 (numbers |> List.tail |> List.tail)
                       |> List.map (fun (a,b,c) -> a+b+c)
        let res = List.zip (triplets |> List.take (length - 1))
                           (triplets |> List.tail)
                  |> List.map (fun (f, s) -> if s > f then 1 else 0)
                  |> List.sum

        printfn "Part 01b result: %d" res
        0
