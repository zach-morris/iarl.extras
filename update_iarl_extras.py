#Script to generate IARL Extras Master XML
import os, glob
base_dir = os.path.dirname(os.path.realpath(__file__))
xml_files = glob.glob(os.path.join(base_dir,'dat_files','*.xml'))
total_lines = 500  #Read up to this many lines looking for the header
new_line = '\r\n'
iarl_extras_text = '<datafile>'+new_line
iarl_extras_entry = '\t<extrafile>'+'xxheader_textxx'+'</extrafile>'+new_line

for xml_file in xml_files:
	if '.xml' in xml_file.lower():
		f=open(xml_file,'rU')
		f.seek(0)
		header_end=0
		line_num=0
		header_text = ''
		while header_end < 1:
			line=f.readline()
			header_text+=str(line)
			line_num = line_num+1
			if '</header>' in header_text: #Found the header
				header_end = 1
				header_text = header_text.split('<header>')[1].split('</header>')[0]
				f.close()
			if line_num == total_lines:  #Couldn't find the header
				header_end = 2
				f.close()
				print('Unable to find the header in the xml file '+str(xml_file))
		if header_end == 1:
			iarl_extras_text = iarl_extras_text+iarl_extras_entry.replace('xxheader_textxx',header_text)

iarl_extras_text = iarl_extras_text+'</datafile>'
iarl_extras_text = iarl_extras_text.replace('\t\t\t','\t\t').replace('\t\t</extrafile>','\t</extrafile>')
with open(os.path.join(base_dir,'iarl_extras.xml'), 'w') as fout:
	fout.write(iarl_extras_text)