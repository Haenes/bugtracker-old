# BugTracker
This is the light version of bug tracker, that have:
  1) Ability to create <b>Projects</b> with different types (Fullstack, Front-end and Back-end);
  2) Ability to create <b>Issues</b> related to one of your projects;
  3) Ability to keep track the progress of your work on issues and projects in general.

Right now this project is still being developed.

<b>Completed</b>:
  1) All HTML templates, style (CSS, Bootstrap) and required JS;
  2) Temporary SQLite database with Django Models and URLconf;
  3) All HTML (except one form in TODO card in boards.html) is filled with information from database;
  4) Registration and log in process;
  5) Ability to create Projects and Issues;
  6) Abillity to add, edit, delete projects and issues;
  7) Ability to edit user details and change password;
  8) Ability to delete an account;
  9) Pagination for projects in projects.hmtl;
  10) Email confirmation for password reset and user register processes.

<b>Nearest to-do list</b>:
  1) Fix bug #1.

<b>It would be great to be able to</b>:
  1) Dynamically change the Favorite status of projects with AJAX or smth (star icon in project.html and boards.html);
  2) Dynamically change the Issue status via drag-n-drop card in boards.html with AJAX;

<b>Bugs and errors detected</b>:
  1) Errors in users.hmtl after change user data WITHOUT changing password (change password form is issue).
