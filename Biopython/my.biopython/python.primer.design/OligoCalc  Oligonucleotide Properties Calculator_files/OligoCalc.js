/*one bug for nearest Neighbor was fixed on 08/02/99 ---"zero the initial values" 
 *see lines 161-166 */
/*add primer self-annealing test*/
/* all object-driven functions moved to OligoCalcObj.js on 12/15/00 WAKibbe */
/* added cookie handling back in on 03/22/2007 WAKibbe */

var blastwindow;	// for blast search
var primerWin;	// for complementarity info
var mfoldWin;	// for mfold info
var minAlignLen; //for 3' complementarity
var minHairpinLen; //for hairpin
var maxMismatchNum=1; //for maxi number of mismatches in an alignment
var previousCookieLoad=""; //check if cookie changed


function CheckOligoCookie(form) {
	var temp = form.oligoBox.value;
	var tseq = GetOligoCookie (temp);
	cookieChanged = (previousCookieLoad != tseq);
	if (temp != tseq && cookieChanged) {
		form.oligoBox.value = GetDelimitedValue (tseq,0,";");
		return 1;
	}
	previousCookieLoad=tseq;
	if (temp != tseq && !cookieChanged) {
		SaveOligoCookie(temp);
		previousCookieLoad=temp;
	}
	if (cookieChanged) {
		document.OligoCalc.emailAddress.value= GetEmailCookie(document.OligoCalc.emailAddress.value);
	}
	return 0;
}

function DoNewFocus(form) 
{
	if (!theOligo){
		CheckOligoCookie(form);
		Calculate(form);
	} else if (CheckOligoCookie(form)) {
		Calculate(form);
	}
}

function Calculate(form) 
{
	var temp;
	var CompString;
	if (!theOligo){
		form.oligoBox.focus();
		theOligo      = new Oligo(); // instantiate Oligo object!
		theComplement = new Oligo();
	}
	ReCalculate(form);
	return false;
}

function ReCalculate(form) 
{
	var temp;
	var CompString;
	if (!theOligo){
		Calculate(form);
		return false;
	}
	temp=CheckBase(form.oligoBox.value);
	if (temp==-1){
		if (form.oligoBox.value.length == 0) form.complementBox.value="";
		return false;
	}
	form.oligoBox.value=temp;
	theOligo.DoOligoCalc(form, temp);
	theOligo.GetOligoMods(form);
	CompString = MakeComplement(form.oligoBox.value, theOligo.isDeoxy);
	theComplement.DoOligoCalc(form, CompString);
	if (!theOligo.isSingleStranded) {
		// calculate the ds MW now that the complement has been made
		theOligo.DoOligoCalc(form, temp);
	}
	theOligo.DoOligoOutput(form, form.oligoBox);
	form.complementBox.value = FormatBaseString(theComplement.Sequence);
	return false;
}

function RecalcMWConcAndOD (form) {
	theOligo.DoChangeInMWConcAndODs(form);
	theComplement.DoChangeInMWConcAndODs(form);
	theOligo.DoChangeInMWConcAndODOutput(form);
}

function SwapStrands(form) {
	if (form.complementBox.value!="") {
		var temp = theOligo;
		theOligo = theComplement;
		theComplement = temp;
	}
	theOligo.SetOligoMods(form);
/*	
	form.fam.value=theOligo.famCount ;
	form.hex.value=theOligo.hexCount ;
	form.tet.value=theOligo.tetCount ;
	form.tamra.value=theOligo.tamraCount ;
*/
	form.ODs.value=theOligo.ODs;
	theOligo.DoOligoOutput(form, form.oligoBox);
	form.complementBox.value =FormatBaseString(theComplement.Sequence);
	return false;
}

