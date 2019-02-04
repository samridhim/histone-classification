
# coding: utf-8

# In[1]:


def pipe(f1,f2):
    
    import sys
    import os
    import subprocess
    
    filename1, file_extension1 = os.path.splitext(f1)
    filename2, file_extension2 = os.path.splitext(f2)

    intermediate_file1= filename1+"_minus_"+filename2+".bed"
    intermediate_file2= filename2+"_minus_"+filename1+".bed"

    fasta_file1 = filename1+"_minus_"+filename2 + ".fa"
    fasta_file2 = filename2+"_minus_"+filename1 + ".fa"

    #converting bed file of 10 columns to 4 column file, with 100 upstream/downstream
    #for i in range(1,3):
    command=''' echo "$(awk '{print $1, $2+$10-100, $2+$10+100, $4}' ''' + f1 + ''' )" > ''' + f1
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2+$10-100, $2+$10+100, $4}' ''' + f2 + ''' )" > ''' + f2
    subprocess.call(command, shell=True)


    #dropping peak info column and storing only 1st 3 columns
    #for i in range(1,3):
    command=''' echo "$(awk '{print $1, $2, $3}' ''' + f1 + ''' )" > ''' + f1
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2, $3}' ''' + f2 + ''' )" > ''' + f2
    subprocess.call(command, shell=True)


    #replacing spaces with tabs
    #for i in range(1,3):
    command=''' echo "$(tr ' ' \\\\t < '''+ f1 + ''' )" > ''' + f1
    subprocess.call(command, shell=True)
    command=''' echo "$(tr ' ' \\\\t < '''+ f2 + ''' )" > ''' + f2
    subprocess.call(command, shell=True)


    #finding intersections and storing a file w/o intersections in intermediate file
    command= ''' bedtools intersect -v -a ''' + f1 + ''' -b ''' + f2 + ''' > ''' + intermediate_file1
    subprocess.call(command, shell=True)
    command= ''' bedtools intersect -v -a ''' + f2 + ''' -b ''' + f1 + ''' > ''' + intermediate_file2
    subprocess.call(command, shell=True)


    #appending a random 4th column to prepare the file for twoBitToFa 
    command=''' echo "$(awk '{print $1, $2, $3,100}' ''' + intermediate_file1 + ''' )" > ''' + intermediate_file1
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2, $3,100}' ''' + intermediate_file2 + ''' )" > ''' + intermediate_file2
    subprocess.call(command, shell=True) 


    #converting bed to fasta
    command=''' twoBitToFa hg19.2bit -bed=''' + intermediate_file1 + ''' ''' + fasta_file1
    subprocess.call(command, shell=True)
    command=''' twoBitToFa hg19.2bit -bed=''' + intermediate_file2 + ''' ''' + fasta_file2
    subprocess.call(command, shell=True)

