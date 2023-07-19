#!/usr/bin/perl -l
# yandeli
# crc_check: config record compatible check
# LOST-36642 分支配置导表序号校验

use XML::LibXML;
use Data::Dumper qw(Dumper);
 
my $parser = XML::LibXML->new;

my %HASH_trunk, %HASH_ptr, %HASH_release;

sub parseRecord($) 
{
    my ($filename) = @_;

    my %re;

    my $dom = $parser->load_xml( location => $filename );

    foreach my $info ($dom->findnodes('//info')) 
    {
        if ($info->findvalue('./@clientMaxSortTag') <= 0)
        {
            next;
        }

        $path = $info->findvalue('./@path');

        $re{$path}{"configType"} = ( split /,/, $info->findvalue('./@ex2') )[13];           #第14位为configType,代码生成工具定义

        $re{$path}{"record"} = { split /,/, $info->findvalue('./@clientFieldRecord') };     
    }

    return %re;
}


sub compatibleCheck($$$)
{
    my $hashref1 = $_[0];

    my $hashref2 = $_[1];

    my $desc = $_[2];

    while ( ($k,$_h1) = each %$hashref1 ) 
    {
        my $zig = 0;

        $_h2 = $hashref2->{$k};

        next if $_h2==0;

        while ( ($_k,$__h1) = each %$_h1)
        {
            $__h2 = $_h2->{$_k};

            if($_k =~ 'configType')
            {
                if($__h1 != $__h2) #  && $__h2 > 0)
                {
                    print "$desc => $k -> configType: \x1b[36m$__h1\x1b[m vs \x1b[31m$__h2\x1b[m";

                    $zig = 1;
                }
            }

            if($_k =~ 'record')
            {
                while ( ($__k,$___h1) = each %$__h1)
                {
                    $___h2 = $__h2->{$__k};

                    if($___h1 != $___h2) #  && $___h2 > 0)
                    {
                        print "$desc => $k -> record -> $__k: \x1b[36m$___h1\x1b[m vs \x1b[31m$___h2\x1b[m";

                        $zig = 1;
                    }
                }
            }
        }

        if($zig == 1)
        {
            print '=' x 150;
        }  
    }
}

%HASH_trunk = parseRecord('/Users/highfly029/Documents/work/lost/Common/record/gameConfigRecord.xml');
%HASH_ptr = parseRecord('/Users/highfly029/Documents/work/lost_ptr/Common/record/gameConfigRecord.xml');
%HASH_release = parseRecord('/Users/highfly029/Documents/work/lost_release/Common/record/gameConfigRecord.xml');
compatibleCheck(\%HASH_ptr, \%HASH_trunk, 'ptr_vs_trunk');
compatibleCheck(\%HASH_ptr, \%HASH_release, 'ptr_vs_release');
compatibleCheck(\%HASH_trunk, \%HASH_release, 'trunk_vs_release');

%HASH_trunk = parseRecord('/Users/highfly029/Documents/work/lost/Common/record/commonConfigRecord.xml');
%HASH_ptr = parseRecord('/Users/highfly029/Documents/work/lost_ptr/Common/record/commonConfigRecord.xml');
%HASH_release = parseRecord('/Users/highfly029/Documents/work/lost_release/Common/record/commonConfigRecord.xml');
compatibleCheck(\%HASH_ptr, \%HASH_trunk, 'ptr_vs_trunk');
compatibleCheck(\%HASH_ptr, \%HASH_release, 'ptr_vs_release');
compatibleCheck(\%HASH_trunk, \%HASH_release, 'trunk_vs_release');
