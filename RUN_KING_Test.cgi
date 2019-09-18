#!/usr/bin/perl
use strict;
BEGIN { $CGITempFile::TMPDIRECTORY = '/data/www/TMP'; }	# Direct temnporary operation files to this directory
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

### Description: First drafted on August 21, 2019, last updated by Dr. Jeff Chen on September 11, 2019.

$CGI::POST_MAX = 1024 * 1024 * 5120 * 1024;		# Up to 4 G loading capability
my $safe_filename_characters = "a-zA-Z0-9_.-";		# For checking weird characters in loading files ro filename
my $upload_dir = "/data/www/TMP";                       # Put data in this directory
my $KGref = "/data/www/TMP/KGref";			# Reference dataset location
my $cmd = "king";

#my $prefix = "Test"."-$$-";				# For testing ..................................................
#my $KING_STDOUT = $prefix."KING_STDOUT";

my $now_start_time = localtime; 			# Moniter and timing 

my $start_run = time();					# Check the run tim for the CGI

my $query = new CGI;					# Use perl CGI module

my $related=$query->param("related");

my $Pedigree_Inference = $query->param("Pedigree_Inference");

my $Encryption = $query->param("Encryption");

print $query->header ( );                               # For error checking and debugging

#print "$Pedigree_Inference ***********";
#print "$related *********<br>";
#print "Encryption =====> $Encryption ********* <br>";

####################### Clean up the Workspace first #####################################################################

#print "<font color=white size=+5>Cleaning ********************************************************************** </font>";

#system("rm /data/www/TMP/*");				# Workspace for data and rresults ................................

#system("rm /data/www/TMP/Error_openSNP/*");
#system("rm /data/www/TMP/Error_openSNP/.RData");
#system("rm /data/www/TMP/Error_openSNP/._openSNP-merge3301.bed");
#system("rmdir /data/www/TMP/Error_openSNP/");

#exit(0);

####### Loading individual *.bed, *.bim and *.fam files ******************************************************************** 

my $filename = $query->param("bed");                    # Get *.bed file name
my $bim_filename=$query->param("bim");                  # Get *.bim file name
my $fam_filename=$query->param("fam");			# Get *.fam file name

my $bed_filename_prefix=$filename;			# For alternative file checking
my $bim_filename_prefix=$bim_filename;			# For alternative file checking
my $fam_filename_prefix=$fam_filename;			# For alternative file checking

$bed_filename_prefix =~s/.bed$//; 
$bim_filename_prefix =~s/.bim$//;
$fam_filename_prefix =~s/.fam$//;


if($bed_filename_prefix ne $bim_filename_prefix || $bed_filename_prefix ne $fam_filename_prefix){
print "<br><br><center><table><tr><td bgcolor=white><font color=blue size=+3>Error!  Uploaded Filenames Are Inconsistent, Execution Is Terminated !</font></td></tr></table></center><br><br><hr>";
exit(0);
}

my $prefix = "$bed_filename_prefix".".$$";		# Get the result ouput prefix
my $KING_STDOUT = $prefix.".KING_STDOUT";

my $zipped_filename = $query->param("photo");           # Using traditional photo as the large binary formated *.tar.gz file

#print "$filename<br>";					# Testing .....................
#print "$bim_filename<br>";
#print "$fam_filename<br>";


print "<br><br><center>";				 # Start the CGI program

print "<table bgcolor=white><tr><td><font color=red size=+3>CGI Starts: <b>$now_start_time</b></font></td><tr></table></center>";


########################################### For file format manipulaion to standarization #######################################

####### Checking Loaded *.bed file format ***************************************************************************************

my ( $name, $path, $extension ) = fileparse ( $filename, '..*' );

$filename = $name . $extension;

$filename =~ tr/ /_/;

$filename =~ s/[^$safe_filename_characters]//g;

if ( $filename =~ /^([$safe_filename_characters]+)$/ )
        {
	$filename = $1;
        }
elsif (!$zipped_filename)    {
	die "*.bed Filename contains invalid characters or no *.bed file uploaded !";
        }

########################################## Take care of the uploaded file data ####################################################

### *.bed file ************

