package ratelimiter

import (
	"errors"
	"time"
)

func NewRateLimiter(rateLimit uint64, every string, waitDuration time.Duration) *RateLimiter {
	return &RateLimiter{
		timeUnit:     0,
		rate:         0,
		rateLimit:    rateLimit,
		every:        every,
		waitDuration: waitDuration,
	}
}

type RateLimiter struct {
	timeUnit uint32
	rate uint64
	rateLimit uint64
	every string
	waitDuration time.Duration
}


func (r RateLimiter) OK() (bool, error) {
	var t uint32
	if r.every == "second" {
		t = getSecond()
	} else if r.every == "minute" {
		t = getMinute()
	} else if r.every == "hour" {
		t = getHour()
	} else {
		return false, errors.New("invalid every argument (must be: second | minute | hour")
	}

	if t != r.timeUnit {
		r.rate = 0
	}

	if r.rate > r.rateLimit {
		return false, nil
	}
	return true, nil
}

func (r RateLimiter) Wait() error {
	var (
		ok bool
		err error
	)

	for {
		ok, err = r.OK()
		if err != nil {
			return err
		}
		if ok {
			return nil
		}

		time.Sleep(r.waitDuration)
	}
}