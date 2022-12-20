package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"

	"github.com/gammazero/deque"
)

const input = "./input.txt"

func parse() ([]*int64, error) {
	buf, err := os.ReadFile(input)
	if err != nil {
		return nil, fmt.Errorf("could not read input: %w", err)
	}

	lines := strings.Split(strings.TrimSpace(string(buf)), "\n")

	nums := make([]*int64, len(lines))
	for idx, line := range lines {
		n, _ := strconv.ParseInt(line, 10, 16)
		n2 := int64(n)
		nums[idx] = &n2
	}
	return nums, nil
}

func part1(ordered []*int64) {
	// create deque
	var zero *int64
	data := deque.New[*int64](len(ordered))
	for _, n := range ordered {
		data.PushBack(n)
		if *n == 0 {
			zero = n
		}
	}

	// mix
	for _, n := range ordered {
		data.Rotate(data.Index(func(n2 *int64) bool { return n == n2 }))
		p := data.PopFront()
		data.Rotate(int(*n))
		data.PushFront(p)
	}

	// grove coordinates
	data.Rotate(data.Index(func(n2 *int64) bool { return zero == n2 }))
	grove := 0
	for i := 0; i < 3; i++ {
		data.Rotate(1000)
		grove += int(*data.Front())
	}

	fmt.Println("Answer 1:", grove)
}

func part2(ordered []*int64) {
	// create deque
	var zero64 *int64
	data := deque.New[*int64](len(ordered))
	for _, n := range ordered {
		data.PushBack(n)
		if *n == 0 {
			zero64 = n
		}
	}

	// mix 10 times
	for i := 0; i < 10; i++ {
		for _, n := range ordered {
			data.Rotate(data.Index(func(n2 *int64) bool { return n == n2 }))
			p := data.PopFront()
			data.Rotate(int(*n))
			data.PushFront(p)
		}
	}

	// grove coordinates
	data.Rotate(data.Index(func(n2 *int64) bool { return zero64 == n2 }))
	grove := 0
	for i := 0; i < 3; i++ {
		data.Rotate(1000)
		grove += int(*data.Front())
	}

	fmt.Println("Answer 2:", grove)
}

func main() {
	// parse
	ordered, err := parse()
	if err != nil {
		panic(fmt.Errorf("could not parse: %w", err))
	}

	part1(ordered)

	// add decryption key
	for _, n := range ordered {
		*n *= 811589153
	}

	part2(ordered)
}
