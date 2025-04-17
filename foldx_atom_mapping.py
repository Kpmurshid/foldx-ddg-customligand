from rdkit import Chem
from rdkit.Chem import AllChem

# FoldX-style atom-residue mapping
def translateMappings(atom):
    if atom == "O_hydroxyl": return ("OG", "SER")
    elif atom == "O_ring": return ("O4*", "A")
    elif atom == "O_minus": return ("OD1", "ASP")
    elif atom == "O_carboxamide": return ("OD1", "ASN")
    elif atom == "N_amino": return ("NZ", "LYS")
    elif atom == "N_guanidino": return ("NH2", "ARG")
    elif atom == "N_imidazol_plus": return ("ND1", "HIS")
    elif atom == "N_imidazol_minus": return ("NE2", "HIS")
    elif atom == "N_pyrazole": return ("N", "PRO")
    elif atom == "N_amide": return ("ND2", "ASP")
    elif atom == "C_ring_not_arom": return ("CG", "PRO")
    elif atom == "C_ring_arom": return ("CZ", "PHE")
    elif atom == "C_single_link": return ("CG2", "THR")
    elif atom == "C_double_link": return ("CG", "ARG")
    elif atom == "C_triple_link": return ("CG", "LEU")
    else: return ("?", "?")

# Atom type inference based on context
def infer_foldx_type(atom):
    symbol = atom.GetSymbol()
    is_arom = atom.GetIsAromatic()
    ring = atom.IsInRing()
    neighbors = [n.GetSymbol() for n in atom.GetNeighbors()]
    formal_charge = atom.GetFormalCharge()
    hybridization = atom.GetHybridization()

    if symbol == "O":
        if formal_charge == -1:
            return "O_minus"
        elif "C" in neighbors and "N" in neighbors:
            return "O_carboxamide"
        elif "H" in neighbors:
            return "O_hydroxyl"
        elif ring:
            return "O_ring"
        else:
            return "O_hydroxyl"
    elif symbol == "N":
        if formal_charge == +1 and ring:
            return "N_imidazol_plus"
        elif formal_charge == -1 and ring:
            return "N_imidazol_minus"
        elif "C" in neighbors and hybridization == Chem.HybridizationType.SP2:
            return "N_amide"
        elif ring:
            return "N_pyrazole"
        else:
            return "N_amino"
    elif symbol == "C":
        if is_arom:
            return "C_ring_arom"
        elif ring:
            return "C_ring_not_arom"
        elif hybridization == Chem.HybridizationType.SP:
            return "C_triple_link"
        elif hybridization == Chem.HybridizationType.SP2:
            return "C_double_link"
        else:
            return "C_single_link"
    return "UNKNOWN"

# === MAIN CODE ===
ligand_file = "ligand.pdb"
smiles = "COc1c2c(cc(c1N3CC4CCCNC4C3)F)C(=O)C(=CN2C5CC5)C(=O)O"  # Replace as needed

# Create a template from SMILES
template = Chem.MolFromSmiles(smiles)
if template is None:
    raise ValueError("Invalid SMILES provided.")

# Read PDB and assign bond orders from SMILES
mol = Chem.MolFromPDBFile(ligand_file, removeHs=False)
if mol is None:
    raise ValueError("Unable to read ligand.pdb.")

mol = AllChem.AssignBondOrdersFromTemplate(template, mol)
Chem.SanitizeMol(mol)

# Print to terminal
print(f"{'Idx':<5} {'Name':<6} {'Symbol':<6} {'FoldX Type':<20} {'FoldX Atom':<10} {'FoldX Res':<10}")

# Write to file
with open("foldx_atom_types.txt", "w") as f:
    f.write("atomMappingsDict = {\n")
    for atom in mol.GetAtoms():
        name = atom.GetPDBResidueInfo().GetName().strip()
        symbol = atom.GetSymbol()
        foldx_type = infer_foldx_type(atom)
        pdb_atom, pdb_res = translateMappings(foldx_type)
        print(f"{atom.GetIdx():<5} {name:<6} {symbol:<6} {foldx_type:<20} {pdb_atom:<10} {pdb_res:<10}")
        f.write(f'    "{name}": "{foldx_type}",\n')
    f.write("}\n")

