
<div align="center">
<h1>
Exercise
</h1>
<h2>
Requirement:  Change the game to allow user to get a Hint by responding "H" to the prompt
</h2>
</div>
<h3>Comments</h3>

This is a simple-minded implementation of the feature:

The info we need is available in the objects
that are available at the point of asking the question. So it is possible to implement the 
new feature by conditional logic with the existing variables.  

One more property is tacked on to the `Question` class, which allows that class
to produce a single random incorrect answer.

Instead of changing Question, it would have been possible to retrieve the incorrect answers
and pick on of them in the `_play_round` method of `WhoWantsToBeAMillionaire` class.  Which
approach is better?