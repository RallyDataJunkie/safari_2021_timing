## Rules

from durable.lang import *
from durable.lang import _main_host

txts = []

if _main_host is not None:
    _main_host._ruleset_directory.clear()

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
        txts.append(f'{c.m.code} was in first with a time of {c.m.TimeInS}s.')
    
    #We can be a bit more creative in the other results
    @when_all(m.position>1)
    def whos_where(c):
        """Generate a sentence to describe the position of each other placed vehicle."""
        
        #Use the inflect package to natural language textify position numbers...
        nth = p.number_to_words(p.ordinal(int(c.m.position)))
        #Use various probabalistic text generators to make a comment for each other result
        first_opts = [c.s.first_code, 'the stage winner', f'stage winner {c.s.first_code}']
        first_text = "{}s behind {}".format(str(c.m.gap), pickone_equally(first_opts))
        #if c.m.Brand==c.s.first_brand:
        #    first_opts.append(f'the first placed {c.m.Brand}')
        t = pickone_equally([f'with a time of {c.m.TimeInS}s',
                             '{}{}'.format(first_text,
                                           sometimes(f"in a time of {c.m.TimeInS}s", prefix=" ")),
                             f"{c.m.diff}s behind {c.s.prev_code}"],
                           prefix=', ')
        
        #And add even more variation possibilities into the returned generated sentence
        txts.append(f'{c.m.code} was in {nth}{sometimes(" position")}{t}.')
        c.s.prev_code = c.m.code
