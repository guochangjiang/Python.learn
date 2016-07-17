/* This program is free software; you can redistribute it and/or modify it under the terms of the GNU
 * General Public License as published by the Free Software Foundation; either version 2 of the 
 * License, or (at your option) any later version
                                
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
 * even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
 * Public License for more details. 
 * 
 * You should have received a copy of the GNU General Public License along with this program; if not, 
 * write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA                                                                  

 *       Marine Dumousseau and Nicolas Lenovere                                                   
 *       EMBL-EBI, neurobiology computational group,                          
 *       Cambridge, UK. e-mail: lenov@ebi.ac.uk, marine@ebi.ac.uk        */

package melting.patternModels.specificAcids;

import melting.configuration.OptionManagement;
import melting.configuration.RegisterMethods;
import melting.methodInterfaces.NamedMethod;
import melting.methodInterfaces.PatternComputationMethod;

import java.util.HashMap;

/**
 * This class represents the locked nucleic acid (AL, GL, CL or TL) model owc11. It extends PatternComputation.
 * 
 * McTigue et al.(2004). Biochemistry 43 : 5388-5405
 */
public class Owczarzy11SingleMismatchLockedAcid extends LockedAcidNNMethod
  implements NamedMethod
{
	// Instance variables

	/**
	 * String defaultFileName : default name for the xml file containing the thermodynamic parameters for locked nucleic acid
	 */
	public static String defaultFileName = "Owczarzy2011lockedmmn.xml";

  /**
   * Full name of the method.
   */
  private static String methodName = "Owczarzy et al. (2011)";


	@Override
	public void initialiseFileName(String methodName){
		super.initialiseFileName(methodName);

		if (this.fileName == null){
			this.fileName = defaultFileName;
		}
	}

  /**
   * Gets the full name of the method.
   * @return The full name of the method.
   */
  @Override
  public String getName()
  {
    return methodName;
  }

    @Override
    public void loadData(HashMap<String, String> options) {
        super.loadData(options);

        // load single mismatch parameters (fixed to owc11 because need the formula owc11)
        RegisterMethods register = new RegisterMethods();
        PatternComputationMethod singleMismatch = register.getPatternComputationMethod(OptionManagement.lockedAcidMethod, "owc11");
        singleMismatch.initialiseFileName("owc11");
        String fileSingleMismatch = singleMismatch.getDataFileName("owc11");
        loadFile(fileSingleMismatch, this.collector);

        // load tandem parameters  (fixed to owc11 because need the formula owc11)
        PatternComputationMethod tandemMismatch = register.getPatternComputationMethod(OptionManagement.tandemLockedAcidMethod, "owc11");
        tandemMismatch.initialiseFileName("owc11");
        String fileTandemMismatch = tandemMismatch.getDataFileName("owc11");

        loadFile(fileTandemMismatch, this.collector);

    }
}
