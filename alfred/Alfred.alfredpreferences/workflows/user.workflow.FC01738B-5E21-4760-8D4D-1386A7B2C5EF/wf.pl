#!/usr/bin/perl -ln -s
# yandeli


/$query/ and $_ =~ s/[,"]/ /g and $path=getPath() and print "{\"subtitle\":\"$ARGV\",\"arg\":\"$path\", \"title\":\"$_\"},";


sub getPath {
	$name = $ARGV;
	$name =~ s-.*/--g;
	$name =~ s-csv-xlsx-;
	if ($name =~ /c[A-Z]/) {
		return "/Users/hedley/Documents/workspace/lost/Common/xlsx_config/commonConfig/$name"
	} else {
		return "/Users/hedley/Documents/workspace/lost/Common/xlsx_config/gameConfig/$name"
	}
}
