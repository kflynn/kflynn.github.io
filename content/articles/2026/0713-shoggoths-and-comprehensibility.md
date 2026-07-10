+++
date = 2026-07-13
title = "Shoggoths and Comprehensibility"
draft = true

[taxonomies]
categories = [ "theory of computing", "crystal ball" ]
tags = [ "shoggoth", "llm", "ai", "comprehensibility" ]
+++

_...the shoggoths of the sea, reproducing by fission and acquiring a dangerous degree of accidental intelligence, presented for a time a formidable problem._

_-- H. P. Lovecraft, "At the Mountains of Madness", 1931_

<!-- more -->
----

Not long ago, I attended a presentation on AI given by some engineers at a company working on self-driving cars.
During the Q&A session, I asked them how many of the people at their company truly understood how exactly the LLMs they used worked.
"Oh," said the one engineer, "I don't think _anyone_ really does."
His colleague merely nodded sagely.

This was what I expected to hear.
There aren't any humans who actually understand these things, because they aren't things that humans _can_ understand.

Naturally, this prompted quite the hue and cry -- the sort of thing presaging pitchforks and torches and lynch mobs. But

---



Claiming that something created by humans is beyond human comprehension is - obviously - not exactly free from controversy.
To be clear, I'm not trying to argue no one understands how neural networks work, nor that it's impossible for humans to understand how, say, autoregression functions.
It's pretty evident that we as a race are perfectly capable of comprehending these things.

No, what I'm talking about how is the kind of understanding that allows prediction and explanation.
Given a model of sufficient complexity that we find it useful, it's not possible for a human - any human - to understand it well enough to correctly predict its response to a given input, nor to explain why it produced a given output.
The problem is with complexity and emergent behaviors, and it shows up all over the place in computing.

For example, a single bipolar junction transistor is easy to grasp: you have terminals named base, emitter, and collector, and current flowing from emitter to base allows current to flow from emitter to collector.[^1]
It's easy to predict what currents flow when, and it's easy to immediately see how to apply it as an amplifier or a switch.

[^1]: Yes, the emitter is sourcing the current, Ben Franklin got it wrong, it's a whole thing, let's not fight about it kthx.

If you take _two_ of these transistors and wire them together correctly, though, you get a flip-flop, and suddenly it's a different world.
To predict what a flip-flop will do,





In particular, this implies that it's not possible to predict when a hallucination will occur, nor to explain why a given hallucination occurred.
Further, this isn't something that training or practice can correct: it's a structural limitation.

Obviously I'm doing a certain amount of crystal-ball gazing here, and it's possible that I'll turn out to be badly wrong.

---
