---
layout: single
title: The Comment Manifesto
categories: [programming, comments, documentation, wisdom-of-the-ages]
toc: true
sidebar:
  nav: "sidebar"
---

_(This was originally an internal Datawire memo, but I think it's worth sharing more widely.)_

# The Comment Manifesto

> If this code ships and your comments aren't in it, you'll regret it -- maybe
> not today, maybe not tomorrow, but soon, and for the rest of your life.

## Ladies and Gentlemen and Children of All Ages:

**Write comments.**

Write _lots_ of comments.

Write good, long, expressive, literate comments, in full sentences, with metaphors and
similes and room for all the creativity that you feel is ground out of you by Go's
Draconian rules about how uncuddled `else` is not acceptable, or by Python's
idiosyncratic insistence on indentation.

Write about your intentions. Write about what you're trying to get to the code to do,
and about why you think doing that is important. Write down all the things that need to
be true for your code to work, and how and why you're checking on them. Write descriptive
variable names, too – they make the comments easier.

We can read the code to see what it actually does, but we can't know what you wanted
unless you actually write down what's on your mind while you're coding. Don't worry if it
feels like you're writing a novel – modern editors can fold the comments out of the way if
the reader needs them to, and it's way more pleasant to read the code when the author
is narrating it while you go.

----

Mind you, I didn't believe in commenting back in the Pleistocene when I first got into
software. Back then, you would've found me huddled in a dark cubicle in front of a
TeleVideo 925, 80 columns by 24 rows of green letters glowing on a black background,
writing in K&R C and trying to cram my whole program onto a single line. The Real
Programmers who mentored me barely used whitespace, much less comments, and I
inherited their healthy scorn for anything so pedestrian as trying to explain what the
code was about.


Of course, those guys also told me that Real Programmers only used `ed`, that a
coredump was the only error message anyone needed anyway, and that they had to
walk ten miles to work every day, uphill both ways in the blistering July heat. But still,
they were my mentors, so I believed that they were showing me the Way of Good Code.

But over time, I slowly realized that the Real Programmers of the day wouldn't be
around for long. A few months down the road they'd be off on New Important Projects,
leaving behind their mountains of code for us more-junior engineers to try to maintain,
with no access to the original authors, and no hints of what they'd been thinking... and it
only got worse the first time I came back to some of my own code and realized that I no
longer remembered what I had been thinking.

----

Honestly, as I look back at my own older Datawire code, I feel like I didn't comment
enough either, for which I'd like to apologize. It takes time to comment well, and startup
life always feels like there's never enough time. But for awhile now, I've been trying to
always leave code more-commented than I found it, and to make sure new stuff I write
explains what I'm thinking -- and where the bodies are buried. I'd like to ask everyone
else here to do the same. Some of you have already seen me request changes on a PR
because there aren't enough comments, and there'll be more of that; it's important now,
and it's becoming more so as we grow.

Soon enough, anything you write will have someone else coming back and needing to
truly understand it -- maybe a new colleague, maybe a community member, maybe
yourself six months down the line. Whoever it is, they'll thank you for writing down
all the stuff that's in your head right now.

Even if it's you.
