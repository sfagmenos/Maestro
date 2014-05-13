#!/usr/bin/env ruby

require 'json'

count = Hash.new(0)
ARGV.each do |arg|
  puts arg
  JSON.load(arg).each do |k,v|
    count[k] += v
  end
end
File.open('TestsOutput/check.txt', 'w') { |file| file.write("check") }

puts JSON.dump(count)
File.open('final_count.txt', 'w') do |f|
  f.puts JSON.dump(count)
end
