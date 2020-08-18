-- +goose Up
    CREATE table if not exists task_history(
        id int auto_increment not null,
        task_id int not null,
        tweet_id VARCHAR(255) not null,
        tweet_text VARCHAR(255) not null,
        created_at timestamp default current_timestamp not null,
        praised int default 0 not null,
        primary key (id)        
    );
-- +goose StatementBegin
SELECT 'up SQL query';
-- +goose StatementEnd

-- +goose Down
    DROP table if exists task_history;
-- +goose StatementBegin
SELECT 'down SQL query';
-- +goose StatementEnd

