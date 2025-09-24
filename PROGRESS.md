<!DOCTYPE html>
<html>
<body>

<ul>
  <li>When I press the continue function after the first question so question 2 and above in the details page, I get an error. Update, it happens when I remove the number in the marks entry widget, it returns `expected floating-point number but got "" ` because in the entry, there is nothing in it. About 20:00, 23/09/25
</li>
<li>Found the solution, I just changed the data type of the entry from IntVar to StringVar. This allows/prevent the floating error from occurring as obviously, string has no floating problems. 20:38 23/09/25</li>

<li>20:48 Another problem right now is that when I move forward, the time and marks entry values do not change to the saved value inserted before it, it returns the value of the previous widgets instead, backwards works fine, it returns the value of the saved value inserted, but when you go forward, it doesn't work properly
</li>
<li></li>
</ul>

# Copyright (c) 2024 Sam
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

