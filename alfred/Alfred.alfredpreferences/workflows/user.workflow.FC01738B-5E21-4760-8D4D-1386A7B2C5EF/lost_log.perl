#! /usr/bin/perl -n -s

($pre,$x,$c)=$_=~/([^{}]+)({)(.*)/;

$tab=0;
while(defined $x)
{
	if($pre =~ /[^\s]/)
	{
		$pre=~s/^\s*|\s*$//g;


		if($C || $tab==0)
		{
			tab_print($pre);
		}
		elsif($tab>0)
		{
			print (tab()."$_\n") for split ' ', $pre;
		}
	}
	
	if($x eq "{")
	{
		tab_print($x);
		$tab++;
	}else
	{
		$tab--;
		tab_print($x);
	}

	($pre,$x,$c2)=$c=~/^([^{}]+)({)(.*)/;

	if(! defined $x)
	{
		($pre,$x,$c2)=$c=~/^([^{}]+)(})(.*)/;
	}

	$c=$c2;
}


sub tab_print
{
	print tab(), $_[0], "\n";
}

sub tab 
{
	return "\t" x $tab;
}

