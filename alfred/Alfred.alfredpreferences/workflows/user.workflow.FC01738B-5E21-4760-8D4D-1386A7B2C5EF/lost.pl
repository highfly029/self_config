#!/usr/bin/perl -ln


if($_ =~ /Response/) 
{
	 s:(.*)Response:$1Request: and print;
} 

elsif($_ =~ /Request/)
{
	s:(.*)Request:$1Response: and print;
}

elsif($_ =~ /\.dataID$/)
{
	s:(.*)\.dataID:=\s*new $1: and print;
}

elsif($_ =~ /new /)
{
	s:.*new (.*):$1.dataID: and print;
}
