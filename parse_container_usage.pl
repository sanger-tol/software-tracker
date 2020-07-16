#!/usr/bin/perl

# Original file at /nfs/pathogen/user-tracking/container_usage.csv

$first = 1 ;
print "INSERT IGNORE INTO `logging_event` (`uuid`,`user`,`image`,`timestamp`,`path`,`executable`,`parameters`,`origin`) VALUES \n" ;

while ( <> ) {
	if ( $_ =~ m~^(path[a-z]+|[a-z]{2,3}\d*),(\d{8}_\d{6}),(.{3,})$~ ) {
		my $user = $1 ;
		my $timestamp = $2 ;
		my $image = $3 ;
		to_sql ( $user , $image , $timestamp , '' , '' , '' ) ;
	} elsif ( $_ =~ m~^(path[a-z\-]+|[a-z]{2,3}\d*),(\d{8}_\d{6}),(/[^,]{3,}),(/[^,]{3,}),(.+?),(.*)$~ ) {
		my $user = $1 ;
		my $timestamp = $2 ;
		my $image = $3 ;
		my $path = $4 ;
		my $executable = $5 ;
		my $parameters = $6 ;
		to_sql ( $user , $image , $timestamp , $path , $executable , $parameters ) ;
	} else {
		#print $_ ;
		next ;
	}
}

print ";\n" ;

sub escape {
	my ( $s ) = @_ ;
	$s =~ s/^\s+// ;
	chomp $s ;
	$s =~ s/'/\\'/g ;
	return $s ;
}

sub to_sql {
	my ( $user , $image , $timestamp , $path , $executable , $parameters ) = @_ ;
	$user = escape ( $user ) ;
	$image = escape ( $image ) ;
	$timestamp = escape ( $timestamp ) ;
	$timestamp =~ s/^(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})$/$1:$2:$3 $4:$5:$6/ ;
	$path = escape ( $path ) ;
	$executable = escape ( $executable ) ;
	$parameters = escape ( $parameters ) ;
	if ( $first == 1 ) {
		$first = 0 ;
	} else {
		print ",\n" ;
	}
	print "(uuid() , '$user' , '$image' , '$timestamp' , '$path' , '$executable' , '$parameters' , 'logfile' )" ;
}