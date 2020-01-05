namespace AoC2017

open NUnit.Framework

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

    let rec getValueAt' coords depth =
        let (x, y) = coords
        let ring = max (abs x) (abs y)
        let spaces = String.replicate depth " "
        printfn "%sgetValueAt %d %d, ring %d" spaces x y ring

        let getNeighbor (coords: int*int) =
            let (x, y) = coords
            getValueAt'' (x, y) (depth + 1)

        match (x < 0, y < 0) with
        | (true, true) ->
            // top left quadrant
            let up =
                if -y < ring then
                    getNeighbor(x, y-1) + getNeighbor(x+1, y-1)
                else
                    0
            up + getNeighbor(x+1, y) + getNeighbor(x+1, y+1)

        | (true, false) ->
            // bottom left quadrant
            let left = 
                if -x < ring then
                    getNeighbor(x-1, y-1) + getNeighbor(x-1, y)
                else
                    0
            left + getNeighbor(x, y-1) + getNeighbor(x+1, y-1)

        | (false, true) ->
            // top right quadrant
            if x = 0 && y = -1 then
                4
            else
                let right =
                    if x < ring then
                        getNeighbor(x+1, y) + getNeighbor(x+1, y+1)
                    else
                        0
                right + getNeighbor(x-1, y+1) + getNeighbor(x, y+1)

        | (false, false) ->
            // bottom right quadrant
            if x = 1 && y = 0 then
                1
            else
                let down =
                    if y < ring then
                        getNeighbor(x-1, y+1) + getNeighbor(x, y+1)
                    else
                        0
                down + getNeighbor(x-1, y-1) + getNeighbor(x-1, y)

    and getValueAt'' coords depth =
        match coords with
        | 0, 0 -> 1
        | x, y ->
            match depth with
            | a when a >= 50 ->
                printfn "Depth %A reached at %A %A" a x y
                0
            | _ -> getValueAt' (x, y) depth

    let getValueAt = function
        | (0, 0) -> 1
        | coords -> getValueAt' coords 0

    let partB () =
        let coords = findCoords input
        let value = getValueAt (-2, -1)
        printfn "Value %A" value
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

    [<Test>]
    let ``getValueAt: 0, 0 gets 1``() =
        Assert.AreEqual(1, getValueAt (0, 0))
    [<Test>]
    let ``getValueAt: 1, 0 gets 1``() =
        Assert.AreEqual(1, getValueAt (1, 0))
    [<Test>]
    let ``getValueAt: 0, -1 gets 4``() =
        Assert.AreEqual(4, getValueAt (0, -1))
    [<Test>]
    let ``getValueAt: 1, 1 gets 25``() =
        Assert.AreEqual(25, getValueAt (1, 1))
    [<Test>]
    let ``getValueAt: -2, -1 gets 304``() =
        Assert.AreEqual(304, getValueAt (-2, -1))
    [<Test>]
    let ``getValueAt: -1, 2 gets 747``() =
        Assert.AreEqual(747, getValueAt (-1, 2))
