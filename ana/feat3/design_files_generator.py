import glob
import os
DER_DIR = "/projects/niblab/bids_projects/Experiments/ChocoData/derivatives"
SESSIONS = ["ses-3"] #, "ses-2"] #, "ses-3", "ses-4"]
COPE_CT = 28



for ses in SESSIONS:
    subject_paths= glob.glob(os.path.join(DER_DIR, "sub-*/%s"%ses))
    for d in range(0, COPE_CT):
        with open(os.path.join(DER_DIR, "design_files/design3_104subs.fsf"), 'r') as infile:
            tempfsf=infile.read()
            cope_id = d + 1
            output_folder = os.path.join(DER_DIR, "group_ana/%s/cope_%s"%(ses, cope_id))
            print(output_folder)
            if not os.path.exists(os.path.join(DER_DIR, "group_ana/%s"%(ses))):
                os.makedirs(os.path.join(DER_DIR, "group_ana/%s"%(ses)))
            #REPLACE OUTPUT
            tempfsf = tempfsf.replace("OUTPUT", output_folder)
            for c, path in enumerate(sorted(subject_paths)):
                #REPLACE
                input_id = c+1
                keyword = "FEAT-%s_FILE"%input_id
                cope_folder = os.path.join(path, "func/Analysis/feat2/%s.gfeat/cope%s.feat"%(path.split("/")[-2], cope_id))
                #print(keyword, cope_folder)
                tempfsf = tempfsf.replace(keyword, cope_folder)
            OUTFILE_PATH = os.path.join(DER_DIR, "group_ana/%s/cope_%s.fsf"%(ses,cope_id))
            with open(OUTFILE_PATH, "w") as outfile:
                outfile.write(tempfsf)
            outfile.close()
        infile.close()