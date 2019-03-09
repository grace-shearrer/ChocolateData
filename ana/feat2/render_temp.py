# Code below extended from Jeannette Mumford Brain stats - 
import os
import glob
import pdfkit
import pandas as pd
import jinja2 
import pdfkit
# We will start with the registration png files
outfile = "/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/feat2_ana.html"
#os.system("rm %s"%(outfile))
 
sessions = ["ses-1", "ses-2", "ses-3", "ses-4"]
dataframes = []

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
#TEMPLATE_FILE = "feat2_template.html"
#template = templateEnv.get_template(TEMPLATE_FILE)

for ses in sessions:
    ses_dict = {}
    #ses="ses-1"
    bad_subjects=[]
    outfile = "lev2_QA_%s.html"%ses
    #os.system("rm %s"%(outfile))
 
    all_feats = glob.glob('/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/sub-*/%s/func/Analysis/feat2/sub-*.gfeat'%(ses))
    
    for file in list(all_feats):
        subject = file.split("/")[7]
        filename = "%s"%(subject)
        if subject not in ses_dict:
            ses_dict[subject] = {}
        

        masksum_img = "%s/inputreg/masksum_overlay.png"%(file)
        maskunique_img = "%s/inputreg/maskunique_overlay.png"%(file)
        
        if not os.path.exists(masksum_img) and not os.path.exists(maskunique_img):
            ses_dict[subject] = "ERROR"
        else:
            ses_dict[subject] = [masksum_img, maskunique_img]
        
        
    for a in ses_dict:
        if ses_dict[a] == "ERROR":
            bad_subjects.append(a)
    if len(bad_subjects) == 0:
        print("> SUBJECT COUNT FOR SESSION %s: %s"%(ses.split("-")[1], len(all_feats)))
    else:
        print("> BAD SUBJECTS FOR SESSION %s: %s"%(ses.split("-")[1], bad_subjects))
        print("> SUBJECT COUNT FOR SESSION %s: %s"%(ses.split("-")[1], len(all_feats) - len(bad_subjects)))
    outputText = template.render(dict=ses_dict, sess=ses)
        
    html_file = open('feat2_%s.html'%ses, 'w')
    html_file.write(outputText)
    html_file.close()
        
