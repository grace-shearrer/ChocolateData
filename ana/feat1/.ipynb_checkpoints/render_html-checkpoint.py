# Code below extended from Jeannette Mumford Brain stats - 
import os
import glob
import pdfkit
import pandas as pd
import jinja2 
import pdfkit
# We will start with the registration png files
outfile = "/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/feat1_ana.html"
#os.system("rm %s"%(outfile))
 
sessions = ["ses-1"]#, "ses-2", "ses-3", "ses-4"]
dataframes = []

templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "feat1_ana.html"
template = templateEnv.get_template(TEMPLATE_FILE)


#f = open(outfile, "w")
for ses in sessions:
    all_feats = glob.glob('/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/sub-*/%s/func/Analysis/feat1/task*'%ses)
    ses_dict = {}
    ses_id = ses.split("-")[1]
    
    for file in list(all_feats):
        subject = file.split("/")[7]
        milk_id = file.split("/")[-1].split(".")[0].split("-")[1]
        filename = "%s_%s"%(subject, milk_id)
        if subject not in ses_dict:
            ses_dict[subject] = {}
        

        design_img = "%s/design.png"%(file)
        design_cov_img = "%s/design_cov.png"%(file)
        func2highres_img =  "%s/reg/example_func2highres.png"%(file)
        func2standard_img = "%s/reg/example_func2standard.png"%(file)
        highres2standard_img = "%s/reg/highres2standard.png"%(file)
        if os.path.exists(design_img) and milk_id not in ses_dict[subject]:
            ses_dict[subject][milk_id] = [design_img, design_cov_img, func2highres_img, func2standard_img, highres2standard_img]
        
        outputText = template.render(dict=ses_dict, sess=ses_id)
        
        df = pd.DataFrame.from_dict({(i,j): ses_dict[i][j] 
                           for i in ses_dict.keys() 
                           for j in ses_dict[i].keys()},
                       orient='index')
        html_file = open('session-%s.html'%ses_id, 'w')
        html_file.write(outputText)
        html_file.close()
        
