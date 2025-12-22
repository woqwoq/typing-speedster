import json

class JsonHandler:

    def __init__(self, file_path, schema, schema_preprocess):
        self.file_path = file_path

        self.schema = schema
        self.schema_preprocess = schema_preprocess

        self.contents = self._parse_json(file_path)


    def _parse_json(self, file_path):
        try:
            file = open(file_path, 'r')
            contents = json.load(file)
            file.close()
        except FileNotFoundError:
            return None

        return contents

    def _split_keep_delimiter(self, txt, delimiter):
        return [line + delimiter for line in txt.split(delimiter) if line]

    def _remove_last_newline(self, arr):
        if arr:
            arr[-1] = arr[-1].rstrip('\n')

        return arr

    def _preprocess_code(self, code: str):
        if not code:
            return code
        
        code = code.replace("    ", "\t")
        code_lines = self._split_keep_delimiter(code, '\n')
        code_lines = self._remove_last_newline(code_lines)

        return code_lines
    
    def _preprocess_if_applicable(self, entry_data):        
        for i in range(len(entry_data)):
            if self.schema_preprocess[i]:
                entry_data[i] = self._preprocess_code(entry_data[i])
        
        return entry_data
    
    def write_json(self):
        file = open(self.file_path, 'w')
        json.dump(self.contents, file, indent=4)

    def _assemble_entry(self, entry_data):
        if len(entry_data) != len(self.schema):
            return None

        entry_data = self._preprocess_if_applicable(entry_data)

        entry = {}
        for i in range(len(self.schema)):
            entry[self.schema[i]] = entry_data[i]

        return entry

    def add_json_entry(self, entry_data, write: bool = False):
        entry = self._assemble_entry(entry_data)
        if entry:
            self.contents.append(entry)

        if write:
            self.write_json()

    def remove_entry(self, number, write: bool = False):
        if number > len(self.contents)-1:
            return
        
        self.contents.pop(number)

        if write:
            self.write_json()

    def is_valid(self):
        return self.contents != None

    def get_entry(self, number):
        if self.contents != None:
            return self.contents[number]
        
        return None
    
    def size(self):
        if self.contents != None:
            return len(self.contents)
        
        return 0
        
    def __str__(self):
        return str(json.dumps(self.contents, indent=4))

