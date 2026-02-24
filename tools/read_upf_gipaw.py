import numpy as np
import matplotlib.pylab as plt
import os, re, sys

import xml.etree.ElementTree as ET


def test_exist( data ):
    try:
        data
    except NameError:
        return False
    else:
        return True

def read_upf_xml( filename_upf ):

    # Read entire file
    with open(filename_upf, "r") as f:
        content = f.read()

    # Wrap in a root tag (required if file isn't a single XML tree)
    #content = f"<ROOT>{content}</ROOT>"
    
    root = ET.fromstring(content)   
    pp_mesh = root.find("PP_MESH")
    dx = float(pp_mesh.attrib["dx"])
    mesh = int(pp_mesh.attrib["mesh"])
    xmin = float(pp_mesh.attrib["xmin"])
    rmax = float(pp_mesh.attrib["rmax"])    
    zmesh = float(pp_mesh.attrib["rmax"])
    print(dx, mesh, xmin, rmax, zmesh)
    
    """
    pp_aug = root.find(".//PP_NON_LOCAL/PP_AUGMENTATION")
    print(pp_aug)
    q_with_l = bool(pp_aug.attrib["q_with_l"])
    nqf = int(pp_aug.attrib["nqf"])
    nqlc = float(pp_aug.attrib["nqlc"])
    print(q_with_l, nqf, nqlc)    
    """
 
    for _, elem in ET.iterparse(filename_upf, events=("end",)):
        if elem.tag == "PP_R":
            pp_r = [float(x) for x in elem.text.split()]
            print('PP_R found',test_exist( pp_r ),len(pp_r))
            break
    
    for _, elem in ET.iterparse(filename_upf, events=("end",)):
        if elem.tag == "PP_RAB":
            pp_rab = [float(x) for x in elem.text.split()]
            print('PP_RAB found',test_exist( pp_rab ),len(pp_rab))
            break
    
    for _, elem in ET.iterparse(filename_upf, events=("end",)):
        if elem.tag == "PP_NLCC":
            pp_nlcc = [float(x) for x in elem.text.split()]
            print('PP_NLCC found',test_exist( pp_nlcc ), len(pp_nlcc))
            break
    
    for _, elem in ET.iterparse(filename_upf, events=("end",)):
        if elem.tag == "PP_LOCAL":
            pp_local = [float(x) for x in elem.text.split()]
            print('PP_LOCAL found',test_exist( pp_local ), len(pp_local))
            break
    
    betas = []  # list of dicts: {"tag": ..., "attrib": ..., "values": [...]}
    for event, elem in ET.iterparse(filename_upf, events=("end",)):
        if elem.tag.startswith("PP_BETA."):
            values = [float(x) for x in (elem.text or "").split()]
            betas.append({
            "tag": elem.tag,          # e.g. "PP_BETA.1"
            "index": int(elem.attrib.get("index", elem.tag.split(".")[1])),
            "label": elem.attrib.get("label"),
            "l": int(elem.attrib.get("angular_momentum")),
            "cutoff_radius": float(elem.attrib.get("cutoff_radius")),
            "ultrasoft_cutoff_radius": float(elem.attrib.get("ultrasoft_cutoff_radius")),
            "values": values,
            })
            elem.clear()

    nbetas = len(betas)
    print("Found", nbetas, "PP_BETA blocks")
    for b in betas:
        print(b["tag"], "len=", len(b["values"]), "l=", b["l"], "label=", b["label"],
              "cutoff=",b["ultrasoft_cutoff_radius"],'index=',b["index"])    
        #plt.plot(np.array(pp_r),np.array(b["values"])/np.array(pp_r))
        #plt.xlim(0,b["ultrasoft_cutoff_radius"])
    

    for _, elem in ET.iterparse(filename_upf, events=("end",)):
        if elem.tag == "PP_DIJ":
            pp_dij = [float(x) for x in elem.text.split()]
            print('PP_DIJ found',test_exist( pp_dij ), len(pp_dij))
            pp_dij_mat = np.array(pp_dij).reshape((nbetas,nbetas))
            #print(pp_dij_array)
            break    
        

    for _, elem in ET.iterparse(filename_upf, events=("end",)):
        if elem.tag == "PP_Q":
            pp_q = [float(x) for x in elem.text.split()]
            print('PP_Q found',test_exist( pp_dij ), len(pp_dij))
            pp_q_mat = np.array(pp_q).reshape((nbetas,nbetas))
            #print(pp_dij_array)
            break    


    qs = []  # list of dicts: {"tag": ..., "attrib": ..., "values": [...]}
    for event, elem in ET.iterparse(filename_upf, events=("end",)):
        if elem.tag.startswith("PP_QIJ."):
            values = [float(x) for x in (elem.text or "").split()]
            qs.append({
            "tag": elem.tag,          # e.g. "PP_BETA.1"
            "index": int(elem.attrib.get("index", elem.tag.split(".")[1])),
            "first_index": elem.attrib.get("first_index"),
            "second_index": int(elem.attrib.get("second_index")),
            "composite_index": int(elem.attrib.get("composite_index")),            
            "values": values,
            })
            elem.clear()
            
    nqs = len(qs)
    print("Found", nqs, "PP_QIJ blocks")
    for q in qs:
        print('index=',q["tag"])    
        #plt.plot(np.array(pp_r),np.array(q["values"])/np.array(pp_r))
        #plt.xlim(0,b["ultrasoft_cutoff_radius"])

    chis = []  # list of dicts: {"tag": ..., "attrib": ..., "values": [...]}
    for event, elem in ET.iterparse(filename_upf, events=("end",)):
        if elem.tag.startswith("PP_CHI."):
            values = [float(x) for x in (elem.text or "").split()]
            chis.append({
            "tag": elem.tag,          # e.g. "PP_BETA.1"
            "index": int(elem.attrib.get("index", elem.tag.split(".")[1])),
            "label": elem.attrib.get("label"),
            "l": int(elem.attrib.get("l")),
            "occupation": float(elem.attrib.get("occupation")),
            "cutoff_radius": float(elem.attrib.get("cutoff_radius")),
            "ultrasoft_cutoff_radius": float(elem.attrib.get("ultrasoft_cutoff_radius")),
            "values": values,
            })
            elem.clear()

    nchis = len(chis)
    print("Found", nchis, "PP_CHI blocks")
    for c in chis:
        print(c["tag"], "len=", len(c["values"]), "l=", c["l"], "label=", c["label"],
              "cutoff=",c["ultrasoft_cutoff_radius"],'index=',c["index"])    
    

    for _, elem in ET.iterparse(filename_upf, events=("end",)):
        if elem.tag == "PP_RHOATOM":
            pp_rhoatom = [float(x) for x in elem.text.split()]
            print('PP_RHOATOM found',test_exist( pp_rhoatom ), len(pp_rhoatom))
            break
    #plt.plot(np.array(pp_r),np.array(pp_rhoatom))
    
    gipaw = root.find("PP_GIPAW")
    gipaw_data_format = int(gipaw.attrib["gipaw_data_format"])
    print('GIPAW DATA FORMAT =',gipaw_data_format)

    gipaw_core = root.find(".//PP_GIPAW_CORE_ORBITALS")
    gipaw_ncores = int(gipaw_core.attrib["number_of_core_orbitals"])
    print('GIPAW N CORE ORBITALS =',gipaw_ncores)

    gipaw_cores = []  # list of dicts: {"tag": ..., "attrib": ..., "values": [...]}
    for event, elem in ET.iterparse(filename_upf, events=("end",)):
        if elem.tag.startswith("PP_GIPAW_CORE_ORBITAL."):
            values = [float(x) for x in (elem.text or "").split()]
            gipaw_cores.append({
            "tag": elem.tag,          # e.g. "PP_BETA.1"
            "index": int(elem.attrib.get("index", elem.tag.split(".")[1])),
            "label": elem.attrib.get("label"),
            "n": float(elem.attrib.get("n")),            
            "l": float(elem.attrib.get("l")),
            "values": values,
            })
            elem.clear()

    ngipaw_cores = len(gipaw_cores)
    print("Found", nchis, "PP_GIPAW_CORE_ORBITAL blocks")
    for core in gipaw_cores:
        print(core["tag"], "len=", len(core["values"]), "n=", core["n"], "l=", core["l"])
        #plt.plot(np.array(pp_r),np.array(core["values"])/np.array(pp_r))
        #plt.xlim(0,0.4)

    gipaw_val = root.find(".//PP_GIPAW_ORBITALS")
    gipaw_nvals = int(gipaw_val.attrib["number_of_valence_orbitals"])
    print('GIPAW N VALENCE ORBITALS =',gipaw_nvals)



    orbitals = []

    for orb in root.findall(".//PP_GIPAW_ORBITALS/*"):

        ae_elem = orb.find("PP_GIPAW_WFS_AE")
        ps_elem = orb.find("PP_GIPAW_WFS_PS")

        ae_vals = [float(x) for x in (ae_elem.text or "").split()]
        ps_vals = [float(x) for x in (ps_elem.text or "").split()]

        meta = orb.attrib   # index, label, l, cutoff_radius, etc

        orbitals.append({
            "meta": meta,
            "AE": ae_vals,
            "PS": ps_vals
            })

    print("Found", len(orbitals), "orbitals")
    for valence in orbitals[1:4]:
        print(valence["meta"])
        plt.plot(pp_r,valence["AE"])
        plt.plot(pp_r,valence["PS"])
        #plt.xlim(0,10)

if __name__ == '__main__':
    #read_upf( 'Nb.pbe-rrkjus-semi-gipaw-ct-dc.UPF' )
    read_upf_xml( 'Nb.pbe-rrkjus-semi-gipaw-ct-dc.UPF' )
    
