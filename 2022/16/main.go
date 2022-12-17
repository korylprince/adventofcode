package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

var valveregexp = regexp.MustCompile(`([A-Z]{2}).*=(\d+);.*?((?:[A-Z]{2}(?:, )?)+)`)

type valve struct {
	Name  string
	Rate  uint16
	Edges string
}

func parse() ([]*valve, error) {
	buf, err := os.ReadFile("./input.txt")
	if err != nil {
		return nil, fmt.Errorf("could not read input: %w", err)
	}
	lines := strings.Split(strings.TrimSpace(string(buf)), "\n")
	valves := make([]*valve, len(lines))
	for idx, line := range lines {
		m := valveregexp.FindStringSubmatch(line)
		i, _ := strconv.Atoi(m[2])
		valves[idx] = &valve{Name: m[1], Rate: uint16(i), Edges: m[3]}
	}
	return valves, nil
}

func floydWarshall(valves []*valve) map[*valve]map[*valve]uint16 {
	graph := make(map[*valve]map[*valve]uint16)
	for _, v1 := range valves {
		graph[v1] = make(map[*valve]uint16)
		for _, v2 := range valves {
			if v1 == v2 {
				graph[v1][v2] = 0
			} else if strings.Contains(v1.Edges, v2.Name) {
				graph[v1][v2] = 1
			} else {
				graph[v1][v2] = 0xff
			}
		}
	}

	for _, k := range valves {
		for _, i := range valves {
			for _, j := range valves {
				if graph[i][j] > graph[i][k]+graph[k][j] {
					graph[i][j] = graph[i][k] + graph[k][j]
				}
			}
		}
	}

	return graph
}

func main() {
	valves, err := parse()
	if err != nil {
		panic(err)
	}

	graph := floydWarshall(valves)

	// pick valves with flow and starting point
	var worthit []*valve
	for _, v := range valves {
		if v.Rate > 0 || v.Name == "AA" {
			worthit = append(worthit, v)
		}
	}

	// assign bits
	bitfield := make(map[*valve]uint16)
	for idx, v := range worthit {
		bitfield[v] = 1 << idx
	}

	// find start
	var start uint16
	for _, v := range worthit {
		if v.Name == "AA" {
			start = bitfield[v]
			break
		}
	}

	// create slice for fast edge lookup
	bitgraphsl := make([]uint16, 0xffff)
	for _, v1 := range worthit {
		for _, v2 := range worthit {
			bitgraphsl[bitfield[v1]|bitfield[v2]] = graph[v1][v2]
		}
	}

	// create slice for fast node lookup
	worthbitsl := make([][2]uint16, len(worthit))
	for idx, v := range worthit {
		worthbitsl[idx] = [2]uint16{bitfield[v], v.Rate}
	}

	// part 1
	var dfs func(target, pressure, minute, on, node uint16) uint16
	dfs = func(target, pressure, minute, on, node uint16) uint16 {
		max := pressure
		for _, w := range worthbitsl {
			if node == w[0] || w[0] == start || w[0]&on != 0 {
				continue
			}
			l := bitgraphsl[node|w[0]] + 1
			if minute+l > target {
				continue
			}
			if next := dfs(target, pressure+(target-minute-l)*w[1], minute+l, on|w[0], w[0]); next > max {
				max = next
			}
		}
		return max
	}

	part1 := dfs(30, 0, 0, 0, start)
	fmt.Println("Answer 1:", part1)

	// part 2
	var dfspaths func(target, pressure, minute, on, node, path uint16) [][2]uint16
	dfspaths = func(target, pressure, minute, on, node, path uint16) [][2]uint16 {
		paths := [][2]uint16{{pressure, path}}
		for _, w := range worthbitsl {
			if w[0] == node || w[0] == start || w[0]&on != 0 {
				continue
			}
			l := bitgraphsl[node|w[0]] + 1
			if minute+l > target {
				continue
			}
			paths = append(paths, dfspaths(target, pressure+(target-minute-l)*w[1], minute+l, on|w[0], w[0], path|w[0])...)
		}
		return paths
	}

	allpaths := dfspaths(26, 0, 0, 0, start, 0)

	// reduce paths (presumably, both paths are at least half of part 1)
	var trimpaths [][2]uint16
	for _, p := range allpaths {
		if p[0] > part1/2 {
			trimpaths = append(trimpaths, p)
		}
	}

	// compare all paths to find max
	var max uint16 = 0
	for idx := 0; idx < len(trimpaths); idx += 1 {
		for jdx := idx + 1; jdx < len(trimpaths); jdx += 1 {
			if trimpaths[idx][1]&trimpaths[jdx][1] != 0 {
				continue
			}
			if m := trimpaths[idx][0] + trimpaths[jdx][0]; m > max {
				max = m
			}
		}
	}

	fmt.Println("Answer 2:", max)
}
