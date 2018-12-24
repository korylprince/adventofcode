package main

import (
	"container/heap"
	"fmt"
	"math"
	"os"
)

//items
const (
	TORCH int = iota
	GEAR
	NEITHER
)

//regions
const (
	ROCKY int = iota
	WET
	NARROW
)

var validItems = map[int]map[int]struct{}{
	ROCKY:  {TORCH: {}, GEAR: {}},
	WET:    {GEAR: {}, NEITHER: {}},
	NARROW: {TORCH: {}, NEITHER: {}},
}

var adjacent = [][2]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}

type item struct {
	value    [3]int
	priority int
	index    int
}

type priorityQueue []*item

func (pq priorityQueue) Len() int { return len(pq) }

func (pq priorityQueue) Less(i, j int) bool {
	return pq[i].priority < pq[j].priority
}

func (pq priorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *priorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*item)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *priorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	item.index = -1
	*pq = old[0 : n-1]
	return item
}

const depth = 8103

var target = [3]int{9, 758, TORCH}

var erosionCache = make(map[[2]int]int)

func erosion(x, y int) (e int) {
	if er, ok := erosionCache[[2]int{x, y}]; ok {
		return er
	}
	defer func() {
		erosionCache[[2]int{x, y}] = e
	}()
	if (x == 0 && y == 0) || (x == target[0] && y == target[1]) {
		return (depth % 20183)
	}

	if x == 0 {
		return ((y * 48271) + depth) % 20183
	}

	if y == 0 {
		return ((x * 16807) + depth) % 20183
	}

	return ((erosion(x-1, y) * erosion(x, y-1)) + depth) % 20183
}

var regionCache = make(map[[2]int]int)

func region(x, y int) (r int) {
	if rg, ok := regionCache[[2]int{x, y}]; ok {
		return rg
	}
	r = erosion(x, y) % 3
	regionCache[[2]int{x, y}] = r
	return r
}

func heuristic(x1, y1, x2, y2 int) int {
	return int(math.Abs(float64(x2-x1)) + math.Abs(float64(y2-y1)))
}

func aStar() int {
	source := [3]int{0, 0, TORCH}
	seen := make(map[[3]int]struct{})
	distances := map[[3]int]int{source: 0}
	pq := make(priorityQueue, 1)
	pq[0] = &item{value: source, priority: heuristic(source[0], source[1], target[0], target[1])}
	heap.Init(&pq)
	for pq.Len() > 0 {
		i := heap.Pop(&pq).(*item)
		if i.value == target {
			return distances[i.value]
		}
		seen[i.value] = struct{}{}

		for _, a := range adjacent {
			newValue := [3]int{i.value[0] + a[0], i.value[1] + a[1], i.value[2]}

			if _, ok := seen[newValue]; ok || newValue[0] < 0 || newValue[1] < 0 {
				continue
			}

			if _, ok := validItems[region(newValue[0], newValue[1])][i.value[2]]; !ok {
				continue
			}

			dist := distances[i.value] + 1
			if d, ok := distances[newValue]; ok && dist >= d {
				continue
			}
			distances[newValue] = dist
			heap.Push(&pq, &item{value: newValue, priority: dist + heuristic(newValue[0], newValue[1], target[0], target[1])})
		}

		for newItem := range validItems[region(i.value[0], i.value[1])] {
			if i.value[2] == newItem {
				continue
			}
			newValue := [3]int{i.value[0], i.value[1], newItem}

			if _, ok := seen[newValue]; ok {
				continue
			}

			dist := distances[i.value] + 7
			if d, ok := distances[newValue]; ok && dist >= d {
				continue
			}
			distances[newValue] = dist
			heap.Push(&pq, &item{value: newValue, priority: dist + heuristic(newValue[0], newValue[1], target[0], target[1])})
		}
	}

	return 0
}

func dijkstra() int {
	source := [3]int{0, 0, TORCH}
	seen := make(map[[3]int]struct{})
	distances := map[[3]int]int{source: 0}
	pq := make(priorityQueue, 1)
	pq[0] = &item{value: source, priority: 0}
	heap.Init(&pq)
	for pq.Len() > 0 {
		i := heap.Pop(&pq).(*item)
		if i.value == target {
			return distances[i.value]
		}
		seen[i.value] = struct{}{}

		for _, a := range adjacent {
			newValue := [3]int{i.value[0] + a[0], i.value[1] + a[1], i.value[2]}

			if _, ok := seen[newValue]; ok || newValue[0] < 0 || newValue[1] < 0 {
				continue
			}

			if _, ok := validItems[region(newValue[0], newValue[1])][i.value[2]]; !ok {
				continue
			}

			dist := distances[i.value] + 1
			if d, ok := distances[newValue]; ok && dist >= d {
				continue
			}
			distances[newValue] = dist
			heap.Push(&pq, &item{value: newValue, priority: dist})
		}

		for newItem := range validItems[region(i.value[0], i.value[1])] {
			if i.value[2] == newItem {
				continue
			}
			newValue := [3]int{i.value[0], i.value[1], newItem}

			if _, ok := seen[newValue]; ok {
				continue
			}

			dist := distances[i.value] + 7
			if d, ok := distances[newValue]; ok && dist >= d {
				continue
			}
			distances[newValue] = dist
			heap.Push(&pq, &item{value: newValue, priority: dist})
		}
	}

	return 0
}

func main() {
	if os.Args[1] == "a" {
		fmt.Println("Answer 2:", aStar())
	}
	if os.Args[1] == "d" {
		fmt.Println("Answer 2:", dijkstra())
	}
}