# SCHEMA = ['song_name', 'lyrics']
# SCHEMA_PREPROCESS = [0, 1]
#
# message = """[Intro: Eminem]
# (Yo, left, yo, left) 'Cause sometimes you just feel tired
# (Yo, left, right, left) Feel weak, and when you feel weak
# (Yo, left, yo, left) You feel like you wanna just give up
# (Yo, left, right, left) But you gotta search within you
# (Yo, left, yo, left) Try to find that inner strength and just pull that shit out of you
# (Yo, left, right, left) And get that motivation to not give up
# (Yo, left, yo, left) And not be a quitter
# (Yo, left, right, left) No matter how bad you wanna just fall flat on your face and collapse
#
# [Verse 1: Eminem]
# 'Til I collapse, I'm spillin' these raps long as you feel 'em
# 'Til the day that I drop, you'll never say that I'm not killin' 'em
# 'Cause when I am not, then I'ma stop pennin' 'em
# And I am not hip-hop and I'm just not Eminem
# Subliminal thoughts, when I'ma stop sendin' 'em?
# Women are caught in webs, spin 'em and hock venom
# Adrenaline shots of penicillin could not get the illin' to stop
# Amoxicillin's just not real enough
# The criminal, cop-killin', hip-hop villain
# A minimal swap to cop millions of Pac listeners
# You're comin' with me, feel it or not
# You're gonna fear it like I showed ya the spirit of God lives in us
# You hear it a lot, lyrics to shock
# Is it a miracle or am I just product of pop fizzin' up?
# Fa' shizzle, my wizzle, this is the plot, listen up
# You bizzles forgot, Slizzle does not give a fuck
# See upcoming rap shows
# Get tickets for your favorite artists
# You might also like
# Lose Yourself
# Eminem
# Family Matters
# Drake
# HISS
# Megan Thee Stallion
# [Chorus: Nate Dogg & Eminem]
# 'Til the roof comes off, 'til the lights go out
# 'Til my legs give out, can't shut my mouth
# 'Til the smoke clears out, am I high? Perhaps
# I'ma rip this shit 'til my bones collapse
# 'Til the roof comes off, 'til the lights go out ('Til the roof, until the roof)
# 'Til my legs give out, can't shut my mouth (The roof comes off, the roof comes off)
# 'Til the smoke clears out, am I high? Perhaps ('Til my legs, until my legs)
# I'ma rip this shit 'til my bones collapse (Give out from underneath me)
#
# [Verse 2: Eminem]
# Music is like magic, there's a certain feelin' you get
# When you real and you spit, and people are feelin' your shit
# This is your moment, and every single minute you spend
# Tryna hold on to it, 'cause you may never get it again
# So while you're in it, try to get as much shit as you can
# And when your run is over, just admit when it's at its end
# 'Cause I'm at the end of my wits with half the shit that gets in
# I got a list, here's the order of my list that it's in
# It goes: Reggie, JAY-Z, 2Pac and Biggie
# André from OutKast, Jada, Kurupt, Nas, and then me
# But in this industry I'm the cause of a lot of envy
# So when I'm not put on this list, this shit does not offend me
# That's why you see me walk around like nothing's botherin' me
# Even though half you people got a fuckin' problem with me
# You hate it, but you know respect you got to give me
# The press's wet dream, like Bobby and Whitney—Nate, hit me
# [Chorus: Nate Dogg & Eminem]
# 'Til the roof comes off, 'til the lights go out
# 'Til my legs give out, can't shut my mouth
# 'Til the smoke clears out, am I high? Perhaps
# I'ma rip this shit 'til my bones collapse
# 'Til the roof comes off, 'til the lights go out ('Til the roof, until the roof)
# 'Til my legs give out, can't shut my mouth (The roof comes off, the roof comes off)
# 'Til the smoke clears out, am I high? Perhaps ('Til my legs, until my legs)
# I'ma rip this shit 'til my bones collapse (Give out from underneath me)
#
# [Verse 3: Eminem]
# Soon as a verse starts, I eat at an MC's heart
# What is he thinking? How not to go against me, smart
# And it's absurd how people hang on every word
# I'll prob'ly never get the props I feel I ever deserve
# But I'll never be served, my spot is forever reserved
# If I ever leave Earth, that would be the death of me first
# 'Cause in my heart of hearts I know nothin' could ever be worse
# That's why I'm clever when I put together every verse
# My thoughts are sporadic, I act like I'm an addict
# I rap like I'm addicted to smack like I'm Kim Mathers
# But I don't wanna go forth and back in constant battles
# The fact is I would rather sit back and bomb some rappers
# So this is like a full-blown attack I'm launchin' at 'em
# The track is on some battlin' raps, who wants some static?
# 'Cause I don't really think that the fact that I'm Slim matters
# A plaque and platinum status is wack if I'm not the baddest, so
# [Chorus: Nate Dogg & Eminem]
# 'Til the roof comes off, 'til the lights go out
# 'Til my legs give out, can't shut my mouth
# 'Til the smoke clears out, am I high? Perhaps
# I'ma rip this shit 'til my bones collapse
# 'Til the roof comes off, 'til the lights go out ('Til the roof, until the roof)
# 'Til my legs give out, can't shut my mouth (The roof comes off, the roof comes off)
# 'Til the smoke clears out, am I high? Perhaps ('Til my legs, until my legs)
# I'ma rip this shit 'til my bones collapse (Give out from underneath me)
#
# [Outro: Eminem, Nate Dogg & Eminem & Nate Dogg]
# Until the roof, until the roof
# The roof comes off, the roof comes off
# Until my legs, until my legs
# Give out from underneath me, I
# I will not fall, I will stand tall
# Feels like no one can beat me"""
# handler = JsonHandler('Lyrics.txt', SCHEMA, SCHEMA_PREPROCESS)
#
# handler.add_json_entry(['Eminem - \'Till I Collapse', message], True)
