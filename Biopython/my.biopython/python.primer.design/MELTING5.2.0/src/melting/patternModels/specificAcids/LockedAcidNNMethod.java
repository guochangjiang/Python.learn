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

import melting.Environment;
import melting.ThermoResult;
import melting.Thermodynamics;
import melting.configuration.OptionManagement;
import melting.methodInterfaces.NamedMethod;
import melting.patternModels.PatternComputation;
import melting.sequences.NucleotidSequences;

/**
 * This class represents the locked nucleic acid (AL, GL, CL or TL) model owc11. It extends PatternComputation.
 * 
 * McTigue et al.(2004). Biochemistry 43 : 5388-5405
 */
public abstract class LockedAcidNNMethod extends PatternComputation
  implements NamedMethod
{	

	// PatternComputationMethod interface implementation

	@Override
	public boolean isApplicable(Environment environment, int pos1,
			int pos2) {
		boolean isApplicable = super.isApplicable(environment, pos1, pos2);

		int [] positions = correctPositions(pos1, pos2, environment.getSequences().getDuplexLength());
		pos1 = positions[0];
		pos2 = positions[1];
		
		if (environment.getHybridization().equals("dnadna") == false) {
			OptionManagement.logWarning("\n The thermodynamic parameters for locked nucleic acids of" +
					"Owczarzy et al. (2011) are established for DNA sequences.");
		}
				
		if ((pos1 == 0 || pos2 == environment.getSequences().getDuplexLength() - 1) && environment.getSequences().calculateNumberOfTerminal("L", "-", pos1, pos2) > 0){
			OptionManagement.logWarning("\n The thermodynamics parameters for locked nucleic acids of " +
					"McTigue (2004) are not established for terminal locked nucleic acids.");
			isApplicable = false;
		}
		
		return isApplicable;
	}
	
	@Override
	public ThermoResult computeThermodynamics(NucleotidSequences sequences,
			int pos1, int pos2, ThermoResult result) {
		int [] positions = correctPositions(pos1, pos2, sequences.getDuplexLength());
		pos1 = positions[0];
		pos2 = positions[1];
		
		NucleotidSequences newSequences = sequences.getEquivalentSequences("dna");
		
		OptionManagement.logMessage("\n The locked acid nuceic model is");
        OptionManagement.logMethodName(getName());
        OptionManagement.logFileName(getDataFileName(getName()));

		double enthalpy = result.getEnthalpy();
		double entropy = result.getEntropy();
		
		Thermodynamics lockedAcidValue;
		
		for (int i = pos1; i < pos2; i++){
			lockedAcidValue = this.collector.getLockedAcidValue(newSequences.getSequenceNNPair(i), newSequences.getComplementaryNNPair(i));

			OptionManagement.logMessage(newSequences.getSequenceNNPair(i) + "/" + newSequences.getComplementaryNNPair(i) + " : enthalpy = " + lockedAcidValue.getEnthalpy() + "  entropy = " + lockedAcidValue.getEntropy());

			enthalpy += lockedAcidValue.getEnthalpy();
			entropy += lockedAcidValue.getEntropy();
		}
		
		result.setEnthalpy(enthalpy);
		result.setEntropy(entropy);
		
		return result;
	}

	@Override
	public boolean isMissingParameters(NucleotidSequences sequences, int pos1,
			int pos2) {

        int[] positions = correctPositions(pos1, pos2, sequences.getDuplexLength());
        pos1 = positions[0];
        pos2 = positions[1];

        NucleotidSequences newSequences = sequences.getEquivalentSequences("dna");

        for (int i = pos1; i < pos2; i++) {
            if (this.collector.getLockedAcidValue(sequences.getSequenceNNPair(i), sequences.getComplementaryNNPair(i)) == null) {
                OptionManagement.logWarning("\n The thermodynamic parameters for " + sequences.getSequenceNNPair(i) + "/" + sequences.getComplementaryNNPair(i) +
                        "are missing. Check the locked nucleic acid parameters.");
                return true;
            }
        }

        return super.isMissingParameters(newSequences, pos1, pos2);
    }

	// private methods
	
	/**
	 * corrects the pattern positions in the duplex to have the adjacent
	 * base pair of the pattern included in the subsequence between the positions pos1 and pos2
	 * @param pos1 : starting position of the internal loop
	 * @param pos2 : ending position of the internal loop
	 * @param duplexLength : total length of the duplex
	 * @return int [] positions : new positions of the subsequence to have the pattern surrounded by the
	 * adjacent base pairs in the duplex.
	 */
	private int[] correctPositions(int pos1, int pos2, int duplexLength){
		if (pos1 > 0){
			pos1 --;
		}
		if (pos2 < duplexLength - 1){
			pos2 ++;
		}
		int [] positions = {pos1, pos2};
		return positions;
	}

  /**
   * Gets the full name of the method.
   * @return The full name of the method.
   */
  @Override
  public abstract String getName();
}
