+++
date = 2026-07-10
title = '"AI" is a Terrible Name'

[taxonomies]
categories = [ "theory of computing", "crystal ball" ]
tags = [ "shoggoth", "llm", "ai", "pi", "naming is hard" ]
+++

_Finkle-McGraw brightened a bit. "You know, when I was a lad they called
it A.I. Artificial intelligence."_

_Hackworth allowed himself a tight, narrow, and brief smile. "Well,
there's something to be said for cheekiness, I suppose."_

_-- (Neal Stephenson, <strong>The Diamond Age</strong>)_

<!-- more -->
---

Naming things is hard[^1]. 😂

[^1]: They say that the two hardest problems in computing are naming
      things, cache invalidation, and off-by-one errors. (I've seen this
      attributed to one Phil Karlton, but only from a single source, so
      I'd love to hear from anyone who can be more definitive.)

Sadly, it's also important. Giving something a name is, at minimum,
giving everyone who will ever use it a hint about how you want them to
think about it. There are a lot of different ways you can approach this,
but whatever you're naming, it's worth considering how you want people to
think about it, and about how you should reflect that in its name.

Sadly, any such consideration will reveal that "artificial intelligence"
is a terrible name for our current crop of tools, because they are _not
intelligent_ (even though they're obviously artificial).

What we use right now are Large Language Models (LLMs), which I often
call shoggoths. Glossing over a _huge_ amount of very important detail,
they're all basically glorified [Markov chains]: they take a godawful
amount of training data, slice it up into features represented by tensors
of absurdly high dimensionality, and generate output by looking at what
sequences of these tensors happen in the training data.

Shoggoths can obviously do some really impressive things this way. A
properly-trained shoggoth is far, far better than I am at writing CSS and
JavaScript, for example[^2], and while shoggoths may or may not be
_better_ than I am at Go, they're certainly far _faster_. This opens some
really cool doors, but it's more about mechanical brute force than
intelligence.

[^2]: In fact, a shoggoth wrote most of the CSS customization for this
      website. Not coincidentally, I _hate_ CSS.

We can draw an analogy to calculators here. A calculator is _far_ better
than I am at doing arithmetic, but everyone these days understands that a
calculator is just a tool that uses a kind of silicon-based brute force
to do things inhumanly fast. No one today would claim that calculator -
or a calculator program running on a computer, or the computer itself -
is intelligent.

Back in the early days, though, people _would_ talk about how the
calculator or computer "could think"[^3]. It took awhile for the
collective "us" to be educated enough to get past that.

[^3]: Anyone remember the 80s-era supercomputer/AI firm [Thinking
      Machines]?

I think that's pretty much where we are with LLMs right now. Lots of
hype, lots of misunderstanding, lots of misuse _because_ the name so
encourages us buy into the hype. (And sure, there are folks who argue
that the glorified Markov chain is all human intelligence is, but I don't
buy that -- good topic for a future article, maybe.)

What would be better? Stephenson in _[The Diamond Age]_ actually coined a
name I like far far better: "pseudo-intelligence" or "PI". It's a
throwaway in the book, but it fits _ever_ so much better: what we have
right now are a crop of tools that mimic intelligence even though they
aren't intelligent.

I'd forgotten about the term "PI" until I reread _The Diamond Age_ while
recovering from surgery (🤦‍♂️). But I've wanted something better than
"AI" for a long time, and who knows, maybe it's not too late.

A constant reminder that these things are only mimicking intelligence
would be a good thing.

----

[Markov chains]: https://en.wikipedia.org/wiki/Markov_chain
[Thinking Machines]: https://en.wikipedia.org/wiki/Thinking_Machines_Corporation
[The Diamond Age]: https://www.amazon.com/Diamond-Age-Neal-Stephenson/dp/0553573314
