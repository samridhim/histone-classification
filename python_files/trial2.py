def pipe(f1,f2):
    
    import sys
    import os
    import subprocess
    
    filename1, file_extension1 = os.path.splitext(f1)
    filename2, file_extension2 = os.path.splitext(f2)

    file1_70= filename1+"_70percent.bed"
    file1_30= filename1+"_30percent.bed"
    file2_70= filename2+"_70percent.bed"
    file2_30= filename2+"_30percent.bed"

    intermediate_file1= filename1+"_minus_"+filename2+".bed"
    intermediate_file2= filename2+"_minus_"+filename1+".bed"

    file1_70_fasta = filename1+"_70"+ ".fa"
    file2_70_fasta = filename2+"_70"+".fa"
    file1_30_fasta = filename1+"_30"+".fa"
    file2_30_fasta = filename2+"_30"+".fa"


    #dividing files into 70-30%
    command=''' awk 'END{print NR}' ''' + f1
    num_rows_in1 = subprocess.check_output(command, shell=True)
    output1=float(num_rows_in1)
    output1=0.7*output1
    output1=int(output1)


    command=''' awk 'NR>=1&&NR<='''+str(output1)+''' ' '''+f1+''' > '''+file1_70
    subprocess.call(command, shell=True)
    command=''' awk 'NR>'''+str(output1)+'''&&NR<='''+str(num_rows_in1)+''' ' '''+f1+''' > '''+file1_30
    subprocess.call(command, shell=True)


    command=''' awk 'END{print NR}' ''' + f2
    num_rows_in2 = subprocess.check_output(command, shell=True)
    output2=float(num_rows_in2)
    output2=0.7*output2
    output2=int(output2)


    command=''' awk 'NR>=1&&NR<='''+str(output2)+''' ' '''+f2+''' > '''+file2_70
    subprocess.call(command, shell=True)
    command=''' awk 'NR>'''+str(output2)+'''&&NR<='''+str(num_rows_in2)+''' ' '''+f2+''' > '''+file2_30
    subprocess.call(command, shell=True)


    #converting bed file of 10 columns to 4 column file, with 100 upstream/downstream
    #for i in range(1,3):
    command=''' echo "$(awk '{print $1, $2+$10-100, $2+$10+100, $4}' ''' + file1_70 + ''' )" > ''' + file1_70
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2+$10-100, $2+$10+100, $4}' ''' + file1_30 + ''' )" > ''' + file1_30
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2+$10-100, $2+$10+100, $4}' ''' + file2_70 + ''' )" > ''' + file2_70
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2+$10-100, $2+$10+100, $4}' ''' + file2_30 + ''' )" > ''' + file2_30
    subprocess.call(command, shell=True)

  
    #dropping peak info column and storing only 1st 3 columns
    #for i in range(1,3):
    command=''' echo "$(awk '{print $1, $2, $3}' ''' + file1_70 + ''' )" > ''' + file1_70
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2, $3}' ''' + file1_30 + ''' )" > ''' + file1_30
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2, $3}' ''' + file2_70 + ''' )" > ''' + file2_70
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2, $3}' ''' + file2_30 + ''' )" > ''' + file2_30
    subprocess.call(command, shell=True)


    #replacing spaces with tabs
    #for i in range(1,3):
    command=''' echo "$(tr ' ' \\\\t < '''+ file1_70 + ''' )" > ''' + file1_70
    subprocess.call(command, shell=True)
    command=''' echo "$(tr ' ' \\\\t < '''+ file1_30 + ''' )" > ''' + file1_30
    subprocess.call(command, shell=True)
    command=''' echo "$(tr ' ' \\\\t < '''+ file2_70 + ''' )" > ''' + file2_70
    subprocess.call(command, shell=True)
    command=''' echo "$(tr ' ' \\\\t < '''+ file2_30 + ''' )" > ''' + file2_30
    subprocess.call(command, shell=True)


    #finding intersections and storing a file w/o intersections in intermediate file
    command= ''' bedtools intersect -v -a ''' + file1_70 + ''' -b ''' + file2_70 + ''' > ''' + intermediate_file1
    subprocess.call(command, shell=True)
    command= ''' bedtools intersect -v -a ''' + file2_70 + ''' -b ''' + file1_70 + ''' > ''' + intermediate_file2
    subprocess.call(command, shell=True)


    #appending a random 4th column to prepare the file for twoBitToFa 
    command=''' echo "$(awk '{print $1, $2, $3,100}' ''' + intermediate_file1 + ''' )" > ''' + intermediate_file1
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2, $3,100}' ''' + intermediate_file2 + ''' )" > ''' + intermediate_file2
    subprocess.call(command, shell=True) 
    command=''' echo "$(awk '{print $1, $2, $3,100}' ''' + file1_30 + ''' )" > ''' + file1_30
    subprocess.call(command, shell=True)
    command=''' echo "$(awk '{print $1, $2, $3,100}' ''' + file2_30 + ''' )" > ''' + file2_30
    subprocess.call(command, shell=True) 


    #converting bed to fasta
    command=''' twoBitToFa hg19.2bit -bed=''' + intermediate_file1 + ''' ''' + file1_70_fasta
    subprocess.call(command, shell=True)
    command=''' twoBitToFa hg19.2bit -bed=''' + intermediate_file2 + ''' ''' + file2_70_fasta
    subprocess.call(command, shell=True)
    command=''' twoBitToFa hg19.2bit -bed=''' + file1_30 + ''' ''' + file1_30_fasta
    subprocess.call(command, shell=True)
    command=''' twoBitToFa hg19.2bit -bed=''' + file2_30 + ''' ''' + file2_30_fasta
    subprocess.call(command, shell=True)



def main():
	import sys
	pipe(sys.argv[1],sys.argv[2])


if __name__ == '__main__':
    main()

