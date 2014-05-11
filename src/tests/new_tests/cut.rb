#!/usr/bin/env ruby

txt = ARGV[0]
txts = txt.split('.')
body = txts[0...-1].join('.')
ext = txts[-1]

cuts = ARGV[1].to_i


files = cuts.times.to_a.map { |i| "#{body}#{i}.#{ext}" }
files.each { |fn| open(fn, 'w') { |f| f.puts } }

open(txt, 'r').readlines.each_with_index do |l, i|
  open(files[i % cuts], 'a') { |f| f.puts l } if l
end

print files.map { |f| "./#{f}" }.join("\n")
