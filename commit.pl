#!/usr/bin/perl

use strict;

my $name = shift @ARGV || die "\nLack of commit name\n\n";

foreach my $arg ( @ARGV ) {
  $name .= " $arg";
}

system("git add *.py");
system("git add commit.pl");
system("git add LICENSE.txt");
system("git add README.md");
system("git add ss.png");
system("git commit -m \"$name\"");


