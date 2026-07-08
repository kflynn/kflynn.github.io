+++
date = 2026-07-05
title = "On Shipping Software"
draft = true

[taxonomies]
categories = ["craft of computing"]
tags = ["best practices", "cat herding", "release management"]
+++

_There are two kinds of software: software that ships, and software
that's irrelevant._

<!-- more -->
----

If you're producing software, you need to get it out into the world.
However you do that - publishing container images, posting binaries for
download, mailing out DVDs - you'll have to do it more than once. And,
every time, you'll have to decide when it's ready to go out.

There are fundamentally two ways to do that:

1. You can get all your features finished, and ship whenever that
   happens.
2. You can pick a time to ship, and ship whatever's ready at that time.

On the face of it, it seems obvious that #1 is the way to go: after all,
shipping something that's incomplete seems silly, right? As it turns out,
though, there's absolutely a place for choosing a date and shipping
whatever is ready, rather than waiting to ship until a feature set is
finished. It all gets back to to an old engineering truth that I'll call
the _Engineering Uncertainty Principle_[^1].

[^1]: Wikipedia covers this, sort of, as the [Project Management Triangle](https://en.wikipedia.org/wiki/Project_management_triangle). That's the more abstract version that deals with project management in general rather than focusing on engineering like I want to do here.

## Good, Fast, or Cheap

The Engineering Uncertainty Principle is usually phrased as follows:

> In engineering, we get to pick only two of "good", "fast", and "cheap".

If you want something good, and you want it fast, you'll need to be prepared to pay for it.
If you want something quickly and you're not able to pay much for it, it's not likely to be high-quality.

Really, though, those three terms are shorthand for talking about
_predictability_. The Engineering Uncertainty Principle would be better phrased as:

> In engineering, we get to pick only two of predictable quality, predictable time to completion, and predictable cost.

Fundamentally, this is another facet of Murphy's Law: you're going to have something go wrong, and that's why you can't predict all three things at once.

In all cases, we're talking more about not exceeding some threshold than we are about any absolute numbers.
Predictable cost, for example, doesn't necessarily mean that the project is cheap: it means that we didn't spend more than we planned to.
(Obviously, spending  _less_ than we planned is pretty much always OK.)


Conversely, if you need both predictable quality and a predictable delivery date, then you won't be able to predict what the cost will be.
Treat this as a law of nature: you only get two.

This all ties into releases because choosing to ship only when everything is finished is choosing predictable quality (so you can't have both predictable time and predictable cost), and choosing to ship whatever is ready on a given date is choosing predictable time (so you can't have both predictable quality and predictable cost).

## Volunteer Projects

For projects staffed by volunteers, though, the project has already chosen to have a predictable cost: by definition, anything that gets done by the volunteer staff must have a cost of zero.
That, in turn, means that a volunteer project that wants to ship when the features are done has already chosen the which two things can be predicted!
Since you're required predictable quality and predictable cost, you _cannot_ also predict when you'll be able to ship.
It's simply not possible.

So we're doomed, right? Not quite.

## Unpredictable Quality != Low Quality

Being unable to predict the quality doesn't mean that you have to ship





