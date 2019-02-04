import sys
import os
import subprocess


filename1, file_extension1 = os.path.splitext(sys.argv[1])
filename2, file_extension2 = os.path.splitext(sys.argv[2])


print(filename1)
print(filename2)


f1="70percent.bed"
f2="30percent.bed"

intermediate_file1= filename1+"_minus_"+filename2+".bed"
intermediate_file2= filename2+"_minus_"+filename1+".bed"


fasta_file1 = filename1+"_minus_"+filename2 + ".fa"
fasta_file2 = filename2+"_minus_"+filename1 + ".fa"

command=''' awk 'END{print NR}' ''' + sys.argv[1]
num = subprocess.check_output(command, shell=True)
print(num)

output=float(num)
output=0.7*output
output=int(output)


command=''' awk 'NR>=1&&NR<='''+str(output)+''' ' '''+sys.argv[1]+''' > '''+f1
subprocess.call(command, shell=True)
command=''' awk 'NR>'''+str(output)+'''&&NR<='''+str(num)+''' ' '''+sys.argv[1]+''' > '''+f2
subprocess.call(command, shell=True)
