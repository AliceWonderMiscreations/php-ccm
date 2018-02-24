PSR-2 NOTE
==========

I appreciate the PHP Framework Interop Group and like what they do but I am
personally not a huge fan of PSR-2.

I do not mind if others follow PSR-2 but I think it goes overboard.

I see PSR-2 as a guideline, not a standard, and PHP code used in this project
will not strictly comply with PSR-2.

The differences in style I use and PSR-2 have absolutely zero impact on how PHP
interprets the code, so...

Indentation Spacing
-------------------

For my own personal code I tend to use two spaces. This has to do with short
term memory issues and my frequent use of `vim` in a terminal console to code.

With an 80 character screen, 4 spaces is 5% of the screen. As it is proper to
indent, that means the beginning of a class starts out with 5% of the
horizontal space gone for most of the code. As the code blocks for functions
also should be indented, the actual code within the method now has 10% of the
horizontal space gone. Blocks within the function should be indented too. The
white space ends up taking quite a bit of the horizontal space, resulting in
more lines visually wrapping, resulting in fewer visible lines available in the
console window.

Using two spaces instead of four greatly reduces the wasted horizontal spacing
but the visible indentation is still clear.

Generally I will try to change to four spaces before I publish the code, but
there will be times I forget to. PHP itself doesn't give a damn how many spaces
were used for indentation, or if there was indentation at all, but I will try
to switch to four before publishing code used in this project.


Curly Braces
------------

Putting each curly brace on a newline again reduces the vertical lines that can
be seen at the same time in a terminal window. For someone with short term
memory issues that results in more scrolling to see the exact spelling of what
they just saw.

I do often put the open curly brace for a class on a new line but for other
blocks I generally do not.

For me it isn't just the vertical space and my short term memory issues, it
also may be related to my autism and how I view the code.

With PHP each line of code ends in a `;` or a `}` -- that tells the PHP
interpreter that it needs to execute everything in that line before doing
anything else. A `{` to me is a way of noting the line isn't finished even
though a newline character directly follows it. What is inside gets interpreted
before the line being worked on is finished.

When I see a line of PHP that does not end in a `;` or `}` it mentally bothers
me. What is interesting, JSLint and JSON also like the `{` at the end of the
line rather than on its own line.


StudlyCase and camelCode
------------------------

Historically I used camelCode for everything, but I am switching to using
ucfirst camelCode (e.g. CamelCode) for class names, which I think is what PSR-2
actually means by StudlyCase.

However if I begin a class name with an acronym, the acronym will be lower
case. This is because I do not want the first letter of the next word to be
confused as part of the acronym.


Closing `?>`
------------

PSR-2 says files that only contain PHP should not have a closing `?>` tag. The
entire reason for that is sloppy code. Sloppy developers would have white space
after the closing `?>` that would result in the PHP interpreter sending a blank
line to the browser if the server did not have output buffering turned on.

Do not write sloppy code and there is no issue with a closing `?>` in your PHP
and using a closing `?>` is the right thing to do.

PHP uses a `<?php` to tell the engine to start processing and `?>` to tell it
to stop. The closing tag should be there.

Yes, the PHP will compensate by assuming a closing `?>` if it is missing. I
prefer precision over assumed compensation. That's actually why I also prefer
XML over HTML and use XHTML for all my personal projects.

My PHP will have the closing the `?>` and it is ridiculous that PSR-2 says it
should not be there.
