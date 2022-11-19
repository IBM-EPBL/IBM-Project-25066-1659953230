<?php
include('config.php');
session_start();
if (isset($_POST['apply']))
{
	$email=$_SESSION['email'];
	$filename=$_FILES['files']['name'];
	$tmp=$_FILES['files']['tmp_name'];
	$path='uploads/'.$filename;
	move_uploaded_file($tmp,$path);
	
	$result=mysqli_query($con,"update register set FName='".$_POST['fname']."',Mobile='".$_POST['mobile']."',College='".$_POST['college']."',Qualfi='".$_POST['qual']."',Resume='$filename',Descriptions='".$_POST['desc']."',Skills='".$_POST['skills']."',Area='".$_POST['area']."',LName='".$_POST['lname']."' where Email='$email'");
	if($result)
	{
			header("Location:dashboard.php");
	
	}
	else {
		echo '<script language="javascript">alert("Please Try Again");location.href=\'' . $_SERVER['HTTP_REFERER'] . '\'</script>';
	}
}

if (isset($_POST['login'])) {
	

	$result=mysqli_query($con,"select * from register where username='".$_POST['username']."' and Password='".$_POST['password']."'");
	if ($row=mysqli_fetch_assoc($result)) {
		$_SESSION['email']=$row['Email'];
		header("Location:dashboard.php");

	} else {
		echo '<script language="javascript">alert("Invalid Username and Password");location.href=\'' . $_SERVER['HTTP_REFERER'] . '\'</script>';
	}
}


	
?>