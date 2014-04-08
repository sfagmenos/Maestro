#!/usr/bin/env ruby

File.open("/tmp/test.txt", 'w') { |file| file.write("Hello World!") }
