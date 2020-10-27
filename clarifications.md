# Clarifications from eClass
- Username names and passwords can't [have spaces](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1527826#p4003096), only alphanumeric characters.
- Priviledged users are [already in the database](eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1530061), can't be added via registraction.
- The "number of matching keywords" refers to the number of [distinct keywords](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1528512) that appear in the title, body or tag fields. Multiple occurances of a given keyword do not increase the matching keyword count.
- As per `uid char(4)`, U001, U01, and U1 should all be considered [different IDs](eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1534956).
- Tags can be multiple words ("big query"), and when searching, the post should be returned if [any part of the tag matches](eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1537384) ("uery" would match "big query").
