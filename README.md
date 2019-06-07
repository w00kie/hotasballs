# Hot As Balls

[![CircleCI](https://circleci.com/gh/w00kie/hotasballs.svg?style=svg)](https://circleci.com/gh/w00kie/hotasballs)
[![Coverage Status](https://coveralls.io/repos/github/w00kie/hotasballs/badge.svg?branch=master)](https://coveralls.io/github/w00kie/hotasballs?branch=master)

## What is this?

It's a twitter bot that posts to various accounts (currently @tokyohotasballs) when it's really hot as balls outside.

## How does it run?

It's a Lambda function on AWS with a CloudWatch cron to run one a day.

## Notes

### How to get Twitter api keys for an account?

```bash
go get github.com/k0kubun/twitter-auth
twitter-auth -k consumer-key -s consumer-secret
```
