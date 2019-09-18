#!/usr/bin/perl
use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

my $query = new CGI;

print $query->header ( );  

my $username = $query->param("Username");
my $full_name= $query->param("Full_Name");
my $email =$query->param("Email");
my $organization = $query->param("Organization");

my $password = $query->param("Initial_Password");
my $confirmed_password = $query->param("Confirmed_Password");

my $cmd = "/usr/bin/htpasswd -b /data/www/TMP/.htpasswd $username $password";
system ("$cmd");				# Working ................

print "<br><br><center><h2>Thanks for the Info Submitted:<br></h2><table><tr><td><hr>";
print "Username ===> $username<br>";
print "Full Name ===> $full_name<br>";
print "Email ===> $email<br>";
print "Organization ===> $organization<hr><br>";

if ($password ne $confirmed_password){
	print "<br><font color=red size=+2>Passwords are not the same, please reset!</font><br><hr><br>";
	exit(0);
}

print "</td></tr></table>";

print "<br><font color=dargreen size=+2><b>Thanks <font color=darkgreen>$username</font> for registering in using Virginia KING Web System!<br><br>Please Login in Now !<br>";
print " <br>You Will Be Contacted by Members of Our Administrative Team for the Next Steps in the Registration Process.</b></font><br><br>";

################# Sending responding email  ********************************************

my($mailprog) = '/usr/sbin/sendmail';

my ($from_address) ='king@kingserver.UVA.edu';

my ($to_address) = "$email, xc3m\@virginia.edu, xianfengchen05\@gmail.com";

       open (MAIL, "|$mailprog -t $to_address") || die "Can't open $mailprog!\n";

       print MAIL "To: $to_address\n";
       print MAIL "From: $from_address\n";
       print MAIL "Subject: Thanks for Registering with";
       print MAIL " UVA KING Web!\n";
       print MAIL "Greeting from Virginia KING Web Server, Says Hello to User: $username .....\n\n";

       print MAIL "You Will Be Contacted by Members of Our Administrative Team for the Next Steps in the Registration Process.\n\n ";
       
       print MAIL "If You Have Technical Issues, Please Contact Dr. Jeff Chen at xc3m\@virginia.edu,\n\nThanks, \n\nBye Now !\n\n";
       
	close (MAIL);

system("mkdir /data/www/TMP/Encryption");

my $Client_Data ="/data/www/TMP/user.$$.txt";

my $datestring = localtime();

open(my $fh, ">$Client_Data");

print $fh "$username\t";
print $fh "$full_name\t";
print $fh "$email\t";
print $fh "$organization\t";

print $fh "$password\t";
print $fh "$confirmed_password\t";
print $fh "$datestring\n\n";

close ($fh);

system("/usr/bin/cat $Client_Data >> /data/www/TMP/Email/Client_DATA");
system("mv $Client_Data /data/www/TMP/Email/");

##### Testing zip file *************************************************

system("/usr/bin/tar cf /data/www/TMP/Ex.tar /data/www/TMP/EX"); 				# Works ......


#system("/usr/bin/zip --password jeff /data/www/TMP/Ex.tar.zip /data/www/TMP/Ex.tar");		# Works ...... for zip

system("/usr/bin/openssl enc -aes-256-cbc -salt -e -in /data/www/TMP/Ex.tar -out /data/www/TMP/Ex.tar.enc -k jeff");	# Encrypt the file ........... for openssl

#openssl enc -aes-256-cbc -salt -d -e -in ex.119897.tar02.enc -out ex.119897.tar.unenc -k jeff		# Decrypt the file

system("/usr/bin/mv /data/www/TMP/Ex.tar.enc /data/www/TMP/Encryption");

print <<END_HTML;

<center><a href="http://king.cphg.virginia.edu/TMP/Email/Client_DATA"><h2>Registered Data Here</h2></a></center>

<!---
<center><a href="http://king.cphg.virginia.edu/TMP/.htpasswd"><h2>Password File Here</h2></a></center>
---->


<center><br><hr><br>
<b>This <a href="https://en.wikipedia.org/wiki/Common_Gateway_Interface">CGI Program</a> was first  setup on August 23, 2019, last updated by <a href="http://people.virginia.edu/~xc3m/" target=Dr.XianfengJeffChen>Dr.$
(<a href="https://www.linkedin.com/in/xianfeng-jeff-chen-ph-d-50b36772" target=Dr.Xianfeng(Jeff)Chen>
<img src="../linkedin.png">&nbsp</a>
<a href="https://twitter.com/XianfengC" target=Dr.JeffChen><img src="../twitter.png">&nbsp&nbsp</a>
<a href="https://www.youtube.com/watch?v=KYQ2dPW5nEU" target=ComputationAndSystemsBiology><img src="../youtube.png"></a>)
on September 10, 2019.</b>
</center><br><hr><br>

</body>
</html>

END_HTML

exit(0);


