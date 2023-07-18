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
  5) Abillity to add, edit, delete projects and issues;
  6) Ability to edit user details and change password;
  7) Pagination for projects in projects.hmtl.

<b>Nearest to-do list</b>:
  1) Add ability to delete account;
  2) Add author foreign_key in Project model (FIX BUG: 1);
  3) Make the app finally dynamic (right now some data is taken in advance from db for convenience, for example - user);
  4) Add dynamically change of favorite project icon (star in project.html and boards.html);
  5) Add dynamically change of Issue status via drag-n-drop card in boards.html.

<b>Bugs and errors detected</b>:
  1) Projects are not tied to a specific user (who created it) - need to add Foreign key to Project model;
  2) Errors in users.hmtl after change user data WITHOUT changing password (change password form is issue).
