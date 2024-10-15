<!DOCTYPE html>
<html>
<body>

<h1>ExamApp</h1>
<h2>Documentation for my ExamApp</h2>
<p>This is an app that will make an exam or text. Just input questions, save them and use them as text or exam later in the future. Well, i would like to say that the app is not fully complete, yes it works but it is not clean, has some bugs and has features that are not perfect. More insight on these below: </p>

<h2>Errors/Issues in the App: </h2>
<p class="errors">- The storaging process is not fully right as sometimes the options and/or answers switch themselves in  weird ways.</p>
<p class="errors">- If the question is very long, it's display it not good as the text overflows the label.</p>
<p class="errors">- Code is not clean, it is messy and not documentated well enough</p>

<h2>Bad Features</h2>
<p class="bad-features">- The "Search" and "Delete" buttons doesn't work. So it ahs no functionality after clicking the "Ok" button. They also can bring up multiple pages when you click on them more than once.</p>
<p class="bad-features">- The treeview when you click the edit button just doesn't look good and after editing a topic and its questions, that deleted question stays because the treeview isn't reloaded.</p>
<p class="bad-features">- The marks label(actually a ctk entry) doesn't change to the actual marks assigned to the topic choosen. Actually for this one, i just forgot to do it and i am so lazy to do it cause the code is a lot &#128513;</p>
<p class="bad-features">In "Without Option", the answers submitted by the user(the person answering the questions) must be excatly the same as the answer provided by the examiner/questioner(the person that added the questions). <br> Therefore, this is not totally practical, for example, if someone's answer is "Dog", and the questioner inserts "dog" for their answer,the user will get it wrong despite both both words being the same ("Dog" and "dog" are same). This is probably oversimplified and some people will say why not use capitalize() or something like that. <br> Well imagine a question like "What day did WW2 start?", some answer will be "1st September, 1939" or "1 September, 1939", "01/09/39" or some werid, stressful but funny guy may write "First day of the 9th month of the year, One thousand, nine hundred and thirty-nine years after the birth of Christ" and so on, these different possibilties can make a right answer a wrong answer especially for question of definition, logic, etc</p>
<p class="bad-features">- I know this is not a feature but a missing one, there is not "back" and "forth" button, buttons that would go back to previous and current question skipped or answer wrong by the user</p>

<h2>Specific Fixes/Solutions</h2>
<p class="fix">The Search button should pass the topic inserted in its entry to the about_to_start_func inother to start the quiz for that question</p>
<p class="fix">The Delete button should delete the topic inserted in its entry</p>
<p class="fix">Without options i think should just be more flexible to different kinds of answers</p>
<p class="fix">I would like the treeview to be changed to checkboxes and radio if anyone is out there.For the delete, it should display the questions after deletion</p>

<h2>Sorry to say there is actually no real documantation</h2>
</body>
</html>

# Copyright (c) 2024 Sam
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

