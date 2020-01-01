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
