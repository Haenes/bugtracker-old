# BugTracker
This is the light version of bug tracker, that have:
  1) Ability to create <b>Projects</b> with different types (Fullstack, Front-end and Back-end);
  2) Ability to create <b>Issues</b> related to one of your projects;
  3) Ability to keep track the progress of your work on issues and projects in general.

Right now this project is still being developed.

<b>Completed</b>:
  1) All HTML templates, style (CSS, Bootstrap) and required JS;
  2) Temporary SQLite database with Django Models and URLconf;
  3) All HTML (except all forms + modals from Bootstrap) is filled with information from database.

<b>Nearest to-do list</b>:
  1) Add validation for the remaining forms and modals;
  2) Make "Author" and "Project" fields invisible to the user in the Issue details form and Issue create modal;
  3) Get rid of a bunch of unnecessary imports and do;
  4) Make the app finally dynamic (right now some data is taken in advance from db for convenience);
  5) Change db to SQL (after complete a fully working app);
  6) Code refactoring
  7) Fix current bugs and future ones (if they are, AND THEY WILL).

<b>Bugs and errors detected</b>:
  1) Projects are not tied to a specific user (who created it) - need to add Foreign key to Project model;
