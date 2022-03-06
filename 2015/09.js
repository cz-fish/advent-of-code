const fs = require("fs");
const assert = require("assert");

function makeGraph(lines) {
	const graph = {};
	for (let line of lines) {
		line = line.trim();
		if (!line) {
			continue;
		}
		const parts = line.split(" ");
		assert.equal(parts.length, 5);
		const city1 = parts[0];
		const city2 = parts[2];
		const distance = parseInt(parts[4]);
		if (!graph[city1]) {
			graph[city1] = [];
		}
		if (!graph[city2]) {
			graph[city2] = [];
		}
		graph[city1].push({ city: city2, dist: distance });
		graph[city2].push({ city: city1, dist: distance });
	}
	return graph;
}

function shortest(val, new_val) {
	return (val === null || new_val < val) ? new_val : val;
}


function longest(val, new_val) {
	return (val === null || new_val > val) ? new_val : val;
}

let comparison_fn = shortest;

function shortestPath(graph, where, visited, pathHops, distance) {
	const pos = visited.size;
	//console.log(`where ${where} dist ${distance} target ${pathHops} pos ${pos}`);
	if (pos === pathHops) {
		return distance;
	}
	let best = null;
	const currentNode = graph[where];
	for (i in currentNode) {
		const nextCity = currentNode[i].city;
		const addDist = currentNode[i].dist;
		if (visited.has(nextCity)) {
			continue;
		}
		visited.add(nextCity);
		let len = shortestPath(graph, nextCity, visited, pathHops, distance + addDist);
		visited.delete(nextCity);
		best = comparison_fn(best, len);
	}
	if (best === null) {
		throw "Cannot find next city!";
	}
	return best;
}

function find_best_path(input) {
	const lines = input.split('\n');
	const graph = makeGraph(lines);
	const pathHops = Object.keys(graph).length;
	let best = null;
	const visited = new Set();
	for (start in graph) {
		visited.add(start);
		let len = shortestPath(graph, start, visited, pathHops, 0);
		visited.delete(start);
		best = comparison_fn(best, len);
	}
	return best;
}

// -- Test --
const example = "London to Dublin = 464\n\London to Belfast = 518\n\Dublin to Belfast = 141";
// part 1
comparison_fn = shortest;
const test_res_part1 = find_best_path(example);
console.log(`Test part 1 expected 605, got ${test_res_part1}`);
assert.equal(test_res_part1, 605);
// part 2
comparison_fn = longest;
const test_res_part2 = find_best_path(example);
console.log(`Test part 2 expected 982, got ${test_res_part2}`);
assert.equal(test_res_part2, 982);

// -- Actual input --
fs.readFile('./input09.txt', 'utf8', (err, data) => {
	if (err) {
		console.error(err);
		return;
	}
	comparison_fn = shortest;
	const res_part1 = find_best_path(data);
	console.log(`Part 1 result ${res_part1}`);
	comparison_fn = longest;
	const res_part2 = find_best_path(data);
	console.log(`Part 2 result ${res_part2}`);
})
