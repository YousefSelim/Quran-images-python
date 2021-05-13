#Not revised , use at your own risk
#Also not the cleanest code , made on mobile and in a hurry so..
#but i suppose it does the job
#also i am fairly new to python
#any modification or suggestion is more than welcomed
#fonts are from https://github.com/quran/quran.com-images, which they got from king fahd complex
#v1 glyph codes are from Quran-api
#verses data from https://alquran.cloud/api
import json
import os
from PIL import ImageFont,Image,ImageDraw
export_images=True# faster generation of ayah marker position
debug=False#shows bounds of eaxh line , ayah marke of tru
factor=1#resolution factor , aspect ratio is fixed at 1024*1690
f=open("cleaned_ayahs_words2.json", "r")
c=f.read().encode().decode('utf-8-sig')
json_c=json.loads(c)
f=open("Verses.json", "r")
c=f.read().encode().decode('utf-8-sig')
verses=json.loads(c)
width=1024*factor
lis={}
glyphs_data={}
def draw_header(drw,width,_y,i):
		font =ImageFont.truetype(f"QCF_BSML.TTF",70*factor)
		font2 =ImageFont.truetype(f"QCF_BSML.TTF",114*factor)
		f=open("chapters.txt", "r")
		c=f.read().encode().decode('utf-8-sig')
		chapters=c.split("\n")
		headerwidth,y =drw.textsize(text=chapters[114],font=font2)
		x0=(width-headerwidth)/2
		drw.text(xy=(x0,(_y)-y/3+2),text=chapters[114],font=font2)
		word_width,y2=drw.textsize(text=chapters[i]+"\\",font=font)
		drw.text(xy=(x0+(headerwidth-word_width)/2,_y-y/3+2+((y)/2-y2/3)),text=chapters[i]+"\\",font=font)
def draw_basmalla(drw,width,_y,size=64):
		font2 =ImageFont.truetype(f"QCF_BSML.TTF",size*factor)
		headerwidth,y =drw.textsize(text="321",font=font2)
		x0=(width-headerwidth)/2
		drw.text(xy=(x0,(_y)-5),text="321",font=font2)
	
