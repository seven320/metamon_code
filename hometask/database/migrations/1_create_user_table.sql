-- +goose Up
    CREATE table if not exists user(
        id int auto_increment not null,
        username varchar(255) not null,
        user_id varchar(255) not null,
        twitter_id varchar(255),
        created_at timestamp default current_timestamp not null,
        secret_account boolean default 0 not null,
        primary key(id)
    );
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd

-- +goose Down
    DROP table if exists user;
-- +goose StatementBegin
SELECT 'down SQL query';
-- +goose StatementEnd
