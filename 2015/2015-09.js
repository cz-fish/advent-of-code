const fs = require('fs');
const assert = require('assert');

const useTestInput = false;

function makeGraph(lines) {
	const graph = {};
	for (line of lines) {
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
		graph[city1].push({city: city2, dist:distance});
		graph[city2].push({city: city1, dist:distance});
	}
	return graph;
}

//let global_best = null;
//let global_path = [];

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
		//if (global_best === null || distance < global_best) {
		//	global_best = distance;
		//	console.log(`path ${distance}: ` + JSON.stringify(global_path));
		//}
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
		//global_path.push(nextCity);
		let len = shortestPath(graph, nextCity, visited, pathHops, distance + addDist);
		visited.delete(nextCity);
		//global_path.pop();
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
	//console.log(JSON.stringify(graph, null, 4));
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

if (useTestInput){
  const example = "London to Dublin = 464\n\London to Belfast = 518\n\Dublin to Belfast = 141";
  comparison_fn = shortest;
  const res_part1 = find_best_path(example);
  console.log(`Test part 1 expected 605, got ${res_part1}`);
  comparison_fn = longest;
  const res_part2 = find_best_path(example);
  console.log(`Test part 2 expected 982, got ${res_part2}`);
} else {
  fs.readFile('/storage/emulated/0/wrk/input09-2015.txt', 'utf8' , (err, data) => {
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
}
