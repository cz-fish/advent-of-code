namespace AoC2017

open NUnit.Framework
open System.Collections.Generic

module Day03 =

    let input = 325489

    let findCoords = function
        | 1 -> (0, 0)
        | num ->
            // the spiral starts with 1, not with 0
            let num' = num - 1
            // find biggest odd square less than num
            let ring' = int(sqrt(float num'))
            let ring = ring' - ((ring' + 1) % 2)
            let half = (ring - 1) / 2
            let half' = half + 1
            let remainder = num' - ring * ring
            let edge = remainder / (ring + 1)
            let onEdge = remainder % (ring + 1)
            match edge with
                | 0 -> (half', half - onEdge)
                | 1 -> (half - onEdge, -half')
                | 2 -> (-half', -half + onEdge)
                | 3 -> (-half + onEdge, half')
                | _ -> failwith "Logic error, invalid edge of the spiral"

    let partA () =
        let (x, y) = findCoords input
        let distance = (abs x) + abs y
        printfn "Distance %A" distance
        0

    [<Test>]
    let ``findCoords: 1 is in the middle``() =
        Assert.AreEqual( (0, 0), findCoords 1 )
    [<Test>]
    let ``findCoords: 2 is on (1, 0)``() =
        Assert.AreEqual( (1, 0), findCoords 2 )
    [<Test>]
    let ``findCoords: 12 is on (2, -1)``() =
        Assert.AreEqual( (2, -1), findCoords 12 )
    [<Test>]
    let ``findCoords: 17 is on (-2, -2)``() =
        Assert.AreEqual( (-2, -2), findCoords 17 )
    [<Test>]
    let ``findCoords: 19 is on (-2, 0)``() =
        Assert.AreEqual( (-2, 0), findCoords 19 )
    [<Test>]
    let ``findCoords: 25 is on (2, 2)``() =
        Assert.AreEqual( (2, 2), findCoords 25 )

    // ---- part B ----
    type EdgeDir =
        | Up
        | Left
        | Down
        | Right
    type Edge = { dir: EdgeDir; length: int; pos: int }
    type Pos = { x: int; y: int; length: int }

    let nextEdge = function
        | Up -> Left
        | Left -> Down
        | Down -> Right
        | Right -> Up

    let newPos (pos:Pos) (edge:Edge) =
        match edge.dir with
            | Up    -> { x = pos.x; y = pos.y-1; length = pos.length+1}
            | Left  -> { x = pos.x-1; y = pos.y; length = pos.length+1}
            | Down  -> { x = pos.x; y = pos.y+1; length = pos.length+1}
            | Right -> { x = pos.x+1; y = pos.y; length = pos.length+1}

    let newEdge (pos:Pos) (edge:Edge) =
        if edge.pos = edge.length then
            let nEdge = nextEdge edge.dir
            let nLength = if nEdge = Left || nEdge = Right then edge.length + 1 else edge.length
            { dir = nEdge; length = nLength; pos = 0 }
        else
            { dir = edge.dir; length = edge.length; pos = edge.pos + 1 }

    let rec generateSpiral' totLength (pos:Pos) (edge:Edge) (spiral:Dictionary<(int*int), int>) generator =
        let last = generator spiral pos edge
        spiral.Add((pos.x, pos.y), last)
        if totLength = pos.length then
            last
        else
            let npos = newPos pos edge
            let nedge = newEdge pos edge
            generateSpiral' totLength npos nedge spiral generator

    let generateSpiral totLength generator =
        let spiral = new Dictionary<(int * int), int>()
        generateSpiral'
            (totLength - 1)
            { x = 0; y = 0; length = 0 }
            { dir = EdgeDir.Right; length = 0; pos = 0 }
            spiral
            generator

    let sumsGenerator (spiral:Dictionary<(int*int), int>) (pos:Pos) edge =
        if pos.x = 0 && pos.y = 0 then
            1
        else
            let sum = spiral.GetValueOrDefault((pos.x-1, pos.y-1), 0) +
                      spiral.GetValueOrDefault((pos.x, pos.y-1), 0) +
                      spiral.GetValueOrDefault((pos.x+1, pos.y-1), 0) +
                      spiral.GetValueOrDefault((pos.x-1, pos.y), 0) +
                      spiral.GetValueOrDefault((pos.x+1, pos.y), 0) +
                      spiral.GetValueOrDefault((pos.x-1, pos.y+1), 0) +
                      spiral.GetValueOrDefault((pos.x, pos.y+1), 0) +
                      spiral.GetValueOrDefault((pos.x+1, pos.y+1), 0)
            sum

    // ---- wrong attempt - actually calculates something else than needed ----
    let partB' () =
        let value = generateSpiral input sumsGenerator
        printfn "Value %A" value
        0

    [<Test>]
    let ``spiral value at pos 1 is 1``() =
        Assert.AreEqual(1, generateSpiral 1 sumsGenerator)
    [<Test>]
    let ``spiral value at pos 2 is 1``() =
        Assert.AreEqual(1, generateSpiral 2 sumsGenerator)
    [<Test>]
    let ``spiral value at pos 4 is 4``() =
        Assert.AreEqual(4, generateSpiral 4 sumsGenerator)
    [<Test>]
    let ``spiral value at pos 9 is 25``() =
        Assert.AreEqual(25, generateSpiral 9 sumsGenerator)
    [<Test>]
    let ``spiral value at pos 18 is 304``() =
        Assert.AreEqual(304, generateSpiral 18 sumsGenerator)
    [<Test>]
    let ``spiral value at pos 22 is 747``() =
        Assert.AreEqual(747, generateSpiral 22 sumsGenerator)

    // ---- partB ----
    let rec generateSpiral'' target (pos:Pos) (edge:Edge) (spiral:Dictionary<(int*int), int>) generator =
        let next = generator spiral pos edge
        if next > target then
            next
        else
            spiral.Add((pos.x, pos.y), next)
            let npos = newPos pos edge
            let nedge = newEdge pos edge
            generateSpiral'' target npos nedge spiral generator

    let firstValueGreaterThan target =
        let spiral = new Dictionary<(int*int), int>()
        generateSpiral''
            target
            { x = 0; y = 0; length = 0 }
            { dir = Right; length = 0; pos = 0 }
            spiral
            sumsGenerator

    let partB () =
        printfn "First greater value: %d" (firstValueGreaterThan input)
        0

    [<Test>]
    let ``first value greater than 1 is 2``() =
        Assert.AreEqual(2, firstValueGreaterThan 1)
    [<Test>]
    let ``first value greater than 7 is 10``() =
        Assert.AreEqual(10, firstValueGreaterThan 7)
    [<Test>]
    let ``first value greater than 22 is 23``() =
        Assert.AreEqual(23, firstValueGreaterThan 22)
    [<Test>]
    let ``first value greater than 59 is 122``() =
        Assert.AreEqual(122, firstValueGreaterThan 59)
