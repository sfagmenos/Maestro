#!/usr/bin/env ruby

require 'json'

count = Hash.new(0)
ARGF.read.strip.split(/\s+/).each do |w|
  count[w] += 1
end

print "#{JSON.dump(count)}"
