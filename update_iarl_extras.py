#Script to generate IARL Extras Master XML
import os, glob, datetime

last_update_time = datetime.datetime.now()
base_dir = os.path.dirname(os.path.realpath(__file__))
xml_files = glob.glob(os.path.join(base_dir,'dat_files','*.xml'))
total_lines = 500  #Read up to this many lines looking for the header
new_line = '\r\n'
try:
	last_update_comment = raw_input('Enter an update Comment:  ')
except:
	last_update_comment = ''
	print 'No Update Comment was provided'
iarl_extras_text = '<datafile>\r\n\t<last_update>xxlast_updatexx</last_update>\r\n\t<last_update_comment>xxlast_update_commentxx</last_update_comment>'.replace('xxlast_updatexx',last_update_time.strftime("%Y-%m-%d")).replace('xxlast_update_commentxx',last_update_comment)+new_line
iarl_extras_entry = '\t<extrafile>'+new_line+'\t\t<emu_extras_filename>xxxml_filenamexx</emu_extras_filename>'+'xxheader_textxx'+'</extrafile>'+new_line
dont_include_these_lines = ['<emu_parser>','<emu_category>','<emu_author>','<emu_homepage>','<emu_baseurl>','<emu_launcher>','<emu_ext_launch_cmd>','<emu_downloadpath>','<emu_postdlaction>'] #Do not need to include this info in the summary xml

for xml_file in xml_files:
	if '.xml' in xml_file.lower():
		f=open(xml_file,'rU')
		f.seek(0)
		header_end=0
		line_num=0
		header_text = ''
		while header_end < 1:
			line=f.readline()
			include_line = True
			for ditl in dont_include_these_lines: #Remove unneeded lines from the summary xml
				if ditl in line:
					include_line = False
			if include_line:
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
			iarl_extras_text = iarl_extras_text+iarl_extras_entry.replace('xxheader_textxx',header_text).replace('xxxml_filenamexx',str(os.path.split(xml_file)[-1]))

iarl_extras_text = iarl_extras_text+'</datafile>'
iarl_extras_text = iarl_extras_text.replace('\t\t\t','\t\t').replace('\t\t</extrafile>','\t</extrafile>').replace('\t\t\t<emu_','\t\t<emu_')
with open(os.path.join(base_dir,'iarl_extras.xml'), 'w') as fout:
	fout.write(iarl_extras_text)