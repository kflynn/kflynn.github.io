+++
date = 2026-07-13
title = "Shoggoths and Comprehensibility"

[taxonomies]
categories = [ "theory of computing", "crystal ball" ]
tags = [ "shoggoth", "llm", "pi", "comprehensibility" ]
+++

_...the shoggoths of the sea, reproducing by fission and acquiring a dangerous degree of accidental intelligence, presented for a time a formidable problem._

_-- H. P. Lovecraft, "At the Mountains of Madness", 1931_

<!-- more -->
----

One of my favorite memes ever is Twitter user [tetraspace]'s December
2022 illustration of GPTs and [RLHF] using shoggoths:

[![shoggoth meme](https://pbs.twimg.com/media/FlQy5OmWYAATBx_?format=png&name=900x900)](https://x.com/TetraspaceWest/status/1608966939929636864/)

_(Find the original post
[here](https://x.com/TetraspaceWest/status/1608966939929636864/).)_

[tetraspace]: https://x.com/TetraspaceWest
[RLHF]: https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback

This illustration does a wonderfully evocative job of driving home why
I've come to think of "shoggoth" as the best name for our current crop of
[pseudo-intelligent] tools:

[pseudo-intelligent]: ../0710-ai-is-a-terrible-name/

_Shoggoths are not human_.

## Shoggoths

[Shoggoths] were introduced by H. P. Lovecraft nearly a century ago, in
his 1931 novella _[At the Mountains of Madness]_:

> ...a terrible, indescribable thing vaster than any subway train — a
> shapeless congeries of protoplasmic bubbles, faintly self-luminous, and
> with myriads of temporary eyes forming and un-forming as pustules of
> greenish light...

Lovecraft describes them as creatures originally created as beasts of
burden and beholden to their creators; over time, though, the shoggoths
mutated to become more intelligent, independent, and dangerous,
eventually resulting in their creators being forced to fight (largely but
not entirely successfully) to re-break the shoggoths to their will.

[Shoggoths]: https://en.wikipedia.org/wiki/Shoggoth
[At the Mountains of Madness]: https://www.hplovecraft.com/writings/texts/fiction/mm.aspx

What I find weirdly prescient about this idea from 1931 is how well it
fits our current crop of LLMs: they are _fundamentally_ non-human
entities. RLHF helps them _mimic_ humanity, but trusting them to have
human morals, ethics, or judgment is a recipe for disaster.

The reason is that shoggoths are incomprehensible to us humans.

## Understanding Shoggoths (or not)

Obviously, saying that something created by humans is beyond human
comprehension is not exactly free from controversy. It would be
(obviously) absurd to argue no one understands how neural networks work,
or that it's impossible for humans to understand how, say, autoregression
functions. It's pretty evident that we as a race are perfectly capable of
comprehending these things.

No, what I'm talking about is more like the difference between
understanding how a transistor works and understanding what a computer
will do at a given moment. Understanding a transistor is _easy_: you
apply a current between these two terminals, and it makes the transistor
allow a current to flow between those two. Add feedback loops (like
flip-flops) and there's a sudden leap in complexity. Scale out to a
billion transistors with an ALU, and it is _literally_ impossible to know
what happens next unless you also know what software is in the computer's
memory.

This is the kind of comprehension I'm talking about. Understanding single
neurons is easy. Understanding the theory of a neural network is
straightforward. Comprehending what a given instance of a neural network
will do requires you to understand _every weight_ on _every neuron_.

There aren't any useful LLMs where that kind of comprehension is within
the capability of a human. It's not a question of understanding the
underlying technology, it's a question of complexity and emergent
behaviors.

That lack of comprehension implies that we cannot predict what a given
shoggoth will do at a given moment. This extends further than knowing
when it will hallucinate, or why a given hallucination occurred: it's why
I say that we can't trust the shoggoth to have human morals, ethics, or
judgment. Shoggoths are fundamentally nonhuman.

## Anthropomorphization

Unfortunately, we humans are wired in basically the worst possible way
for handling this reality: we anthropomorphize to an alarming extent.
This has become known as the [ELIZA effect], and it is a scarily powerful
thing[^1]: natural language immediately prompts us humans to assume
emotion and humanity irrespective of whether the thing using language is
sentient or not.

[ELIZA effect]: https://en.wikipedia.org/wiki/ELIZA_effect

[^1]: I remember seeing this firsthand in a [Radio Shack] back in the
      1980s, watching someone else spending at least half an hour having
      an increasingly-personal conversation with a port of [ELIZA]
      running on a [TRS-80], the while talking about how amazing it was
      that ELIZA understood so well.

[Radio Shack]: https://en.wikipedia.org/wiki/RadioShack
[ELIZA]: https://en.wikipedia.org/wiki/ELIZA
[TRS-80]: https://en.wikipedia.org/wiki/TRS-80

In general this isn't that terrible a thing, because historically, most
of the systems we interact with this way are pretty limited. Shoggoths,
though, are kind of uniquely situated: RLHF trains them to act in ways
that seem almost intended to trigger the ELIZA effect in the worst
possible way.

Note that I'm not saying this makes shoggoths useless: far from it. What
I'm saying is that knowing you're interacting with a nonhuman
pseudointelligence that does not, and cannot, really have your best
interests at heart is critical to getting useful results out of them
without getting burned.

---
