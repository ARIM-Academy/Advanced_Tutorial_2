import os, re
import py3Dmol
from rdkit import Chem

def safe_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '_', name)

def write_xyz_input(mol, confId, filename):
    try:
        atoms = mol.GetAtoms()
        conf = mol.GetConformer(confId)
        with open(filename, "w") as f:
            f.write(f"{mol.GetNumAtoms()}\n")
            f.write("0 1\n")
            for atom in atoms:
                pos = conf.GetAtomPosition(atom.GetIdx())
                f.write(f"{atom.GetSymbol()} {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}\n")
            f.write("\n")
    except Exception as e:
        print(f"[ERROR] write_xyz_input failed: {filename}")
        raise e

def write_gaussian_input(mol, confId, filename, method="B3LYP", basis="6-31G(d)", title="Gaussian job"):
    try:
        atoms = mol.GetAtoms()
        conf = mol.GetConformer(confId)
        with open(filename, "w") as f:
            f.write(f"%chk={filename.replace('.gjf','.chk')}\n")
            f.write(f"#p {method}/{basis} Opt\n\n")
            f.write(f"{title}\n\n")
            f.write("0 1\n")
            for atom in atoms:
                pos = conf.GetAtomPosition(atom.GetIdx())
                f.write(f"{atom.GetSymbol()} {pos.x:.6f} {pos.y:.6f} {pos.z:.6f}\n")
            f.write("\n")
    except Exception as e:
        print(f"[ERROR] write_gaussian_input failed: {filename}")
        raise e

def show_3D_from_xyz(xyz_path: str, width=400, height=400, background='#e1e1e1'):
    with open(xyz_path, 'r') as f:
        xyz = f.read()

    view = py3Dmol.view(width=width, height=height)
    view.addModel(xyz, 'xyz')
    view.setStyle({'stick': {}})
    view.setBackgroundColor(background)
    view.zoomTo()
    return view.show()