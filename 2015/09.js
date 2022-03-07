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

function shortestPath(graph, where, visited, pathHops, distance, comparison_fn) {
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
		let len = shortestPath(graph, nextCity, visited, pathHops, distance + addDist, comparison_fn);
		visited.delete(nextCity);
		best = comparison_fn(best, len);
	}
	if (best === null) {
		throw "Cannot find next city!";
	}
	return best;
}

function find_best_path(input, comparison_fn) {
	const lines = input.split('\n');
	const graph = makeGraph(lines);
	const pathHops = Object.keys(graph).length;
	let best = null;
	const visited = new Set();
	for (start in graph) {
		visited.add(start);
		let len = shortestPath(graph, start, visited, pathHops, 0, comparison_fn);
		visited.delete(start);
		best = comparison_fn(best, len);
	}
	return best;
}

function run() {
	// -- With Actual input --
	const data = fs.readFileSync('./input09.txt', 'utf8');
	const res_part1 = find_best_path(data, shortest);
	console.log(`Part 1 result ${res_part1}`);
	const res_part2 = find_best_path(data, longest);
	console.log(`Part 2 result ${res_part2}`);
}

exports.run = run;
exports.shortest = shortest;
exports.longest = longest;
exports.find_best_path = find_best_path;

if (require.main === module) {
	run();
}
