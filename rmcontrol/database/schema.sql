drop table if exists commands;
create table commands (
	id integer primary key autoincrement,
	name text not null,
	code text not null
);
