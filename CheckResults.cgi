#!/usr/bin/perl
use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
### Description: To retrieval the results for large computing.
### First drafted on August 28, last updated by Dr. Jeff Chen on August 29, 2018.

my $Process_ID = @ARGV[0];		#
my $data_dir = @ARGV[1];
my $Encryption = @ARGV[2];
my $prefix = $ARGV[3];

 
#print "$Process_ID<br>\n";
#print "$data_dir<br>\n";

my $query = new CGI; 

print $query->header ( );

$Process_ID= $query->param("a");
$data_dir = $query->param("b");
$Encryption = $query->param("c");
$prefix = $query->param("d"); 


my $encription_password= $prefix;
$encription_password =~s/\.//g;

#print "$Process_ID<br>\n";
#print "$data_dir<br>\n";

if($data_dir eq ""){
	system ("ls /data/www/TMP > /data/www/TMP/Dir_File_List.$$");
}else{
	system ("ls /data/www/TMP/$data_dir > /data/www/TMP/Dir_File_List.$$");
}



print "<br><center><img src=\"../KING.png\"></center>";


my $dir="/data/www/TMP/Dir_File_List.$$";

open (my $fh, '<:encoding(UTF-8)', $dir)

      or die "Could not open file==> '$dir' $!";

my $i=0;

print "<br><br><center><table bgcolor=white><tr><td align=center><font color=blue size=+3><b>Download Ancestry Inference Results Here !</b></font><br><hr><br><ol>";

while (my $row =<$fh>){

      chomp $row;

#$Process_ID ="175868";

      if ($row =~/$Process_ID/ && $row !~m/Data_File_List/){

		if($data_dir eq ""){
        		print "<li><a href=\"http://king.cphg.virginia.edu/TMP/$row\" target=$row>$row</a><br>\n";
		}else{
			print "<li><a href=\"http://king.cphg.virginia.edu/TMP/$data_dir/$row\" target=$row>$row</a><br>\n";
		}
        }

      $i++;
}

print "</ol></td></tr></table></center><br><hr>";

close ($fh);

system("rm /data/www/TMP/Dir_File_List*");

######################### Display Encrypted Data **********************************************************************************************************************************


print "<center><table><tr><td bgcolor=white>";

if($Encryption eq "PKZIP"){

print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.zip\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";

print "Based on Password Protection of <a href=\"https://courses.cs.ut.ee/MTAT.07.022/2015_fall/uploads/Main/dmitri-report-f15-16.pdf\" target=PKZIP> <b>PKZIP/ZIP2.0</b></a> Format Encryption Mechanism!</h2>";

print "<i>This Encypted File Can Be Opened by ZIP Utilities on Regular Unix/Linix, Microsoft and Mac Windows Operating Systems.</i><br><br>";

}elsif($Encryption eq "AES256"){

print "<br><center>******** <i>As to How to Decrypt the Advanced Encrypted Result Files,  Please Contact Dr. Jeff Chen: xc3m\@virginia.edu for Technical Support</i> **********</center>";

print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.enc\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";

print "Based on the <a href=\"https://searchsecurity.techtarget.com/definition/Advanced-Encryption-Standard\" target=AES>Advanced Encryption Standard</a> of <a href=\"https://en.wikipedia.org/wiki/Advanced_Encryption_Standard\" target=AES256><b>AES256</b></a> Encryption Mechanism!</h2>";

}elsif($Encryption eq "AES128"){

print "<br><center>******** <i>As to How to Decrypt the Advanced Encrypted Result Files,  Please Contact Dr. Jeff Chen: xc3m\@virginia.edu for Technical Support</i> **********</center>";

print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.enc\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";

print "Based on the <a href=\"https://searchsecurity.techtarget.com/definition/Advanced-Encryption-Standard\" target=AES>Advanced Encryption Standard</a> of  <a href=\"https://en.wikipedia.org/wiki/Advanced_Encryption_Standard\" target=AES128><b>AES128</b></a> Encryption Mechanism!</h2>";

}elsif($Encryption eq "AES192"){

print "<br><center>******** <i>As to How to Decrypt the Advanced Encrypted Result Files,  Please Contact Dr. Jeff Chen: xc3m\@virginia.edu for Technical Support</i> **********</center>";

print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.enc\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";

print "Based on the <a href=\"https://searchsecurity.techtarget.com/definition/Advanced-Encryption-Standard\" target=AES>Advanced Encryption Standard</a> of <a href=\"https://en.wikipedia.org/wiki/Advanced_Encryption_Standard\" target=AES192><b>AES192</b></a> Encryption Mechanism!</h2>";

}elsif($Encryption eq "Base64"){

print "<br><center>******** <i>As to How to Decrypt the Advanced Encrypted Result Files,  Please Contact Dr. Jeff Chen: xc3m\@virginia.edu for Technical Support</i> **********</center>";

print "<center>";

print "<h2><a href=\"http://king.cphg.virginia.edu/TMP/Encryption/$prefix.tar.base64\"><font color=magenta><b>Download Encrypted Result Data Here</font></a> with Accessing Password: <font color=magenta>$encription_password </b></font><br>";

print "Based on the <a href=\"https://searchsecurity.techtarget.com/definition/Advanced-Encryption-Standard\" target=AES>Advanced Encryption Standard</a> of <a href=\"https://en.wikipedia.org/wiki/Base64\" target=base64><b>base64</b></a> Encryption Mechanism!</h2>>";

print "</center>";

}

print "</td></tr></table></center>";




print <<END_HTML;

<center><br><hr><br>

<table bgcolor=white><tr><td align=center>
<b><br>This <a href="https://en.wikipedia.org/wiki/Common_Gateway_Interface">CGI Program</a> was first  setup on August 28, 2019, last updated by <a href="http://people.virginia.edu/~xc3m/" target=Dr.XianfengJeffChen>Dr. Jeff Chen</a>
(<a href="https://www.linkedin.com/in/xianfeng-jeff-chen-ph-d-50b36772" target=Dr.Xianfeng(Jeff)Chen>
<img src="../linkedin.png">&nbsp</a>
<a href="https://twitter.com/XianfengC" target=Dr.JeffChen><img src="../twitter.png">&nbsp&nbsp</a>
<a href="https://www.youtube.com/watch?v=KYQ2dPW5nEU" target=ComputationAndSystemsBiology><img src="../youtube.png"></a>)
on September 11, 2019.</b><br><br><br></td><tr></table>
</center><br><hr><br>

</body>
</html>

END_HTML


exit(0);
