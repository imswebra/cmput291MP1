---- Insert some data to test with
-- insert into users values();
insert into users values("1", "Mitch", "p", "Edmonton", "2020-10-27");
insert into users values("2", "Nayan", "p", "Vancouver", "2020-10-26");
insert into users values("3", "Eric", "p", "Kelowna", "2020-10-20");


insert into privileged values("1");

insert into posts values("1", "2020-09-29", "Qestion?", "This is a post about apple.", "1");
insert into posts values("2", "2020-08-29", "Answer apple", "This is an answer to that qesution", "2");
insert into posts values("3", "2020-08-29", "Another Questions", "This question does not have the keyword in it", "2");
insert into posts values("4", "2020-08-29", "Apple Apple", "This has apple 4 times ApplE", "3");


insert into questions values("1", null);
insert into questions values("3", null);
insert into questions values("4", null);

insert into answers values("2", "1");

insert into tags values("3", "aPPle");
insert into tags values ('3', 'aPPlE');
insert into tags values ('3', 'pear');
insert into tags values("4", "aPPle");
insert into tags values ('4', 'pear');
