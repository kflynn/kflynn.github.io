+++
date = 2026-07-05
title = "On Shipping Software"

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
shipping something that's incomplete seems silly, right? Well, not so
fast! It all gets back to to an old engineering truth that I'll call the
_Engineering Uncertainty Principle_[^1].

[^1]: Wikipedia covers this, sort of, as the [Project Management
    Triangle](https://en.wikipedia.org/wiki/Project_management_triangle).
    That's the more abstract version that deals with project management
    in general rather than focusing on engineering like I want to do
    here.

## Good, Fast, and Cheap

The Engineering Uncertainty Principle is usually phrased as follows:

> In engineering, we get to pick only two of "good", "fast", and "cheap".

If you want something good, and you want it fast, you'll need to be
prepared to pay for it. If you want something quickly and you're not able
to pay much for it, it's not likely to be high-quality.

Really, though, those three terms are shorthand for talking about
_predictability_. The Engineering Uncertainty Principle would be better
phrased as:

> In engineering, we get to pick only two of predictable quality,
> predictable time to completion, and predictable cost.

Fundamentally, this is another facet of Murphy's Law: you're going to
have something go wrong, and that's why you can't predict all three
things at once. Also, in all cases, we're talking more about not
exceeding some threshold than we are about any absolute numbers.
Predictable cost, for example, doesn't necessarily mean that the project
is cheap: it means that we didn't spend more than we planned to.[^2]

[^2]: Obviously, spending  _less_ than we planned is pretty much always OK.

But you still only get two: if you need both predictable cost and
predictable quality, you won't be able to predict the delivery date. If
you need both predictable quality and a predictable delivery date, then
you won't be able to predict what the cost will be.

This all ties into releases because choosing to ship only when everything
is finished means that you're choosing predictable quality, so you only
get one of predictable time and predictable cost. Choosing to ship
whatever is ready on a given date is choosing predictable time, so you
only get one of predictable cost and predictable quality.

## Volunteer Projects

Here's the big problem: projects staffed by volunteers have already
chosen to have a predictable cost. So you've _already picked two_ in a
volunteer project:

- if you choose to ship only when everything is ready, you can't know how long it'll take.
- if you choose to ship on a specific date, you can't predict the quality.

So we're doomed, right? Not quite.

The saving grace here is that being unable to predict the quality doesn't
mean that you have to ship bad code. You can still set a quality bar, and
then simply not ship anything that doesn't meet the bar; basically, you
can finesse quality by being willing to drop things if they're not
ready.[^3]

[^3]: We're assuming that you're past the very early days of not yet
    having an MVP. The "M" stands for "minimum"; it usually doesn't make
    sense before you reach the minimum bar for a functioning product.

This turns out to be a really powerful idea once you get used to it: it's
a way you can ship frequently and still keep up the quality of the things
you ship, which leads us to the final point in favor of shipping what's
ready on a given date.

## Why Bother Shipping Frequently?

Shipping is the way you get feedback on your software. Remember: there's
software that ships, and software that's irrelevant. It fundamentally
doesn't matter what kind of cool stuff you've written if no one ever sees
it -- and, likewise, if you write something and the first time a real
user has a chance to offer feedback is a year later after you've
forgotten everything about it, what's the point?

This is the same idea as tightening up your inner development loop: ship
frequently so your users can tell you what they like and what they don't,
and guide your product that way. For that, nothing beats shipping based
on time instead of based on features.

---
