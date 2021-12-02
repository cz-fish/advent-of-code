namespace AoC2021

open System.IO

exception InvalidInput of string

module Day02 = 

    let loadFile() =
        File.ReadLines("input02.txt")
            |> Seq.toList
            |> List.map (fun line -> line.Split [|' '|]
                                     |> fun s -> (s[0], int s[1]))

    let partA() =
        let directions = loadFile()
        // convert each direction into a tuple of x and y increment
        let vectors = directions
                      |> List.map (function ("forward", a) -> (a, 0)
                                            | ("down", a) -> (0, a)
                                            | ("up", a) -> (0, -a)
                                            | x -> raise (InvalidInput(sprintf "%A" x))
                                  )
        // accumulate all the increments, and then multiply the coords
        let stop = vectors |> List.reduce (fun a b -> (fst(a) + fst(b), snd(a) + snd(b)))
        let res = fst(stop) * snd(stop)
        printfn "Part 02a result: %d" res
        0

    let partB() =
        let directions = loadFile()
        // make a list with relative changes of aim after each direction
        let aimChanges = directions
                         |> List.map (function ("forward", a) -> 0
                                               | ("down", a) -> a
                                               | ("up", a) -> -a
                                               | x -> raise (InvalidInput(sprintf "%A" x))
                         )
        // partial sum to get absolute aim after each direction. This list is 1 longer
        // than the list of directions and must be trimmed
        let aims = (0, aimChanges) ||> List.scan (fun acc change -> acc + change)
                   |> List.take (directions |> List.length)
        // calculate x and y increments, applying aim at each forward direction
        let vectors = List.zip directions aims 
                      |> List.map (function (("forward", amount), aim) -> (amount, amount * aim)
                                            | _ -> (0, 0))
        // accumulate all the increments, and then multiply the coords
        let stop = vectors |> List.reduce (fun a b -> (fst(a) + fst(b), snd(a) + snd(b)))
        let res = fst(stop) * snd(stop)

        printfn "Part 02b result: %d" res
        0
