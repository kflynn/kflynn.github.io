+++
date = 2020-01-01
title = "The Comment Manifesto"

[taxonomies]
categories = ["craft of computing"]
tags = [ "best practices", "wisdom of the ages"]
+++

_If this code ships and your comments aren't in it, you'll regret it -- maybe not today, maybe not tomorrow, but soon, and for the rest of your life._

<!-- more -->
----

## Ladies and Gentlemen and Children of All Ages:

**Write comments.**

Write _lots_ of comments.

Write good, long, expressive, literate comments, in full sentences, with
metaphors and similes and room for all the creativity that you feel is
ground out of you by Go's Draconian rules about how uncuddled `else` is
not acceptable, or by Python's idiosyncratic insistence on indentation.

Write about your intentions. Write about what you're trying to get to the
code to do, and about why you think doing that is important. Write down
all the things that need to be true for your code to work, and how and
why you're checking on them. Write descriptive variable names, too – they
make the comments easier.

We can read the code to see what it actually does, but we can't know what
you wanted it to do unless you actually write down what's on your mind
while you're coding. Don't worry if it feels like you're writing a novel
– modern editors can fold the comments out of the way if the reader needs
them to, and it's _much_ more pleasant to read the code when the author
is narrating it while you go.

----

Mind you, I didn't believe in commenting back in the Pleistocene when I
first got into software. Back then, you would've found me huddled in a
dark cubicle in front of a TeleVideo 925, 80 columns by 24 rows of green
letters glowing on a black background, writing in K&R C and trying to
cram my whole program onto a single line. The Real Programmers who
mentored me barely used whitespace, much less comments, and I inherited
their healthy scorn for anything so pedestrian as trying to explain what
the code was about.

Of course, those guys also told me that Real Programmers only used `ed`,
that a coredump was the only error message anyone needed anyway, and that
they had to walk ten miles to work every day, uphill both ways in the
blistering July heat. But still, they were my mentors, so I believed them
when they told me what good code looked like.

Over time, though, I came to realize that these guys wouldn't be around
forever. A few months down the road they'd be off working on new, more
important projects, leaving behind their mountains of code for us
more-junior engineers to try to maintain, with no access to the original
authors, and no hints of what they'd been thinking... and it only got
worse the first time I came back to some of my own code and realized that
I no longer remembered what _I_ had been thinking when I wrote it.

----

Honestly, looking back at a lot of the code I've written at startups, I
always feel like I'm not commenting enough either, for which I'd like to
apologize. It takes time to comment well, and startup life always feels
like there's never enough time. But I've gotten more than a few thanks
from the folks coming along afterward, telling me that what I wrote saved
them time (and, in some cases, entertained them). And for awhile now,
I've been trying to always leave code more-commented than I found it, and
to make sure new stuff I write explains what I'm thinking -- and where
the bodies are buried. It's _important_, and it only gets more important
as your organization grows.

Soon enough, anything you write will have someone else coming back and
needing to truly understand it -- maybe a new colleague, maybe a
community member, maybe yourself six months down the line. Whoever it is,
they'll thank you for writing down all the stuff that's in your head
right now.

Trust me.

----

_(This was originally an internal memo written at Datawire, probably
actually before 2020.)_
