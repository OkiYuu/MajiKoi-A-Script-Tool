# Importing dependencies
from os import listdir, mkdir
from os.path import isfile, isdir, join
import argparse

# Parser code
parser = argparse.ArgumentParser(description='Desc: Python script to unpack ' + \
'script files and pack translated subdirectories for Majikoi A (NeXAs engine)')
parser.add_argument('cmd', help="Specify \'u\' for unpack, \'p\' for pack")
parser.add_argument('o', nargs='?', default = False, 
                    help="(Optional) Specify folder or .bin file")
args = parser.parse_args()

if args.cmd == 'u':

  # Function to unpack .bin file
  # INPUT: s -- full path of given .bin file
  # OUTPUT: error -- 0 if successful, 1 else
  def unpack_script(s):  
    # Make the folder in EDIT, skip if it is already there
    path = "EDIT\\" + s.split('\\')[-1].split('.')[0]
    try: mkdir(path)
    except OSError: 
      print (path) + ' already exists! Skipping...'
      return 1
    else:
      if (s.split('.')[-1] == 'bin'):
        with open(s, "rb") as f: raw = f.read()
        i = raw.find("\x00\x00\x00NAME") # There tends to be a ...NAME string
        i1 = raw[:i].rfind("\x00\x00\x00") # This will usually be at ...SC
        i0 = raw[:i1].rfind("\x00\x00\x00") + len("\x00\x00\x00")
        
        if i == -1 or i0 == -1 or i1 == -1:
          print("Could not partition bin file (Greedy assumption failed?)")
          return 1
        
        # Debug code for sanity check
        #print(s + 'i0 = ' + str(i0) + ' and i1 = ' + str(i1))
        
        # Partition the raw bin file
        head = raw[:i0]
        body = raw[i0:i1]
        tail = raw[i1:]
        
        # Write out to head and tail
        curr_file = open(path + '\\head.bin','wb')
        curr_file.write(head)
        curr_file.close()
        curr_file = open(path + '\\tail.bin','wb')
        curr_file.write(tail)
        curr_file.close()
        
        # Break the body into human editable text
        example = open('source\\script_ex.txt', 'r')
        script = example.read()
        example.close()
        line = body.split('\x00')
        for l in line:
          script += ('# ' + l.replace('@n','') + '\n')
          if len(l) > 7: script += '# TL NOTE: ' + '-'*((len(l)-7)//2)
          else: script += '# ' + '-'*len(l)
          script += ('\n' + l + '\n\n')
        curr_file = open(path + '\\script.txt','w')
        curr_file.write(script)
        curr_file.close()
        
        return 0
      else: 
        print "Partitioning aborted, file is not .bin!"
        return 1
  
  # Unpack single file
  if args.o: 
    if unpack_script(args.o) == 0: print "Unpacking Successful!"
    else: print "Unpacking failed!"
  # Unpack all from .\IN\ folder
  else: 
    # This line will list files in .\IN\
    #exec("print ''\nprint 'Files in IN:'\nfor s in scripts: print s")
    scripts = [f for f in listdir("IN") if isfile(join("IN",f))]
    for script in scripts: 
      if script.split('.')[-1] == 'bin': unpack_script('IN\\' + script)
    
elif args.cmd == 'p':

  # Function to seperate out given string into lines for neXAs
  # INPUT: to_parse -- given string
  # OUTPUT:
  #   error -- Return 0 on success
  #   s -- successful string
  def break_into_lines(to_parse):
    # CASE 0: The line is already formatted (override parse detection)
    num_line_break = to_parse.count('@n')
    if num_line_break > 2:
      print "Line has too many breaks! Line:\n" + to_parse
      return 1, to_parse
    if num_line_break > 0: return 0, to_parse
    
    # CASE 1: The line has Japanese Quote marks
    if to_parse.find('\x81\x75') != -1 and to_parse.find('\x81\x76') != -1:
      i0 = to_parse.find('\x81\x75') + 2
      i1 = to_parse.find('\x81\x76')
      t_err, t_s = break_into_lines(to_parse[i0:i1])
      if t_err!=0:
        return 1, to_parse
      return 0, to_parse[:i0] + t_s + to_parse[i1:]
      
    # CASE 2: The line has Japanese parenthesis
    if to_parse.find('\x81\x69') != -1 and to_parse.find('\x81\x70') != -1:
      i0 = to_parse.find('\x81\x69') + 2
      i1 = to_parse.find('\x81\x70')
      t_err, t_s = break_into_lines(to_parse[i0:i1])
      if t_err!=0:
        return 1, to_parse
      return 0, to_parse[:i0] + t_s + to_parse[i1:]
    
    # CASE 3: The line has neither of the above
    
    # Can fit roughly 48-51 English characters on a line
    # This means there can be a max of 2 @n's added
    # Only add @n to lines with spaces (English will typically have spaces)
    ctr = 0
    parse = ''
    while len(to_parse) > 48:
      i = to_parse[:48].rfind(' ')
      if i != -1:
        parse += to_parse[:i] + '@n'
        to_parse = to_parse[i+1:]
        ctr += 1
        if ctr > 2: 
          print "English line too long!" 
          return 1, parse
      else:
        parse += to_parse[:48]
        to_parse = to_parse[48:]
      
    parse += to_parse
    return 0, parse
    

  # Function to pack subdirectory to .bin file
  # INPUT: s -- full path of given subdir
  # OUTPUT: error -- 0 if successful, 1 else
  def pack_script(s): 

    # Check for proper components, if missing terminate
    if not (isfile(join(s,'head.bin')) and isfile(join(s,'script.txt'))\
    and isfile(join(s,'tail.bin'))): 
      print "Invalid subdirectory (missing head, script, or tail)"
      return 1
    else:
    
      # Need to convert script.txt into proper body form
      body, pastFirst = '', False
      with open(join(s,'script.txt'), 'r') as f: processed = f.readlines()
      for line in processed:
        if len(line.strip()) > 0 and line.strip()[0] != '#':
          buf = line.strip()
          err, temp = break_into_lines(buf)
          if err: 
            print "ERROR! Failed on line: " + buf
            return 1
          if pastFirst: body += '\x00'
          body += temp
          pastFirst = True
      
      # Now put head, body, and tail together and output to bin
      with open(join(s,'head.bin'), 'rb') as f: head = f.read()
      with open(join(s,'tail.bin'), 'rb') as f: tail = f.read()
      raw = head + body + tail
      
      curr_file = open('OUT\\' + s.split('\\')[-1] + '.bin','wb')
      curr_file.write(raw)
      curr_file.close()
      return 0
      
  if args.o:
    if pack_script(args.o) == 0: print "Packing Successful!"
    else: print "Packing failed!"
  else:
    sdirs = [s for s in listdir("EDIT") if isdir(join("EDIT",s))]
    for s in sdirs: pack_script(join('EDIT',s))
  pass
  
# If nether of above triggered, wrong flag used!  
else: parser.error("cmd argument must be specified as \'u\' or \'p\'")