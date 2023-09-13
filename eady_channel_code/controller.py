import numpy
import subprocess
import re
import os


root_dir = os.getcwd()
print('Current directory is' + root_dir)

# The nondimensional parameters here follow from my notes
# phi1 cannot be zero!
rho1 = []
rho2 = []
rho3 = 1.0

rho1_start = 1.0
rho1_end = 1.0 # 5.0
rho1_interval = 1.0
while rho1_start <= rho1_end:
  rho1.append(str(rho1_start))
  rho1_start = rho1_start + rho1_interval
print('rho1 = ', rho1)

#
rho2_start = 2.0
rho2_end = 20.0
rho2_interval = 2.0
while rho2_start <= rho2_end:
  rho2.append(str(rho2_start))
  rho2_start = rho2_start + rho2_interval
print('rho2 = ', rho2)

# These are fixed
U0 = 0.1
N2f2 = 225.0
H = 4000
Ld = numpy.sqrt(N2f2) * H
# so Ld = 60000
# rho3 = 1 ----> nu_8 = r * Ld^8
# We need to set r so that rho1 and rho2 are set properly

for i in rho1:
  for j in rho2:
 
    r0 = U0 / Ld / float(i)
    beta = r0 * float(j) / Ld 
    nu8 = r0 * (Ld**8)    

    r0_str = str(r0)
    beta_str = str(beta)
    nu8_str = str(nu8)

    print('rho_1 = ' + i)
    print('rho_2 = ' + j)
    print('rho_3 = 1.0')
    print('r0 = ' + r0_str)
    print('beta = ' + beta_str)
    print('nu_8 = ' + nu8_str)

    # Make directory
    dirstr = 'quad_' + i + '_' + j

    command = 'mkdir ' + dirstr
    mkd = subprocess.Popen(command, shell = True)
    mkd.wait()

    # Copy code
    command = 'cp ./code/* ./' + dirstr
    mkd = subprocess.Popen(command, shell = True)
    mkd.wait()

    # Enter directory
    print('Changing to directory ' + dirstr)
    os.chdir(dirstr)

    # Set up strings to replace
    f = open('parameters.f90')
    text = f.read()
    f.close()

    SF = re.compile('REPL1')
    SF2 = re.compile('REPL2')
    SF3 = re.compile('REPL3')
    new = SF.sub('real(dp), parameter :: beta = ' + beta_str + '_dp',text)
    new2 = SF2.sub('real(dp), parameter :: r0 = ' + r0_str + '_dp',new)
    new3 = SF3.sub('real(dp), parameter :: A8 = ' + nu8_str + '_dp',new2)
    f = open('parameters.f90', 'w')
    f.write(new3)
    f.close()

    ###### Edit run script
    f = open('start_QG.sh')
    text = f.read()
    f.close()

    SF = re.compile('REPL1')
    SF2 = re.compile('REPL2')
    new = SF.sub('#PBS -o /glade/scratch/bachman/Ian_QG/' + dirstr,text)   ##
    new = SF2.sub('ln -s /glade/scratch/bachman/Ian_QG/' + dirstr + ' /glade/work/bachman/Jupyter_Notebooks/Ian_QG/' + dirstr, new)
    f = open('start_QG.sh', 'w')
    f.write(new)
    f.close()

    f = open('restart_QG.sh')
    text = f.read()
    f.close()

    SF = re.compile('REPL1')
    SF2 = re.compile('REPL2')
    new = SF.sub('#PBS -o /glade/scratch/bachman/Ian_QG/' + dirstr,text)   ##
    new = SF2.sub('ln -s /glade/scratch/bachman/Ian_QG/' + dirstr + ' /glade/work/bachman/Jupyter_Notebooks/Ian_QG/' + dirstr, new)
    f = open('restart_QG.sh', 'w')
    f.write(new)
    f.close()

    # Submit job
    command = 'qsub start_QG.sh'
    mkd = subprocess.Popen(command, shell = True)
    mkd.wait()

    os.chdir(root_dir)
