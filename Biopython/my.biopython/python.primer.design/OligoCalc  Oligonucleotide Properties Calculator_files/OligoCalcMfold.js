var emailConfirmed=false;

function mfoldCreateWindow() {
	if (document.OligoCalc.oligoBox.value.length < 8) {
		alert("Please enter at least 8 bases before trying to look for folding structures!");
		return false;
	}
	if (! validateEmail(document.OligoCalc.emailAddress.value) || !emailConfirmed) {
		var email=prompt("The mfold server requires an email address. Please enter or confirm your email address",document.OligoCalc.emailAddress.value);
		if (email && email.length > 1) {
			document.OligoCalc.emailAddress.value=email;
			SaveEmailCookie (email);
		} else {
			emailConfirmed=false;
			return false;
		}
		if (!validateEmail(email)) {
			alert("Sorry, "+email+" is not a valid email address.");
			return false;
		}
		emailConfirmed=true;
	}
	mfoldWin=window.open ("OligoCalc2mfold2.html","mfold", "toolbar=yes,directories=no,status=yes,location=yes,scrollbars=yes,resizable=1");
	return false;
}

function mfoldPrepare(theForm) {
	var theSeq="";
	var theEmail="";
	var theMoleculeType="DNA";
	if (opener && opener.document.OligoCalc) {
		var remoteForm=opener.document.OligoCalc;
		theSeq=remoteForm.oligoBox.value;
		theEmail=remoteForm.emailAddress.value;
		var selection=remoteForm.deoxy.options[remoteForm.deoxy.selectedIndex].value;
		theMoleculeType=(selection.indexOf("RNA") > 0) ? 'RNA' :'DNA';
	} else {
		theSeq=GetOligoCookie("");
		theEmail=GetEmailCookie("");
	}
	if (theSeq.length < 8) {
		alert("Please enter at least 8 bases before trying to look for folding structures!");
		return false;
	}
	theForm.SEQ_NAME.value=theSeq;
	theForm.SEQUENCE.value=theSeq;
	theForm.EMAIL_ADDR.value=theEmail;
	theForm.NA.value=theMoleculeType;
	theForm.submit(); // comment out to stop submission!
	return false;
}
