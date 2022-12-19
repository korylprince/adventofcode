package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type cube [3]int8
type set map[cube]struct{}

func (c cube) edges() []cube {
	cubes := make([]cube, 6)
	for idx := 0; idx < 3; idx++ {
		cubes[idx] = c
		cubes[idx][idx] += 1
		cubes[idx+3] = c
		cubes[idx+3][idx] -= 1
	}
	return cubes
}

func parse() ([]cube, error) {
	buf, err := os.ReadFile("./input.txt")
	if err != nil {
		return nil, fmt.Errorf("could not read input: %w", err)
	}
	lines := strings.Split(strings.TrimSpace(string(buf)), "\n")
	cubes := make([]cube, len(lines))
	for idx, line := range lines {
		nums := strings.Split(line, ",")
		x, _ := strconv.ParseInt(nums[0], 10, 8)
		y, _ := strconv.ParseInt(nums[1], 10, 8)
		z, _ := strconv.ParseInt(nums[2], 10, 8)
		cubes[idx] = cube{int8(x), int8(y), int8(z)}
	}
	return cubes, nil
}

func floodAir(start, max cube, lava set) set {
	q := []cube{start}
	seen := make(set)
	seen[start] = struct{}{}
	for len(q) > 0 {
		node := q[0]
		q = q[1:]
	outer:
		for _, edge := range node.edges() {
			for idx := 0; idx < 3; idx++ {
				if _, ok := lava[edge]; ok || edge[idx] < -1 || edge[idx] > max[idx] {
					continue outer
				}
			}

			if _, ok := seen[edge]; !ok {
				q = append(q, edge)
				seen[edge] = struct{}{}
			}
		}
	}

	return seen
}

func floodFill(start, max cube, lava, air set) {
	q := []cube{start}
	seen := make(set)
	seen[start] = struct{}{}
	total := 0
	exposed := 0
	for len(q) > 0 {
		node := q[0]
		q = q[1:]
	outer:
		for _, edge := range node.edges() {
			for idx := 0; idx < 3; idx++ {
				if edge[idx] < -1 || edge[idx] > max[idx] {
					continue outer
				}
			}
			_, airnode := air[node]
			_, lavanode := lava[node]
			_, lavaedge := lava[edge]

			if !lavanode && lavaedge {
				total += 1
			}

			if airnode && lavaedge {
				exposed += 1
			}

			if _, ok := seen[edge]; !ok {
				q = append(q, edge)
				seen[edge] = struct{}{}
			}
		}
	}

	fmt.Println("Answer 1:", total)
	fmt.Println("Answer 2:", exposed)
}

func main() {
	lava, err := parse()
	if err != nil {
		panic(fmt.Errorf("could not parse input: %w", err))
	}

	lavaSet := make(set)
	for _, c := range lava {
		lavaSet[c] = struct{}{}
	}

	max := cube{}
	for _, c := range lava {
		for idx := 0; idx < 3; idx++ {
			if c[idx] > max[idx] {
				max[idx] = c[idx]
			}
		}
	}
	max[0] += 1
	max[1] += 1
	max[2] += 1

	air := floodAir(cube{0, 0, 0}, max, lavaSet)
	floodFill(cube{0, 0, 0}, max, lavaSet, air)
}
