-- sqlacodegen postgresql://zhangyuwei:123456@10.0.2.108:5432/yeyou --tables staff_role

DROP TABLE IF EXISTS staff_staff;
CREATE TABLE staff_staff(
  id SERIAL PRIMARY KEY ,
  zonst_id INTEGER NOT NULL ,
  realname VARCHAR(20) NOT NULL ,
  login_name VARCHAR(20) NOT NULL ,
  role_id INTEGER NOT NULL DEFAULT 0,
  create_time TIMESTAMP        NOT NULL DEFAULT now(),
  UNIQUE (zonst_id)
);

DROP TABLE IF EXISTS staff_role;
CREATE TABLE staff_role (
  id          SERIAL PRIMARY KEY,
  role_name   VARCHAR(20)      NOT NULL DEFAULT 'default',
  endpoints   VARCHAR[] NOT NULL DEFAULT '{}',
  create_time TIMESTAMP        NOT NULL DEFAULT now()
)