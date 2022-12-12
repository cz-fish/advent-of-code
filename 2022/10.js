const fs = require("fs");
const assert = require("assert");

function parseInput(data) {
	return data.split('\n').map(ln => ln.split(' '));
}

function part1(instr){
  var x = 1;
  var cycle = 0;
  var next_mark = 20;
  var signal = 0;
  for (var i of instr) {
  	  var time;
  	  var amount = 0;
  	  if (i[0] === 'addx') {
  	     amount = parseInt(i[1]);
  	     time = 2;
  	  } else {
  	     time = 1;
  	     amount = 0;
  	  }
  	  const new_cycle = cycle + time;
  	  if (new_cycle >= next_mark) {
  	  	   signal += next_mark * x;
  	  	   console.log(`${next_mark}: ${x} -> ${next_mark * x} (${signal})`);
  	  	   next_mark += 40;
  	  	}
  	  	x += amount;
  	  	cycle = new_cycle;
  	}
  return signal;
}

function part2(instr) {
	var screen = [];
	for (var y = 0; y <6;++y) {
		screen.push([]);
		for (var x = 0; x <40; ++x){
			screen[y].push('.');
		}
	}
	
	var cycle = 0;
	var x = 1;
	
	for (var i of instr){
		var time = 1;
		var amount = 0;
		if (i[0] === 'addx'){
			time = 2;
			amount = parseInt(i[1]);
		}
		for (var j = 0; j <time; j++) {
			var col = cycle % 40;
			var row = Math.floor(cycle / 40);
			if (col >= x-1 &&col <= x+1) {
			  screen[row][col]='#';
			}
			//console.log(`${row} ${col} ${x} ${screen[row][col]}`);
			cycle++;
		}
		x += amount;
		//if (cycle > 60) break;
	}
	
	for (var row = 0; row <6; ++row) {
		console.log(screen[row].join(''));
	}
}

function cassert(actual, expected) {
	console.log(`${actual} =?= ${expected}`);
	assert(actual === expected);
}

const useTestInput = false;
let fname = '/storage/emulated/0/Download/input2022-10.txt';
if (useTestInput){
	fname = '/storage/emulated/0/Download/input-t-2022-10.txt';
}
fs.readFile(fname, 'utf8' , (err, data) => {
    if (err) {
      console.error(err);
      return;
    }

  const instr = parseInput(data);
  const p1result = part1(instr);
  console.log(`part1: ${p1result}`);
  if (useTestInput) {
    cassert(p1result, 13140);
  }
  
  part2(instr);

});
