-- +goose Up
    CREATE table if not exists task(
        id int auto_increment not null,
        user_id VARCHAR(255) not null,
        task text not null,
        created_at timestamp default current_timestamp not null,
        primary key (id)
    );
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd
-- +goose Down
    DROP table if exists task;
-- +goose StatementBegin
SELECT 'down SQL query';
-- +goose StatementEnd