##print(json_c["1"])
for i in range(1,605):
	print(i)
	img=Image.new(size=[width,1690*factor],mode="RGBA")
	font =ImageFont.truetype(f"QCF_P{i:03d}.TTF",64*factor)
	drw=ImageDraw.Draw(img)
	last_line=-1
	accumelated_x=10
	#print(i)
	lines={}
	ayah_total={}
	markers={}
	ayah_ending_points=[]
	texts=[]
	lines_list=[]
	page=list(json_c[str(i)].values())
	for ayah in page:
	#arrange words in lines
		for word in ayah:
			if word["line_number"] not in list(lines.keys()):
				lines[word["line_number"]]=[]
				ayah_total[word["line_number"]]=[]
			lines[word["line_number"]].append(word)
			ayah_total[word["line_number"]].append(len(ayah))
	lines_list=list(lines.values())
	#arrange lines ascendingly
	lines_list=sorted(lines_list, key = lambda i: i[0]["line_number"])
	#loop through lines to add place holders for intermediate markeres
	for l in range(0,len(lines_list)):
		line=list(lines.values())[l]
		ay_total=list(ayah_total.values())[l]
		positions=[]
		for lll in line:
			positions.append(lll["position"])
		positions.reverse()
		ay_total.reverse()
		if positions[0]==ay_total[0]:
			markers[line[0]["line_number"]]=(1000,line[0]["line_number"])
	
	line_index=0
	last_line_temp=-1
	#loop through lines to write them 
	for line in lines_list:
			line_index+=1
			#arrange line by words
			line=sorted(line, key = lambda i: i["id"])
			line.reverse()
			texts.append([])
			_x=0
			max_y=90*factor
			text=""
			last_pos=-1
			#join words in ayah segments
			for word in line:
				if word["position"]>=last_pos:
					
					texts[len(texts)-1].append("")
				last_pos=word["position"]
				
				texts[len(texts)-1][len(texts[len(texts)-1])-1]+=word["code_v1"]
				
				text+=word["code_v1"]
				last_line=word["line_number"]
			accumelated_x=(width-_x)/2
			max_y+=10*factor
			_font=font
			accumelated_x=(width-drw.textsize(text=text,font=font)[0])/2
			if(accumelated_x<0):
				_font=ImageFont.truetype(f"QCF_P{i:03d}.TTF",50)
				accumelated_x=0
			_temp_accumelated_x=accumelated_x
			word_index=0
			#text is an ayah segment , from left to right
			for text in texts[len(texts)-1]:
					word_index+=1
					(x,_)=drw.textsize(text=text,font=font)
					drw.text(xy=(accumelated_x,last_line*max_y),text=text,font=font,anchor="la",fill=(255,255,255))
					if _temp_accumelated_x!=accumelated_x:
						ayah_ending_points.append((accumelated_x,last_line*max_y))
						#print(word_index)
					if(word_index==1 and (last_line in list(markers.keys()))):
						ayah_ending_points.append((accumelated_x,last_line*max_y))
					if(debug):
						drw.rectangle([accumelated_x,(last_line)*max_y,accumelated_x+x,(last_line+1)*max_y],outline=(255,0,0))
					accumelated_x+=x
					if((line_index==1 or last_line-last_line_temp>1)and(word_index==len(texts[len(texts)-1]))):
						#print("+"*10+str(last_line))
						ayah_ending_points.append((accumelated_x,last_line*max_y))
			
			last_line_temp=last_line
	#get empty lines
	empty_lines=[]
	for _i in range(1,16):
		Found=False
		
		for line in lines_list:
			if line[0]["line_number"]==_i:
				Found=True
		if not Found:
				empty_lines.append(_i)
						
	#print((ayah_ending_points))
	r=0
	glyphs_data[i]=ayah_ending_points
	if(debug):
		for marker in ayah_ending_points:
			r+=1
			drw.rectangle([marker,(marker[0]+75,marker[1]+100)],outline=(int(marker[1]),int(marker[0]),r*20))
	verses_page=verses[i-1]["ayahs"]
	surahs_ids=[]
	for verse in verses_page:
		if verse["numberInSurah"]==1:
			surahs_ids.append(verse["surah"]["number"])
	drawn_header_index=0
	print(verses_page[0]["surah"]["name"])
	for line_num in empty_lines:
		
		if(i<3):
			if(line_num==1):
				draw_header(drw,width,(line_num)*max_y,surahs_ids[drawn_header_index]-1)
			if(i==2):
			    draw_basmalla(drw,width,(line_num+1.3)*max_y,40)
            	
			break
		#check if only basmala
		if(line_num==1 and 2 not in empty_lines):
			draw_basmalla(drw,width,(line_num)*max_y)
			#drw.line([0,line_num*max_y,1000,line_num*max_y],fill=(0,255,0))
		#check if last line only
		elif (line_num==15 and 14 not in empty_lines):
			draw_header(drw,width,(line_num)*max_y,verses[i-1]["ayahs"][0]["surah"]["number"])
			#drw.line([0,line_num*max_y,1000,line_num*max_y],fill=(255,0,0))
		#check if last line and previous
		else:
			if line_num-1 in empty_lines:
				draw_basmalla(drw,width,(line_num)*max_y)
			else:
				draw_header(drw,width,(line_num)*max_y,surahs_ids[drawn_header_index]-1)
				drawn_header_index+=1
				#drw.line([0,line_num*max_y,1000,line_num*max_y],fill=(255,0,255))
	
	if not (os.path.exists("_out")):
		os.mkdir("_out")
	if(export_images):
		img.save(f"_out//_{i:03d}.png")
f=open("_out//ayah_marker.json","w")
f.write(json.dumps(glyphs_data))