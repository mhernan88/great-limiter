package ratelimiter

import "time"

func getSecond() uint32 {
	now := time.Now()
	hour := now.Hour()
	minute := now.Minute()
	second := now.Second()
	return uint32(hour * 3600 + minute * 60 + second)
}

func getMinute() uint32 {
	now := time.Now()
	hour := now.Hour()
	minute := now.Minute()
	return uint32(hour * 60 + minute)
}

func getHour() uint32 {
	now := time.Now()
	return uint32(now.Hour())
}