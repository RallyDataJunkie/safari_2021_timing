## Rules

from durable.lang import *
from durable.lang import _main_host

txts = []

if _main_host is not None:
    _main_host._ruleset_directory.clear()

from numpy import inf
from pandas import isnull

with ruleset('rule_multi_stage'):
    
    #Display something about the crew in first place
    @when_all(m.position==1)
    def whos_in_first(c):
        """Generate a sentence to report on the first placed vehicle."""
        #We can add additional state, accessible from other rules
        #In this case, record the Crew and Brand for the first placed crew
        c.s.first_code = c.m.code
        c.s.prev_code = c.m.code
        #Python f-strings make it easy to generate text sentences that include data elements
        txts.append(f'{c.m.code} {pickone_equally(["was in first", "took the stage","recorded the stage", "took the stage win"])} {pickone_equally(["with", "in", "recording", "taking", "marking", "making"])} a time of {c.m.TimeInS}s.')
    
    #We can be a bit more creative in the other results
    @when_all((m.position>1) & (m.diff<=60))
    def whos_where(c):
        """Generate a sentence to describe the position of each other placed vehicle."""
        
        #Use the inflect package to natural language textify position numbers...
        nth = p.number_to_words(p.ordinal(int(c.m.position)))
        #Use various probabalistic text generators to make a comment for each other result
        first_opts = [c.s.first_code, 'the stage winner', f'stage winner {c.s.first_code}']
        first_text = "{}s behind {}".format(str(round(c.m.gap,1)), pickone_equally(first_opts))
        #if c.m.Brand==c.s.first_brand:
        #    first_opts.append(f'the first placed {c.m.Brand}')
        
        desc_opts = [f'with a time of {c.m.TimeInS}s',
                             '{}{}'.format(first_text,
                                           sometimes(f"in a time of {c.m.TimeInS}s", prefix=" "))]
        if c.m.diff<0.1:
          t3 = f' {pickone_equally(["recording the same time as", "with the same time as", "matching the time of"])}  {c.s.prev_code}'
        elif c.m.diff<1:
          t3 = pickone_equally([f' {pickone_equally(["and just", ", just", ", only"])} {round(c.m.diff,1)}s {pickone_equally(["behind", "further behind", "further back behind"])} {c.s.prev_code}',
                                f'battling hard with {c.s.prev_code} and just {round(c.m.diff,1)}s {pickone_equally(["further behind", "further back"])}'])
        else:
          desc_opts.append(f'{round(c.m.diff,1)}s {pickone_equally(["behind", "further back behind"])} {c.s.prev_code}')
          t3=''
        
        t = pickone_equally(desc_opts,
                           prefix=', ')
        
        #And add even more variation possibilities into the returned generated sentence
        txts.append(f'{c.m.code} {pickone_equally(["was in", "took"])} {nth}{pickfirst_prob([""," place"," position"])}{t}{t3}.')
        c.s.prev_code = c.m.code

    @when_all((m.position>1) & (m.diff>60) & (m.diff<9999))
    def whos_where_bigdiff(c):
        """Generate a sentence to describe the position of each other placed vehicle."""
        
        #Use the inflect package to natural language textify position numbers...
        nth = p.number_to_words(p.ordinal(int(c.m.position)))
        #Use various probabalistic text generators to make a comment for each other result
        first_opts = [c.s.first_code, 'the stage winner', f'stage winner {c.s.first_code}']
        first_text = "{}s behind {}".format(str(round(c.m.gap,1)), pickone_equally(first_opts))
        #if c.m.Brand==c.s.first_brand:
        #    first_opts.append(f'the first placed {c.m.Brand}')
        t = pickone_equally([f'with a time of {c.m.TimeInS}s',
                             '{}{}'.format(first_text,
                                           sometimes(f"in a time of {c.m.TimeInS}s", prefix=" "))
                              ],
                           prefix=', ')
        t2 = f", {pickone_equally(['well back on', 'significantly further behind' ])} {c.s.prev_code}, who was {round(c.m.diff,1)}s {pickone_equally(['faster','quicker'])}"
        #And add even more variation possibilities into the returned generated sentence
        txts.append(f'{c.m.code} was in {nth}{sometimes(" position")}{t}{t2}.')
        c.s.prev_code = c.m.code
