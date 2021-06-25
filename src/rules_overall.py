## Rules

from durable.lang import *
from durable.lang import _main_host

txts = []

if _main_host is not None:
    _main_host._ruleset_directory.clear()

with ruleset('rule_multi_overall'):
    
    #Display something about the crew in first place
    @when_all(m.position==1)
    def whos_in_first(c):
        """Generate a sentence to report on the first placed vehicle."""
        #We can add additional state, accessible from other rules
        #In this case, record the Crew and Brand for the first placed crew
        c.s.first_code = c.m.code
        c.s.prev_code = c.m.code
        
        txts.append(f'At the end of stage {c.m.stage}:')
        #Python f-strings make it easy to generate text sentences that include data elements
        txts.append(f'- {c.m.code} was {pickone_equally(["in first", "leading the rally", "at the head of the field", "in overall first", "in overall first position"])}') # with a time of {c.m.stageTime}.')
    
    #We can be a bit more creative in the other results
    @when_all(m.position>1)
    def whos_where(c):
        """Generate a sentence to describe the position of each other placed vehicle."""
        
        #Use the inflect package to natural language textify position numbers...
        nth = p.number_to_words(p.ordinal(int(c.m.position)))
        #Use various probabalistic text generators to make a comment for each other result
        first_opts = [c.s.first_code, 'the overall leader']
        #if c.m.Brand==c.s.first_brand:
        #    first_opts.append(f'the first placed {c.m.Brand}')
        #t = pickone_equally([f'with a time of {c.m.totalTime}'
        #                     #"{} behind {}".format(str(c.m.diffFirstS), pickone_equally(first_opts))
        #                     ],
        #                   prefix=', ')
        t2 = f' and {c.m.gap}s {pickone_equally(["behind "+c.s.first_code, "off the lead", "off the overall lead pace"])}' if c.s.first_code!=c.s.prev_code else ''
        #And add even more variation possibilities into the returned generated sentence
        txts.append(f'- {c.m.code} was in {nth}{sometimes(" position")}, {round(c.m.diff,1)}s behind {c.s.prev_code}{t2}')
        c.s.prev_code = c.m.code