if ($filename =~ /bed$/){

my $upload_filehandle = $query->upload("bed");

open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!";

binmode UPLOADFILE;
                                                                                # 1GB contains 8589934592 bites
while ( <$upload_filehandle> ){

        print UPLOADFILE;                                                       # Write data to server side directory

        }


close UPLOADFILE;

###  *.bim file format checking #------------------------------------


if ( !$bim_filename )                                                           # Test whether a file is uploaded
{
        #print $query->header ( );

        print "<br><br><center><b>Get *bim filename</b> ====> Did you upload a *.bim file ? Or there was a problem uploading your *.bim  data files !</center>";

        exit;                                                                    # exit, if no file is uploaded
}


my ( $name, $path, $extension ) = fileparse ( $bim_filename, '..*' );

$bim_filename = $name . $extension;

$bim_filename =~ tr/ /_/;

$bim_filename =~ s/[^$safe_filename_characters]//g;

if ( $bim_filename =~ /^([$safe_filename_characters]+)$/ )
        {
	$bim_filename = $1;
        }
else
    	{
	die "Bim Filename contains invalid characters or no *.bim file uploaded !";
        }


### *.bim file uploading #------------------------------------------

my $bim_upload_filehandle = $query->upload("bim");

open (UPLOADFILE, ">/data/www/TMP/$bim_filename") or die "$!";

binmode UPLOADFILE;

while ( <$bim_upload_filehandle> ){

        print UPLOADFILE;                                                               # Write data to server side directory

        }

close UPLOADFILE;

### *.fam file format checking #------------------------------------

if ( !$fam_filename )                                                               # Test whether a file is uploaded
{
       	#print $query->header ( );

	print "<br><br><center><b>Get *fam filename</b> ====> Did you upload a *.fam file ? Or there was a problem uploading your *.fam data files !</center>";

        exit;                                                                        # exit, if no file is uploaded
}

my ( $name, $path, $extension ) = fileparse ( $fam_filename, '..*' );

$fam_filename = $name . $extension;

$fam_filename =~ tr/ /_/;

$fam_filename =~ s/[^$safe_filename_characters]//g;

if ( $fam_filename =~ /^([$safe_filename_characters]+)$/ ){
       	$fam_filename = $1;
}else{
       	die "Fam Filename contains invalid characters or no *.fam file uploaded !";
}

####### *.fam file uploading #-----------------------------------------

my $fam_upload_filehandle = $query->upload("fam");

open (UPLOADFILE, ">/data/www/TMP/$fam_filename") or die "$!";

binmode UPLOADFILE;

while ( <$fam_upload_filehandle> ){

        print UPLOADFILE;                                                               # Write data to server side directory

}

close UPLOADFILE;

##################################### Response to the web #################################################################

print <<END_HTML;

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>KING Software Developmental Instance!</title>
<style type="text/css">img {border: none;}</style>
</head>

<body bgcolor=#efefef>
<br><br>

<!---------
<center>

<font color=darkgreen size=+3><b>This is the Developmental Instance of the
<a href="http://people.virginia.edu/~wc9c/KING/" target=KING>KING Software</a> Web System<br>
        Based on Our Previous <a href="http://people.virginia.edu/~xc3m/KING/" target=KING_Prototype>Prototype</b></a>
</font><br><br><hr>
<br><br>
<p><img src="http://king.cphg.virginia.edu/KING.png" alt="photo" /></p>
<br><hr><br>

<table><tr><td align=center>

************* <font color=blue size=+3><b>Run King Software on Back End Supercomputational Server</b></font> *************

<br><br><font color=darkgreen size=+2>System (\"king\") Call on KING Software ......</font><br><br>

<font color= red size=+2>Using  ===></font> <font color=blue>/var/www/html/king</font>, results are in the data directory of <font color=magenta>/data/www/TMP/</font>,
        using <font color=blue size=+1><b>$prefix</b></font> as prefix for KING Result Output Files
</td></tr></table>

<br><br><hr>

<center><br> <font color=red size=+4><i>Running KING Software Now .............. <br>Please Wait 1-2 Minutes for the Results to  Display below !</i></font></center><br><hr><br>

</center>

------------->

END_HTML


################################################## Run KING Software on Server Side ###########################################

my $cmd1 = "cd /data/www/TMP; /var/www/html/king  -b $filename";

my $cmd2 = " --related --degree 2 --rpath /usr/bin/R --rplot --prefix $prefix > /data/www/TMP/$KING_STDOUT";

if ($bed_filename_prefix ne $bim_filename_prefix){

	$cmd1 = $cmd1." --bim $bim_filename";

}

if($bed_filename_prefix ne $fam_filename_prefix){
	
	$cmd1 = $cmd1." --fam $fam_filename";

}

$cmd = $cmd1.$cmd2;


###### Complete KING cmd setting for testing ..........................................................................................

#$cmd ="cd /data/www/TMP; /var/www/html/king  -b $filename --related --degree 2 --rplot --prefix $prefix > /data/www/TMP/$KING_STDOUT ";

if ($Pedigree_Inference =~/Homozygosity/){

$cmd=$cmd1." --related --degree 2 --roh --rplot --prefix $prefix > /data/www/TMP/$KING_STDOUT";

}elsif($Pedigree_Inference =~/Ancestry_Inference/){

print "<center><table bgcolor=white><tr><td><font color=brown size=+2>Ancestry Inference Flag =====> Checked</font></center></td</tr></table><br>";
print "<center><font color=brown size=+2><b>Please wait for 5 minutes maximum for results to be displayed below as it is heavy and supercomputing .........</b></font></center><br><br>";

my $reference_set = "$KGref/KGref.bed";

#if($bed_filename_prefix ne $bim_filename_prefix || $bed_filename_prefix ne $fam_filename_prefix){
#print "<font color=blue size=+3>Error, Uploaded Filename Are Inconsistent, Execution Is Terminated !</font><br><br><hr>";
#exit(0);
#}

$cmd="cd /data/www/TMP; /var/www/html/king -b $reference_set,$filename --rpath /usr/bin/R --mds --projection --rplot --prefix $prefix > /data/www/TMP/$KING_STDOUT";

}

#my $cmd_print= "---->king  -b $filename --related --degree 2 --rplot --prefix $prefix"; 

my $cmd_print = $cmd;

print "<center><b><font color=magenta size=+3>Running KING (<font color=skyblue>1-2 Minutes</font>) on Backend Supercomputational Server:</font><br><br><font color=blue size=+2>\$CMD:</font> $cmd_print</b></center><br><hr>";


system("$cmd");

############## Encryption of result files **********************************************************************

system("/usr/bin/tar cf /data/www/TMP/$prefix.tar /data/www/TMP/$prefix*");                                                                     # Working .......

my $data_name=$prefix;

$data_name =~s/\.//;

my $encription_password= $data_name;

if($Encryption eq "PKZIP"){
system("/usr/bin/zip --password $encription_password  /data/www/TMP/$prefix.tar.zip /data/www/TMP/$prefix.tar > /data/www/TMP/ZIP.out");        # Working  .......
system("/usr/bin/mv /data/www/TMP/$prefix.tar.zip /data/www/TMP/Encryption");
print "<center>";
print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.zip\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";
print "Based on Password Protection of  <a href=\"https://courses.cs.ut.ee/MTAT.07.022/2015_fall/uploads/Main/dmitri-report-f15-16.pdf\" target=PKZIP><b>PKZIP/ZIP2.0</b></a> Format Encryption Mechanism!</h2>";
print "<i>This Encypted File Can Be Opened by ZIP Ultilities on Regular  Unix/Linux, Microsoft and Mac Windows Operating Systems.</i><br><br><hr>";
print "</center>";

}elsif($Encryption eq "AES256"){

print "<br><center>******** <i>As to How to Decrypt the Advanced Encrypted Result Files,  Please Contact Dr. Jeff Chen: xc3m\@virginia.edu for Technical Support</i> **********</center>";

system("/usr/bin/openssl enc -aes-256-cbc -salt -e -in /data/www/TMP/$prefix.tar -out /data/www/TMP/$prefix.tar.enc -k $encription_password");

system("/usr/bin/mv /data/www/TMP/$prefix.tar.enc /data/www/TMP/Encryption");

print "<center>";
print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.enc\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";
print "Based on the <a href=\"https://searchsecurity.techtarget.com/definition/Advanced-Encryption-Standard\" target=AES>Advanced Encryption Standard</a> of <a href=\"https://www.thesslstore.com/blog/what-is-256-bit-encryption/\" target=AES256><b>AES256</b></a> Encryption Mechanism!</h2><hr>";
print "</center>";

}elsif($Encryption eq "AES128"){

print "<br><center>******** <i>As to How to Decrypt the Advanced Encrypted Result Files,  Please Contact Dr. Jeff Chen: xc3m\@virginia.edu for Technical Support</i> **********</center>";

system("/usr/bin/openssl enc -aes-128-cbc -salt -e -in /data/www/TMP/$prefix.tar -out /data/www/TMP/$prefix.tar.enc -k $encription_password");

system("/usr/bin/mv /data/www/TMP/$prefix.tar.enc /data/www/TMP/Encryption");

print "<center>";
print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.enc\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";
print "Based on the <a href=\"https://searchsecurity.techtarget.com/definition/Advanced-Encryption-Standard\" target=AES>Advanced Encryption Standard</a> of <a href=\"https://www.idera.com/glossary/aes-128-bit-encryption\" target=AES128><b>AES128</b></a> Encryption Mechanism!</h2><hr>";
print "</center>";

}elsif($Encryption eq "AES192"){

print "<br><center>******** <i>As to How to Decrypt the Advanced Encrypted Result Files,  Please Contact Dr. Jeff Chen: xc3m\@virginia.edu for Technical Support</i> **********</center>";

system("/usr/bin/openssl enc -aes-192-cbc -salt -e -in /data/www/TMP/$prefix.tar -out /data/www/TMP/$prefix.tar.enc -k $encription_password");

system("/usr/bin/mv /data/www/TMP/$prefix.tar.enc /data/www/TMP/Encryption");

print "<center>";
print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.enc\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";
print "Based on the <a href=\"https://searchsecurity.techtarget.com/definition/Advanced-Encryption-Standard\" target=AES>Advanced Encryption Standard</a> of  <a href=\"https://www.thesslstore.com/blog/what-is-256-bit-encryption/\" target=AES192><b>AES192</b></a> Encryption Mechanism!</h2><hr>";
print "</center>";

}elsif($Encryption eq "Base64"){

print "<br><center>******** <i>As to How to Decrypt the Advanced Encrypted Result Files,  Please Contact Dr. Jeff Chen: xc3m\@virginia.edu for Technical Support</i> **********</center>";

system("/usr/bin/openssl enc -base64 -salt -e -in /data/www/TMP/$prefix.tar -out /data/www/TMP/$prefix.tar.base64 -k $encription_password");

system("/usr/bin/mv /data/www/TMP/$prefix.tar.base64 /data/www/TMP/Encryption");  # openssl enc -d -base64 -in  Test.97683.tar.base64 -out tmp-Test.97683.tar -k Test97683

print "<center>";
print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.base64\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";
print "Based on the <a href=\"https://searchsecurity.techtarget.com/definition/Advanced-Encryption-Standard\" target=AESBase64>Advanced Encryption Standard</a> of  <a href=\"https://en.wikipedia.org/wiki/Base64\" target=base64><b>base64</b></a> Encryption Mechanism!</h2><hr>";
print "</center>";

}

##### Display no encrypted files ********************************************************************************

system ("ls /data/www/TMP/ > /data/www/TMP/$prefix.Dir_File_List");

my $dir="/data/www/TMP/$prefix.Dir_File_List";

open (my $fh, '<:encoding(UTF-8)', $dir)

      or die "Could not open file==> '$dir' $!";

print "<br><center><table><tr><td align=center><font color=blue size=+3><b>Check Results Here !</b></font><br><hr><ol>";

while (my $row =<$fh>){

      chomp $row;

      if ($row=~m/^$prefix/ && $row !~m/Dir_File_List/){

        print "<li><a href=\"http://king.cphg.virginia.edu/TMP/$row\" target=$row>$row</a><br>\n";

        }

}

print "</ol></td></tr></table></center><br><hr><br>";

close ($fh);


} ### End of loading of individual *.bed, *.bim and *.fam files


if ($filename ne ""){

print <<END;
<center>
<font color=darkgreen size=+3><b>Genotype Datasets Client just Submitted for KING Analysis</b></font><br><br><br>

<table border=1><tr>
<td align=center><b>Client Uploaded Filename</b></td><td><b>Status</b></td>
</tr><tr>
<td><p>Client Submitted *.bed File : <a href="http://king.cphg.virginia.edu/TMP/$filename"><font color=red>$filename</font></a></p></td><td align=center><font color=blue>Good</font></td>
</tr><tr>
<td><p>Client Submitted *.bim File : <a href="http://king.cphg.virginia.edu/TMP/$bim_filename" target=User_Bim><font color=red>$bim_filename</font></a></p></td><td align=center><font color=blue>Good</font></td>
</tr><tr>
<td><p>Client Submitted *.fam File : <a href="http://king.cphg.virginia.edu/TMP/$fam_filename" target=User_Fam><font color=red>$fam_filename</font></a></p></td><td align=center><font color=blue>Good</font></td>
</tr></table>

<br><hr>

END

}

######## Loading *.tar.gz file ************************************************************************************************


if($Pedigree_Inference =~/Ancestry_Inference/ && $filename eq ""){

print "<br><center><table bgcolor=white><tr><td><font color=brown size=+2>Ancestry Inference Flag =====> Checked</font></center></td</tr></table><br>";

}elsif($filename =~/bed$/) {

print "<center><table><tr><td align=center>";
print "<font color=darkgreen size=+3><b>Thanks for Using the KING Software Web System<br> Hosted at the <a href=\"https://www.virginia.edu/\" target=UVA>University of Virginia</b></a> !</font><br>";
print "</td></tr></table></center>";

if($Pedigree_Inference !~ /Homozygosity/){

print <<END_HTML;
<center><br><hr><br>
<table bgcolor=white><tr><td>
<b>This <a href="https://en.wikipedia.org/wiki/Common_Gateway_Interface">CGI Program</a> was first  setup on August 21, 2019, last updated by <a href="http://people.virginia.edu/~xc3m/" target=Dr.XianfengJeffChen>Dr. Jeff Chen</a>
(<a href="https://www.linkedin.com/in/xianfeng-jeff-chen-ph-d-50b36772" target=Dr.Xianfeng(Jeff)Chen>
<img src="../linkedin.png">&nbsp</a>
<a href="https://twitter.com/XianfengC" target=Dr.JeffChen><img src="../twitter.png">&nbsp&nbsp</a>
<a href="https://www.youtube.com/watch?v=KYQ2dPW5nEU" target=ComputationAndSystemsBiology><img src="../youtube.png"></a>)
on September 11, 2019.</b>
END_HTML

}

print "</td></tr></table></center>";

}else{

        print "<br><center><table bgcolor=skyblue><tr><td align=center><font color=yellow size=+3><b>If No Immediate Result Display below, Please Wait for 30 Seconds to 1 Minute for Supercomputing!</b></font></center></td></tr></table><br><hr>";
}


################################################################################################################################

#system("rm /data/www/TMP/*");				# Clean the workspace first ...........................................
#system("rm /data/www/TMP/hapmap/*");
#system("rm /data/www/TMP/hapmap/.RData");
#system("rmdir /data/www/TMP/hapmap/");


#system("rm $upload_dir/ex/*");				# Do some cleaning up for working direcotry

system("rm /data/www/TMP/openSNP/*");			# openSNP test dataset
#system("rm /data/www/TMP/openSNP/openSNP/*");
#system("rm /data/www/TMP/openSNP/._openSNP-merge3301.bed");
#system("rm /data/www/TMP/openSNP/.RData");
#system("rmdir /data/www/TMP/openSNP/openSNP/");
#system("rmdir /data/www/TMP/openSNP/");

#system("rm /data/www/TMP/JeffopenSMP/*");
#system("rm /data/www/TMP/JeffopenSMP/.RData");
#system("rmdir /data/www/TMP/JeffopenSMP/");

#system("rm $upload_dir/Dir_File_List*");
#system("rm $upload_dir/CGItemp*");
#system("rm $upload_dir/KGref/.RData");
#system("rm /data/www/TMP/KGref/*");
#system("rmdir $upload_dir/KGref");
#system("rm $upload_dir/ex/.RData");
#system("rmdir $upload_dir/ex/");
#system("rm /data/www/TMP/Test/*");
#system("rm /data/www/TMP/Test/.RData");
#system("rmdir rm /data/www/TMP/Test/");

#exit(0);						# Finsihed cleanup .....................................................

#################################################################################################################################

if ( !$zipped_filename && !$filename)                                # Test whether a file is uploaded
{
        print "<br><br><center><b>Get data (*.bed or *.tar.gz) filename</b> ====> Did you upload a binary file ? Or there was a problem uploading your binary data files !</center>";

        exit;                                            # exit, if no file is uploaded, this can be disabled in last version
}


########################################### For file format manipulaion to standarization #########################################

if(!$filename){

my ( $name, $path, $extension ) = fileparse ( $zipped_filename, '..*' );

my $zipped_filename = $name . $extension;

$zipped_filename =~ tr/ /_/;

$zipped_filename =~ s/[^$safe_filename_characters]//g;

if ( $zipped_filename =~ /^([$safe_filename_characters]+)$/ )
        {
	$zipped_filename = $1;
        }
else    {
	print "*.tar.gz Filename contains invalid characters or no *.bed file uploaded !";
        }


########################################## Save the uploaded zipped file to backend disk ##########################################

my $load_time = time();						# Stampled the starting point of loading time

my $upload_filehandle = $query->upload("photo");		# File handler for data manipulation

open ( UPLOADFILE, ">$upload_dir/$zipped_filename" ) or die "$!";

binmode UPLOADFILE;						# Binary write to disk

                                                                # 1GB contains 8589934592 bites
while ( <$upload_filehandle> ){

        print UPLOADFILE;                                       # Write data to server side directory

        }

close UPLOADFILE;						# Safely close the file handler and leave cash memory

my $loaded_time = time();					# Stampled the finsihing loading time

my $finished_loaded_time =localtime;

#print "Finished Loading: <b>$finished_loaded_time</b><br>";

my $time_to_load = $loaded_time - $load_time;			# Check how much time taken for loading the large data file

#print "Time Taken to Loaded: <b>$time_to_load</b><br>";

#print $query->header ( );					# for error checking and debugging

#print "$zipped_filename ====> $zipped_filename\n<br><br>";	# For debugging ............


################################ Un-zip and un-tar the uploaded file ***************************************************************

my $data_dir = $zipped_filename;				# Get the uploaded filename

$data_dir =~s/.tar.gz$//;					# Just the file name .......

#$data_dir=$data_dir.$$;					# Add the process ID to data diretory	

my $prefix="$data_dir.$$";                                      # Add process ID to make filesa and results unique

my $data_name =$data_dir;

#$data_dir="ex";						# For testing ......................................................

#system ("mkdir $upload_dir/$data_dir");			# for making a working direcotry on backend server

#print "directory name ===> $data_dir<br><br>";			# For error checking

system("gunzip $upload_dir/$zipped_filename");			# Unzip the laoded file

$zipped_filename =~s/.gz$//;					# Get the *.tar filename

#print "unziped ====> $zipped_filename<br>";			# For error checking

								# untar the tared uploaded file, out in data directroy

#system("tar xvf $upload_dir/$zipped_filename -C $upload_dir/$data_dir > $upload_dir/tar_file_list");

system("tar xvf $upload_dir/$zipped_filename -C $upload_dir > $upload_dir/tar_file_list");

my $test_Bed_file = $data_dir.".bed";

#print "test_Bed_file ====> $test_Bed_file<br><br>";

if (-e "$upload_dir/$test_Bed_file"){
	$data_dir=$upload_dir;
}else{
	system ("mkdir $upload_dir/$data_dir");
	#print "directory name ===> $data_dir<br><br>";           # For error checking
	$data_dir=$upload_dir."/".$data_dir;

}

#print "Data Directory Name ===> $data_dir<br><br>";


##### ....................... Do some cleaning up on the zipped file loaded working directory ...........................#######

system("rm $upload_dir/*.gz");					
system("rm $upload_dir/*.tar"); 
system("rm $upload_dir/tar_file_list");

#exit(0);							# For cleaning up in debugging ...................................

################################ Run King ########################################################################################

my $bed=""; my $bim=""; my $fam="";				# Used to get the *.bed, *.bim, and *.fam file names for KING analysis

system ("ls $data_dir > $data_dir/$prefix.Data_File_List");

open (my $fh, '<:encoding(UTF-8)', "$data_dir/$prefix.Data_File_List")

      or die "Could not open file==> '$prefix.Data_File_List' $!";


while (my $row =<$fh>){						# Get the uploaded data filename

      chomp $row;
 
	if($row=~m/.bed$/){
	$bed=$row;
	#print "Got ==> $bed<br>";				# Get the *.bed filename
	}

	if($row=~m/.bim$/){
	$bim=$row;
	#print "Got ==> $bim<br>";				# Get the *.bim filename
	}

	if($row=~m/.fam$/){
	$fam=$row;						# Get the *.fam filename
	#print "Got ==> $fam<br>";

	}
}

my $bed_filename=$bed;						# Copy file name for testing whether altnative *.bim or *.fam files provided
my $bim_filename=$bim;
my $fam_filename=$fam;
$bed_filename=~s/.bed//;					# Remove the file prefix to be used in script callings
$bim_filename=~s/.bim//;
$fam_filename=~s/.fam//;

#print "$bed_filename ===> $bim_filename ===> $fam_filename *********<br>";

my $cmd="run king ....";					# Prepare to run KING software

my $cmd1 = " cd $data_dir; /var/www/html/king -b $data_dir/$bed";

my $cmd2 = " --related --rplot --degree 2 --rpath /usr/bin/R --prefix $data_dir/$prefix  > $data_dir/$prefix.\"STDOUT\"";


#####*********************************************** Basic Parameter Setting for KING to Run *********************************######## 

if($bed_filename eq $bim_filename && $bim_filename eq $fam_filename && $bed_filename eq $fam_filename){
	$cmd=$cmd1.$cmd2;
}								# Run if all the 3 file names are the same ---- *.bed, *.bim, *.fam

if($bed_filename ne $fam_filename){
	$cmd1= $cmd1." --fam $upload_dir/$data_dir/$fam;"		# *.fam	is an alternative file
}								


if($bed_filename ne $bim_filename){

	$cmd1= $cmd1." --bim $upload_dir/$data_dir/$bim";		# *.bim	is an alternative file
}

my $reference_data = "$KGref/KGref.bed";

if ($Pedigree_Inference =~/Ancestry_Inference/){

	if($related =~/on/){

		$cmd="cd $data_dir; /var/www/html/king -b $reference_data,$bed --related --rpath /usr/bin/R --mds --projection --rplot --prefix $data_dir/$prefix  > $data_dir/$prefix.STDOUT";
	
	}else{

	 	$cmd="cd $data_dir; /var/www/html/king -b $reference_data,$bed --rpath /usr/bin/R --mds --projection --rplot --prefix $data_dir/$prefix  > $data_dir/$prefix.STDOUT";

	}

}elsif($Pedigree_Inference =~/Homozygosity/){

	if($related=~/on/){

		$cmd="cd $data_dir; /var/www/html/king -b $bed --related --rpath /usr/bin/R --roh --rplot --prefix $data_dir/$prefix  > $data_dir/$prefix.STDOUT";

	}else{
		$cmd="cd $data_dir; /var/www/html/king -b $bed --rpath /usr/bin/R --roh --rplot --prefix $data_dir/$prefix  > $data_dir/$prefix.STDOUT";
	}
}else{
	$cmd = $cmd1.$cmd2;
}

if ($Pedigree_Inference =~ /Ancestry_Inference/){

print "<br><center><table bgcolor=lightskyblue><tr><td align=center><font color=brown size=+3 ><b><blink>Running KING Software on the Backend Supercomputers</blink> ..........</font><br>";

#print "<br>$cmd </b></center><br><br>";				# For debugging ...................................................

print "<center><font color=yellow size=+2><br><b>If Running Ancestry Inference and No Immediate Results Show up below, Please Wait for up to 3-5 Minutes for the Results to Display .....</b></font></td></tr></table><br><hr></center>";

if($data_dir eq $upload_dir){
	
	print "<br><center><table bgcolor=white><tr><td align=center><font size=+2>5 Minutes Late, Please <a href=\"http://king.cphg.virginia.edu/cgi-bin/CheckResults.cgi?a=$$&c=$Encryption&d=$prefix\" target=Check_Results><font color=magenta size=+2> Check Results Here</font></a>";
}else{

	print "<br><center><table bgcolor=white><tr><td align=center><font size=+2> If Results Do Not Display below within Two Minutes, Please <a href=\"http://king.cphg.virginia.edu/cgi-bin/CheckResults.cgi?a=$$&b=$data_name&c=$Encryption&d=$prefix\" target= Check_results><font color=magenta size=+2> Check Results Here</font></a> 5 Minutes Late";

}

print ", If Running Ancestry Inference as It Is Time Consuming and Heavy Supercomputing.....</font></td></tr></table></center><br><br><hr>";

}

print "<br><center><table bgcolor=white><tr><td align=center><font color=red size++3><b>CMD: </b></font>$cmd</td></tr></table></center><br><hr><br>";

print "<center><img src=\"../KING.png\"><br><br><table><tr><td bgcolor=white><font color=darkgreen size=+2>****** Running KING with Backend Supercomputing, Please Wait for Results to Display below ******</font></td></tr></table></center>";

if($Pedigree_Inference =~ /Ancestry_Inference/){

print <<END_HTML;

<center><br><hr><br>
<table bgcolor=white><tr><td>
<b>This <a href="https://en.wikipedia.org/wiki/Common_Gateway_Interface">CGI Program</a> was first  setup on August 21, 2019, last updated by <a href="http://people.virginia.edu/~xc3m/" target=Dr.XianfengJeffChen>Dr. Jeff Chen</a>
(<a href="https://www.linkedin.com/in/xianfeng-jeff-chen-ph-d-50b36772" target=Dr.Xianfeng(Jeff)Chen>
<img src="../linkedin.png">&nbsp</a>
<a href="https://twitter.com/XianfengC" target=Dr.JeffChen><img src="../twitter.png">&nbsp&nbsp</a>
<a href="https://www.youtube.com/watch?v=KYQ2dPW5nEU" target=ComputationAndSystemsBiology><img src="../youtube.png"></a>)
on September 10, 2019.</b>
</td></tr></table>
</center><br><hr>

</body>
</html>

END_HTML

}

system("$cmd");							# Run KING software .........................................................

###############################################################################

#system("rm $upload_dir/$data_dir/$bed");
#system("rm $upload_dir/$data_dir/$bim");
#system("rm $upload_dir/$data_dir/$fam");
#system("rm $upload_dir/$data_dir/tmp*");
#system("rm $upload_dir/$data_dir/Jeff_Dev.*");

################################################################################

print <<START_HTML;

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>KING Software Developmental Instance!</title>
<style type="text/css">img {border: none;}</style>
</head>

<body bgcolor=#efefef>

START_HTML

################################ Display Results #####################################################################

system("/usr/bin/tar cf /data/www/TMP/$prefix.tar /data/www/TMP/$prefix*");									# Working .......

my $encription_password= $data_name.$$;

if($Encryption eq "PKZIP"){

system("/usr/bin/zip --password $encription_password  /data/www/TMP/$prefix.tar.zip /data/www/TMP/$prefix.tar > /data/www/TMP/ZIP.out");  	# Working  .......

system("/usr/bin/mv /data/www/TMP/$prefix.tar.zip /data/www/TMP/Encryption");

print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.zip\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";

print "Based on Password Protection of <a href=\"https://courses.cs.ut.ee/MTAT.07.022/2015_fall/uploads/Main/dmitri-report-f15-16.pdf\" target=PKZIP> <b>PKZIP/ZIP2.0</b></a> Format Encryption Mechanism!</h2>";

print "<i>This Encypted File Can Be Opened by ZIP Utilities on Regular Unix/Linix, Microsoft and Mac Windows Operating Systems.</i><br><br><hr>";

}elsif($Encryption eq "AES256"){

system ("/usr/bin/openssl enc -aes-256-cbc -salt -e -in /data/www/TMP/$prefix.tar -out /data/www/TMP/$prefix.tar.enc -k $encription_password");

system("/usr/bin/mv /data/www/TMP/$prefix.tar.enc /data/www/TMP/Encryption");

print "<br><center>******** <i>As to How to Decrypt the Advanced Encrypted Result Files,  Please Contact Dr. Jeff Chen: xc3m\@virginia.edu for Technical Support</i> **********</center>";

print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.enc\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";

print "Based on the <a href=\"https://searchsecurity.techtarget.com/definition/Advanced-Encryption-Standard\" target=AES>Advanced Encryption Standard</a> of <a href=\"https://en.wikipedia.org/wiki/Advanced_Encryption_Standard\" target=AES256><b>AES256</b></a> Encryption Mechanism!</h2><hr>";

}elsif($Encryption eq "AES128"){

system ("/usr/bin/openssl enc -aes-128-cbc -salt -e -in /data/www/TMP/$prefix.tar -out /data/www/TMP/$prefix.tar.enc -k $encription_password");

system("/usr/bin/mv /data/www/TMP/$prefix.tar.enc /data/www/TMP/Encryption");

print "<br><center>******** <i>As to How to Decrypt the Advanced Encrypted Result Files,  Please Contact Dr. Jeff Chen: xc3m\@virginia.edu for Technical Support</i> **********</center>";

print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.enc\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";

print "Based on the <a href=\"https://searchsecurity.techtarget.com/definition/Advanced-Encryption-Standard\" target=AES>Advanced Encryption Standard</a> of  <a href=\"https://en.wikipedia.org/wiki/Advanced_Encryption_Standard\" target=AES128><b>AES128</b></a> Encryption Mechanism!</h2><hr>";

}elsif($Encryption eq "AES192"){

system ("/usr/bin/openssl enc -aes-192-cbc -salt -e -in /data/www/TMP/$prefix.tar -out /data/www/TMP/$prefix.tar.enc -k $encription_password");

system("/usr/bin/mv /data/www/TMP/$prefix.tar.enc /data/www/TMP/Encryption");

print "<br><center>******** <i>As to How to Decrypt the Advanced Encrypted Result Files,  Please Contact Dr. Jeff Chen: xc3m\@virginia.edu for Technical Support</i> **********</center>";

print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.enc\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";

print "Based on the <a href=\"https://searchsecurity.techtarget.com/definition/Advanced-Encryption-Standard\" target=AES>Advanced Encryption Standard</a> of <a href=\"https://en.wikipedia.org/wiki/Advanced_Encryption_Standard\" target=AES192><b>AES192</b></a> Encryption Mechanism!</h2><hr>";

}elsif($Encryption eq "Base64"){

print "<br><center>******** <i>As to How to Decrypt the Advanced Encrypted Result Files,  Please Contact Dr. Jeff Chen: xc3m\@virginia.edu for Technical Support</i> **********</center>";

system("/usr/bin/openssl enc -base64 -salt -e -in /data/www/TMP/$prefix.tar -out /data/www/TMP/$prefix.tar.base64 -k $encription_password");

system("/usr/bin/mv /data/www/TMP/$prefix.tar.base64 /data/www/TMP/Encryption");

print "<center>";
print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.base64\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";
print "Based on the <a href=\"https://searchsecurity.techtarget.com/definition/Advanced-Encryption-Standard\" target=AES>Advanced Encryption Standard</a> of <a href=\"https://en.wikipedia.org/wiki/Base64\" target=base64><b>base64</b></a> Encryption Mechanism!</h2><hr>";
print "</center>";

}

if($Pedigree_Inference =~/Ancestry_Inference/){

	print "<h2>****** Running KING with the above CMD ******</h2><hr>";
}


#####  Display no cripted data here *****************************************************************************

system ("ls $data_dir > $data_dir/$prefix.Result_File_List");

my $dir="$data_dir/$prefix.Result_File_List";

open (my $fh, '<:encoding(UTF-8)', $dir)

      or die "Could not open file==> '$dir' $!";

my $i=0;

print "<br><center><table><tr><td align=center><font color=blue size=+3><b>Results Here !</b></font><br><hr><ol>";

while (my $row =<$fh>){

      chomp $row;

#print "$row ===> $prefix<br>";

      if ($row=~m/$prefix/ && $row !~m/File_List/){
       		if($data_dir eq "$upload_dir"){
        		print "<li><a href=\"http://king.cphg.virginia.edu/TMP/$row\" target=$row>$row</a><br>\n";
		}else {
			print "<li><a href=\"http://king.cphg.virginia.edu/TMP/$data_name/$row\" target=$row>$row</a><br>\n";
		}
       }

      $i++;
}

print "</ol>";
print "</td></tr></table>";
print "</center>";

my $ending_time = localtime;

#print "CGI Ends: <b>$ending_time</b><br>";

my $end_run = time();

my $run_time = $end_run - $start_run;

print "<br><center><font color=darkgreen size=+2><b>Summary of Computational Time</b></font></center><br>";
print "<center><table border=1><tr>";
print "<td>CGI Starts:</td><td> <b>$now_start_time</b></td></tr><tr>";
print "<td>Finished Loading:</td><td> <b>$finished_loaded_time</b></td></tr><tr>";
print "<td>CGI Ends:</td><td><b>$ending_time</b></td></tr><tr>";
print "<td>The CGI Job Taken:</td><td align=center>  <b>$run_time Seconds</b>";
print "</td></tr></table> </center><br>";

} #### end of if no *.bed file and only loaded *.tar.gz file

###################################################################################

if($Pedigree_Inference !~/Ancestry_Inference/){

print <<END_HTML;

<center><br><hr><br>
<b>This <a href="https://en.wikipedia.org/wiki/Common_Gateway_Interface">CGI Program</a> was first  setup on August 21, 2019, last updated by <a href="http://people.virginia.edu/~xc3m/" target=Dr.XianfengJeffChen>Dr. Jeff Chen</a>
(<a href="https://www.linkedin.com/in/xianfeng-jeff-chen-ph-d-50b36772" target=Dr.Xianfeng(Jeff)Chen>
<img src="../linkedin.png">&nbsp</a>
<a href="https://twitter.com/XianfengC" target=Dr.JeffChen><img src="../twitter.png">&nbsp&nbsp</a>
<a href="https://www.youtube.com/watch?v=KYQ2dPW5nEU" target=ComputationAndSystemsBiology><img src="../youtube.png"></a>)
on September 11, 2019.</b>
</center><br><hr><br>

</body>
</html>

END_HTML

}
exit(0);


