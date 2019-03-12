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

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
#TEMPLATE_FILE = "feat2_template.html"
#template = templateEnv.get_template(TEMPLATE_FILE)

for ses in sessions:
    ses_dict = { }
    #ses="ses-1"
    bad_subjects=[]
    outfile = "lev2_QA_%s.html"%ses
    #os.system("rm %s"%(outfile))
 
    sub_count = len(glob.glob('/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/sub-*/%s'%ses))
    feat2_count = len(glob.glob('/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/sub-*/%s/func/Analysis/feat2/sub-*.gfeat'%ses))
        
    print("> Session: %s"%ses)
    print("> Total subject count: %s"%sub_count)
    print("> Total feat2 sub count: %s"%feat2_count)
    
    all_feats = glob.glob('/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/sub-*/%s/func/Analysis/feat2/sub-*.gfeat'%(ses))
    
    for file in list(all_feats):
        subject = file.split("/")[7]
        filename = "%s"%(subject)


        masksum_img = "%s/inputreg/masksum_overlay.png"%(file)
        maskunique_img = "%s/inputreg/maskunique_overlay.png"%(file)
        
        if not os.path.exists(masksum_img) or not os.path.exists(maskunique_img):
            bad_subjects.append(subject)
        else:
            if subject not in ses_dict:
                if subject not in ses_dict:
                    ses_dict[subject] = {}
                ses_dict[subject]["MASKSUM"] = masksum_img 
                ses_dict[subject]["MASKUNIQUE"] = maskunique_img
    
    df = pd.DataFrame.from_dict(ses_dict, orient='index')
    outputText = template.render(dict=df, sess=ses.split("-")[1], ct=feat2_count)
    html_file = open('feat2_%s.html'%ses, 'w')
    html_file.write(outputText)
    html_file.close()
        

      

        
